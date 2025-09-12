import os
import pandas as pd
from collections import defaultdict, Counter

def clean_entity(e: str) -> str:
    """Basic cleaning: strip whitespace and outer quotes/brackets."""
    e = e.strip()
    # remove common surrounding punctuation
    e = e.strip(' "\'[]()')
    return e

def main():
    # find script folder
    script_folder = os.path.dirname(os.path.abspath(__file__))
    # repo base and data folder
    repo_base = os.popen("git rev-parse --show-toplevel").read().strip()
    data_folder = os.path.join(repo_base, "dataset")
    files = [
        "final_dataset_output.csv"
    ]

    # containers
    entity_lang_counts = defaultdict(Counter)  # {entity: Counter({lang: count})}
    entity_counter = Counter()                 # total counts per entity

    total_rows = 0
    processed_entities = 0

    for f in files:
        file_path = os.path.join(data_folder, f)
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        try:
            df = pd.read_csv(file_path, dtype=str, low_memory=False)
            if "named_entity" not in df.columns:
                print(f"No 'named_entity' column in {f}")
                continue
            # Keep only rows that have a named_entity
            df_nonull = df[df["named_entity"].notna()].copy()

            # iterate rows and split comma-separated entities
            for idx, row in df_nonull.iterrows():
                total_rows += 1
                raw_named = row["named_entity"]
                # if somehow not a string, cast
                raw_named = str(raw_named)
                # language: if missing, mark as 'Unknown'
                lang = row.get("language", None)
                if pd.isna(lang) or lang is None:
                    lang = "Unknown"
                else:
                    # keep as-is (string), strip whitespace
                    lang = str(lang).strip()

                # split on commas
                parts = [p for p in raw_named.split(",") if p and p.strip()]

                for p in parts:
                    ent = clean_entity(p)
                    if not ent:
                        continue
                    entity_lang_counts[ent][lang] += 1
                    entity_counter.update([ent])
                    processed_entities += 1

            print(f"Processed {f} -> rows with named_entity: {len(df_nonull)}")
        except Exception as e:
            print(f"Error reading {f}: {e}")

    # Save language-per-entity file in script folder
    output_file = os.path.join(script_folder, "lang_per_named_entity.txt")
    with open(output_file, "w", encoding="utf-8") as out:
        for ent, lang_counts in sorted(entity_lang_counts.items(), key=lambda x: -sum(x[1].values())):
            total = sum(lang_counts.values())
            langs_str = ", ".join([f'"{lang}": {count}' for lang, count in sorted(lang_counts.items(), key=lambda x: -x[1])])
            out.write(f"{ent} [{total}]: [{langs_str}]\n")

    # Save named_entity counts
    counts_file = os.path.join(script_folder, "named_entity_counts.txt")
    with open(counts_file, "w", encoding="utf-8") as out2:
        for ent, cnt in entity_counter.most_common():
            out2.write(f"{ent}:{cnt}\n")

    print(f"\nWrote: {output_file}")
    print(f"Wrote: {counts_file}")
    print(f"Total rows scanned (with named_entity): {total_rows}")
    print(f"Total individual entities extracted: {processed_entities}")

if __name__ == "__main__":
    main()
