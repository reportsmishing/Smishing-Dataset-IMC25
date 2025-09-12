import os
import pandas as pd
from collections import defaultdict, Counter

def main():
    # 1. base of the git repo
    repo_base = os.popen("git rev-parse --show-toplevel").read().strip()
    # 2. Path to the folder with datasets
    data_folder = os.path.join(repo_base, "dataset")
    # 3. The files to process
    files = [
        "final_dataset_output.csv"
    ]
    # 4. Dictionary: scam_type -> Counter of languages
    scam_lang_counts = defaultdict(Counter)

    for f in files:
        file_path = os.path.join(data_folder, f)
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        try:
            df = pd.read_csv(file_path, dtype=str, low_memory=False)
            if "scam_type" not in df.columns:
                print(f"No 'scam_type' column in {f}")
                continue
            # Drop missing scam_type
            df = df[df["scam_type"].notna()].copy()
            for _, row in df.iterrows():
                scam = str(row["scam_type"]).strip().lower()
                lang = row.get("language", "Unknown")
                if pd.isna(lang) or not lang.strip():
                    lang = "Unknown"
                else:
                    lang = str(lang).strip()
                scam_lang_counts[scam][lang] += 1
            print(f"Processed {f} with {len(df)} scam_type rows")
        except Exception as e:
            print(f"Error reading {f}: {e}")

    # 5. Save results in current working directory
    output_file = os.path.join(os.getcwd(), "scam_type_lang_counts.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        for scam, lang_counts in sorted(scam_lang_counts.items(), key=lambda x: -sum(x[1].values())):
            total = sum(lang_counts.values())
            langs_str = ", ".join([f'"{lang}": {count}' for lang, count in sorted(lang_counts.items(), key=lambda x: -x[1])])
            f.write(f"{scam} [{total}]: [{langs_str}]\n")

    print(f"\nScam type + language counts written to {output_file}")

if __name__ == "__main__":
    main()
