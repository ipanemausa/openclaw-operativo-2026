import os

class Config:
    AGENT_NAME = os.getenv('AGENT_NAME', 'video_agent')
    AGENT_PORT = int(os.getenv('AGENT_PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    
    # Paths
    VIDEOS_DIR = '/app/videos'
    OUTPUT_DIR = '/app/output'
    
    # Video processing
    MAX_VIDEO_SIZE_MB = 500
    ALLOWED_FORMATS = ['mp4', 'mov', 'avi', 'mkv', 'webm']
    FRAME_EXTRACTION_RATE = 1  # Extract frame every N seconds
