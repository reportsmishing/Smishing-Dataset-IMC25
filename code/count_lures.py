import os
import pandas as pd
from collections import Counter

def main():
    # 1. Find the base of the git repo
    repo_base = os.popen("git rev-parse --show-toplevel").read().strip()

    # 2. Path to the folder with datasets
    data_folder = os.path.join(repo_base, "dataset")

    # 3. The files to process
    files = [
        "final_dataset_output.csv"
    ]

    # 4. Counter for all lure principles
    lure_counter = Counter()

    for f in files:
        file_path = os.path.join(data_folder, f)
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        try:
            df = pd.read_csv(file_path, dtype=str, low_memory=False)
            if "lure_principles" not in df.columns:
                print(f"No 'lure_principles' column in {f}")
                continue

            # Collect lure principles
            lures = (
                df["lure_principles"]
                .dropna()
                .astype(str)
                .str.strip()
                .tolist()
            )

            # Handle comma-separated multiple lures in one row
            split_lures = []
            for lure in lures:
                split_lures.extend([l.strip() for l in lure.split(",") if l.strip()])

            lure_counter.update(split_lures)
            print(f"Processed {f} with {len(split_lures)} lure principle entries")

        except Exception as e:
            print(f"Error reading {f}: {e}")

    # 5. Save results in the current working directory
    output_file = os.path.join(os.getcwd(), "lure_principle_counts.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        for lure, count in lure_counter.most_common():
            f.write(f"{lure}:{count}\n")

    print(f"\nLure principle counts written to {output_file}")

if __name__ == "__main__":
    main()
