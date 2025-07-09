# Nova Act POC - Shipping Company Automation

This is a proof-of-concept (POC) demonstrating how Amazon Nova Act can automate web form interactions for shipping companies. The solution uses the **official Nova Act SDK** to automate the process of logging into vendor portals, uploading shipment documents, filling out forms with JSON data, and submitting them.

## 🎯 Project Overview

### Business Problem
Shipping companies need to manually:
- Log into various vendor portals
- Upload shipment documents  
- Fill out web forms with delivery data
- Submit forms manually

This process is time-consuming, error-prone, and not scalable.

### Solution
Using **Amazon Nova Act**, this POC automates the entire workflow:
1. **Automated Login**: Natural language instructions for secure portal access
2. **Two Automation Modes**: Manual form filling OR auto-fill via JSON upload
3. **Intelligent Form Processing**: AI-powered form field identification and completion
4. **File Upload**: Automated document upload with validation
5. **Form Submission**: Intelligent form submission with confirmation capture

## 🏗️ Architecture

```
[User] → [Nova Act Automation] → [Demo Vendor Portal]
   ↓
[JSON Data] → [Parser] → [Form Fields] → [Submission]
   ↓
[Results] → [Local Storage] → [Confirmation]
```

## 📁 Project Structure

```
Nova-Act-POC-/
├── demo_vendor_portal/          # Demo web portal for testing
│   ├── app.py                   # Flask application
│   ├── templates/               # HTML templates
│   │   ├── base.html           # Base template
│   │   ├── login.html          # Login page
│   │   ├── dashboard.html      # Dashboard
│   │   ├── shipment_form.html  # Main form
│   │   └── submission_success.html # Success page
│   ├── requirements.txt         # Python dependencies
│   ├── uploads/                 # File upload directory
│   └── submissions/             # Form submission results
├── nova_act_automation/         # Main automation code
│   ├── main.py                  # Primary automation script
│   ├── json_parser.py           # JSON parsing utilities
│   ├── file_utils.py            # File handling utilities
│   ├── config.py                # Configuration management
│   └── requirements.txt         # Python dependencies
├── sample_data/                 # Sample JSON files
│   ├── shipment_data.json       # Standard format
│   ├── nested_shipment_data.json # Nested format
│   └── alternative_format.json  # Alternative format
├── examples/                    # Example scripts
│   ├── simple_nova_act_example.py
│   └── test_nova_act.py
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- **Nova Act API Key** (required)
- Basic familiarity with command line

### 1. Get Nova Act API Key
1. Visit [nova.amazon.com](https://nova.amazon.com) and sign in
2. Navigate to the **Act** section
3. Generate your API key

### 2. Clone and Setup
```bash
git clone <your-repo-url>
cd Nova-Act-POC-
```

### 3. Install Dependencies
```bash
# Install Nova Act automation dependencies
pip install -r nova_act_automation/requirements.txt

# Install demo portal dependencies
pip install -r demo_vendor_portal/requirements.txt
```

### 4. Configure API Key
Set your Nova Act API key as an environment variable:
```bash
export NOVA_ACT_API_KEY=your-api-key-here
```

### 5. Start Demo Portal
```bash
cd demo_vendor_portal
python app.py
```

### 6. Access Demo Portal
- Open http://localhost:5000
- Login with credentials:
  - Username: `shipping_admin`
  - Password: `secure_pass123`

### 7. Run Automation
```bash
cd nova_act_automation
python main.py
```

## ⚙️ Automation Modes

This POC supports **two automation modes** configurable in `nova_act_automation/main.py`:

### Mode 1: Manual Form Filling (Default)
```python
'use_manual_filling': True  # Set to True for manual mode
```

**How it works:**
1. Nova Act reads data from JSON file
2. Fills each form field individually using natural language commands
3. Submits the form

**Best for:** Simple forms, debugging, understanding the process

### Mode 2: Auto-Fill via JSON Upload
```python
'use_manual_filling': False  # Set to False for auto-fill mode
```

**How it works:**
1. Nova Act uploads the JSON file using playwright to the portal
2. Frontend JavaScript automatically fills all form fields
3. Nova Act submits the form

**Best for:** Complex forms, faster processing, production use

## 📊 Sample Data Format

The POC uses **MM/DD/YYYY** date format and supports multiple JSON structures:

### Standard Format (`sample_data/shipment_data.json`)
```json
{
  "shipper_name": "Global Shipping Solutions Inc.",
  "shipper_address": "1234 Industrial Blvd\nWarehouse District\nSeattle, WA 98101",
  "recipient_name": "Pacific Coast Logistics",
  "recipient_address": "567 Harbor View Drive\nSuite 200\nSan Francisco, CA 94111",
  "package_weight": 45.5,
  "package_dimensions": "24x18x12",
  "tracking_number": "GS2024010001",
  "shipping_date": "07/15/2025",
  "special_instructions": "Handle with care - fragile electronics inside."
}
```

### Nested Format (`sample_data/nested_shipment_data.json`)
```json
{
  "shipment": {
    "sender": {
      "name": "TechCorp Industries",
      "address": "4567 Technology Drive\nAustin, TX 78701"
    },
    "receiver": {
      "name": "Innovation Labs",
      "address": "890 Research Park\nBoston, MA 02101"
    },
    "package": {
      "weight": "12.7 lbs",
      "dimensions": "16x12x8 inches",
      "reference": "TC2024020001"
    },
    "details": {
      "ship_date": "03/20/2025",
      "instructions": "Deliver to loading dock"
    }
  }
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NOVA_ACT_API_KEY` | Your Nova Act API key | Required |
| `PORTAL_URL` | Demo portal URL | `http://localhost:5000` |
| `PORTAL_USERNAME` | Portal login username | `shipping_admin` |
| `PORTAL_PASSWORD` | Portal login password | `secure_pass123` |
| `DATA_FILE` | Path to JSON data file | `sample_data/shipment_data.json` |
| `UPLOAD_FILE` | Path to file to upload | `sample_data/shipment_data.json` |
| `HEADLESS` | Run browser in headless mode | `true` |
| `TIMEOUT` | Operation timeout in seconds | `300` |

### Configuration Examples

```bash
# Run with visible browser (for debugging)
HEADLESS=false python main.py

# Run with different data file
DATA_FILE=sample_data/nested_shipment_data.json python main.py

# Run with different credentials
PORTAL_USERNAME=logistics_user PORTAL_PASSWORD=logistics_pass456 python main.py
```

## 🔧 Features

### Nova Act Integration
- **Natural Language Automation**: Use plain English commands to control the browser
- **Intelligent Form Filling**: AI-powered form field identification and completion
- **Context-Aware Actions**: Nova Act understands page context and takes appropriate actions
- **File Upload Handling**: Automated file upload with proper validation

### JSON Parser (`json_parser.py`)
- **Flexible Field Mapping**: Automatically maps various JSON field names to form fields
- **Nested Structure Support**: Handles complex nested JSON objects
- **Data Validation**: Validates required fields and provides helpful warnings
- **Multiple Format Support**: Works with different JSON structures

### File Utilities (`file_utils.py`)
- **File Validation**: Validates file types, sizes, and formats
- **Multiple Format Support**: JSON, PDF, CSV, XML, TXT
- **Security Checks**: Prevents malicious file uploads

### Demo Portal Features
- **Modern UI**: Bootstrap-based responsive design
- **Two-Column Layout**: Optimized form layout for better usability
- **File Upload**: Drag-and-drop file upload with auto-fill
- **Real-time Validation**: Form validation with helpful error messages
- **Session Management**: Secure user authentication

## 🐛 Troubleshooting

### Common Issues

#### Nova Act API Key Issues
```bash
# Error: Invalid API key
# Solution: Verify your API key is correctly set
export NOVA_ACT_API_KEY=your-actual-api-key-here
python examples/test_nova_act.py
```

#### Portal Connection Issues
```bash
# Error: Connection refused
# Solution: Ensure demo portal is running
cd demo_vendor_portal
python app.py
```

#### Date Field Issues
- **Issue**: Date not entering correctly
- **Solution**: Use MM/DD/YYYY format in JSON data
- **Note**: Date field is now a text input for better compatibility

#### Form Filling Issues
- **Issue**: Form fields not found
- **Solution**: Check JSON field names match expected format
- **Debug**: Run with `HEADLESS=false` to see browser actions

### Debugging Tips
1. **Use Visible Browser**: Set `HEADLESS=false` to see what's happening
2. **Check Logs**: Review console output for detailed error messages
3. **Test Individual Components**: Use example scripts to verify setup
4. **Verify Data Format**: Check JSON data structure and field mappings

## 🛠️ Development

### Running Tests
```bash
# Test Nova Act setup
python examples/test_nova_act.py

# Test with simple example
python examples/simple_nova_act_example.py
```

### Adding New Field Mappings
Edit `nova_act_automation/json_parser.py` to add new field variations:

```python
'new_field_name': [
    'new_field_name', 'alternative_name', 'another_variation'
]
```

### Extending Automation
- Add new automation steps in `main.py`
- Use natural language commands with Nova Act
- Handle edge cases and error scenarios

## 📈 Results and Monitoring

### Result Storage
Results are automatically saved to `nova_act_automation/automation_results_TIMESTAMP.json`:

```json
{
  "automation_run": {
    "timestamp": "2025-01-15T10:30:00Z",
    "config": { ... },
    "confirmation": {
      "confirmation_number": "CONF123456",
      "submission_time": "2025-01-15 10:30:00",
      "status": "success"
    }
  }
}
```

### Logging
- **INFO**: General automation progress
- **WARNING**: Non-critical issues (missing optional fields)
- **ERROR**: Critical failures
- **DEBUG**: Detailed Nova Act actions

## 🚨 Production Considerations

### Security
- **Never hard-code credentials**: Always use environment variables
- **Secure API keys**: Keep Nova Act API key secure
- **File validation**: Always validate uploaded files
- **HTTPS**: Use HTTPS for production portals

### Performance
- **Headless mode**: Use for production to save resources
- **Timeout settings**: Adjust based on portal response times
- **Error handling**: Implement proper retry logic

### Scaling
- **Batch processing**: Process multiple shipments
- **Queue management**: Use message queues for high volume
- **Monitoring**: Implement proper logging and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in the console
3. Test with visible browser mode
4. Open an issue on GitHub

---

**Note**: This is a demonstration POC. For production use, implement additional security measures, comprehensive error handling, and monitoring. 