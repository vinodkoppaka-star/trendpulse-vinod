
import pandas as pd
import numpy as np

INPUT_FILE = "data/trends_clean.csv"
OUTPUT_FILE = "data/trends_analysed.csv"


def main():
    # ---------------------------------
    # 1 — Load and Explore the Data
    # ---------------------------------
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"Loaded data: {df.shape}")
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # Show first 5 rows
    print("
First 5 rows:")
    print(df.head())

    # Average score and comments
    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()

    print(f"
Average score   : {int(avg_score):,}")
    print(f"Average comments: {int(avg_comments):,}")

    # ---------------------------------
    # 2 — Analysis using NumPy
    # ---------------------------------
    print("
--- NumPy Stats ---")

    scores = df["score"].values
    comments = df["num_comments"].values

    # Basic statistics
    mean_score = np.mean(scores)
    median_score = np.median(scores)
    std_score = np.std(scores)

    print(f"Mean score   : {int(mean_score):,}")
    print(f"Median score : {int(median_score):,}")
    print(f"Std deviation: {int(std_score):,}")

    print(f"Max score    : {int(np.max(scores)):,}")
    print(f"Min score    : {int(np.min(scores)):,}")

    # Category with most stories
    category_counts = df["category"].value_counts()
    top_category = category_counts.idxmax()
    top_count = category_counts.max()

    print(f"
Most stories in: {top_category} ({top_count} stories)")

    # Story with most comments
    max_comments_index = np.argmax(comments)
    top_story = df.iloc[max_comments_index]

    print(f'
Most commented story: "{top_story["title"]}" — {int(top_story["num_comments"]):,} comments')

    # ---------------------------------
    # 3 — Add New Columns
    # ---------------------------------

    # Engagement = comments per upvote (avoid division by zero using +1)
    df["engagement"] = df["num_comments"] / (df["score"] + 1)

    # is_popular = True if score > average score
    df["is_popular"] = df["score"] > avg_score

    # ---------------------------------
    # 4 — Save the Result
    # ---------------------------------
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"
Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
