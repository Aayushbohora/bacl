# app.py
import streamlit as st
from pytube import YouTube
import os

# Streamlit Page Config
st.set_page_config(page_title="YT Video Downloader", page_icon="🎥", layout="centered")

st.title("🎥 YouTube Video Downloader")
st.write("Download Shorts or Long YouTube Videos in MP4 format.")

# Input box for URL
url = st.text_input("Enter YouTube Video URL:")

if url:
    try:
        yt = YouTube(url)

        st.subheader("📌 Video Info")
        st.image(yt.thumbnail_url, width=400)
        st.write(f"**Title:** {yt.title}")
        st.write(f"**Channel:** {yt.author}")
        st.write(f"**Length:** {yt.length} seconds")

        # Select stream quality
        streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc()
        options = [f"{s.resolution} - {round(s.filesize / (1024*1024), 2)} MB" for s in streams]
        choice = st.selectbox("Select quality:", options)

        if st.button("⬇️ Download"):
            index = options.index(choice)
            stream = streams[index]

            # Download video
            file_path = stream.download()

            with open(file_path, "rb") as f:
                st.download_button(
                    label="Save Video",
                    data=f,
                    file_name=yt.title.replace(" ", "_") + ".mp4",
                    mime="video/mp4"
                )

            os.remove(file_path)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
