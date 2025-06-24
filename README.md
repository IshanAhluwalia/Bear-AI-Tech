# Bear AI Technical Take-Home Assignment

## Complete Setup (Do This First)

### System Prerequisites
1. **Python 3.8+** 
   - macOS: `brew install python3` or download from python.org
   - Windows: Download from python.org and add to PATH
   - Linux: `sudo apt install python3 python3-pip python3-venv`

2. **Google Chrome Browser**
   - Download from chrome.google.com
   - Must be installed (scraper uses system Chrome)

3. **PostgreSQL Database**
   - macOS: `brew install postgresql@15`
   - Windows: Download from postgresql.org
   - Linux: `sudo apt install postgresql postgresql-contrib`

4. **Git** (if cloning repository)
   - macOS: `xcode-select --install` or `brew install git`
   - Windows: Download from git-scm.com
   - Linux: `sudo apt install git`

### macOS Quick Setup
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install everything at once
brew install python3 postgresql@15 git

# Start PostgreSQL (will auto-start on future reboots)
brew services start postgresql@15
```

### Project Setup
```bash
# Navigate to project directory
cd "/path/to/Bear AI Take-Home"

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR venv\Scripts\activate  # Windows

# Install all dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Start PostgreSQL if not already running
brew services start postgresql@15  # macOS
# OR sudo systemctl start postgresql  # Linux
# OR start via Windows Services  # Windows

# Verify setup
python setup_test.py
```

**🧪 Setup Verification Script**  
The `setup_test.py` script automatically verifies:
- Python version compatibility
- All required modules installed
- Project structure complete
- Chrome browser available
- Database system running
- Virtual environment active
- Basic functionality working

 **Setup is complete when the verification script shows all checks passing.**

------

##  Stage 1: Web Scraping (5 minutes)

**Prerequisites**: Complete setup above, active ChatGPT account

```bash
# Navigate to scraper and run
cd stage1_scraper
python GPT_scraper.py
```

**Interactive Process**:
1. Type `y` to start scraping
2. Chrome browser opens automatically
3. **Manual step**: Log into ChatGPT in the browser window
4. Return to terminal, press Enter when ready
5. **Automatic**: Scraper processes all 10 prompts (~5-10 minutes)

**Output**: `brand_mentions_results_[timestamp].json` with complete analysis

---

## 🌐 Stage 2: REST API (1 minute)

**Prerequisites**: Stage 1 completed (JSON file exists)

```bash
# Navigate to API directory
cd ../stage2_api

# Load data and start server
python data_loader.py
python main.py
```

**API Ready**: `http://localhost:8000`

### Test the API
```bash
# Test endpoints
curl http://localhost:8000/mentions
curl http://localhost:8000/mentions/Nike
curl http://localhost:8000/health

# Interactive documentation
open http://localhost:8000/docs
```

---

## 🧪 Complete Test Run

```bash
# 1. One-time setup (if not done)
cd "/path/to/Bear AI Take-Home"
source venv/bin/activate
python setup_test.py  # Verify everything ready

# 2. Run Stage 1
cd stage1_scraper
python GPT_scraper.py  # Follow prompts

# 3. Run Stage 2  
cd ../stage2_api
python data_loader.py && python main.py

# 4. Test API
curl http://localhost:8000/mentions
```

---

## 📊 Expected Output

### Stage 1: `brand_mentions_results_[timestamp].json`
```json
{
  "analysis_timestamp": "2025-06-23T19:31:49.692708",
  "summary": {
    "total_responses_processed": 10,
    "overall_brand_totals": {
      "Nike": 58,
      "Adidas": 33,
      "Jordan": 8,
      "Hoka": 7,
      "New Balance": 4
    },
    "grand_total_mentions": 110
  },
  "comprehensive_analysis": {
    "brand_analysis": {
      "Nike": {
        "total_mentions": 58,
        "percentage": 52.73,
        "avg_per_response": 5.8,
        "max_in_single_response": 12,
        "responses_with_mentions": 10,
        "response_coverage": 100.0
      },
      "Adidas": {
        "total_mentions": 33,
        "percentage": 30.0,
        "avg_per_response": 3.3,
        "max_in_single_response": 8,
        "responses_with_mentions": 10,
        "response_coverage": 100.0
      },
      "Jordan": {
        "total_mentions": 8,
        "percentage": 7.27,
        "avg_per_response": 0.8,
        "max_in_single_response": 3,
        "responses_with_mentions": 5,
        "response_coverage": 50.0
      },
      "Hoka": {
        "total_mentions": 7,
        "percentage": 6.36,
        "avg_per_response": 0.7,
        "max_in_single_response": 2,
        "responses_with_mentions": 5,
        "response_coverage": 50.0
      },
      "New Balance": {
        "total_mentions": 4,
        "percentage": 3.64,
        "avg_per_response": 0.4,
        "max_in_single_response": 2,
        "responses_with_mentions": 3,
        "response_coverage": 30.0
      }
    },
    "key_insights": {
      "most_mentions_single_response": {
        "count": 17,
        "response_number": 2,
        "prompt": "Top performance sneakers for athletes"
      },
      "dominant_brand": {
        "name": "Nike",
        "mentions": 58,
        "percentage": 52.73
      },
      "second_place_brand": {
        "name": "Adidas",
        "mentions": 33,
        "percentage": 30.0
      },
      "response_consistency": {
        "consistency_percentage": 47.06,
        "min_mentions": 8,
        "max_mentions": 17,
        "range": 9
      }
    }
  },
  "individual_responses": [
    {
      "response_number": 1,
      "prompt": "What are the best running shoes in 2025?",
      "response": "Based on current innovations and athlete feedback, here are the top running shoes for 2025:\n\n**For Performance Racing:**\n- Nike Vaporfly Next% 3 - Revolutionary carbon plate technology\n- Adidas Adizero Adios Pro 3 - Lightweight with responsive foam\n- Hoka Cielo X1 - Maximum energy return for marathons\n\n**For Daily Training:**\n- Nike Air Zoom Pegasus 41 - Reliable workhorse for all runners\n- Adidas Ultraboost 23 - Superior comfort and energy return\n- New Balance Fresh Foam X 1080v13 - Plush cushioning for long runs\n\n**For Trail Running:**\n- Nike Terra Kiger 9 - Excellent grip and durability\n- Adidas Terrex Speed Ultra - Lightweight trail performance\n\nEach brand offers unique technologies, so the best choice depends on your running style, foot type, and specific needs.",
      "brand_mentions": {
        "Nike": 3,
        "Adidas": 3,
        "Hoka": 1,
        "New Balance": 1,
        "Jordan": 0
      },
      "total_mentions": 8,
      "timestamp": "2025-06-23T19:31:49.692708"
    }
  ]
}
```

### Stage 2: API Response Examples

#### GET `/mentions` - All Brands
```json
{
  "total_mentions": 110,
  "total_responses": 10,
  "analysis_date": "2025-06-23T19:31:49",
  "brands": [
    {
      "brand": "Nike",
      "total_mentions": 58,
      "total_responses": 10,
      "avg_mentions_per_response": 5.8,
      "max_mentions_single_response": 12,
      "percentage_of_total": 52.73,
      "last_updated": "2025-06-23T19:31:49"
    },
    {
      "brand": "Adidas",
      "total_mentions": 33,
      "total_responses": 10,
      "avg_mentions_per_response": 3.3,
      "max_mentions_single_response": 8,
      "percentage_of_total": 30.0,
      "last_updated": "2025-06-23T19:31:49"
    },
    {
      "brand": "Jordan",
      "total_mentions": 8,
      "total_responses": 10,
      "avg_mentions_per_response": 0.8,
      "max_mentions_single_response": 3,
      "percentage_of_total": 7.27,
      "last_updated": "2025-06-23T19:31:49"
    },
    {
      "brand": "Hoka",
      "total_mentions": 7,
      "total_responses": 10,
      "avg_mentions_per_response": 0.7,
      "max_mentions_single_response": 2,
      "percentage_of_total": 6.36,
      "last_updated": "2025-06-23T19:31:49"
    },
    {
      "brand": "New Balance",
      "total_mentions": 4,
      "total_responses": 10,
      "avg_mentions_per_response": 0.4,
      "max_mentions_single_response": 2,
      "percentage_of_total": 3.64,
      "last_updated": "2025-06-23T19:31:49"
    }
  ]
}
```

#### GET `/mentions/Nike` - Specific Brand
```json
{
  "brand": "Nike",
  "total_mentions": 58,
  "total_responses": 10,
  "avg_mentions_per_response": 5.8,
  "max_mentions_single_response": 12,
  "percentage_of_total": 52.73,
  "exists": true,
  "last_updated": "2025-06-23T19:31:49"
}
```

#### GET `/mentions/Nike/details` - Detailed Brand Analysis
```json
{
  "brand": "Nike",
  "total_mentions": 58,
  "detailed_analysis": {
    "response_breakdown": [
      {
        "response_number": 1,
        "prompt": "What are the best running shoes in 2025?",
        "mentions_in_response": 3,
        "timestamp": "2025-06-23T19:31:49"
      },
      {
        "response_number": 2,
        "prompt": "Top performance sneakers for athletes",
        "mentions_in_response": 12,
        "timestamp": "2025-06-23T19:31:49"
      }
    ],
    "statistics": {
      "avg_per_response": 5.8,
      "max_single_response": 12,
      "min_single_response": 2,
      "response_coverage": 100.0,
      "consistency_score": 0.73
    }
  }
}
```

#### GET `/mentions/InvalidBrand` - Error Response
```json
{
  "detail": "Brand 'InvalidBrand' not found. Available brands: Nike, Adidas, Hoka, New Balance, Jordan"
}
```

---

## 🏗️ Project Structure

```
Bear AI Take-Home/
├── stage1_scraper/           # Web scraping ChatGPT
│   ├── GPT_scraper.py       # Main scraper script
│   ├── prompts.py           # 10 sportswear prompts
│   ├── data_processor.py    # Brand mention processing
│   └── *.json               # Results
├── stage2_api/              # REST API
│   ├── main.py              # FastAPI application
│   ├── database.py          # PostgreSQL models
│   ├── data_loader.py       # Load scraped data
│   └── models.py            # API response models
├── venv/                    # Virtual environment
├── requirements.txt         # All dependencies
├── setup_test.py           # Setup verification
└── README.md               # This guide
```

---

## 🔧 Troubleshooting

### Setup Issues
- **Python not found**: Ensure Python 3.8+ installed and in PATH
- **Virtual environment**: Use `python3 -m venv venv` if `python` fails
- **PostgreSQL not starting**: Try `brew services restart postgresql@15`
- **Permission errors**: Use `sudo` on Linux/macOS or run as Administrator

### Stage 1 Issues  
- **Chrome not found**: Install Chrome browser (not Chromium)
- **ChatGPT login**: Manual login required in browser window
- **No responses**: Check internet connection and ChatGPT account

### Stage 2 Issues
- **Port 8000 busy**: Kill existing process or change port in `main.py`
- **Database connection**: Ensure PostgreSQL is running
- **Module errors**: Ensure virtual environment is activated

### Quick Fixes
```bash
# Restart everything
brew services restart postgresql@15
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Verify setup
python setup_test.py
```

---

## 📋 Quick Start Checklist

**✅ One-Time Setup (Do Once)**
- [ ] Install Python 3.8+, Chrome, PostgreSQL, Git
- [ ] Create virtual environment: `python3 -m venv venv`  
- [ ] Activate environment: `source venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Start PostgreSQL: `brew services start postgresql@15`
- [ ] Verify setup: `python setup_test.py` (all checks pass)

**✅ Stage 1 Execution**
- [ ] `cd stage1_scraper && python GPT_scraper.py`
- [ ] Log into ChatGPT when browser opens
- [ ] Wait for completion, verify JSON file created

**✅ Stage 2 Execution**  
- [ ] `cd ../stage2_api && python data_loader.py && python main.py`
- [ ] Test API: `curl http://localhost:8000/mentions`

**🎉 Project Complete!**

---

Built with Python, FastAPI, Selenium, and SQLAlchemy

