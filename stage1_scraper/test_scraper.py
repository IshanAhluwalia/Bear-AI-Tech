import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from prompts import get_prompts
from data_processor import BrandMentionProcessor


class ChatGPTScraper:
    
    def __init__(self, headless=False, delay=3):
        
        self.headless = headless
        self.delay = delay
        self.driver = None  # Will hold our browser controller
        self.processor = BrandMentionProcessor()  # Our text analyzer
        
        print(f"Scraper created:")
        print(f" Headless mode: {headless}")
        print(f"  Delay between actions: {delay} seconds")
    
    def setup_browser(self):
        
        print("Setting up Chrome browser...")
        
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")  # Run invisibly
            print("Running in headless mode (invisible)")
        else:
            print("Running in visible mode")
        
        #  avoid crashes
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            print(" Trying auto-download ChromeDriver...")
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print(" Browser started with auto-downloaded driver!")
            return True
            
        except Exception as e:
            print(f" Auto-download failed: {e}")
            
            try:
                # try system Chrome
                print(" Trying system Chrome without explicit driver...")
                self.driver = webdriver.Chrome(options=chrome_options)
                print(" Browser started with system driver")
                return True
                
            except Exception as e2:
                print(f"  system Chrome also failed: {e2}")
                return False
    
    def test_basic_navigation(self):
       
        print("\n🧪 Testing basic browser navigation...")
        
        try:
            # Navigate to a simple website first
            print("   🌐 Navigating to Google...")
            self.driver.get("https://www.google.com")
            
            time.sleep(2)
            
            title = self.driver.title
            print(f"Page title: {title}")
            
            if "Google" in title:
                print("  Navigation test successful!")
                return True
            else:
                print("  Navigation test failed!")
                return False
                
        except Exception as e:
            print(f"  Navigation test error: {e}")
            return False
    
    def close_browser(self):
    
        if self.driver:
            print("\n🔒 Closing browser...")
            self.driver.quit()
            print("   ✅ Browser closed successfully!")
    
    def navigate_to_chatgpt(self):
        """Navigate to ChatGPT website"""
        print("\nNavigating to ChatGPT...")
        
        try:
            self.driver.get("https://chat.openai.com")
            time.sleep(3)  # Wait for page to load
            
            title = self.driver.title
            print(f"   Page title: {title}")
            
            if "ChatGPT" in title or "OpenAI" in title:
                print("   Successfully reached ChatGPT!")
                return True
            else:
                print("   Didn't reach ChatGPT page")
                return False
                
        except Exception as e:
            print(f"    Navigation error: {e}")
            return False
    
    def find_input_element(self):
        """Find the ChatGPT input text box"""
        print("\n🔍 Looking for ChatGPT input box...")
        
        # Common selectors for ChatGPT input - we'll try multiple approaches
        selectors = [
            "textarea[placeholder*='Message']",  # Most common
            "textarea[data-id='root']",
            "textarea",  # Fallback to any textarea
            "div[contenteditable='true']",  # Sometimes it's a div
        ]
        
        for selector in selectors:
            try:
                print(f"   Trying selector: {selector}")
                
                # Wait up to 10 seconds for element to appear
                wait = WebDriverWait(self.driver, 10)
                element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                
                print(f"   ✅ Found input element with: {selector}")
                return element
                
            except Exception as e:
                print(f"   ❌ Selector failed: {e}")
                continue
        
        print("   ❌ Could not find input element")
        return None
    
    def check_for_verification_challenge(self):
        """Check if there's a verification challenge blocking interaction"""
        print("\n🛡️ Checking for verification challenges...")
        
        # Common verification indicators
        verification_indicators = [
            "Are you human",
            "Verify you are human", 
            "Security check",
            "Please verify",
            "captcha",
            "CAPTCHA",
            "I'm not a robot",
            "Cloudflare",
            "Just a moment",
            "Checking your browser"
        ]
        
        try:
            # Get page text
            page_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            
            # Check for verification text
            for indicator in verification_indicators:
                if indicator.lower() in page_text:
                    print(f"   🚨 Detected verification challenge: '{indicator}'")
                    return True
            
            # Check for common verification elements
            verification_selectors = [
                "iframe[src*='captcha']",
                "div[class*='captcha']",
                "div[class*='challenge']",
                "div[class*='verification']",
                "form[action*='captcha']"
            ]
            
            for selector in verification_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"   🚨 Detected verification element: {selector}")
                        return True
                except:
                    continue
            
            print("   ✅ No verification challenges detected")
            return False
            
        except Exception as e:
            print(f"   ⚠️ Error checking for verification: {e}")
            return False
    
    def handle_manual_intervention(self, context="general issue"):
        """Pause for manual intervention"""
        print(f"\n⏸️ MANUAL INTERVENTION REQUIRED")
        print("=" * 50)
        print(f"Context: {context}")
        print()
        print("Please do the following in the browser window:")
        print("1. 🔍 Look for any verification challenges (CAPTCHA, 'Are you human?', etc.)")
        print("2. ✅ Complete any verification if present")
        print("3. 🔄 Make sure you're on the main ChatGPT chat page")
        print("4. 👤 Ensure you're logged in properly")
        print("5. ⌨️ Test that you can click in the input box manually")
        print()
        print("When everything looks ready:")
        print("➡️ Press Enter here to continue scraping...")
        print("➡️ Type 'skip' to skip this prompt and try the next one")
        print("➡️ Type 'quit' to stop scraping entirely")
        
        while True:
            user_choice = input("\nYour choice (Enter/skip/quit): ").strip().lower()
            
            if user_choice == "":
                print("✅ Continuing with scraping...")
                return "continue"
            elif user_choice == "skip":
                print("⏭️ Skipping this prompt...")
                return "skip"
            elif user_choice == "quit":
                print("🛑 Stopping scraping...")
                return "quit"
            else:
                print("❌ Invalid choice. Please press Enter, type 'skip', or type 'quit'")
    
    def submit_prompt_with_intervention(self, prompt_text):
        """Submit a prompt with manual intervention capabilities"""
        print(f"\n📝 Submitting prompt: '{prompt_text[:50]}...'")
        
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            print(f"\n🔄 Attempt {attempt}/{max_attempts}")
            
            # Check for verification challenges first
            if self.check_for_verification_challenge():
                action = self.handle_manual_intervention("Verification challenge detected")
                if action == "skip":
                    return "skip"
                elif action == "quit":
                    return "quit"
                # If continue, try again
                
            try:
                # Find the input element
                input_element = self.find_input_element()
                if not input_element:
                    print("   ❌ Could not find input element")
                    if attempt == max_attempts:
                        action = self.handle_manual_intervention("Cannot find input element")
                        if action != "continue":
                            return action
                    continue
                
                # Check if element is interactable
                if not input_element.is_enabled() or not input_element.is_displayed():
                    print("   ⚠️ Input element found but not interactable")
                    action = self.handle_manual_intervention("Input element not interactable")
                    if action != "continue":
                        return action
                    continue
                
                # Clear and type the prompt
                try:
                    input_element.clear()
                    time.sleep(1)
                    
                    # Type more naturally with random delays
                    for char in prompt_text:
                        input_element.send_keys(char)
                        time.sleep(0.03 + (0.05 * __import__('random').random()))  # 30-80ms per char
                    
                    time.sleep(1)
                    
                    # Submit the prompt
                    success = False
                    try:
                        # Method 1: Look for submit button
                        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='send-button']")
                        submit_button.click()
                        print("   ✅ Clicked submit button")
                        success = True
                    except:
                        try:
                            # Method 2: Press Enter
                            input_element.send_keys("\n")
                            print("   ✅ Pressed Enter to submit")
                            success = True
                        except:
                            print("   ❌ Could not submit prompt")
                    
                    if success:
                        print("   ⏳ Waiting for ChatGPT response...")
                        time.sleep(3)  # Wait for response to start
                        return "success"
                    else:
                        if attempt == max_attempts:
                            action = self.handle_manual_intervention("Cannot submit prompt")
                            if action != "continue":
                                return action
                        
                except Exception as e:
                    print(f"   ❌ Error typing/submitting: {e}")
                    if "element not interactable" in str(e).lower():
                        action = self.handle_manual_intervention("Element interaction blocked")
                        if action != "continue":
                            return action
                    elif attempt == max_attempts:
                        action = self.handle_manual_intervention(f"Typing error: {e}")
                        if action != "continue":
                            return action
                
            except Exception as e:
                print(f"   ❌ Unexpected error: {e}")
                if attempt == max_attempts:
                    action = self.handle_manual_intervention(f"Unexpected error: {e}")
                    if action != "continue":
                        return action
            
            if attempt < max_attempts:
                print(f"   🔄 Waiting 3 seconds before retry...")
                time.sleep(3)
        
        return "failed"
    
    def extract_response(self):
        """Extract ChatGPT's response from the page"""
        print("\n📖 Extracting ChatGPT response...")
        
        try:
            # Wait for response to appear and finish
            time.sleep(10)  # Wait for response to complete
            
            # Common selectors for ChatGPT responses
            response_selectors = [
                "div[data-message-author-role='assistant']",
                ".markdown",
                "div.min-h-\\[20px\\]",  # Common ChatGPT response container
                "div[data-testid*='conversation']",
            ]
            
            for selector in response_selectors:
                try:
                    print(f"   Trying response selector: {selector}")
                    
                    # Find all response elements
                    response_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if response_elements:
                        # Get the last response (most recent)
                        last_response = response_elements[-1]
                        response_text = last_response.text.strip()
                        
                        if response_text and len(response_text) > 10:  # Make sure it's not empty
                            print(f"   ✅ Found response ({len(response_text)} characters)")
                            print(f"   Preview: {response_text[:100]}...")
                            return response_text
                    
                except Exception as e:
                    print(f"   ❌ Selector failed: {e}")
                    continue
            
            # Fallback: try to get any text from the page
            print("   🔄 Trying fallback: searching page text...")
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            # Look for response patterns
            lines = page_text.split('\n')
            for i, line in enumerate(lines):
                if len(line) > 50 and any(word in line.lower() for word in ['recommend', 'suggest', 'best', 'good', 'great']):
                    # Found a potential response line, get a few lines around it
                    response_lines = lines[max(0, i-2):i+5]
                    response_text = '\n'.join(response_lines).strip()
                    if len(response_text) > 50:
                        print(f"   ✅ Found response via fallback ({len(response_text)} characters)")
                        return response_text
            
            print("   ❌ Could not extract response")
            return None
            
        except Exception as e:
            print(f"   ❌ Error extracting response: {e}")
            return None
    
    def run_full_scraping(self):
        """Run the complete scraping workflow"""
        print("\n🚀 STARTING FULL CHATGPT SCRAPING")
        print("=" * 50)
        
        # Get our prompts
        prompts = get_prompts()
        print(f"📋 Loaded {len(prompts)} prompts to process")
        
        # Setup browser
        if not self.setup_browser():
            print("❌ Browser setup failed!")
            return False
        
        # Navigate to ChatGPT
        if not self.navigate_to_chatgpt():
            print("❌ Could not reach ChatGPT!")
            return False
        
        print(f"\n⏸️  PAUSE: Please log in to ChatGPT manually!")
        print("   1. The browser window should be open")
        print("   2. Log in to your ChatGPT account")
        print("   3. Make sure you're on the chat page")
        print("   4. Press Enter here when ready...")
        input()  # Wait for user to log in
        
        successful_scrapes = 0
        
        # Process each prompt
        for i, prompt in enumerate(prompts, 1):
            print(f"\n📝 PROCESSING PROMPT {i}/{len(prompts)}")
            print("-" * 30)
            
            # Submit prompt
            result = self.submit_prompt_with_intervention(prompt)
            
            if result == "success":
                # Extract response
                response = self.extract_response()
                
                if response:
                    # Process with our data analyzer
                    processed_result = self.processor.process_response(prompt, response)
                    print(f"   📊 Brand mentions found: {processed_result['brand_counts']}")
                    successful_scrapes += 1
                else:
                    print("   ❌ Could not extract response")
                    action = self.handle_manual_intervention("Failed to extract ChatGPT response")
                    if action == "quit":
                        break
                    elif action == "skip":
                        continue
                    # If continue, we already logged the failure
                        
            elif result == "skip":
                print("   ⏭️ Skipping this prompt...")
                continue
                
            elif result == "quit":
                print("   🛑 User chose to quit scraping")
                break
                
            else:  # failed
                print("   ❌ Failed to submit prompt after all attempts")
                action = self.handle_manual_intervention("All submission attempts failed")
                if action == "quit":
                    break
                elif action == "skip":
                    continue
                # If continue, we move to next prompt
            
            # Wait between prompts (be respectful)
            if i < len(prompts):
                print(f"   ⏳ Waiting {self.delay} seconds before next prompt...")
                time.sleep(self.delay)
        
        # Generate final results
        print(f"\n🎉 SCRAPING COMPLETE!")
        print(f"   Successful scrapes: {successful_scrapes}/{len(prompts)}")
        
        if successful_scrapes > 0:
            # Print summary
            self.processor.print_detailed_summary()
            
            # Save results
            filename = f"chatgpt_scraping_results_{int(time.time())}.json"
            self.processor.save_to_json(filename)
            print(f"💾 Results saved to: {filename}")
        
        return successful_scrapes > 0


# 🧪 TEST FUNCTION - Let's see our scraper in action!
def test_scraper_basics():

    print("🧪 TESTING SCRAPER BASICS")
    print("=" * 40)
    
    # Create scraper (visible mode so you can watch!)
    scraper = ChatGPTScraper(headless=False, delay=2)
    
    try:
        # Test 1: Start browser
        if not scraper.setup_browser():
            print(" Browser setup failed")
            return False
        
        # Test 2: Navigate to a simple site
        if not scraper.test_basic_navigation():
            print(" Navigation test failed")
            return False
        
        # 🎉 Success!
        print("\n All basic tests passed!")
        print("You should see a Chrome window that opened Google!")
        
        print("⏳ Keeping browser open for 5 seconds so you can see it...")
        time.sleep(5)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
        
    finally:
        scraper.close_browser()


def test_chatgpt_navigation():
    """Test ChatGPT navigation and interface detection"""
    print("\n🧪 TESTING CHATGPT NAVIGATION")
    print("=" * 40)
    
    scraper = ChatGPTScraper(headless=False, delay=2)
    
    try:
        # Setup browser
        if not scraper.setup_browser():
            print("❌ Browser setup failed!")
            return False
        
        # Navigate to ChatGPT
        if not scraper.navigate_to_chatgpt():
            print("❌ Could not reach ChatGPT!")
            return False
        
        print("\n⏸️  MANUAL LOGIN REQUIRED:")
        print("   1. Please log in to ChatGPT in the browser window")
        print("   2. Make sure you're on the main chat page")
        print("   3. Press Enter here when ready...")
        input()
        
        # Test finding input element
        input_element = scraper.find_input_element()
        if input_element:
            print("✅ Successfully found ChatGPT input!")
            
            # Test typing something (but don't submit)
            test_text = "Hello ChatGPT!"
            input_element.clear()
            input_element.send_keys(test_text)
            print(f"✅ Successfully typed test text: '{test_text}'")
            
            print("\n⏸️  You should see the test text in ChatGPT input box.")
            print("   Press Enter to clear it and continue...")
            input()
            
            input_element.clear()
            print("✅ Cleared test text")
            
        else:
            print("❌ Could not find ChatGPT input element")
            return False
        
        print("\n✅ ChatGPT navigation test passed!")
        print("⏳ Keeping browser open for 10 seconds...")
        time.sleep(10)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
        
    finally:
        scraper.close_browser()


def test_manual_intervention():
    """Test the manual intervention and verification detection"""
    print("\n🧪 TESTING MANUAL INTERVENTION FEATURES")
    print("=" * 40)
    
    scraper = ChatGPTScraper(headless=False, delay=2)
    
    try:
        # Setup browser
        if not scraper.setup_browser():
            print("❌ Browser setup failed!")
            return False
        
        # Navigate to ChatGPT
        if not scraper.navigate_to_chatgpt():
            print("❌ Could not reach ChatGPT!")
            return False
        
        print("\n⏸️ INITIAL LOGIN/SETUP:")
        print("   1. Please log in to ChatGPT in the browser window")
        print("   2. Make sure you're on the main chat page")
        print("   3. Press Enter here when ready...")
        input()
        
        # Test verification detection
        has_verification = scraper.check_for_verification_challenge()
        if has_verification:
            print("✅ Verification detection is working!")
        else:
            print("✅ No verification detected - page looks clean")
        
        # Test manual intervention flow
        print("\n🧪 Testing manual intervention flow...")
        action = scraper.handle_manual_intervention("Testing the intervention system")
        print(f"✅ Manual intervention returned: {action}")
        
        # Test single prompt submission
        print("\n🧪 Testing single prompt submission...")
        test_prompt = "Hello ChatGPT! Please just say 'Hello back' and mention Nike once."
        result = scraper.submit_prompt_with_intervention(test_prompt)
        print(f"✅ Prompt submission returned: {result}")
        
        if result == "success":
            response = scraper.extract_response()
            if response:
                print(f"✅ Response extracted: {response[:100]}...")
                
                # Test our data processor
                processed = scraper.processor.process_response(test_prompt, response)
                print(f"✅ Brand analysis: {processed['brand_counts']}")
            else:
                print("❌ Could not extract response")
        
        print("\n✅ Manual intervention test complete!")
        print("⏳ Keeping browser open for 10 seconds...")
        time.sleep(10)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
        
    finally:
        scraper.close_browser()


def main():
    """Main function - gives user options"""
    print("🤖 CHATGPT SCRAPER")
    print("=" * 30)
    print("Choose an option:")
    print("1. Test basic browser functionality")
    print("2. Test ChatGPT navigation and interface")
    print("3. Test manual intervention features")
    print("4. Run full ChatGPT scraping (all 10 prompts)")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        test_scraper_basics()
    elif choice == "2":
        test_chatgpt_navigation()
    elif choice == "3":
        test_manual_intervention()
    elif choice == "4":
        print("\n🚀 Starting full scraping...")
        scraper = ChatGPTScraper(headless=False, delay=5)  # Longer delay for full scraping
        try:
            scraper.run_full_scraping()
        finally:
            scraper.close_browser()
    elif choice == "5":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Please run the script again.")


if __name__ == "__main__":
    main() 