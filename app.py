import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- LOAD DATA ----------------
df = pd.read_csv("Dataset.csv", encoding="ISO-8859-1")

# Clean column names
df.columns = df.columns.str.replace(".", "_").str.lower()

# Rename for easy use (if needed)
df = df.rename(columns={
    "track_name": "track",
    "artist_name": "artist",
    "beats_per_minute": "bpm",
    "length_": "length"
})

# Set plot style
sns.set(style="whitegrid")

# ---------------- 1. Popularity Distribution ----------------
plt.figure()
sns.histplot(df["popularity"], bins=15, kde=True)
plt.title("Popularity Distribution")
plt.xlabel("Popularity")
plt.ylabel("Count")
plt.show()


# ---------------- 2. Top 10 Artists ----------------
plt.figure()
df["artist"].value_counts().head(10).plot(kind="bar")
plt.title("Top 10 Artists with Most Songs")
plt.xlabel("Artist")
plt.ylabel("Number of Songs")
plt.xticks(rotation=45)
plt.show()


# ---------------- 3. Genre Dominance ----------------
plt.figure()
sns.countplot(y="genre", data=df, order=df["genre"].value_counts().index)
plt.title("Genre Dominance")
plt.xlabel("Count")
plt.ylabel("Genre")
plt.show()


# ---------------- 4. Danceability vs Energy ----------------
plt.figure()
sns.scatterplot(x="danceability", y="energy", data=df, hue="genre")
plt.title("Danceability vs Energy")
plt.show()


# ---------------- 5. Acousticness Over Time ----------------
# Only if year column exists
if "year" in df.columns:
    plt.figure()
    sns.lineplot(x="year", y="acousticness", data=df)
    plt.title("Acousticness Over Time")
    plt.show()
else:
    print("No 'year' column available → Skipping Acousticness Over Time plot.")


# ---------------- 6. Tempo Analysis (BPM Distribution) ----------------
plt.figure()
sns.histplot(df["bpm"], bins=15)
plt.title("Tempo (BPM) Distribution")
plt.xlabel("BPM")
plt.ylabel("Count")
plt.show()


# ---------------- 7. Loudness vs Popularity ----------------
plt.figure()
sns.regplot(x="loudness", y="popularity", data=df)
plt.title("Loudness vs Popularity")
plt.show()


# ---------------- 8. Valence vs Danceability ----------------
plt.figure()
sns.scatterplot(x="valence", y="danceability", data=df, hue="genre")
plt.title("Valence vs Danceability")
plt.show()


# ---------------- 9. Speechiness in Top Genres ----------------
top_genres = df["genre"].value_counts().head(3).index
plt.figure()
sns.boxplot(x="genre", y="speechiness", data=df[df["genre"].isin(top_genres)])
plt.title("Speechiness in Top Genres")
plt.xticks(rotation=45)
plt.show()


# ---------------- 10. Song Duration Trends ----------------
plt.figure()
sns.histplot(df["length"], bins=15)
plt.title("Song Duration Distribution")
plt.xlabel("Length (seconds)")
plt.ylabel("Count")
plt.show()

print("Average song duration:", df["length"].mean())
