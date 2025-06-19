import instaloader
import re
import os

def download_instagram_media(post_url):
    try:
        # Initialize Instaloader
        loader = instaloader.Instaloader()

        # Extract shortcode from URL
        shortcode = re.search(r'/p/([A-Za-z0-9_-]+)|/reel/([A-Za-z0-9_-]+)', post_url)
        if not shortcode:
            print("Invalid Instagram URL. Please provide a valid post or reel URL.")
            return

        shortcode = shortcode.group(1) or shortcode.group(2)

        # Load the post
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        # Create a directory for downloads
        download_dir = "instagram_downloads"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Set download path
        loader.dirname_pattern = download_dir

        # Download the post (images, videos, captions)
        loader.download_post(post, target=download_dir)
        print(f"Media downloaded successfully to {download_dir}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    url = input("Enter Instagram post or reel URL: ")
    download_instagram_media(url)
