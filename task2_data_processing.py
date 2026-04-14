
import pandas as pd
import os

# NOTE:
# Update this filename based on your actual JSON file from Task 1
INPUT_FILE = "data/trends_20260414.json"
OUTPUT_FILE = "data/trends_clean.csv"


def main():
    # -----------------------------
    # 1 — Load JSON File
    # -----------------------------
    try:
        df = pd.read_json(INPUT_FILE)
        print(f"Loaded {len(df)} stories from {INPUT_FILE}")
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return

    # -----------------------------
    # 2 — Data Cleaning Steps
    # -----------------------------

    # Remove duplicate stories based on post_id
    before = len(df)
    df = df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")

    # Remove rows with missing important fields
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # Convert data types
    # score and num_comments should be integers
    df["score"] = df["score"].astype(int)

    # Some stories may not have comments → fill with 0
    df["num_comments"] = df["num_comments"].fillna(0).astype(int)

    # Remove low-quality posts (score < 5)
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # Clean title text (remove extra spaces)
    df["title"] = df["title"].str.strip()

    # -----------------------------
    # 3 — Save Clean Data
    # -----------------------------

    # Ensure data folder exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # Save to CSV
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"
Saved {len(df)} rows to {OUTPUT_FILE}")

    # -----------------------------
    # 4 — Category Summary
    # -----------------------------
    print("
Stories per category:")
    print(df["category"].value_counts())


if __name__ == "__main__":
    main()
