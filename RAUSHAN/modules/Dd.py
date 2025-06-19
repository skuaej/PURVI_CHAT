import yt_dlp

from flask import Flask
app = Flask(__name__) 

@app.route('/down', methods=['GET'])
def download_reel():
    reel_id = request.args.get('id')
    reel_url = request.args.get('url')

    # Construct URL if only ID is provided
    if reel_id:
        reel_url = f'https://www.instagram.com/reel/{reel_id}/'

    if not reel_url:
        return jsonify({'error': 'Please provide either "id" or "url" parameter'}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'force_generic_extractor': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(reel_url, download=False)
            video_url = info.get('url')
            title = info.get('title')
            thumbnail = info.get('thumbnail')
            uploader = info.get('uploader')

            return jsonify({
                'title': title,
                'uploader': uploader,
                'thumbnail': thumbnail,
                'video_url': video_url
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
