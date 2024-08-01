import streamlit as st
from googleapiclient.discovery import build
import random

# Function to search YouTube videos
def search_youtube_videos(query, api_key, max_results=50):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results
    )
    response = request.execute()
    return response['items']

# Function to filter workout videos
def filter_workout_videos(videos):
    workout_keywords = ["workout", "exercise", "fitness", "training", "routine"]
    filtered_videos = []
    for video in videos:
        title = video['snippet']['title'].lower()
        description = video['snippet'].get('description', '').lower()
        if any(keyword in title or keyword in description for keyword
in workout_keywords):
            filtered_videos.append(video)
    return filtered_videos

# Streamlit app
def main():
    st.title("Fitness App: YouTube Workout Videos")

    api_key = st.text_input("Enter YouTube API Key")
    query = st.text_input("Enter search query (e.g., 'swimming workouts')")

    difficulty = st.selectbox("Select difficulty level", ["Beginner",
"Intermediate", "Advanced"])
    max_length = st.slider("Select maximum video length (minutes)", 1, 60, 30)

    if 'videos' not in st.session_state:
        st.session_state.videos = []

    if st.button("Search"):
        if api_key and query:
            # Modify query based on difficulty level
            if difficulty == "Beginner":
                query += " beginner"
            elif difficulty == "Intermediate":
                query += " intermediate"
            elif difficulty == "Advanced":
                query += " advanced"

            videos = search_youtube_videos(query, api_key)

            # Shuffle the results to increase variety
            random.shuffle(videos)

            # Filter workout videos
            filtered_videos = filter_workout_videos(videos)

            # Store videos in session state
            st.session_state.videos = filtered_videos[:5]
        else:
            st.error("Please enter both API key and search query.")

    # Display videos with delete option
    for i, video in enumerate(st.session_state.videos):
        video_id = video['id']['videoId']
        video_title = video['snippet']['title']
        video_thumbnail = video['snippet']['thumbnails']['high']['url']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        st.image(video_thumbnail, width=200)
        st.write(f"[{video_title}]({video_url})")
        if st.button(f"Delete {video_title}", key=f"delete_{i}"):
            st.session_state.videos.pop(i)
            st.experimental_rerun()

if __name__ == "__main__":
    main()