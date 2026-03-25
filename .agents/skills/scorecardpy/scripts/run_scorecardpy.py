#!/usr/bin/env python3
"""
Run scorecardpy workflow on a sampled DuckDB table.

Example:
python run_scorecardpy.py \
  --db-path data/model.duckdb \
  --table dev_sample_all_bads \
  --target target \
  --id-col entity_id \
  --out-dir artifacts
"""

from __future__ import annotations

import base64
import argparse
import json
import os
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import List

import duckdb
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scorecardpy as sc
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


@dataclass
class RunConfig:
    db_path: str
    table: str
    target: str
    id_col: str | None
    out_dir: str
    test_size: float
    random_state: int
    positive_label: str
    max_iter: int
    save_plots: bool
    plots_subdir: str
    plots_max: int
    x_cols: List[str] | None
    x_cols_json: str | None


def parse_args() -> RunConfig:
    parser = argparse.ArgumentParser(description="Run scorecardpy on DuckDB sample table")
    parser.add_argument("--db-path", required=True, help="Path to DuckDB database file")
    parser.add_argument("--table", required=True, help="DuckDB table name for development sample")
    parser.add_argument("--target", default="target", help="Binary target column name")
    parser.add_argument("--id-col", default="entity_id", help="Optional ID column to drop before modeling")
    parser.add_argument("--out-dir", default="artifacts", help="Output directory for artifacts")
    parser.add_argument("--test-size", type=float, default=0.3, help="Test split ratio")
    parser.add_argument("--random-state", type=int, default=20260325, help="Random seed")
    parser.add_argument(
        "--positive-label",
        default="1",
        help="scorecardpy positive label value passed to woebin/perf_eva",
    )
    parser.add_argument("--max-iter", type=int, default=200, help="Max iterations for logistic regression")
    parser.add_argument(
        "--save-plots",
        action="store_true",
        help="Save scorecardpy matplotlib plots as PNG + HTML under out-dir/plots/",
    )
    parser.add_argument("--plots-subdir", default="plots", help="Subdirectory name under --out-dir")
    parser.add_argument(
        "--plots-max",
        type=int,
        default=50,
        help="Max number of matplotlib figures to export per plot call (limits runtime/output volume)",
    )
    parser.add_argument(
        "--x-cols",
        default=None,
        help="Handpicked feature columns to model, comma-separated (e.g. a,b,c). "
        "When provided, var_filter auto-selection is bypassed.",
    )
    parser.add_argument(
        "--x-cols-json",
        default=None,
        help="Path to JSON file containing a list of feature column names to model. "
        "When provided, var_filter auto-selection is bypassed.",
    )
    args = parser.parse_args()

    if args.x_cols and args.x_cols_json:
        raise SystemExit("Only one of --x-cols and --x-cols-json can be provided.")

    x_cols: List[str] | None = None
    if args.x_cols:
        x_cols = [c.strip() for c in args.x_cols.split(",") if c.strip()]
    elif args.x_cols_json:
        p = Path(args.x_cols_json)
        if not p.is_file():
            raise SystemExit(f"--x-cols-json file not found: {p}")
        loaded = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(loaded, list) or not all(isinstance(x, str) for x in loaded):
            raise SystemExit("--x-cols-json must be a JSON array of strings.")
        x_cols = [x.strip() for x in loaded if x and isinstance(x, str)]

    return RunConfig(
        db_path=args.db_path,
        table=args.table,
        target=args.target,
        id_col=args.id_col,
        out_dir=args.out_dir,
        test_size=args.test_size,
        random_state=args.random_state,
        positive_label=args.positive_label,
        max_iter=args.max_iter,
        save_plots=args.save_plots,
        plots_subdir=args.plots_subdir,
        plots_max=args.plots_max,
        x_cols=x_cols,
        x_cols_json=args.x_cols_json,
    )


def _save_fig_to_png_and_html(fig: plt.Figure, png_path: Path) -> None:
    """
    Save a single matplotlib figure to PNG, and write a self-contained HTML embedding the PNG.

    HTML is generated using base64 so callers don't need extra asset files.
    """
    png_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(png_path), bbox_inches="tight")
    png_bytes = png_path.read_bytes()
    b64 = base64.b64encode(png_bytes).decode("ascii")
    html_path = png_path.with_suffix(".html")
    html = (
        "<!doctype html>"
        "<html><head><meta charset='utf-8'></head><body>"
        f"<img src='data:image/png;base64,{b64}' />"
        "</body></html>"
    )
    html_path.write_text(html, encoding="utf-8")


def _save_all_open_figures(plots_dir: Path, prefix: str, plots_max: int) -> List[Path]:
    fig_nums = sorted(plt.get_fignums())
    if plots_max and len(fig_nums) > plots_max:
        fig_nums = fig_nums[:plots_max]

    saved: List[Path] = []
    for idx, n in enumerate(fig_nums):
        fig = plt.figure(n)
        png_path = plots_dir / f"{prefix}_{idx:03d}.png"
        _save_fig_to_png_and_html(fig, png_path)
        saved.append(png_path)
    return saved


def load_data(cfg: RunConfig) -> pd.DataFrame:
    sql = f"SELECT * FROM {cfg.table}"
    con = duckdb.connect(cfg.db_path)
    try:
        df = con.execute(sql).df()
    finally:
        con.close()
    if cfg.target not in df.columns:
        raise ValueError(f"Target column '{cfg.target}' not found in {cfg.table}")
    return df


def ensure_binary_target(df: pd.DataFrame, target: str) -> pd.DataFrame:
    vals = set(df[target].dropna().unique().tolist())
    if not vals.issubset({0, 1}):
        raise ValueError(f"Target column '{target}' must contain only 0/1 values, got: {sorted(vals)}")
    return df


def prepare_xy(df: pd.DataFrame, cfg: RunConfig) -> pd.DataFrame:
    drop_cols: List[str] = []
    if cfg.id_col and cfg.id_col in df.columns:
        drop_cols.append(cfg.id_col)
    model_df = df.drop(columns=drop_cols)
    return model_df


def fit_pipeline(df: pd.DataFrame, cfg: RunConfig) -> dict:
    train_df, test_df = train_test_split(
        df,
        test_size=cfg.test_size,
        random_state=cfg.random_state,
        stratify=df[cfg.target],
    )

    requested_x_cols: List[str] | None = cfg.x_cols
    if requested_x_cols:
        missing = [c for c in requested_x_cols if c not in train_df.columns]
        if missing:
            raise ValueError(f"Handpicked --x-cols contains missing columns: {missing}")
        # Restrict modeling frame early so woebin/woebin_ply only sees what it should.
        train_f = train_df[[cfg.target] + requested_x_cols].copy()
        bins = sc.woebin(
            train_f,
            y=cfg.target,
            x=requested_x_cols,
            positive=cfg.positive_label,
        )
    else:
        train_f = sc.var_filter(train_df, y=cfg.target)
        requested_x_cols = [c for c in train_f.columns if c != cfg.target]
        bins = sc.woebin(
            train_f,
            y=cfg.target,
            x=requested_x_cols,
            positive=cfg.positive_label,
        )

    # scorecardpy may further drop variables (e.g. due to invalid binning),
    # so treat bins.keys() as the true effective column set downstream.
    used_x_cols = list(bins.keys())

    plots_dir: Path | None = None
    if cfg.save_plots:
        plots_dir = Path(cfg.out_dir) / cfg.plots_subdir
        # woebin_plot typically creates one matplotlib figure per variable.
        plt.close("all")
        sc.woebin_plot(bins)
        if plots_dir is not None:
            _save_all_open_figures(plots_dir, prefix="woebin", plots_max=cfg.plots_max)
        plt.close("all")

    train_woe = sc.woebin_ply(train_f, bins)
    test_woe = sc.woebin_ply(test_df[[cfg.target] + used_x_cols], bins)

    woe_cols = [c for c in train_woe.columns if c.endswith("_woe")]
    # scorecardpy can leave NaN in WOE outputs for sparse / unseen bins on small samples.
    # Fill with 0 so the downstream logistic regression remains numerically valid.
    train_woe[woe_cols] = train_woe[woe_cols].fillna(0)
    test_woe[woe_cols] = test_woe[woe_cols].fillna(0)
    lr = LogisticRegression(max_iter=cfg.max_iter)
    lr.fit(train_woe[woe_cols], train_woe[cfg.target])

    train_pred = lr.predict_proba(train_woe[woe_cols])[:, 1]
    test_pred = lr.predict_proba(test_woe[woe_cols])[:, 1]

    if cfg.save_plots and plots_dir is not None:
        plt.close("all")
    eva_train = sc.perf_eva(
        label=train_woe[cfg.target],
        pred=train_pred,
        title="train",
        positive=cfg.positive_label,
        show_plot=cfg.save_plots,
    )
    if cfg.save_plots and plots_dir is not None:
        _save_all_open_figures(plots_dir, prefix="perf_train", plots_max=cfg.plots_max)
        plt.close("all")

    if cfg.save_plots and plots_dir is not None:
        plt.close("all")
    eva_test = sc.perf_eva(
        label=test_woe[cfg.target],
        pred=test_pred,
        title="test",
        positive=cfg.positive_label,
        show_plot=cfg.save_plots,
    )
    if cfg.save_plots and plots_dir is not None:
        _save_all_open_figures(plots_dir, prefix="perf_test", plots_max=cfg.plots_max)
        plt.close("all")

    card = sc.scorecard(bins=bins, model=lr, xcolumns=woe_cols)
    scored_test = sc.scorecard_ply(test_df[[cfg.target] + used_x_cols], card, only_total_score=False)

    return {
        "train_df": train_df,
        "test_df": test_df,
        "train_filtered": train_f,
        "x_cols": used_x_cols,
        "x_cols_requested": cfg.x_cols,
        "woe_cols": woe_cols,
        "bins": bins,
        "lr": lr,
        "card": card,
        "eva_train": eva_train,
        "eva_test": eva_test,
        "scored_test": scored_test,
    }


def _to_jsonable(value: object) -> object:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, dict):
        return {str(k): _to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(v) for v in value]
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass
    if hasattr(value, "tolist"):
        try:
            return value.tolist()
        except Exception:
            pass
    return str(value)


def save_artifacts(result: dict, cfg: RunConfig) -> None:
    os.makedirs(cfg.out_dir, exist_ok=True)

    with open(os.path.join(cfg.out_dir, "bins.pkl"), "wb") as f:
        pickle.dump(result["bins"], f)
    with open(os.path.join(cfg.out_dir, "model_lr.pkl"), "wb") as f:
        pickle.dump(result["lr"], f)
    with open(os.path.join(cfg.out_dir, "scorecard.pkl"), "wb") as f:
        pickle.dump(result["card"], f)

    summary = {
        "table": cfg.table,
        "target": cfg.target,
        "x_cols": result["x_cols"],
        "woe_cols": result["woe_cols"],
        "train_rows": int(len(result["train_df"])),
        "test_rows": int(len(result["test_df"])),
        "test_size": cfg.test_size,
        "random_state": cfg.random_state,
    }
    with open(os.path.join(cfg.out_dir, "run_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    metrics = {
        "train": _to_jsonable(result.get("eva_train", {})),
        "test": _to_jsonable(result.get("eva_test", {})),
    }
    with open(os.path.join(cfg.out_dir, "metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    result["scored_test"].to_csv(
        os.path.join(cfg.out_dir, "scored_test.csv"),
        index=False,
    )


def main() -> None:
    cfg = parse_args()
    df = load_data(cfg)
    df = ensure_binary_target(df, cfg.target)
    df = prepare_xy(df, cfg)
    result = fit_pipeline(df, cfg)
    save_artifacts(result, cfg)
    print(f"Saved artifacts to: {cfg.out_dir}")
    print(f"Selected variables: {len(result['x_cols'])}")
    print("Done.")


if __name__ == "__main__":
    main()
