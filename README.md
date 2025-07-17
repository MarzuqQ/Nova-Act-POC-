# Nova Act POC - Advanced Shipping Portal Automation

This is a comprehensive proof-of-concept (POC) demonstrating how **Amazon Nova Act** can automate complex web form interactions for shipping companies. The solution uses the **official Nova Act SDK** with **advanced preview features** to automate complete workflows including login, intelligent form processing, file uploads, and structured data extraction.

## 🎯 Project Overview

### Business Problem
Shipping companies need to manually:
- Log into various vendor portals
- Upload shipment documents in different formats
- Fill out complex web forms with delivery data
- Handle multiple JSON formats and data structures
- Submit forms manually and capture confirmations

This process is time-consuming, error-prone, and not scalable across different data formats.

### Solution Architecture
Using **Amazon Nova Act** with **intelligent automation**:
1. **Automated Login**: Natural language instructions for secure portal access
2. **Dual Automation Modes**: Manual form filling OR intelligent auto-fill via JSON upload
3. **Intelligent JSON Processing**: Handles 90+ field name variations across different formats
4. **Advanced File Handling**: Supports multiple file types with validation and size limits
5. **Structured Data Extraction**: AI-powered confirmation capture with Pydantic schemas
6. **Preview Performance**: Enhanced speed with Nova Act's playwright actuation preview

## 🏗️ Architecture

```
[JSON Data] → [Intelligent Parser] → [Nova Act Automation] → [Demo Vendor Portal]
     ↓              ↓                        ↓                       ↓
[90+ Field     [Nested Structure        [Dual Mode           [JavaScript
 Mappings]      Flattening]             Processing]           Auto-Fill]
     ↓              ↓                        ↓                       ↓
[Normalized] → [Standardized] → [Form Fields] → [Structured] → [Confirmation]
   Data          Data            Population     Submission      Capture
```

## 🧠 Intelligent JSON Processing

The POC includes a sophisticated **JsonParser** that handles diverse data formats:

### Field Mapping Intelligence
- **90+ field name variations** across 9 standard fields
- **Three-tier matching**: Exact → Case-insensitive → Partial matching
- **Nested structure support**: Handles `shipment.sender.name` format
- **Data normalization**: Weight extraction, date formatting, address cleanup

### Supported Field Variations
```python
# Example field mappings (shipper_name):
'shipper_name', 'shipper', 'sender_name', 'sender', 'from_name', 'from',
'origin_name', 'origin_company', 'shipping_company', 'company_name'

# Handles nested structures like:
{
  "shipment": {
    "sender": {"name": "Company Name"}
  }
}
```

## 📁 Project Structure

```
Nova-Act-POC-/
├── README.md                    # This documentation
├── .gitignore                   # Git ignore patterns
├── .gitattributes               # Git attributes
├── docker/                      # Docker configuration
│   ├── docker-compose.yml       # Multi-service orchestration
│   ├── docker.env.template      # Environment template
│   └── DOCKER.md                # Docker documentation
├── src/                         # Source code
│   ├── automation/              # Nova Act automation
│   │   ├── Dockerfile           # Automation container
│   │   ├── main.py              # Primary automation orchestrator (401 lines)
│   │   ├── json_parser.py       # Intelligent JSON parsing (318 lines)
│   │   ├── file_utils.py        # Advanced file handling (246 lines)
│   │   ├── requirements.txt     # Python dependencies
│   │   └── wait-for-it.sh       # Service dependency script
│   └── portal/                  # Demo vendor portal
│       ├── Dockerfile           # Portal container
│       ├── app.py               # Flask application with authentication
│       ├── templates/           # Responsive HTML templates
│       │   ├── base.html        # Base template with modern UI
│       │   ├── login.html       # Login page
│       │   ├── dashboard.html   # Dashboard
│       │   ├── shipment_form.html # Advanced form with auto-fill JavaScript
│       │   └── submission_success.html # Success confirmation page
│       └── requirements.txt     # Flask dependencies
├── data/                        # All data files
│   ├── samples/                 # Sample JSON files in different formats
│   │   ├── shipment_data.json   # Standard format
│   │   ├── nested_shipment_data.json # Nested structure format
│   │   └── alternative_format.json # Alternative field names format
│   ├── uploads/                 # File uploads (shared between services)
│   ├── submissions/             # Form submissions (shared between services)
│   └── results/                 # Automation results (shared between services)
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker and Docker Compose
- Nova Act API Key

**Setup:**
```bash
# 1. Clone repository
git clone <your-repo-url>
cd Nova-Act-POC-

# 2. Configure environment
cp docker/docker.env.template .env
# Edit .env and add your Nova Act API key

# 3. Run everything with Docker
cd docker && docker-compose up --build

# 4. Access portal at http://localhost:5000
# Login: shipping_admin / secure_pass123
```

**📖 For detailed Docker instructions, see [DOCKER.md](DOCKER.md)**

### Option 2: Local Development

**Prerequisites:**
- Python 3.8+
- Nova Act API Key
- Basic familiarity with command line

**Setup:**
```bash
# 1. Get Nova Act API Key
# Visit nova.amazon.com → Act section → Generate API key

# 2. Clone and Setup
git clone <your-repo-url>
cd Nova-Act-POC-

# 3. Install Dependencies
pip install -r src/automation/requirements.txt
pip install -r src/portal/requirements.txt

# 4. Configure API Key
export NOVA_ACT_API_KEY=your-api-key-here

# 5. Start Demo Portal
cd src/portal
python app.py

# 6. Run Automation (in another terminal)
cd src/automation
python main.py
```

**Access:**
- Portal: http://localhost:5000
- Login: `shipping_admin` / `secure_pass123`

## ⚙️ Advanced Automation Modes

This POC supports **dual automation modes** with intelligent processing:

### Mode 1: Manual Form Filling
```python
# In src/automation/main.py
'use_manual_filling': True  # Set to True for manual mode
```

**How it works:**
1. **JsonParser** intelligently parses JSON data (handles 90+ field variations)
2. **Nova Act** fills each form field individually using natural language
3. **Structured confirmation** capture with Pydantic schemas

**Best for:** Debugging, understanding workflow, complex validations

### Mode 2: Intelligent Auto-Fill (Default)
```python
# In src/automation/main.py
'use_manual_filling': False  # Set to False for auto-fill mode
```

**How it works:**
1. **File validation** with size limits and type checking
2. **Nova Act + Playwright** hybrid approach for file upload
3. **Frontend JavaScript** auto-fills all fields instantly
4. **Structured data extraction** for confirmation details

**Best for:** Production use, speed, handling large volumes

## 🔧 File Handling Capabilities

### Supported File Types & Limits
```python
SUPPORTED_TYPES = {
    '.json': 1024 * 1024,      # 1MB - Primary format
    '.pdf': 10 * 1024 * 1024,  # 10MB - Documents
    '.csv': 2 * 1024 * 1024,   # 2MB - Data files
    '.xml': 1024 * 1024,       # 1MB - Structured data
    '.txt': 1024 * 1024,       # 1MB - Text files
}
```

### File Processing Features
- **Validation**: Type checking, size limits, permissions
- **Preparation**: Timestamp generation, secure uploads
- **Cleanup**: Automatic temporary file management
- **Information**: MIME type detection, metadata extraction

## 📊 JSON Format Support

The POC handles **multiple JSON formats** intelligently:

### Standard Format (`data/samples/shipment_data.json`)
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

### Nested Format (`data/samples/nested_shipment_data.json`)
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
    "schedule": {
      "pickup_date": "2024-02-01",
      "notes": "Priority delivery"
    }
  }
}
```

### Alternative Format (`data/samples/alternative_format.json`)
```json
{
  "from_name": "Express Logistics LLC",
  "from_addr": "2468 Warehouse Blvd; Atlanta, GA 30309",
  "to_name": "Retail Distribution Hub",
  "to_addr": "1357 Commerce Center; Miami, FL 33101",
  "gross_weight": 33.2,
  "lwh": "20x15x10",
  "awb_number": "EL2024030001",
  "dispatch_date": "03/15/2024",
  "remarks": "Fragile items - this side up only"
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NOVA_ACT_API_KEY` | Your Nova Act API key | **Required** |
| `PORTAL_URL` | Demo portal URL | `http://localhost:5000` |
| `PORTAL_USERNAME` | Portal login username | `shipping_admin` |
| `PORTAL_PASSWORD` | Portal login password | `secure_pass123` |
| `DATA_FILE` | Path to JSON data file | `sample_data/shipment_data.json` |
| `UPLOAD_FILE` | Path to file to upload | `sample_data/shipment_data.json` |
| `HEADLESS` | Run browser in headless mode | `true` |
| `TIMEOUT` | Operation timeout in seconds | `300` |

### Nova Act Preview Features

The POC includes **Nova Act's latest preview features** for enhanced performance:

```python
# Enhanced speed with playwright actuation
with NovaAct(
    starting_page=self.config['portal_url'],
    headless=self.config['headless'],
    nova_act_api_key=self.config['nova_act_api_key'],
    ignore_https_errors=True,
    preview={"playwright_actuation": True}  # 🚀 Enhanced performance
) as nova:
```

## 🎯 Advanced Features

### 1. Intelligent Data Processing
- **90+ field mappings** across different naming conventions
- **Nested structure flattening** for complex JSON formats
- **Data normalization** for weights, dates, and addresses
- **Validation reporting** with detailed feedback

### 2. Robust Error Handling
- **Retry logic** for navigation failures
- **Fallback mechanisms** for form verification
- **Comprehensive logging** with structured output
- **Graceful degradation** for missing data

### 3. Structured Data Extraction
```python
# Extract confirmation with schema validation
result = nova.act(
    "Extract confirmation number, submission time, and status",
    schema=ConfirmationData.model_json_schema()
)
```

### 4. Dual-Mode File Upload
- **Backend**: Nova Act + Playwright hybrid approach
- **Frontend**: JavaScript auto-fill for instant population
- **Validation**: Size limits, type checking, security

### 5. Comprehensive Results Management
- **Timestamped outputs** for all automation runs
- **Structured JSON** results with metadata
- **Local storage** with optional S3 integration
- **Detailed logging** for debugging and monitoring

## 🔍 Testing

### Testing the Application
```bash
# Test with different JSON formats
cd nova_act_automation
DATA_FILE=../sample_data/nested_shipment_data.json python main.py

# Test in headless mode
HEADLESS=true python main.py

# Test with manual filling mode
# Edit main.py: 'use_manual_filling': True
python main.py
```

## 📚 Documentation

### Key Classes

1. **NovaActAutomation** (`main.py`):
   - Main orchestrator with workflow management
   - Dual-mode processing logic
   - Configuration management

2. **JsonParser** (`json_parser.py`):
   - Intelligent JSON parsing with 90+ field mappings
   - Nested structure handling
   - Data normalization and validation

3. **FileUtils** (`file_utils.py`):
   - File validation and processing
   - Upload preparation and cleanup
   - Sample file discovery

### Workflow Steps

1. **Configuration Loading**: Environment variables and defaults
2. **Data Parsing**: Intelligent JSON processing with validation
3. **Nova Act Initialization**: With preview features enabled
4. **Portal Login**: Automated authentication
5. **Form Navigation**: Intelligent navigation with retry logic
6. **Form Processing**: Dual-mode filling (manual vs auto-fill)
7. **Form Submission**: Automated submission with verification
8. **Confirmation Capture**: Structured data extraction
9. **Results Storage**: Timestamped JSON output

## 🚀 Performance Optimizations

### Nova Act Preview Features
- **Playwright actuation**: Enhanced browser interaction speed
- **Structured responses**: Faster data extraction with schemas
- **Headless mode**: Improved performance for production use

### Intelligent Processing
- **Field mapping cache**: Optimized JSON parsing
- **Batch operations**: Efficient form field population
- **Async capabilities**: Ready for parallel processing

## 🔒 Security Considerations

### File Upload Security
- **File type validation**: Whitelist of allowed extensions
- **Size limits**: Prevent DoS attacks
- **Secure filename handling**: Prevents directory traversal
- **Permission checks**: Validates file access rights

### Data Protection
- **Credential management**: Environment variable configuration
- **Session handling**: Secure Flask session management
- **Input validation**: Comprehensive form validation
- **Error sanitization**: Prevents information leakage

## 📈 Production Considerations

### Scalability
- **Parallel processing**: Multiple automation instances
- **Queue management**: Handle high-volume requests
- **Resource monitoring**: Track memory and CPU usage
- **Error recovery**: Robust retry mechanisms

### Monitoring
- **Structured logging**: JSON-formatted log outputs
- **Performance metrics**: Timing and success rates
- **Health checks**: API endpoint monitoring
- **Alert mechanisms**: Failure notification systems

## 🛠️ Development

### Code Quality
- **Type hints**: Comprehensive type annotations
- **Documentation**: Detailed docstrings and comments
- **Error handling**: Comprehensive exception management
- **Testing**: Unit tests and integration examples

### Architecture
- **Modular design**: Separate concerns and responsibilities
- **Configuration management**: Environment-based settings
- **Dependency injection**: Loose coupling between components
- **Extension points**: Easy customization and enhancement

## 🔧 Troubleshooting

### Common Issues

1. **Port 5000 in use**: Disable AirPlay Receiver in macOS System Settings
2. **Nova Act API key**: Ensure valid key is set in environment
3. **File upload failures**: Check file types and size limits
4. **Form auto-fill issues**: Verify JSON format matches expected structure
5. **Browser crashes**: Ensure sufficient system resources in headless mode

### Debug Mode
```bash
# Enable debug logging
export NOVA_ACT_DEBUG=true

# Run with verbose output
python main.py --verbose

# Test individual components
python -c "from json_parser import JsonParser; parser = JsonParser(); print(parser.parse_json_file('sample_data/shipment_data.json'))"
```
---

## 📄 License

This project is a proof-of-concept demonstration. Please review Amazon Nova Act terms of service for production use.

## 🤝 Contributing

This is a POC project. For production implementations, consider:
1. Enhanced error handling and logging
2. Comprehensive test coverage
3. Security auditing and penetration testing
4. Performance optimization and load testing
5. Documentation and user training materials 