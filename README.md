# Nova Act POC - Shipping Company Automation

This is a proof-of-concept (POC) demonstrating how Amazon Nova Act can automate web form interactions for shipping companies. The solution uses the **official Nova Act SDK** to automate the process of logging into vendor portals, uploading shipment documents, filling out forms with JSON data, and submitting them.

> **✨ Now Updated**: This implementation has been completely rewritten to use the actual Nova Act SDK with proper natural language automation, replacing the previous mock implementation with real AI-powered browser automation.

## 🎯 Project Overview

### Business Problem
Shipping companies need to manually:
- Log into various vendor portals
- Upload shipment documents
- Fill out web forms with delivery data
- Submit forms manually

This process is time-consuming, error-prone, and not scalable.

### Solution
Using the **Amazon Nova Act SDK**, this POC automates the entire workflow:
1. **Automated Login**: Natural language instructions for login automation
2. **JSON Data Processing**: Flexible parser handles various JSON formats
3. **Form Automation**: AI-powered form filling using natural language commands
4. **File Upload**: Automated document upload with Nova Act
5. **Form Submission**: Intelligent form submission with confirmation capture

## 🏗️ Architecture

```
[User] → [Docker Container] → [Nova Act] → [Demo Portal]
   ↓
[JSON Data] → [Parser] → [Form Fields] → [Submission]
   ↓
[Results] → [S3/Local Storage] → [Confirmation]
```

## 📁 Project Structure

```
Nova Act POC WWEX/
├── demo_vendor_portal/          # Demo web portal for testing
│   ├── app.py                   # Flask application
│   ├── templates/               # HTML templates
│   ├── requirements.txt         # Python dependencies
│   └── uploads/                 # File upload directory
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
├── scripts/                     # Build and deployment scripts
│   └── build.sh                 # Docker build script
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Container orchestration
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- **Nova Act API Key** (required - see setup below)
- AWS credentials (optional - for S3 storage)
- Basic familiarity with command line

### 1. Get Nova Act API Key
1. Visit [nova.amazon.com](https://nova.amazon.com) and sign in with your Amazon account
2. Navigate to the **Act** section in the Labs
3. Request access if needed (approval typically takes 24 hours)
4. Generate your API key once approved

⚠️ **Important**: Nova Act is currently only available in the US.

### 2. Clone and Setup
```bash
git clone <your-repo-url>
cd "Nova Act POC WWEX"
```

### 3. Configure API Key
Set your Nova Act API key as an environment variable:
```bash
export NOVA_ACT_API_KEY=your-api-key-here
```

### 4. Install Dependencies
```bash
# Install Nova Act SDK
pip install nova-act
pip install -r nova_act_automation/requirements.txt

# Install Playwright (required by Nova Act)
playwright install chrome
```

### 5. Test Nova Act Setup
```bash
# Test your Nova Act configuration
python test_nova_act.py
```

### 6. Start Demo Portal
```bash
# Start the demo portal
cd demo_vendor_portal
pip install -r requirements.txt
python app.py
```

### 7. Access Demo Portal
- Open http://localhost:5000
- Login with credentials:
  - Username: `shipping_admin`, Password: `secure_pass123`
  - Username: `logistics_user`, Password: `logistics_pass456`

### 8. Run Automation
```bash
# Run with default data
python nova_act_automation/main.py

# Or run with custom data file
DATA_FILE=sample_data/nested_shipment_data.json python nova_act_automation/main.py
```

## ⚙️ Configuration

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
| `OUTPUT_BUCKET` | S3 bucket for results (optional) | `` |
| `AWS_REGION` | AWS region for S3 | `us-east-1` |

### Configuration Examples

```bash
# Run with visible browser (for debugging)
HEADLESS=false python nova_act_automation/main.py

# Run with different credentials
PORTAL_USERNAME=logistics_user PORTAL_PASSWORD=logistics_pass456 python nova_act_automation/main.py

# Run with S3 output
OUTPUT_BUCKET=my-automation-results python nova_act_automation/main.py
```

## 📊 Sample Data Formats

The POC supports multiple JSON formats:

### Standard Format
```json
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
}
```

### Nested Format
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
    }
  }
}
```

### Alternative Format
```json
{
  "from_name": "Express Logistics LLC",
  "from_addr": "2468 Warehouse Blvd; Atlanta, GA 30309",
  "to_name": "Retail Distribution Hub",
  "to_addr": "1357 Commerce Center; Miami, FL 33101",
  "gross_weight": 33.2,
  "lwh": "20x15x10",
  "awb_number": "EL2024030001"
}
```

## 🔧 Features

### Nova Act SDK Integration
- **Natural Language Automation**: Use plain English commands to control the browser
- **Intelligent Form Filling**: AI-powered form field identification and completion
- **Structured Data Extraction**: Extract confirmation data using Pydantic schemas
- **Context-Aware Actions**: Nova Act understands page context and takes appropriate actions

### JSON Parser
- **Flexible Field Mapping**: Automatically maps various JSON field names to form fields
- **Nested Structure Support**: Handles complex nested JSON objects
- **Data Validation**: Validates required fields and data types
- **Format Normalization**: Normalizes dates, addresses, and numeric values

### File Upload
- **Multiple Format Support**: JSON, PDF, CSV, XML, TXT
- **File Size Validation**: Configurable size limits per file type
- **AI-Powered Upload**: Nova Act intelligently handles file upload interfaces
- **Upload Verification**: Confirms successful file upload

### Automation Features
- **Headless Operation**: Runs without GUI for production deployments
- **Error Handling**: Comprehensive error handling and logging
- **Session Management**: Proper browser session handling with Nova Act
- **Result Storage**: Saves results to S3 or local storage

## 🌐 Demo Portal Features

### Authentication
- Session-based authentication
- Multiple user accounts for testing
- Secure credential handling

### Form Handling
- Comprehensive shipment form with all required fields
- File upload with drag-and-drop support
- Real-time validation
- Form pre-filling from uploaded JSON

### Responsive Design
- Mobile-friendly interface
- Modern Bootstrap-based UI
- Interactive form elements
- Success/error messaging

## 🔧 Best Practices

### Nova Act Usage
- **Break Down Complex Tasks**: Use multiple `act()` calls for complex workflows
- **Use Natural Language**: Write instructions as if talking to a human
- **Verify Actions**: Check page state before proceeding to next steps
- **Handle Errors Gracefully**: Implement proper error handling and retries

### Data Handling
- **Validate JSON Data**: Always validate input data before processing
- **Handle Missing Fields**: Gracefully handle missing or null data fields
- **Normalize Data**: Ensure consistent data formatting across different sources

### Security
- **Never Hard-Code Credentials**: Always use environment variables
- **Secure API Keys**: Keep your Nova Act API key secure and never commit it to version control
- **Validate File Uploads**: Always validate file types and sizes

## 🐛 Troubleshooting

### Common Issues

#### Nova Act API Key Issues
```bash
# Error: Invalid API key
# Solution: Verify your API key is correctly set
export NOVA_ACT_API_KEY=your-actual-api-key-here
python test_nova_act.py
```

#### Browser/Playwright Issues
```bash
# Error: Browser not found
# Solution: Install Playwright browsers
playwright install chrome
```

#### Portal Connection Issues
```bash
# Error: Connection refused
# Solution: Ensure demo portal is running
cd demo_vendor_portal
python app.py
```

#### Form Filling Issues
- **Issue**: Form fields not found
- **Solution**: Check if field selectors match the actual form structure
- **Debug**: Run with `HEADLESS=false` to see browser actions

#### File Upload Issues
- **Issue**: File not uploading
- **Solution**: Ensure file path is absolute and accessible
- **Debug**: Check file permissions and format

### Debugging Tips
1. **Use Visible Browser**: Set `HEADLESS=false` to see what's happening
2. **Check Logs**: Review console output for detailed error messages
3. **Test Individual Components**: Use the test script to verify Nova Act setup
4. **Verify Data**: Check JSON data format and field mappings

## 📚 API Reference

### NovaActAutomation Class

#### Methods
- `run_automation()`: Main automation workflow
- `login_to_portal(nova)`: Login to vendor portal
- `navigate_to_shipment_form(nova)`: Navigate to form page
- `fill_shipment_form(nova, data)`: Fill form with data
- `upload_file(nova)`: Upload file attachment
- `submit_form(nova)`: Submit the form
- `capture_confirmation(nova)`: Capture confirmation data

#### Configuration
- Uses environment variables for configuration
- Supports multiple JSON data formats
- Handles file uploads and S3 storage

## 🚢 AWS Deployment

### ECS Deployment
```bash
# Build for ECS
docker build -t nova-act-automation .

# Tag for ECR
docker tag nova-act-automation:latest <account-id>.dkr.ecr.<region>.amazonaws.com/nova-act-automation:latest

# Push to ECR
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/nova-act-automation:latest
```

### Lambda Deployment
The automation can be packaged for AWS Lambda:
```bash
# Create deployment package
cd nova_act_automation
zip -r ../lambda-deployment.zip .
```

### Environment Variables for Production
```bash
# Required
PORTAL_URL=https://vendor-portal.example.com
PORTAL_USERNAME=automation_user
PORTAL_PASSWORD=secure_password
AWS_REGION=us-east-1
OUTPUT_BUCKET=automation-results-bucket

# Optional
TIMEOUT=300
HEADLESS=true
LOG_LEVEL=INFO
```

## 🔍 Monitoring and Logging

### Log Levels
- **INFO**: General automation progress
- **WARNING**: Non-critical issues
- **ERROR**: Critical failures
- **DEBUG**: Detailed debugging information

### Result Storage
Results are stored in JSON format:
```json
{
  "automation_run": {
    "timestamp": "2024-01-15T10:30:00Z",
    "status": "success",
    "config": { ... },
    "confirmation": {
      "page_content": "...",
      "screenshot": "base64_encoded_image"
    }
  }
}
```

## 🛠️ Development

### Running Locally
```bash
# Install dependencies
pip install -r nova_act_automation/requirements.txt
pip install -r demo_vendor_portal/requirements.txt

# Run demo portal
cd demo_vendor_portal
python app.py

# Run automation
cd nova_act_automation
python main.py
```

### Testing
```bash
# Test JSON parser
python nova_act_automation/json_parser.py

# Test file utilities
python nova_act_automation/file_utils.py

# Manual testing via demo portal
curl -X POST http://localhost:5000/api/health
```

## 🚨 Troubleshooting

### Common Issues

1. **Docker Build Fails**
   - Ensure Docker is running
   - Check internet connectivity
   - Verify Dockerfile syntax

2. **Nova Act Connection Issues**
   - Verify AWS credentials
   - Check Nova Act service availability
   - Ensure proper IAM permissions

3. **Portal Access Issues**
   - Verify portal is running: `docker-compose ps`
   - Check port availability: `lsof -i :5000`
   - Review portal logs: `docker-compose logs demo-portal`

4. **File Upload Problems**
   - Check file size limits
   - Verify file format support
   - Ensure proper file permissions

### Debug Commands
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f nova-act-automation

# Access container shell
docker-compose exec nova-act-automation /bin/bash

# Test portal connectivity
curl -f http://localhost:5000/api/health
```

## 📈 Performance Considerations

### Scaling
- **Horizontal Scaling**: Run multiple automation containers
- **Queue Management**: Use SQS for job queuing
- **Load Balancing**: Distribute requests across instances

### Optimization
- **Headless Mode**: Reduces resource usage
- **Caching**: Cache frequently used data
- **Batch Processing**: Process multiple shipments together

## 🔒 Security

### Credential Management
- Environment variables for sensitive data
- AWS IAM roles for production
- Encrypted storage for credentials

### Network Security
- VPC deployment for AWS
- Security groups for access control
- HTTPS for all communications

## 📚 API Reference

### Nova Act Methods Used
- `start_session()`: Initialize automation session
- `navigate()`: Navigate to URL
- `wait_for_element()`: Wait for page elements
- `type_text()`: Enter text into form fields
- `click()`: Click buttons/links
- `upload_file()`: Upload files
- `take_screenshot()`: Capture screenshots
- `end_session()`: Clean up session

### Configuration Options
- `PORTAL_URL`: Target portal URL
- `PORTAL_USERNAME/PASSWORD`: Authentication credentials
- `DATA_FILE`: JSON data file path
- `UPLOAD_FILE`: File to upload
- `TIMEOUT`: Operation timeout in seconds
- `HEADLESS`: Run without GUI (true/false)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs
3. Open an issue on GitHub
4. Contact the development team

## 🎉 Acknowledgments

- Amazon Nova Act team for the automation framework
- Flask community for the web framework
- Bootstrap for the UI components
- Docker for containerization

---

**Note**: This is a demonstration POC. For production use, additional security measures, error handling, and monitoring should be implemented. 