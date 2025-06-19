import pytube
import os

def download_youtube_video(video_url):
    try:
        # Initialize YouTube object
        yt = pytube.YouTube(video_url)

        # Get available video streams
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

        if not streams:
            print("No suitable video streams found. Try another video.")
            return

        # Display available resolutions
        print("\nAvailable resolutions:")
        for i, stream in enumerate(streams, 1):
            print(f"{i}. {stream.resolution} ({stream.filesize_mb:.2f} MB)")

        # Prompt user to select a resolution
        choice = int(input("\nEnter the number of your preferred resolution: ")) - 1
        if choice < 0 or choice >= len(streams):
            print("Invalid choice. Selecting highest resolution by default.")
            choice = 0

        selected_stream = streams[choice]

        # Create download directory
        download_dir = "youtube_downloads"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Download the video
        print(f"\nDownloading: {yt.title} ({selected_stream.resolution})...")
        selected_stream.download(output_path=download_dir)
        print(f"Video downloaded successfully to {download_dir}/{yt.title}.mp4")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    url = input("Enter YouTube video URL: ")
    download_youtube_video(url)
