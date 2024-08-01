import streamlit as st
from googleapiclient.discovery import build

# Function to search YouTube videos
def search_youtube_videos(query, api_key, max_results=5):
	youtube = build('youtube', 'v3', developerKey=api_key)
	request = youtube.search().list(
		q=query,
		part='snippet',
		type='video',
		maxResults=max_results
	)
	response = request.execute()
	return response['items']

# Streamlit app
def main():
	st.title("Fitness App: YouTube Workout Videos")
	
	api_key = st.text_input("Enter YouTube API Key")
	query = st.text_input("Enter search query (e.g., 'swimming workouts')")
	
	if st.button("Search"):
		if api_key and query:
			videos = search_youtube_videos(query, api_key)
			for video in videos:
				video_id = video['id']['videoId']
				video_title = video['snippet']['title']
				video_url = f"https://www.youtube.com/watch?v={video_id}"
				st.write(f"{video_title}")
		else:
			st.error("Please enter both API key and search query.")

if __name__ == "__main__":
	main()