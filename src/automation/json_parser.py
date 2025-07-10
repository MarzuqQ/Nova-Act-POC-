"""
JSON Parser utility for Nova Act automation
Handles different JSON formats and maps them to form fields
"""
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class JsonParser:
    """JSON parser for shipment data"""
    
    def __init__(self):
        """Initialize the JSON parser"""
        self.field_mappings = self._get_field_mappings()
    
    def _get_field_mappings(self) -> Dict[str, List[str]]:
        """
        Get field mappings from various JSON formats to standard form fields.
        Returns a dictionary where keys are standard field names and values are lists of possible JSON keys.
        """
        return {
            'shipper_name': [
                'shipper_name', 'shipper', 'sender_name', 'sender', 'from_name', 'from',
                'origin_name', 'origin_company', 'shipping_company', 'company_name'
            ],
            'shipper_address': [
                'shipper_address', 'shipper_addr', 'sender_address', 'sender_addr', 
                'from_address', 'from_addr', 'origin_address', 'origin_addr', 'pickup_address'
            ],
            'recipient_name': [
                'recipient_name', 'recipient', 'receiver_name', 'receiver', 'to_name', 'to',
                'destination_name', 'dest_name', 'customer_name', 'consignee_name', 'consignee'
            ],
            'recipient_address': [
                'recipient_address', 'recipient_addr', 'receiver_address', 'receiver_addr',
                'to_address', 'to_addr', 'destination_address', 'dest_address', 'delivery_address'
            ],
            'package_weight': [
                'package_weight', 'weight', 'pkg_weight', 'total_weight', 'gross_weight',
                'shipment_weight', 'parcel_weight', 'item_weight'
            ],
            'package_dimensions': [
                'package_dimensions', 'dimensions', 'pkg_dimensions', 'size', 'measurements',
                'length_width_height', 'lwh', 'box_size'
            ],
            'tracking_number': [
                'tracking_number', 'tracking_no', 'tracking_id', 'track_number', 'reference_number',
                'reference_no', 'shipment_id', 'order_number', 'order_id', 'awb_number'
            ],
            'shipping_date': [
                'shipping_date', 'ship_date', 'pickup_date', 'dispatch_date', 'send_date',
                'departure_date', 'collection_date', 'scheduled_date'
            ],
            'special_instructions': [
                'special_instructions', 'instructions', 'notes', 'comments', 'remarks',
                'delivery_instructions', 'handling_instructions', 'special_notes', 'description'
            ]
        }
    
    def parse_json_file(self, file_path: str) -> Dict[str, Any]:
        """Parse JSON file and return standardized data"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"JSON file not found: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            logger.info(f"Successfully loaded JSON from {file_path}")
            return self.parse_json_data(raw_data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format in {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error parsing JSON file {file_path}: {e}")
            raise
    
    def parse_json_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse JSON data and return standardized format"""
        try:
            # Handle nested structures (e.g., shipment.shipper.name)
            flattened_data = self._flatten_json(data)
            
            # Map to standard fields
            standardized_data = {}
            for standard_field, possible_keys in self.field_mappings.items():
                value = self._find_value_by_keys(flattened_data, possible_keys)
                if value is not None:
                    standardized_data[standard_field] = self._normalize_value(standard_field, value)
            
            # Add metadata
            standardized_data['_metadata'] = {
                'parsed_at': datetime.now().isoformat(),
                'original_keys': list(flattened_data.keys()),
                'found_mappings': {k: v for k, v in standardized_data.items() if not k.startswith('_')}
            }
            
            logger.info(f"Successfully parsed JSON data with {len(standardized_data)} fields")
            return standardized_data
            
        except Exception as e:
            logger.error(f"Error parsing JSON data: {e}")
            raise
    
    def _flatten_json(self, data: Dict[str, Any], parent_key: str = '', separator: str = '.') -> Dict[str, Any]:
        """Flatten nested JSON structure"""
        items = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                new_key = f"{parent_key}{separator}{key}" if parent_key else key
                
                if isinstance(value, dict):
                    items.extend(self._flatten_json(value, new_key, separator).items())
                elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                    # Handle array of objects (take first item)
                    items.extend(self._flatten_json(value[0], new_key, separator).items())
                else:
                    items.append((new_key, value))
        
        return dict(items)
    
    def _find_value_by_keys(self, data: Dict[str, Any], possible_keys: List[str]) -> Any:
        """Find value by trying multiple possible keys"""
        # Try exact matches first
        for key in possible_keys:
            if key in data:
                return data[key]
        
        # Try case-insensitive matches
        data_lower = {k.lower(): v for k, v in data.items()}
        for key in possible_keys:
            if key.lower() in data_lower:
                return data_lower[key.lower()]
        
        # Try partial matches
        for key in possible_keys:
            for data_key, value in data.items():
                if key.lower() in data_key.lower() or data_key.lower() in key.lower():
                    return value
        
        return None
    
    def _normalize_value(self, field_name: str, value: Any) -> str:
        """Normalize value based on field type"""
        if value is None:
            return ''
        
        # Convert to string
        str_value = str(value).strip()
        
        # Field-specific normalization
        if field_name == 'package_weight':
            # Extract numeric value
            import re
            match = re.search(r'(\d+\.?\d*)', str_value)
            return match.group(1) if match else str_value
        
        elif field_name == 'shipping_date':
            # Normalize date format
            return self._normalize_date(str_value)
        
        elif field_name in ['shipper_address', 'recipient_address']:
            # Handle address formatting
            return self._normalize_address(str_value)
        
        return str_value
    
    def _normalize_date(self, date_str: str) -> str:
        """Normalize date string to YYYY-MM-DD format"""
        try:
            # Common date formats
            formats = [
                '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d',
                '%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M:%S',
                '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f'
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            
            # If no format matches, return as-is
            return date_str
            
        except Exception:
            return date_str
    
    def _normalize_address(self, address_str: str) -> str:
        """Normalize address string"""
        # Replace common separators with newlines
        address_str = address_str.replace('|', '\n').replace(';', '\n')
        
        # Remove extra whitespace
        lines = [line.strip() for line in address_str.split('\n') if line.strip()]
        
        return '\n'.join(lines)
    
    def validate_parsed_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate parsed data and return validation report"""
        required_fields = ['shipper_name', 'recipient_name', 'package_weight', 'shipping_date']
        
        validation_report = {
            'is_valid': True,
            'missing_required': [],
            'found_fields': [],
            'warnings': []
        }
        
        # Check required fields
        for field in required_fields:
            if field not in data or not data[field]:
                validation_report['missing_required'].append(field)
                validation_report['is_valid'] = False
        
        # Check found fields
        for field in self.field_mappings.keys():
            if field in data and data[field]:
                validation_report['found_fields'].append(field)
        
        # Generate warnings
        if 'package_weight' in data:
            try:
                weight = float(data['package_weight'])
                if weight <= 0:
                    validation_report['warnings'].append('Package weight should be greater than 0')
                elif weight > 1000:
                    validation_report['warnings'].append('Package weight seems unusually high')
            except (ValueError, TypeError):
                validation_report['warnings'].append('Package weight is not a valid number')
        
        if 'shipping_date' in data:
            try:
                ship_date = datetime.strptime(data['shipping_date'], '%Y-%m-%d')
                if ship_date < datetime.now():
                    validation_report['warnings'].append('Shipping date is in the past')
            except ValueError:
                validation_report['warnings'].append('Shipping date format is invalid')
        
        logger.info(f"Validation report: {validation_report}")
        return validation_report
    
    def get_sample_json_formats(self) -> List[Dict[str, Any]]:
        """Get sample JSON formats for testing"""
        return [
            {
                "shipper_name": "Global Shipping Solutions Inc.",
                "shipper_address": "1234 Industrial Blvd\nSeattle, WA 98101",
                "recipient_name": "Pacific Coast Logistics",
                "recipient_address": "567 Harbor View Drive\nSan Francisco, CA 94111",
                "package_weight": 45.5,
                "package_dimensions": "24x18x12",
                "tracking_number": "GS2024010001",
                "shipping_date": "2024-01-15",
                "special_instructions": "Handle with care - fragile electronics"
            },
            {
                "shipment": {
                    "sender": {
                        "name": "ABC Corp",
                        "address": "123 Main St | New York, NY 10001"
                    },
                    "receiver": {
                        "name": "XYZ Ltd",
                        "address": "456 Oak Ave | Los Angeles, CA 90001"
                    },
                    "package": {
                        "weight": "25.3 lbs",
                        "dimensions": "12x8x6 inches",
                        "reference": "REF123456"
                    },
                    "schedule": {
                        "pickup_date": "2024-01-20",
                        "notes": "Fragile - handle with care"
                    }
                }
            },
            {
                "from_name": "Warehouse Solutions",
                "from_addr": "789 Industrial Way; Chicago, IL 60601",
                "to_name": "Distribution Center",
                "to_addr": "321 Commerce Blvd; Phoenix, AZ 85001",
                "weight": 15.8,
                "lwh": "10x10x10",
                "awb_number": "AWB789012",
                "dispatch_date": "01/25/2024",
                "remarks": "Standard delivery"
            }
        ]

def main():
    """Test the JSON parser"""
    parser = JsonParser()
    
    # Test with sample data
    sample_formats = parser.get_sample_json_formats()
    
    for i, sample in enumerate(sample_formats, 1):
        print(f"\n=== Testing Sample Format {i} ===")
        print(f"Original: {json.dumps(sample, indent=2)}")
        
        parsed = parser.parse_json_data(sample)
        print(f"Parsed: {json.dumps(parsed, indent=2)}")
        
        validation = parser.validate_parsed_data(parsed)
        print(f"Validation: {validation}")

if __name__ == "__main__":
    main() 