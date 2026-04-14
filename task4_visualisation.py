
import pandas as pd
import matplotlib.pyplot as plt
import os

INPUT_FILE = "data/trends_analysed.csv"
OUTPUT_DIR = "outputs"


def shorten_title(title, max_len=50):
    'Shorten long titles for better display on charts'
    return title if len(title) <= max_len else title[:47] + "..."


def main():
    # -----------------------------
    # 1 — Setup
    # -----------------------------
    try:
        df = pd.read_csv(INPUT_FILE)
        print("Data loaded successfully")
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Create outputs folder if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # -----------------------------
    # 2 — Chart 1: Top 10 Stories
    # -----------------------------
    top_stories = df.sort_values(by="score", ascending=False).head(10)

    # Shorten titles for display
    titles = top_stories["title"].apply(shorten_title)
    scores = top_stories["score"]

    plt.figure()
    plt.barh(titles, scores)
    plt.xlabel("Score")
    plt.ylabel("Story Title")
    plt.title("Top 10 Stories by Score")
    plt.gca().invert_yaxis()  # highest score on top

    plt.savefig(f"{OUTPUT_DIR}/chart1_top_stories.png")
    plt.close()

    # -----------------------------
    # 3 — Chart 2: Stories per Category
    # -----------------------------
    category_counts = df["category"].value_counts()

    plt.figure()
    plt.bar(category_counts.index, category_counts.values)
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.title("Stories per Category")

    plt.savefig(f"{OUTPUT_DIR}/chart2_categories.png")
    plt.close()

    # -----------------------------
    # 4 — Chart 3: Scatter Plot
    # -----------------------------
    plt.figure()

    # Split data into popular and non-popular
    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]

    plt.scatter(popular["score"], popular["num_comments"], label="Popular")
    plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.title("Score vs Comments")
    plt.legend()

    plt.savefig(f"{OUTPUT_DIR}/chart3_scatter.png")
    plt.close()

    # -----------------------------
    # Bonus — Dashboard
    # -----------------------------
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Chart 1 in dashboard
    axes[0].barh(titles, scores)
    axes[0].set_title("Top Stories")
    axes[0].invert_yaxis()

    # Chart 2 in dashboard
    axes[1].bar(category_counts.index, category_counts.values)
    axes[1].set_title("Categories")

    # Chart 3 in dashboard
    axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
    axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
    axes[2].set_title("Score vs Comments")
    axes[2].legend()

    fig.suptitle("TrendPulse Dashboard")

    plt.savefig(f"{OUTPUT_DIR}/dashboard.png")
    plt.close()

    print("All charts saved in outputs/ folder")


if __name__ == "__main__":
    main()
