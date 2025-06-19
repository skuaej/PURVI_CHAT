import requests
from bs4 import BeautifulSoup
import re

def get_terabox_download_link(terabox_url):
    """
    Fetches a direct download link for a TeraBox video using a web-based downloader.
    Args:
        terabox_url (str): The TeraBox sharing URL (e.g., https://terabox.com/s/...)
    Returns:
        str: Direct download link or error message
    """
    try:
        # Hypothetical web-based downloader URL (replace with actual service like TeraDownloader.com)
        downloader_url = "https://teradownloader.com/generate"  # Example endpoint
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://teradownloader.com/'
        }

        # Send POST request with TeraBox URL to the downloader service
        payload = {'url': terabox_url}
        response = requests.post(downloader_url, headers=headers, data=payload, timeout=10)

        # Check if request was successful
        if response.status_code != 200:
            return f"Error: Failed to connect to downloader service (Status: {response.status_code})"

        # Parse the response to find the download link
        soup = BeautifulSoup(response.text, 'html.parser')
        download_link_tag = soup.find('a', href=re.compile(r'https://.*\.terabox\.com.*download.*'))

        if not download_link_tag:
            return "Error: Could not find download link in response"

        download_link = download_link_tag['href']
        return download_link

    except requests.exceptions.RequestException as e:
        return f"Error: Network issue occurred - {str(e)}"
    except Exception as e:
        return f"Error: An unexpected issue occurred - {str(e)}"

def download_file(download_url, output_path):
    """
    Downloads the file from the provided URL and saves it to the specified path.
    Args:
        download_url (str): Direct download URL
        output_path (str): Path to save the downloaded file
    """
    try:
        response = requests.get(download_url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"File downloaded successfully to {output_path}")
        else:
            print(f"Error: Failed to download file (Status: {response.status_code})")
    except Exception as e:
        print(f"Error downloading file: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Replace with your TeraBox video URL
    terabox_url = "https://terabox.com/s/1RCBLl4RBXh446ZKoHgHZJt_Q"
    output_file = "downloaded_video.mp4"

    # Get direct download link
    download_link = get_terabox_download_link(terabox_url)
    print(f"Download Link: {download_link}")

    # Download the file if link is valid
    if download_link.startswith("https://"):
        download_file(download_link, output_file)
    else:
        print(download_link)
