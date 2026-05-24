import os

class Config:
    AGENT_NAME = os.getenv('AGENT_NAME', 'marketing_generator')
    AGENT_PORT = int(os.getenv('AGENT_PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    
    # Paths
    PRODUCTS_DIR = '/app/products'
    OUTPUT_DIR = '/app/output'
    
    # HB Jewelry Configuration
    HB_JEWELRY_PRICE_MIN = int(os.getenv('HB_JEWELRY_PRICE_MIN', 15))
    HB_JEWELRY_PRICE_MAX = int(os.getenv('HB_JEWELRY_PRICE_MAX', 50))
    HB_JEWELRY_STYLE = os.getenv('HB_JEWELRY_STYLE', 'contemporary')
    HB_JEWELRY_AGE_MIN = int(os.getenv('HB_JEWELRY_AGE_MIN', 18))
    HB_JEWELRY_AGE_MAX = int(os.getenv('HB_JEWELRY_AGE_MAX', 45))
    HB_JEWELRY_PRODUCT_TYPES = os.getenv('HB_JEWELRY_PRODUCT_TYPES', 'rings,necklaces,bracelets,earrings,sets').split(',')
    
    # Copy Generation
    TONE = "contemporary, accessible, aspirational, inclusive"
    MAX_COPY_LENGTH = 280  # Twitter/short format
    PLATFORMS = ['instagram', 'tiktok', 'shopify', 'email']
