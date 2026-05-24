from flask import Flask, request, jsonify
from config import Config
import os
import json
from pathlib import Path

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'agent': 'video_agent'}), 200

@app.route('/api/process-video', methods=['POST'])
def process_video():
    """Process a video file and extract metadata"""
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        video_file = request.files['video']
        if video_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Save video
        video_path = os.path.join(Config.VIDEOS_DIR, video_file.filename)
        video_file.save(video_path)
        
        # Extract metadata (basic implementation)
        metadata = {
            'filename': video_file.filename,
            'size_bytes': os.path.getsize(video_path),
            'path': video_path,
            'status': 'processed'
        }
        
        # Save metadata
        output_path = os.path.join(Config.OUTPUT_DIR, f"{Path(video_file.filename).stem}_metadata.json")
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return jsonify({
            'message': 'Video processed successfully',
            'metadata': metadata,
            'output': output_path
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/list-videos', methods=['GET'])
def list_videos():
    """List all processed videos"""
    try:
        videos = []
        if os.path.exists(Config.VIDEOS_DIR):
            videos = os.listdir(Config.VIDEOS_DIR)
        
        return jsonify({
            'videos': videos,
            'count': len(videos)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs(Config.VIDEOS_DIR, exist_ok=True)
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    
    app.run(host='0.0.0.0', port=Config.AGENT_PORT, debug=Config.DEBUG)
