import os

class Config:
    AGENT_NAME = os.getenv('AGENT_NAME', 'shopify_integration')
    AGENT_PORT = int(os.getenv('AGENT_PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    
    # Paths
    CONFIG_DIR = '/app/config'
    LOGS_DIR = '/app/logs'
    
    # Shopify Configuration
    SHOPIFY_STORE_URL = os.getenv('SHOPIFY_STORE_URL', '')
    SHOPIFY_ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN', '')
    SHOPIFY_API_VERSION = os.getenv('SHOPIFY_API_VERSION', '2024-01')
    
    # Sync Configuration
    SYNC_INTERVAL = 3600  # seconds
    BATCH_SIZE = 100
