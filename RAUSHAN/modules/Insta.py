import pytube
import os
from pytube.exceptions import PytubeError

def download_youtube_video(video_url):
    try:
        # Initialize YouTube object with error handling
        yt = pytube.YouTube(video_url)

        # Get available video streams (progressive MP4 or adaptive streams)
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        if not streams:
            # Fallback to adaptive streams if no progressive streams found
            streams = yt.streams.filter(file_extension='mp4').order_by('resolution').desc()
            if not streams:
                print("No suitable MP4 streams found. Try another video.")
                return

        # Display available resolutions
        print("\nAvailable resolutions:")
        for i, stream in enumerate(streams, 1):
            size_mb = stream.filesize / (1024 * 1024) if stream.filesize else "Unknown"
            print(f"{i}. {stream.resolution or 'Unknown'} ({size_mb:.2f} MB)")

        # Prompt user to select a resolution
        choice = input("\nEnter the number of your preferred resolution (or press Enter for highest): ")
        if choice.strip() == "":
            choice = 0
        else:
            choice = int(choice) - 1

        if choice < 0 or choice >= len(streams):
            print("Invalid choice. Selecting highest resolution by default.")
            choice = 0

        selected_stream = streams[choice]

        # Create download directory
        download_dir = "youtube_downloads"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Download the video
        print(f"\nDownloading: {yt.title} ({selected_stream.resolution or 'Unknown'})...")
        file_path = selected_stream.download(output_path=download_dir)
        print(f"Video downloaded successfully to {file_path}")

    except PytubeError as pe:
        print(f"Pytube error: {pe}")
        print("This may be due to YouTube API changes. Try updating pytube: pip install --upgrade pytube")
    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Ensure the URL is valid and your internet connection is stable.")

if __name__ == "__main__":
    url = input("Enter YouTube video URL: ")
    download_youtube_video(url)
