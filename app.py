import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Spotify Data Analysis", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv", encoding="ISO-8859-1")

    # Clean column names
    df.columns = df.columns.str.replace(".", "_").str.lower()

    # Rename important columns for easy use
    df = df.rename(columns={
        "track_name": "track",
        "artist_name": "artist",
        "beats_per_minute": "bpm",
        "length_": "length",
        "loudness__db_": "loudness"
    })

    return df


df = load_data()

# ---------------- TITLE ----------------
st.title("🎵 Spotify Top Songs — Data Analysis Dashboard")
st.markdown("**Covers all 10 analytical questions from the assignment.**")

# ---------------- SIDEBAR FILTER ----------------
st.sidebar.header("Filter Data")

genres = df["genre"].dropna().unique()

selected_genres = st.sidebar.multiselect(
    "Select Genre",
    options=genres,
    default=genres
)

filtered_df = df[df["genre"].isin(selected_genres)]

st.write(f"### Total Songs Displayed: {filtered_df.shape[0]}")

# ============================================================
# 1️⃣ Popularity Distribution
# ============================================================
st.subheader("1️⃣ Popularity Distribution")

fig1 = px.histogram(filtered_df, x="popularity", nbins=15)
st.plotly_chart(fig1, use_container_width=True)

# ============================================================
# 2️⃣ Top 10 Artists
# ============================================================
st.subheader("2️⃣ Top 10 Artists with Most Songs")

top_artists = (
    filtered_df["artist"]
    .value_counts()
    .reset_index()
    .head(10)
)
top_artists.columns = ["Artist", "Number of Songs"]

fig2 = px.bar(top_artists, x="Artist", y="Number of Songs", color="Artist")
st.plotly_chart(fig2, use_container_width=True)

# ============================================================
# 3️⃣ Genre Dominance
# ============================================================
st.subheader("3️⃣ Genre Dominance")

genre_counts = filtered_df["genre"].value_counts().reset_index()
genre_counts.columns = ["Genre", "Count"]

fig3 = px.bar(genre_counts, x="Genre", y="Count", color="Genre")
st.plotly_chart(fig3, use_container_width=True)

# ============================================================
# 4️⃣ Danceability vs Energy
# ============================================================
st.subheader("4️⃣ Danceability vs Energy")

fig4 = px.scatter(
    filtered_df,
    x="danceability",
    y="energy",
    color="genre",
    hover_name="track"
)
st.plotly_chart(fig4, use_container_width=True)

# ============================================================
# 5️⃣ Acousticness Over Time (if year exists)
# ============================================================
st.subheader("5️⃣ Acousticness Over Time")

if "year" in filtered_df.columns:
    fig5 = px.line(filtered_df, x="year", y="acousticness")
    st.plotly_chart(fig5, use_container_width=True)
else:
    st.info("Year column not available in dataset.")

# ============================================================
# 6️⃣ Tempo (BPM) Distribution
# ============================================================
st.subheader("6️⃣ Tempo (BPM) Distribution")

fig6 = px.histogram(filtered_df, x="bpm", nbins=15)
st.plotly_chart(fig6, use_container_width=True)

# ============================================================
# 7️⃣ Loudness vs Popularity
# ============================================================
st.subheader("7️⃣ Loudness vs Popularity")

fig7 = px.scatter(
    filtered_df,
    x="loudness",
    y="popularity",
    color="genre",
    trendline="ols"
)
st.plotly_chart(fig7, use_container_width=True)

# ============================================================
# 8️⃣ Valence vs Danceability
# ============================================================
st.subheader("8️⃣ Valence vs Danceability")

fig8 = px.scatter(
    filtered_df,
    x="valence",
    y="danceability",
    color="genre",
    hover_name="track"
)
st.plotly_chart(fig8, use_container_width=True)

# ============================================================
# 9️⃣ Speechiness in Top Genres
# ============================================================
st.subheader("9️⃣ Speechiness in Top Genres")

top3_genres = filtered_df["genre"].value_counts().head(3).index
speech_df = filtered_df[filtered_df["genre"].isin(top3_genres)]

fig9 = px.box(speech_df, x="genre", y="speechiness", color="genre")
st.plotly_chart(fig9, use_container_width=True)

# ============================================================
# 🔟 Song Duration Trends
# ============================================================
st.subheader("🔟 Song Duration Distribution & Average")

fig10 = px.histogram(filtered_df, x="length", nbins=15)
st.plotly_chart(fig10, use_container_width=True)

st.metric("Average Song Duration (seconds)", round(filtered_df["length"].mean(), 2))

# ---------------- DATA PREVIEW ----------------
st.subheader("📊 Dataset Preview")
st.dataframe(filtered_df, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Streamlit Dashboard • Data Visualization Assignment")
