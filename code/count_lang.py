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

    # 4. Counter for all languages
    lang_counter = Counter()

    for f in files:
        file_path = os.path.join(data_folder, f)
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        
        try:
            df = pd.read_csv(file_path, dtype=str, low_memory=False)
            if "language" not in df.columns:
                print(f"No 'language' column in {f}")
                continue

            langs = df["language"].dropna().astype(str).str.strip().str.lower().tolist()
            lang_counter.update(langs)
            print(f"Processed {f} with {len(langs)} language entries")

        except Exception as e:
            print(f"Error reading {f}: {e}")

    # 5. Save results in the current working directory
    output_file = os.path.join(os.getcwd(), "language_counts.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        for lang, count in lang_counter.most_common():
            f.write(f"{lang}:{count}\n")

    print(f"\nLanguage counts written to {output_file}")

if __name__ == "__main__":
    main()
