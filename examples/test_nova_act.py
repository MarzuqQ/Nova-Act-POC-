#!/usr/bin/env python3
"""
Test script to verify Nova Act SDK is working correctly
"""

import os
import logging
from nova_act import NovaAct, BOOL_SCHEMA

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_nova_act():
    """Test basic Nova Act functionality"""
    try:
        # Set API key
        api_key = os.getenv('NOVA_ACT_API_KEY', '717e3076-ae10-4853-b9cc-7819b67f056c')
        
        logger.info("Testing Nova Act SDK...")
        
        # Test with a simple website
        with NovaAct(
            starting_page="https://example.com",
            headless=False,  # Set to False to watch browser in real-time
            nova_act_api_key=api_key,
            ignore_https_errors=True  # Allow localhost and self-signed certificates
        ) as nova:
            
            # Simple test action
            result = nova.act("Look at the page and tell me if there is a heading visible", schema=BOOL_SCHEMA)
            
            logger.info(f"Test result: {result}")
            
            if result.matches_schema:
                logger.info("✅ Nova Act SDK is working correctly!")
                return True
            else:
                logger.error("❌ Nova Act SDK test failed - no valid response")
                return False
                
    except Exception as e:
        logger.error(f"❌ Nova Act SDK test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_nova_act()
    if success:
        print("Nova Act SDK test passed!")
    else:
        print("Nova Act SDK test failed!")
        exit(1) 