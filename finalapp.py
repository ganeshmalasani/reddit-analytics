import streamlit as st
import praw
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from datetime import datetime

# Set up Streamlit UI
st.set_page_config(page_title="Reddit Analytics", layout="wide")
st.title("📊 Subreddit Analytics Dashboard")
st.sidebar.header("🔍 Enter Subreddit Name")

# User input for subreddit
subreddit_name = st.sidebar.text_input("Subreddit Name", "python")

# Slider for selecting number of posts
post_limit = st.sidebar.slider("Number of Posts", min_value=100, max_value=500, step=50, value=100)

# Submit button
run_analysis = st.sidebar.button("Run Analysis")

# Reddit API Credentials (Replace with your actual credentials)
CLIENT_ID = "THDuXjl7RPTzd_TK0jLtDA"
CLIENT_SECRET = "w_8bhplHtnixeBOpslvmxobcAiHzqQ"
USER_AGENT = "realtimesocialmedia"

# Initialize Reddit API
reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)

# Function to fetch subreddit posts
def get_subreddit_data(subreddit, limit):
    posts = []
    subreddit = reddit.subreddit(subreddit)
    for post in subreddit.hot(limit=limit):
        posts.append({
            "Title": post.title,
            "Score": post.score,
            "Comments": post.num_comments,
            "Created": datetime.fromtimestamp(post.created_utc),
            "Author": post.author.name if post.author else "[Deleted]"
        })
    return pd.DataFrame(posts)

if run_analysis:
    try:
        df = get_subreddit_data(subreddit_name, post_limit)
        st.success(f"Fetched {len(df)} posts from r/{subreddit_name}")
        
        # Create columns for layout
        col1, col2 = st.columns(2)
        
        # Chart 1: Post frequency over time
        with col1:
            st.subheader("📅 Post Frequency Over Time")
            df["Date"] = df["Created"].dt.date
            daily_posts = df.groupby("Date").size()
            fig, ax = plt.subplots(figsize=(5,3))
            daily_posts.plot(kind="line", ax=ax, color="royalblue")
            ax.set_ylabel("Posts per Day")
            st.pyplot(fig)
        
        # Chart 2: Upvotes vs Comments
        with col2:
            st.subheader("📊 Upvotes vs Comments")
            fig, ax = plt.subplots(figsize=(5,3))
            sns.scatterplot(x=df["Score"], y=df["Comments"], ax=ax, color="green")
            ax.set_xlabel("Upvotes")
            ax.set_ylabel("Comments")
            st.pyplot(fig)
        
        col3, col4 = st.columns(2)
        
        # Chart 3: Word Cloud of Titles
        with col3:
            st.subheader("☁️ Most Used Words in Titles")
            text = " ".join(df["Title"])
            wordcloud = WordCloud(width=600, height=300, background_color="black").generate(text)
            fig, ax = plt.subplots(figsize=(5,3))
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)
        
        # Chart 4: Distribution of Upvotes
        with col4:
            st.subheader("📈 Upvote Distribution")
            fig, ax = plt.subplots(figsize=(5,3))
            sns.histplot(df["Score"], bins=20, kde=True, ax=ax, color="purple")
            ax.set_xlabel("Upvotes")
            st.pyplot(fig)
        
        col5, col6 = st.columns(2)
        
        # Chart 5: Comment Count Distribution
        with col5:
            st.subheader("💬 Comment Count Distribution")
            fig, ax = plt.subplots(figsize=(5,3))
            sns.histplot(df["Comments"], bins=20, kde=True, ax=ax, color="orange")
            ax.set_xlabel("Comments")
            st.pyplot(fig)
        
        # Chart 6: Top 10 Authors by Post Count
        with col6:
            st.subheader("🏆 Top Authors by Post Count")
            top_authors = df["Author"].value_counts().head(10)
            fig, ax = plt.subplots(figsize=(5,3))
            top_authors.plot(kind="bar", ax=ax, color="teal")
            ax.set_ylabel("Number of Posts")
            st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Error fetching data: {e}")
