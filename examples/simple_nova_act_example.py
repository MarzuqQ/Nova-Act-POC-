#!/usr/bin/env python3
"""
Simple Nova Act Example
This script demonstrates basic Nova Act usage patterns based on the official documentation.
"""

import os
import logging
from pydantic import BaseModel
from nova_act import NovaAct, BOOL_SCHEMA

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductInfo(BaseModel):
    name: str
    price: str
    in_stock: bool

class SearchResults(BaseModel):
    products: list[ProductInfo]

def example_search_and_extract():
    """Example: Search for products and extract structured data"""
    api_key = os.getenv('NOVA_ACT_API_KEY', '717e3076-ae10-4853-b9cc-7819b67f056c')
    
    with NovaAct(
        starting_page="https://example-store.com",
        headless=True,
        nova_act_api_key=api_key
    ) as nova:
        
        # Close any cookie banners
        nova.act("Close any cookie banners or promotional popups if they appear")
        
        # Search for a product
        nova.act("Search for 'laptop' in the search box and press enter")
        
        # Wait for results and extract structured data
        result = nova.act(
            "Extract the first 3 products with their names, prices, and availability",
            schema=SearchResults.model_json_schema()
        )
        
        if result.matches_schema:
            products = SearchResults.model_validate(result.parsed_response)
            logger.info("Found products:")
            for product in products.products:
                logger.info(f"- {product.name}: {product.price} (In Stock: {product.in_stock})")
        else:
            logger.warning("Could not extract structured product data")

def example_form_filling():
    """Example: Fill out a contact form"""
    api_key = os.getenv('NOVA_ACT_API_KEY', '717e3076-ae10-4853-b9cc-7819b67f056c')
    
    with NovaAct(
        starting_page="https://example-site.com/contact",
        headless=False,  # Visible for demonstration
        nova_act_api_key=api_key
    ) as nova:
        
        # Fill out contact form
        nova.act("Enter 'John Doe' in the name field")
        nova.act("Enter 'john.doe@example.com' in the email field")
        nova.act("Select 'Sales Inquiry' from the subject dropdown")
        nova.act("Enter 'I am interested in your products' in the message field")
        
        # Check if form is ready to submit
        result = nova.act("Is the submit button enabled and ready to click?", schema=BOOL_SCHEMA)
        
        if result.parsed_response:
            logger.info("Form is ready to submit")
            # nova.act("Click the submit button")  # Uncomment to actually submit
        else:
            logger.warning("Form is not ready to submit")

def example_parallel_processing():
    """Example: Process multiple pages in parallel"""
    from concurrent.futures import ThreadPoolExecutor
    
    api_key = os.getenv('NOVA_ACT_API_KEY', '717e3076-ae10-4853-b9cc-7819b67f056c')
    
    def process_page(url):
        with NovaAct(
            starting_page=url,
            headless=True,
            nova_act_api_key=api_key
        ) as nova:
            # Extract page title
            result = nova.act("What is the main heading or title of this page?")
            return f"{url}: {result.response}"
    
    urls = [
        "https://example.com",
        "https://example.org", 
        "https://example.net"
    ]
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(process_page, urls))
        
    for result in results:
        logger.info(result)

def main():
    """Run all examples"""
    try:
        logger.info("Running Nova Act examples...")
        
        # Example 1: Search and data extraction
        logger.info("=== Example 1: Search and Extract ===")
        example_search_and_extract()
        
        # Example 2: Form filling
        logger.info("=== Example 2: Form Filling ===")
        example_form_filling()
        
        # Example 3: Parallel processing
        logger.info("=== Example 3: Parallel Processing ===")
        example_parallel_processing()
        
        logger.info("All examples completed!")
        
    except Exception as e:
        logger.error(f"Examples failed: {e}")

if __name__ == "__main__":
    main() 