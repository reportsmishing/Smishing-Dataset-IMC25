import os
import pandas as pd
from collections import defaultdict, Counter

def clean_item(x: str) -> str:
    """Strip whitespace and surrounding punctuation."""
    x = str(x).strip()
    return x.strip(' "\'[]()')

def main():
    # 1. Script folder for saving outputs
    script_folder = os.path.dirname(os.path.abspath(__file__))

    # 2. Repo base and data folder
    repo_base = os.popen("git rev-parse --show-toplevel").read().strip()
    data_folder = os.path.join(repo_base, "dataset")

    files = [
        "final_dataset_output.csv"
    ]

    # Dictionary: lure -> Counter of scam_types
    lure_scam_counts = defaultdict(Counter)

    total_rows = 0
    total_entries = 0

    for f in files:
        file_path = os.path.join(data_folder, f)
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        try:
            df = pd.read_csv(file_path, dtype=str, low_memory=False)

            if "lure_principles" not in df.columns or "scam_type" not in df.columns:
                print(f"Missing required columns in {f}")
                continue

            # Drop rows with missing lure_principles
            df_nonull = df[df["lure_principles"].notna()].copy()

            for _, row in df_nonull.iterrows():
                total_rows += 1

                # Scam type
                scam = row.get("scam_type", "Unknown")
                if pd.isna(scam) or not str(scam).strip():
                    scam = "Unknown"
                else:
                    scam = clean_item(scam).lower()

                # Split comma-separated lures
                raw_lures = str(row["lure_principles"])
                lures = [clean_item(l) for l in raw_lures.split(",") if l.strip()]

                for lure in lures:
                    lure_scam_counts[lure][scam] += 1
                    total_entries += 1

            print(f"Processed {f} with {len(df_nonull)} rows containing lures")

        except Exception as e:
            print(f"Error reading {f}: {e}")

    # Save results
    output_file = os.path.join(script_folder, "lure_scam_counts.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        for lure, scam_counts in sorted(lure_scam_counts.items(), key=lambda x: -sum(x[1].values())):
            total = sum(scam_counts.values())
            # Sort scam types by descending count
            scam_str = ", ".join([f'"{scam}": {count}' for scam, count in sorted(scam_counts.items(), key=lambda x: -x[1])])
            f.write(f"{lure} [{total}]: [{scam_str}]\n")

    print(f"\nLure + scam counts written to {output_file}")
    print(f"Total rows scanned: {total_rows}, total (lure, scam) entries counted: {total_entries}")

if __name__ == "__main__":
    main()
