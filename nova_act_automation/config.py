#!/usr/bin/env python3
"""
Configuration settings for Nova Act automation
"""

import os
from typing import Dict, Any

class Config:
    """Configuration class for Nova Act automation"""
    
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        return {
            # Portal configuration
            'portal_url': os.getenv('PORTAL_URL', 'http://localhost:5000'),
            'username': os.getenv('PORTAL_USERNAME', 'shipping_admin'),
            'password': os.getenv('PORTAL_PASSWORD', 'secure_pass123'),
            
            # Nova Act configuration
            'nova_act_api_key': os.getenv('NOVA_ACT_API_KEY', '717e3076-ae10-4853-b9cc-7819b67f056c'),
            'headless': os.getenv('HEADLESS', 'true').lower() == 'true',
            'timeout': int(os.getenv('TIMEOUT', '300')),
            
            # Data files
            'data_file': os.getenv('DATA_FILE', 'sample_data/shipment_data.json'),
            'upload_file': os.getenv('UPLOAD_FILE', 'sample_data/shipment_data.json'),
            
            # Output configuration
            'output_bucket': os.getenv('OUTPUT_BUCKET', ''),
            'aws_region': os.getenv('AWS_REGION', 'us-east-1'),
            
            # Logging
            'log_level': os.getenv('LOG_LEVEL', 'INFO')
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values"""
        return self.config.copy()

# Global configuration instance
config = Config() 