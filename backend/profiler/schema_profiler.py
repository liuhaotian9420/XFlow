"""Dataset schema profiling utilities."""

from __future__ import annotations

from io import BytesIO

import pandas as pd
from fastapi import HTTPException, UploadFile


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
SAMPLING_THRESHOLD = 10_000
SAMPLE_SIZE = 10_000


def profile_upload(file: UploadFile) -> tuple[pd.DataFrame, dict]:
    filename = file.filename or ""
    extension = _extension(filename)
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{extension}'. Use csv/xlsx/xls.",
        )

    raw_bytes = file.file.read()
    if not raw_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    df = _read_dataframe(raw_bytes, extension)
    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded file has no rows.")
    sampled = False
    if len(df) > SAMPLING_THRESHOLD:
        df = df.sample(n=SAMPLE_SIZE, random_state=42).reset_index(drop=True)
        sampled = True

    profile = {
        "filename": filename,
        "row_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "sampled": sampled,
        "columns": [],
    }
    for col in df.columns:
        series = df[col]
        profile["columns"].append(
            {
                "name": str(col),
                "dtype": str(series.dtype),
                "null_count": int(series.isna().sum()),
                "sample_values": _sample_values(series),
            }
        )
    return df, profile


def _read_dataframe(raw_bytes: bytes, extension: str) -> pd.DataFrame:
    buffer = BytesIO(raw_bytes)
    try:
        if extension == ".csv":
            return pd.read_csv(buffer)
        return pd.read_excel(buffer)
    except Exception as exc:  # pragma: no cover - defensive runtime path
        raise HTTPException(
            status_code=400, detail=f"Failed to parse file: {exc}"
        ) from exc


def _sample_values(series: pd.Series, limit: int = 5) -> list[str]:
    sample = series.dropna().astype(str).head(limit).tolist()
    return sample


def _extension(filename: str) -> str:
    if "." not in filename:
        return ""
    return filename[filename.rfind(".") :].lower()

