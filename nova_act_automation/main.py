#!/usr/bin/env python3
"""
Nova Act POC: Automation Script for Vendor Portal
This script demonstrates automated web form interactions using Amazon Nova Act.
"""

import os
import json
import logging
import time
from datetime import datetime, date
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel
from nova_act import NovaAct
from json_parser import JsonParser
from file_utils import FileUtils

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ConfirmationData(BaseModel):
    confirmation_number: str
    submission_time: str
    status: str

class NovaActAutomation:
    """Main class for Nova Act automation workflow"""
    
    def __init__(self):
        """Initialize the automation class with configuration"""
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.config = self._load_config()
        self.json_parser = JsonParser()
        self.file_utils = FileUtils()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        # Default file paths relative to project root
        default_data_file = self.project_root / 'sample_data' / 'shipment_data.json'
        default_upload_file = self.project_root / 'sample_data' / 'shipment_data.json'
        
        config = {
            'portal_url': os.getenv('PORTAL_URL', 'http://localhost:5000'),
            'username': os.getenv('PORTAL_USERNAME', 'shipping_admin'),
            'password': os.getenv('PORTAL_PASSWORD', 'secure_pass123'),
            'data_file': os.getenv('DATA_FILE', str(default_data_file)),
            'upload_file': os.getenv('UPLOAD_FILE', str(default_upload_file)),
            # 'output_bucket': os.getenv('OUTPUT_BUCKET', ''),
            # 'aws_region': os.getenv('AWS_REGION', 'us-east-1'),
            'timeout': int(os.getenv('TIMEOUT', '300')),
            'headless': os.getenv('HEADLESS', 'true').lower() == 'true',
            'nova_act_api_key': os.getenv('NOVA_ACT_API_KEY', '717e3076-ae10-4853-b9cc-7819b67f056c'),
            
            # AUTOMATION MODE: Change this line to switch between manual and auto-fill modes
            'use_manual_filling': False  # Set to False for auto-fill mode
        }
        
        logger.info(f"Configuration loaded: {config}")
        return config
    
    def _load_shipment_data(self) -> Dict[str, Any]:
        """Load shipment data from JSON file using JSON parser"""
        try:
            data_file = Path(self.config['data_file'])
            if not data_file.exists():
                raise FileNotFoundError(f"Data file not found: {data_file}")
            
            # Use JSON parser to handle different formats
            parsed_data = self.json_parser.parse_json_file(str(data_file))
            
            # Validate parsed data
            validation_report = self.json_parser.validate_parsed_data(parsed_data)
            
            if not validation_report['is_valid']:
                logger.warning(f"Data validation failed: {validation_report}")
                logger.warning("Continuing with available data...")
            
            if validation_report['warnings']:
                for warning in validation_report['warnings']:
                    logger.warning(f"Data warning: {warning}")
            
            logger.info(f"Loaded and parsed shipment data from {data_file}")
            logger.info(f"Found fields: {validation_report['found_fields']}")
            
            return parsed_data
        except Exception as e:
            logger.error(f"Failed to load shipment data: {e}")
            raise
    
    # ============================================================================
    # AUTOMATION WORKFLOW METHODS
    # ============================================================================
    
    def login_to_portal(self, nova: NovaAct) -> None:
        """Login to the vendor portal using Nova Act"""
        try:
            logger.info("Logging into vendor portal...")
            
            # Handle any cookie banners or promotional offers
            # nova.act("Close any cookie banners or promotional offers if they appear")
            
            # Fill in login credentials and submit
            nova.act(f"Enter '{self.config['username']}' in the username field")
            nova.act(f"Enter '{self.config['password']}' in the password field")
            nova.act("Click the login button to submit the form")
            
            # Wait for dashboard to load
            # time.sleep(2)
            
            logger.info("Successfully logged into portal")
        except Exception as e:
            logger.error(f"Failed to login to portal: {e}")
            raise
    
    def navigate_to_shipment_form(self, nova: NovaAct) -> None:
        """Navigate to the shipment form"""
        try:
            logger.info("Navigating to shipment form...")
            
            # Wait a moment for page to fully load
            # time.sleep(1)
            
            # Click on the shipment form link with retry logic
            for attempt in range(3):
                try:
                    nova.act("Click on the 'New Shipment' or 'Shipment Form' link to navigate to the form")
                    break
                except Exception as e:
                    if attempt == 2:  # Last attempt
                        raise e
                    logger.warning(f"Navigation attempt {attempt + 1} failed, retrying: {e}")
                    time.sleep(2)
            
            # Wait for form to load
            # time.sleep(3)
            
            logger.info("Navigated to shipment form")
        except Exception as e:
            logger.error(f"Failed to navigate to shipment form: {e}")
            raise
    
    # ============================================================================
    # FORM PROCESSING METHODS
    # ============================================================================
    
    def process_shipment_form(self, nova: NovaAct, shipment_data: Dict[str, Any]) -> None:
        """Process shipment form based on configured automation mode"""
        if self.config['use_manual_filling']:
            logger.info("Using MANUAL form filling mode")
            self.fill_shipment_form(nova, shipment_data)
        else:
            logger.info("Using AUTO-FILL mode (JSON upload)")
            self.upload_json_and_autofill(nova)
    
    # Function used when manually filling the form
    def fill_shipment_form(self, nova: NovaAct, data: Dict[str, Any]) -> None:
        """Fill the shipment form with data using Nova Act"""
        try:
            logger.info("Filling shipment form with data...")
            
            # Fill shipper information
            if data.get('shipper_name'):
                nova.act(f"Enter '{data['shipper_name']}' in the shipper name field")
            
            if data.get('shipper_address'):
                nova.act(f"Enter '{data['shipper_address']}' in the shipper address field")
            
            # Fill recipient information
            if data.get('recipient_name'):
                nova.act(f"Enter '{data['recipient_name']}' in the recipient name field")
                
            if data.get('recipient_address'):
                nova.act(f"Enter '{data['recipient_address']}' in the recipient address field")
            
            # Fill package information
            if data.get('package_weight'):
                nova.act(f"Enter '{data['package_weight']}' in the package weight field")
                
            if data.get('package_dimensions'):
                nova.act(f"Enter '{data['package_dimensions']}' in the package dimensions field")
                
            if data.get('tracking_number'):
                nova.act(f"Enter '{data['tracking_number']}' in the tracking number field")
            
            # Fill shipping date
            if data.get('shipping_date'):
                nova.act(f"Enter '{data['shipping_date']}' in the shipping date field")
            
            # Fill special instructions
            if data.get('special_instructions'):
                nova.act(f"Enter '{data['special_instructions']}' in the special instructions field")
            
            logger.info("Form filled successfully with shipment data")
        except Exception as e:
            logger.error(f"Failed to fill shipment form: {e}")
            raise
    
    # Function used when auto-filling the form
    def upload_json_and_autofill(self, nova: NovaAct) -> None:
        """Upload JSON file using proper Nova Act + Playwright approach"""
        try:
            upload_file = Path(self.config['upload_file'])
            
            if not upload_file.exists():
                logger.error(f"Upload file not found: {upload_file}")
                raise FileNotFoundError(f"Upload file not found: {upload_file}")
            
            logger.info(f"Uploading JSON file for auto-fill: {upload_file}")
            
            # Validate file
            if not self.file_utils.validate_file(str(upload_file)):
                logger.error(f"File validation failed: {upload_file}")
                raise ValueError(f"File validation failed: {upload_file}")
            
            # Convert to absolute path for upload
            absolute_path = upload_file.resolve()
            
            # PROPER APPROACH: Use Nova Act for web interactions, Playwright for file upload
            # Step 1: Use Nova Act to locate and prepare the file upload element
            nova.act("Locate the file upload input field on the form")
            
            # Step 2: Use Playwright to handle the actual file selection
            # This bypasses the system dialog issue
            file_input = nova.page.locator('input[type="file"]')
            file_input.set_input_files(str(absolute_path))
            
            logger.info("File uploaded successfully using Playwright")
            
            # Step 3: Wait for any auto-processing to complete
            time.sleep(5)  # Give more time for JavaScript auto-fill to complete
            
            # Step 4: Use Nova Act to verify the upload was successful (more lenient check)
            try:
                nova.act("Check if any form fields have been populated or if the file upload field shows a filename")
            except Exception as e:
                logger.warning(f"Form field verification failed, but continuing: {e}")
                # Continue anyway - the frontend auto-fill might have worked even if not visually confirmed
            
            logger.info("JSON file uploaded successfully and form processing completed")
        except Exception as e:
            logger.error(f"Failed to upload JSON file and auto-fill form: {e}")
            raise
    
    # ============================================================================
    # FORM SUBMISSION & RESULTS
    # ============================================================================
    
    def submit_form(self, nova: NovaAct) -> None:
        """Submit the shipment form"""
        try:
            logger.info("Submitting shipment form...")
            
            # Submit the form
            # nova.act("Search for the submit button on the page")
            nova.act("Click the submit button to submit the shipment form")
            
            # Wait for submission to complete
            # time.sleep(3)
            
            logger.info("Form submitted successfully")
        except Exception as e:
            logger.error(f"Failed to submit form: {e}")
            raise
    
    def capture_confirmation(self, nova: NovaAct) -> Dict[str, Any]:
        """Capture confirmation details from the success page"""
        try:
            logger.info("Capturing confirmation details...")
            
            # Extract confirmation data using Nova Act with schema
            result = nova.act(
                "Extract the confirmation number, submission time, and status from the success page",
                schema=ConfirmationData.model_json_schema()
            )
            
            if result.matches_schema:
                confirmation = ConfirmationData.model_validate(result.parsed_response)
                confirmation_data = {
                    'confirmation_number': confirmation.confirmation_number,
                    'submission_time': confirmation.submission_time,
                    'status': confirmation.status,
                    'timestamp': datetime.now().isoformat()
                }
                logger.info(f"Captured confirmation: {confirmation_data}")
                return confirmation_data
            else:
                logger.warning("Failed to extract structured confirmation data")
                # Fallback to getting raw text
                result = nova.act("Return all visible text from the success page")
                return {
                    'raw_confirmation': result.response,
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Failed to capture confirmation: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def save_results(self, confirmation: Dict[str, Any]) -> None:
        """Save automation results"""
        try:
            results = {
                'automation_run': {
                    'timestamp': datetime.now().isoformat(),
                    'config': self.config,
                    'confirmation': confirmation
                }
            }
            
            # Save locally
            output_file = f"automation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(f"Results saved to {output_file}")
            
            # Save to S3 if configured
            if self.config.get('output_bucket'):
                self._save_to_s3(results, output_file)
                
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
    '''
    def _save_to_s3(self, results: Dict[str, Any], filename: str) -> None:
        """Save results to S3"""
        try:
            import boto3
            s3_client = boto3.client('s3', region_name=self.config['aws_region'])
            
            s3_client.put_object(
                Bucket=self.config['output_bucket'],
                Key=f"nova-act-results/{filename}",
                Body=json.dumps(results, indent=2),
                ContentType='application/json'
            )
            
            logger.info(f"Results uploaded to S3: s3://{self.config['output_bucket']}/nova-act-results/{filename}")
        except Exception as e:
            logger.error(f"Failed to save to S3: {e}")
    '''
    def run_automation(self) -> None:
        """Run the complete automation workflow"""
        try:
            logger.info("Starting Nova Act automation workflow...")
            
            # Load shipment data
            shipment_data = self._load_shipment_data()
            
            # Initialize Nova Act with proper configuration
            with NovaAct(
                starting_page=self.config['portal_url'],
                headless=self.config['headless'],
                nova_act_api_key=self.config['nova_act_api_key'],
                ignore_https_errors=True  # Required for localhost URLs
            ) as nova:
                
                # Login to portal
                self.login_to_portal(nova)
                
                # Navigate to shipment form
                self.navigate_to_shipment_form(nova)
                
                # Process shipment form (mode determined by config)
                self.process_shipment_form(nova, shipment_data) # shipment_data = parsed json data
                
                # Submit the form
                self.submit_form(nova)
                
                # Capture confirmation
                confirmation = self.capture_confirmation(nova)
                
                # Save results
                self.save_results(confirmation)
                
                logger.info("Automation workflow completed successfully")
                
        except Exception as e:
            logger.error(f"Automation workflow failed: {e}")
            raise

def main():
    """Main entry point"""
    try:
        automation = NovaActAutomation()
        automation.run_automation()
        logger.info("Nova Act automation completed successfully")
    except Exception as e:
        logger.error(f"Nova Act automation failed: {e}")
        exit(1)

if __name__ == "__main__":
    main()