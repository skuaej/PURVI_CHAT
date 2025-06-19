from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import re
import os

app = Flask(__name__)

def get_terabox_download_link(terabox_url):
    """
    Fetches a direct download link for a TeraBox video using a web-based downloader.
    Args:
        terabox_url (str): The TeraBox sharing URL (e.g., https://terabox.com/s/...)
    Returns:
        dict: Contains status and either download link or error message
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
            return {"status": "error", "message": f"Failed to connect to downloader service (Status: {response.status_code})"}

        # Parse the response to find the download link
        soup = BeautifulSoup(response.text, 'html.parser')
        download_link_tag = soup.find('a', href=re.compile(r'https://.*\.terabox\.com.*download.*'))

        if not download_link_tag:
            return {"status": "error", "message": "Could not find download link in response"}

        download_link = download_link_tag['href']
        return {"status": "success", "download_link": download_link}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Network issue occurred - {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected issue occurred - {str(e)}"}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        terabox_url = request.form.get('url')
        if not terabox_url:
            return render_template('index.html', error="Please provide a TeraBox URL")
        
        result = get_terabox_download_link(terabox_url)
        if result['status'] == 'success':
            return render_template('index.html', download_link=result['download_link'])
        else:
            return render_template('index.html', error=result['message'])
    
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
