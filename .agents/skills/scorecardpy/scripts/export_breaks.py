#!/usr/bin/env python3
"""
Export scorecard bin definitions to JSON from pickled bins.

Example:
python export_breaks.py --bins-pkl artifacts/bins.pkl --out-dir artifacts
"""

from __future__ import annotations

import argparse
import json
import os
import pickle
from typing import Any, Dict, List

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export scorecard bins to JSON artifacts")
    parser.add_argument("--bins-pkl", default="artifacts/bins.pkl", help="Path to pickled bins object")
    parser.add_argument("--out-dir", default="artifacts", help="Output directory")
    return parser.parse_args()


def _safe_value(v: Any) -> Any:
    if pd.isna(v):
        return None
    if hasattr(v, "item"):
        try:
            return v.item()
        except Exception:
            return str(v)
    return v


def normalize_bins(bins: Dict[str, pd.DataFrame]) -> Dict[str, List[Dict[str, Any]]]:
    out: Dict[str, List[Dict[str, Any]]] = {}
    for var, df in bins.items():
        rows: List[Dict[str, Any]] = []
        use_cols = [c for c in ["bin", "woe", "breaks", "is_special_values", "count_distr", "badprob"] if c in df.columns]
        for _, row in df[use_cols].iterrows():
            rows.append({col: _safe_value(row[col]) for col in use_cols})
        out[var] = rows
    return out


def main() -> None:
    args = parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    with open(args.bins_pkl, "rb") as f:
        bins = pickle.load(f)

    normalized = normalize_bins(bins)
    out_path = os.path.join(args.out_dir, "breaks_export.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)

    var_list = sorted(list(normalized.keys()))
    with open(os.path.join(args.out_dir, "selected_variables.json"), "w", encoding="utf-8") as f:
        json.dump(var_list, f, ensure_ascii=False, indent=2)

    print(f"Exported {len(var_list)} variables to: {out_path}")


if __name__ == "__main__":
    main()
