# Bear AI Technical Take-Home Assignment

### Step 1: Clone the Repository
```bash
# Clone the repository to your desired location
git clone https://github.com/IshanAhluwalia/Bear-AI-Tech.git

# Navigate into the project directory
cd Bear-AI-Tech
```

### Step 2: System Prerequisites

**macOS Quick Install (Recommended):**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install everything at once
brew install python3 postgresql@15 git

# Start PostgreSQL (will auto-start on future reboots)
brew services start postgresql@15
```

**Manual Installation:**
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

4. **Git** (if not already installed)
   - macOS: `xcode-select --install` or `brew install git`
   - Windows: Download from git-scm.com
   - Linux: `sudo apt install git`

### Step 3: Project Environment Setup

**Run these commands from inside the Bear-AI-Tech directory!**

```bash
# Make sure you're in the project directory
pwd  # Should show: /path/to/Bear-AI-Tech

# Create virtual environment
python3 -m venv venv

# Activate virtual environment (CRITICAL - don't skip!)
source venv/bin/activate  # macOS/Linux
# OR venv\Scripts\activate  # Windows

# You should see (venv) at the start of your terminal prompt

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify setup works
python setup_test.py
```

**✅ Setup is complete when the verification script shows all 7/7 checks passing.**

---

## 🕷️ Stage 1: Web Scraping (5-10 minutes)

**Prerequisites**: Complete setup above + active ChatGPT account

```bash
# IMPORTANT: Make sure virtual environment is activated!
# You should see (venv) in your terminal prompt

# Navigate to scraper directory
cd stage1_scraper

# Run the scraper
python GPT_scraper.py
```

**Interactive Process**:
1. Type `y` to start scraping
2. Chrome browser opens automatically
3. **Manual step**: Log into ChatGPT in the browser window
4. Return to terminal, press Enter when ready
5. **Automatic**: Scraper processes all 10 prompts (~5-10 minutes)

**Output**: `brand_mentions_results_[timestamp].json` with complete analysis

**Common Issues & Fixes:**
- **Virtual env not activated**: Run `source ../venv/bin/activate` from stage1_scraper directory
- **Chrome not opening**: Ensure Chrome is installed (not Chromium)
- **ChatGPT issues**: Make sure you're logged in and have a working account

---

## 🌐 Stage 2: REST API (1 minute)

**Prerequisites**: Stage 1 completed (JSON file exists)

```bash
# From stage1_scraper directory, go back to project root and enter stage2_api
cd ../stage2_api

# Make sure virtual environment is still activated
# You should see (venv) in your terminal prompt
# If not, run: source ../venv/bin/activate

# Load data and start server
python data_loader.py
python main.py
```

**API Ready**: `http://localhost:8000`

### Test the API
```bash
# Open a new terminal and test endpoints
curl http://localhost:8000/mentions
curl http://localhost:8000/mentions/Nike
curl http://localhost:8000/health

# Interactive documentation
open http://localhost:8000/docs  # macOS
# OR visit http://localhost:8000/docs in your browser
```

---

## 🧪 Complete Test Run (Copy-Paste Ready)

**Start Fresh (One-Time Setup):**
```bash
# 1. Clone and navigate
git clone https://github.com/IshanAhluwalia/Bear-AI-Tech.git
cd Bear-AI-Tech

# 2. Install system dependencies (macOS)
brew install python3 postgresql@15 git
brew services start postgresql@15

# 3. Setup project environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python setup_test.py  # Should show 7/7 checks pass

# 4. Run Stage 1
cd stage1_scraper
python GPT_scraper.py  # Follow prompts, login to ChatGPT

# 5. Run Stage 2  
cd ../stage2_api
python data_loader.py
python main.py
```

**Subsequent Runs (After Setup):**
```bash
# Navigate to project and activate environment
cd Bear-AI-Tech
source venv/bin/activate

# Run Stage 1
cd stage1_scraper
python GPT_scraper.py

# Run Stage 2
cd ../stage2_api
python data_loader.py
python main.py
```

---

## 🔧 Troubleshooting & Common Errors

### Virtual Environment Issues
```bash
# Problem: (venv) not showing in terminal
# Solution: Activate the virtual environment
cd Bear-AI-Tech  # Go to project root
source venv/bin/activate

# Problem: "No module named 'selenium'" or similar
# Solution: Make sure venv is activated, then reinstall
source venv/bin/activate
pip install -r requirements.txt
```

### Directory Navigation Issues
```bash
# Problem: "No such file or directory: stage1_scraper"
# Solution: Make sure you're in the project root
pwd  # Should show: /path/to/Bear-AI-Tech
ls   # Should show: stage1_scraper, stage2_api, venv, etc.

# If not in project root:
cd /path/to/Bear-AI-Tech  # Replace with your actual path
```

### Database Issues
```bash
# Problem: PostgreSQL not running
# Solution: Start PostgreSQL
brew services start postgresql@15  # macOS
sudo systemctl start postgresql    # Linux
# Windows: Start via Services manager
```

### Chrome/Selenium Issues
```bash
# Problem: Chrome not found or not opening
# Solution: Install Chrome browser (not Chromium)
# Download from: https://www.google.com/chrome/

# Problem: WebDriver issues
# Solution: Update webdriver-manager
pip install --upgrade webdriver-manager
```

### Port Issues
```bash
# Problem: "Port 8000 already in use"
# Solution: Kill existing process
lsof -ti:8000 | xargs kill -9  # macOS/Linux
# OR change port in stage2_api/main.py
```

### Quick Reset Commands
```bash
# Reset everything and start fresh
cd Bear-AI-Tech
source venv/bin/activate
brew services restart postgresql@15
pip install --upgrade -r requirements.txt
python setup_test.py
```

---

## 📊 Expected Output

### Stage 1: Complete JSON File Example
The scraper creates `brand_mentions_results_[timestamp].json` with complete analysis:

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

### Stage 2: Complete API Response Examples

#### GET `/mentions` - All Brands Summary
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

#### GET `/health` - Health Check
```json
{
  "status": "healthy",
  "timestamp": "2025-06-23T19:31:49"
}
```

---

## 🏗️ Project Structure

```
Bear-AI-Tech/
├── README.md                 # This guide
├── requirements.txt          # Python dependencies
├── setup_test.py            # Environment verification
├── venv/                    # Virtual environment (created during setup)
├── stage1_scraper/
│   ├── GPT_scraper.py       # Main scraper script
│   ├── prompts.py           # 10 sportswear prompts
│   ├── data_processor.py    # Brand mention processing
│   └── *.json               # Results (created after running)
└── stage2_api/
    ├── main.py              # FastAPI application
    ├── database.py          # PostgreSQL models
    ├── data_loader.py       # Load scraped data
    └── models.py            # API response models
```

---

## ✅ Success Checklist

**Environment Setup:**
- [ ] Repository cloned: `git clone https://github.com/IshanAhluwalia/Bear-AI-Tech.git`
- [ ] In project directory: `cd Bear-AI-Tech`
- [ ] System dependencies installed (Python, Chrome, PostgreSQL)
- [ ] Virtual environment created: `python3 -m venv venv`
- [ ] Virtual environment activated: `source venv/bin/activate` (see `(venv)` in prompt)
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Setup verification passed: `python setup_test.py` shows 7/7 checks

**Stage 1 Execution:**
- [ ] In scraper directory: `cd stage1_scraper`
- [ ] Virtual environment still active (see `(venv)` in prompt)
- [ ] Scraper started: `python GPT_scraper.py`
- [ ] ChatGPT login completed in browser
- [ ] JSON results file created with timestamp

**Stage 2 Execution:**
- [ ] In API directory: `cd ../stage2_api`
- [ ] Virtual environment still active (see `(venv)` in prompt)
- [ ] Data loaded: `python data_loader.py`
- [ ] API started: `python main.py`
- [ ] API accessible: `curl http://localhost:8000/mentions`

**🎉 Project Complete!**

---


1. **Always check for `(venv)` in your terminal prompt** - if you don't see it, run `source venv/bin/activate`

2. **Use `pwd` to check your location** - you should be in the correct directory before running scripts

3. **Keep the virtual environment activated** - don't close the terminal between stages

4. **If something fails, run the setup verification**: `python setup_test.py`

5. **For a completely fresh start**, delete the `Bear-AI-Tech` folder and start from Step 1

---

Built with Python, FastAPI, Selenium, and SQLAlchemy | Made foolproof for seamless setup 🚀

