#!/usr/bin/env python3
"""
🧪 BEAR AI TAKE-HOME: SETUP VERIFICATION SCRIPT
===============================================

This script verifies that your environment is properly set up
to run the Bear AI take-home project.

Run this after following the README setup instructions.
"""

import sys
import subprocess
import importlib
import platform
from pathlib import Path

def print_header(title):
    print(f"\n{'=' * 50}")
    print(f"🔍 {title}")
    print('=' * 50)

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def check_python_version():
    print_header("PYTHON VERSION CHECK")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"Python version: {version_str}")
    print(f"Platform: {platform.system()} {platform.machine()}")
    
    if version.major >= 3 and version.minor >= 8:
        print_success("Python version is compatible (3.8+)")
        return True
    else:
        print_error("Python version too old. Need 3.8+")
        return False

def check_required_modules():
    print_header("REQUIRED MODULES CHECK")
    
    required_modules = [
        ('selenium', 'Web scraping'),
        ('fastapi', 'API framework'),
        ('uvicorn', 'API server'),
        ('sqlalchemy', 'Database ORM'),
        ('psycopg2', 'PostgreSQL driver'),
        ('requests', 'HTTP requests'),
        ('json', 'JSON processing (built-in)'),
        ('re', 'Regular expressions (built-in)'),
    ]
    
    all_good = True
    
    for module_name, description in required_modules:
        try:
            importlib.import_module(module_name)
            print_success(f"{module_name:<15} - {description}")
        except ImportError:
            print_error(f"{module_name:<15} - MISSING ({description})")
            all_good = False
    
    return all_good

def check_project_structure():
    print_header("PROJECT STRUCTURE CHECK")
    
    required_files = [
        'stage1_scraper/GPT_scraper.py',
        'stage1_scraper/prompts.py',
        'stage1_scraper/data_processor.py',
        'stage2_api/main.py',
        'stage2_api/database.py',
        'stage2_api/data_loader.py',
        'requirements.txt',
        'README.md'
    ]
    
    all_good = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print_success(f"{file_path}")
        else:
            print_error(f"{file_path} - MISSING")
            all_good = False
    
    return all_good

def check_chrome_browser():
    print_header("CHROME BROWSER CHECK")
    
    chrome_paths = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',     # Windows
        'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',  # Windows 32-bit
        '/usr/bin/google-chrome',  # Linux
        '/usr/bin/chromium-browser',  # Linux alternative
    ]
    
    chrome_found = False
    for chrome_path in chrome_paths:
        if Path(chrome_path).exists():
            print_success(f"Chrome found at: {chrome_path}")
            chrome_found = True
            break
    
    if not chrome_found:
        # Try to run chrome command
        try:
            result = subprocess.run(['google-chrome', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print_success(f"Chrome found via command: {result.stdout.strip()}")
                chrome_found = True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        try:
            result = subprocess.run(['chrome', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print_success(f"Chrome found via command: {result.stdout.strip()}")
                chrome_found = True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
    
    if not chrome_found:
        print_error("Chrome browser not found")
        print("Please install Google Chrome from: https://chrome.google.com")
    
    return chrome_found

def check_database_availability():
    print_header("DATABASE AVAILABILITY CHECK")
    
    # Check PostgreSQL
    postgres_available = False
    try:
        result = subprocess.run(['pg_config', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print_success(f"PostgreSQL found: {result.stdout.strip()}")
            postgres_available = True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print_warning("PostgreSQL not found in PATH")
    
    # Check MySQL
    mysql_available = False
    try:
        result = subprocess.run(['mysql', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print_success(f"MySQL found: {result.stdout.strip()}")
            mysql_available = True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print_warning("MySQL not found in PATH")
    
    if not postgres_available and not mysql_available:
        print_error("No database system found")
        print("Please install PostgreSQL or MySQL")
        return False
    
    return True

def check_virtual_environment():
    print_header("VIRTUAL ENVIRONMENT CHECK")
    
    # Check if we're in a virtual environment
    in_venv = (hasattr(sys, 'real_prefix') or 
               (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))
    
    if in_venv:
        print_success("Running in virtual environment")
        print(f"Virtual env path: {sys.prefix}")
        
        # Test if selenium is actually available (critical check)
        try:
            import selenium
            print_success("selenium module accessible in virtual environment")
        except ImportError:
            print_error("selenium module NOT accessible - virtual environment issue!")
            print("🔧 Fix: Run 'source venv/bin/activate' then 'pip install -r requirements.txt'")
            return False
            
        # Test if fastapi is accessible
        try:
            import fastapi
            print_success("fastapi module accessible in virtual environment")
        except ImportError:
            print_error("fastapi module NOT accessible - virtual environment issue!")
            print("🔧 Fix: Run 'source venv/bin/activate' then 'pip install -r requirements.txt'")
            return False
    else:
        print_error("NOT running in virtual environment")
        print("🔧 CRITICAL: You must activate the virtual environment!")
        print("   Run: source venv/bin/activate")
        print("   Then: python setup_test.py")
        return False
    
    return True

def test_basic_functionality():
    print_header("BASIC FUNCTIONALITY TEST")
    
    try:
        # Test data processor
        sys.path.append('stage1_scraper')
        from data_processor import BrandMentionProcessor
        
        processor = BrandMentionProcessor()
        test_text = "Nike and Adidas are great brands"
        result = processor.count_brand_mentions(test_text)
        
        if result.get('Nike', 0) > 0 and result.get('Adidas', 0) > 0:
            print_success("Data processor working correctly")
        else:
            print_error("Data processor not working properly")
            return False
            
    except Exception as e:
        print_error(f"Data processor test failed: {e}")
        return False
    
    try:
        # Test FastAPI import
        from fastapi import FastAPI
        app = FastAPI()
        print_success("FastAPI can be imported and initialized")
    except Exception as e:
        print_error(f"FastAPI test failed: {e}")
        return False
    
    return True

def main():
    print("🎯 BEAR AI TAKE-HOME: SETUP VERIFICATION")
    print("=========================================")
    print("This script will verify your environment setup.")
    print("Run this after following the README setup instructions.\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Modules", check_required_modules),
        ("Project Structure", check_project_structure),
        ("Chrome Browser", check_chrome_browser),
        ("Database Systems", check_database_availability),
        ("Virtual Environment", check_virtual_environment),
        ("Basic Functionality", test_basic_functionality),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print_error(f"{check_name} check failed with error: {e}")
            results.append((check_name, False))
    
    # Summary
    print_header("SETUP VERIFICATION SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:<25} {status}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print_success("🎉 Your environment is ready for the Bear AI take-home!")
        print("\n📋 IMPORTANT: Always run commands with virtual environment activated!")
        print("\n✅ Correct way to run Stage 1:")
        print("   cd \"/Users/ishanahluwalia/Bear AI Take-Home\"")
        print("   source venv/bin/activate")
        print("   cd stage1_scraper")
        print("   python GPT_scraper.py")
        print("\n✅ Correct way to run Stage 2:")
        print("   cd \"/Users/ishanahluwalia/Bear AI Take-Home\"") 
        print("   source venv/bin/activate")
        print("   cd stage2_api")
        print("   python data_loader.py && python main.py")
        print("\n❌ WRONG (will fail): cd stage1_scraper && python GPT_scraper.py")
        print("   (Missing: source venv/bin/activate)")
    else:
        print_error("❌ Some issues found. Please fix them before proceeding.")
        print("\n🔧 Most common issue: Virtual environment not activated")
        print("   Always run: source venv/bin/activate FIRST")
        print("\nRefer to the README.md for detailed setup instructions.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 