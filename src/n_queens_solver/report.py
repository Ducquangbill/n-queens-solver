"""Generate Elsevier-format report from experiment results."""

import json
from pathlib import Path
from typing import Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_results(results_dir: str = "results") -> pd.DataFrame:
    """Load experiment results from summary.csv."""
    df = pd.read_csv(Path(results_dir) / "summary.csv")
    return df


def create_scaling_plot(df: pd.DataFrame, output_dir: Path):
    """Create scaling plot: time vs N for each method."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    sat_df = df[df["solver_type"] == "sat"].copy()
    baseline_df = df[df["solver_type"] == "baseline"].copy()

    # Plot 1: SAT solvers - binary encoding
    ax = axes[0]
    for solver in sat_df["solver"].unique():
        sdf = sat_df[(sat_df["solver"] == solver) & (sat_df["encoding"] == "binary")]
        if len(sdf) > 0:
            ax.plot(sdf["n"], sdf["time_sec"], marker="o", label=solver)
    ax.set_xlabel("N (board size)")
    ax.set_ylabel("Time (seconds)")
    ax.set_title("SAT Solvers - Binary Encoding")
    ax.set_yscale("log")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 2: SAT solvers - commander encoding
    ax = axes[1]
    for solver in sat_df["solver"].unique():
        sdf = sat_df[(sat_df["solver"] == solver) & (sat_df["encoding"] == "commander")]
        if len(sdf) > 0:
            ax.plot(sdf["n"], sdf["time_sec"], marker="o", label=solver)
    ax.set_xlabel("N (board size)")
    ax.set_ylabel("Time (seconds)")
    ax.set_title("SAT Solvers - Commander (Sorting Network) Encoding")
    ax.set_yscale("log")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 3: SAT solvers - product encoding
    ax = axes[2]
    for solver in sat_df["solver"].unique():
        sdf = sat_df[(sat_df["solver"] == solver) & (sat_df["encoding"] == "product")]
        if len(sdf) > 0:
            ax.plot(sdf["n"], sdf["time_sec"], marker="o", label=solver)
    ax.set_xlabel("N (board size)")
    ax.set_ylabel("Time (seconds)")
    ax.set_title("SAT Solvers - Product (Cardinality Network) Encoding")
    ax.set_yscale("log")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 4: SAT solvers - seqcounter encoding
    ax = axes[3]
    for solver in sat_df["solver"].unique():
        sdf = sat_df[(sat_df["solver"] == solver) & (sat_df["encoding"] == "seqcounter")]
        if len(sdf) > 0:
            ax.plot(sdf["n"], sdf["time_sec"], marker="o", label=solver)
    ax.set_xlabel("N (board size)")
    ax.set_ylabel("Time (seconds)")
    ax.set_title("SAT Solvers - Sequential Counter Encoding")
    ax.set_yscale("log")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / "scaling_plot.png", dpi=300, bbox_inches="tight")
    plt.close()


def create_heatmap(df: pd.DataFrame, output_dir: Path):
    """Create heatmap: encoding vs solver for each N."""
    sat_df = df[df["solver_type"] == "sat"].copy()

    for n in sorted(sat_df["n"].unique()):
        sdf = sat_df[sat_df["n"] == n]
        if len(sdf) == 0:
            continue

        pivot = sdf.pivot_table(
            values="time_sec",
            index="encoding",
            columns="solver",
            aggfunc="median"
        )

        # Ensure all encodings are present
        for enc in ["binary", "commander", "product", "seqcounter"]:
            if enc not in pivot.index:
                pivot.loc[enc] = np.nan

        pivot = pivot.reindex(["binary", "commander", "product", "seqcounter"])

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(
            pivot,
            annot=True,
            fmt=".4f",
            cmap="YlOrRd_r",
            ax=ax,
            cbar_kws={"label": "Time (seconds)"}
        )
        ax.set_title(f"N = {n}: Median Solve Time by Encoding and Solver")
        ax.set_xlabel("SAT Solver")
        ax.set_ylabel("Encoding Method")
        plt.tight_layout()
        plt.savefig(output_dir / f"heatmap_n{n}.png", dpi=300, bbox_inches="tight")
        plt.close()


def create_clause_count_plot(df: pd.DataFrame, output_dir: Path):
    """Create plot: clause count vs N for each encoding."""
    sat_df = df[df["solver_type"] == "sat"].copy()

    # Use first solver's data (clause counts are same for all solvers per encoding/N)
    clause_df = sat_df.drop_duplicates(subset=["n", "encoding"])[["n", "encoding", "clauses", "variables"]]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    for enc in ["binary", "commander", "product", "seqcounter"]:
        sdf = clause_df[clause_df["encoding"] == enc]
        if len(sdf) > 0:
            ax1.plot(sdf["n"], sdf["clauses"], marker="o", label=enc)
    ax1.set_xlabel("N (board size)")
    ax1.set_ylabel("Number of Clauses")
    ax1.set_title("CNF Clause Count by Encoding")
    ax1.set_yscale("log")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    for enc in ["binary", "commander", "product", "seqcounter"]:
        sdf = clause_df[clause_df["encoding"] == enc]
        if len(sdf) > 0:
            ax2.plot(sdf["n"], sdf["variables"], marker="o", label=enc)
    ax2.set_xlabel("N (board size)")
    ax2.set_ylabel("Total Variables (incl. auxiliary)")
    ax2.set_title("Variable Count by Encoding")
    ax2.set_yscale("log")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / "clause_variables.png", dpi=300, bbox_inches="tight")
    plt.close()


def create_comparison_table(df: pd.DataFrame, output_dir: Path):
    """Create LaTeX table comparing SAT vs baseline."""
    sat_df = df[df["solver_type"] == "sat"].copy()
    baseline_df = df[df["solver_type"] == "baseline"].copy()

    # Summary table: best SAT time vs CP-SAT per N
    summary_rows = []
    for n in sorted(sat_df["n"].unique()):
        n_df = sat_df[sat_df["n"] == n]
        bdf = baseline_df[baseline_df["n"] == n]

        if len(bdf) == 0:
            continue

        cp_sat_time = bdf["time_sec"].median()

        row = {"N": n, "CP-SAT (s)": f"{cp_sat_time:.4f}"}
        for enc in ["binary", "commander", "product", "seqcounter"]:
            enc_df = n_df[n_df["encoding"] == enc]
            if len(enc_df) > 0:
                best_time = enc_df["time_sec"].min()
                best_solver = enc_df.loc[enc_df["time_sec"].idxmin(), "solver"]
                row[f"{enc} (s)"] = f"{best_time:.4f}"
                row[f"{enc} solver"] = best_solver
            else:
                row[f"{enc} (s)"] = "—"
                row[f"{enc} solver"] = "—"

        summary_rows.append(row)

    summary_df = pd.DataFrame(summary_rows)

    # Save as CSV
    summary_df.to_csv(output_dir / "comparison_table.csv", index=False)

    # Save as LaTeX
    with open(output_dir / "comparison_table.tex", "w") as f:
        f.write(summary_df.to_latex(index=False, escape=False))

    return summary_df


def generate_report(results_dir: str = "results", output_dir: str = "results"):
    """Generate all report artifacts."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    df = load_results(results_dir)

    print("Generating scaling plot...")
    create_scaling_plot(df, output_path)

    print("Generating heatmaps...")
    create_heatmap(df, output_path)

    print("Generating clause/variable plot...")
    create_clause_count_plot(df, output_path)

    print("Generating comparison table...")
    create_comparison_table(df, output_path)

    print(f"All report artifacts saved to {output_path}")


if __name__ == "__main__":
    generate_report()