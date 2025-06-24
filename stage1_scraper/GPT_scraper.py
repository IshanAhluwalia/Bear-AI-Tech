import time
import random
import json
import subprocess
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Suppress verbose logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from prompts import get_prompts
from data_processor import BrandMentionProcessor


class GPTScrapper:
    """
    GPT Scraper - Automated brand mention extraction from ChatGPT responses
    """
    
    def __init__(self, delay=3):
        self.delay = delay
        self.driver = None
        self.processor = BrandMentionProcessor()
        
        print(f" CHATGPT SCRAPER")
        print(f" Quick delay: {delay} seconds")
        print(f" Uses existing browser session")
    
    def setup_chrome_debug_session(self):
        """Initialize Chrome with remote debugging for GPT scraping"""
        print("\n🚀 Setting up Chrome debug session for GPT scraping...")
        
        try:
            # Kill any existing Chrome processes
            subprocess.run(["pkill", "-f", "Chrome"], capture_output=True)
            time.sleep(1)  # Faster startup
            
            # Start Chrome with remote debugging and suppress logs
            debug_port = 9222
            chrome_cmd = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                f"--remote-debugging-port={debug_port}",
                "--user-data-dir=/tmp/chrome-debug",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-logging",
                "--disable-gpu-logging",
                "--silent",
                "--log-level=3",
                "--disable-extensions-logging",
                "https://chat.openai.com"
            ]
            
            print(f"   🚀 Starting Chrome with debug port {debug_port}...")
            subprocess.Popen(chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(3)  # Faster startup
            
            print("   Chrome started with debugging enabled")
            print("   Please log in to ChatGPT in the Chrome window that opened")
            print("   Take your time to complete login and reach chat page")
            input("   Press Enter when you're logged in and ready...")
            
            return debug_port
            
        except Exception as e:
            print(f"   ❌ Debug session failed: {e}")
            return None
    
    def connect_to_chatgpt_session(self, debug_port):
        """Connect Selenium to the existing ChatGPT browser session"""
        print("\n Connecting to existing Chrome session...")
        
        try:
            options = Options()
            options.add_experimental_option("debuggerAddress", f"localhost:{debug_port}")
            
            self.driver = webdriver.Chrome(options=options)
            
            print("   ✅ Connected to existing Chrome session!")
            print(f"  Current URL: {self.driver.current_url}")
            
            return True
            
        except Exception as e:
            print(f"  Connection failed: {e}")
            return False
    
    def locate_chatgpt_input_field(self):
        """Find and return the ChatGPT message input field"""
        print("\n🔍  Input detection...")
        
        # Shorter wait
        time.sleep(random.uniform(1, 2))
        
        input_selectors = [
            "textarea[placeholder*='Message']",
            "textarea[placeholder*='Send a message']", 
            "div[contenteditable='true']",
            "textarea",
            "#prompt-textarea"
        ]
        
        for selector in input_selectors:
            try:
                print(f"   Trying: {selector}")
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        print(f"   ✅ Found: {selector}")
                        return element
                        
            except Exception as e:
                print(f"   ⚠️ Error with {selector}: {e}")
        
        print("   ❌ No input found")
        return None
    
    def type_prompt_to_chatgpt(self, element, prompt_text):
        """Type the brand mention prompt into ChatGPT input field"""
        print(f"typing prompt")
        
        # Quick focus
        element.click()
        time.sleep(random.uniform(0.3, 0.5))
        
        # Clear existing content
        element.send_keys(Keys.CONTROL + "a")
        time.sleep(0.2)
        element.send_keys(Keys.DELETE)
        time.sleep(0.3)
        
        # Type at reasonable human speed
        for i, char in enumerate(prompt_text):
            element.send_keys(char)
            
            # Faster character delays
            if char == ' ':
                delay = random.uniform(0.05, 0.15)
            elif char in '.,!?':
                delay = random.uniform(0.1, 0.2)
            else:
                delay = random.uniform(0.02, 0.08)
            
            time.sleep(delay)
            
            # Rare thinking pauses - much shorter
            if random.random() < 0.03 and i > 20:
                think_time = random.uniform(0.5, 1.5)
                time.sleep(think_time)
        
        # Short pause before submitting
        time.sleep(random.uniform(0.5, 1))
    
    def submit_prompt_to_chatgpt(self, input_element):
        """Submit the typed prompt to ChatGPT"""
        print("  submission...")
        
        # Try Enter key first (fastest)
        try:
            time.sleep(random.uniform(0.2, 0.5))
            input_element.send_keys(Keys.ENTER)
            time.sleep(random.uniform(0.5, 1))
            print(f"   ✅ Submitted with Enter key")
            return True
            
        except Exception as e:
            print(f"   ⚠️ Enter failed: {e}")
        
        # Try finding send button manually
        try:
            print("   🔍 Looking for send button...")
            send_button_selectors = [
                "button[data-testid='send-button']",
                "button[aria-label*='Send']",
                "button svg",
                "*[role='button'] svg"
            ]
            
            for selector in send_button_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in buttons:
                        if button.is_displayed() and button.is_enabled():
                            time.sleep(0.5)
                            button.click()
                            print(f"   ✅ Clicked button: {selector}")
                            return True
                except:
                    continue
                    
        except Exception as e:
            print(f"  Button search failed: {e}")
        
        print("  All submission methods failed")
        return False
    
    def wait_for_chatgpt_response(self):
        """Wait for and capture ChatGPT's response to the brand mention prompt"""
        print(" Waiting for response ...")
        
        # (15 seconds for complex prompts)
        initial_wait = 15
        print(f"   ⏳ Initial wait for response generation: {initial_wait}s...")
        time.sleep(initial_wait)
        
        response_selectors = [
            "div[data-message-author-role='assistant']",
            "div[data-testid*='conversation-turn']",
            ".markdown", 
            "div.whitespace-pre-wrap"
        ]
        
        max_attempts = 15  # Reasonable attempts after initial wait
        for attempt in range(max_attempts):
            try:
                for selector in response_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            response_text = elements[-1].text.strip()
                            if len(response_text) > 50:  # Higher threshold for confidence
                                print(f"   ✅ Response found! ({len(response_text)} chars)")
                                return response_text
                    except:
                        continue
                
                # Quick checks after initial wait
                time.sleep(1)
                
            except Exception as e:
                print(f"   ⚠️ Check {attempt + 1} error: {e}")
                time.sleep(0.5)
        
        print("  No response after waiting")
        return None
    
    def run_brand_mention_scraping(self):
        """Execute the complete brand mention scraping workflow"""
        print("\n🎯 STARTING BRAND MENTION SCRAPING FROM CHATGPT")
        print("=" * 60)
        
        prompts = get_prompts()
        print(f"📋 Loaded {len(prompts)} brand mention prompts")
        
        # Setup Chrome debug session
        debug_port = self.setup_chrome_debug_session()
        if not debug_port:
            return False
        
        # Connect to ChatGPT session
        if not self.connect_to_chatgpt_session(debug_port):
            return False
        
        try:
            print(f"\n🚀 Starting brand mention extraction...")
            successful_extractions = 0
            start_time = time.time()
            
            for i, prompt in enumerate(prompts, 1):
                prompt_start = time.time()
                print(f"\n📝 PROCESSING PROMPT {i}/{len(prompts)}")
                print("-" * 40)
                print(f"Prompt: {prompt[:60]}...")
                
                # Find ChatGPT input field
                input_element = self.locate_chatgpt_input_field()
                if not input_element:
                    print("   ❌ No input - manual intervention needed")
                    input("   ⏸️ Please fix and press Enter...")
                    continue
                
                # Type prompt for brand mentions
                self.type_prompt_to_chatgpt(input_element, prompt)
                
                # Submit prompt to ChatGPT
                if self.submit_prompt_to_chatgpt(input_element):
                    # Wait for and capture response
                    response = self.wait_for_chatgpt_response()
                    
                    if response:
                        # Process response for brand mentions
                        result = self.processor.process_response(prompt, response)
                        print(f"   📊 Brands found: {result['brand_mentions']}")
                        successful_extractions += 1
                        
                        prompt_time = time.time() - prompt_start
                        print(f"   ⏱️ Prompt completed in {prompt_time:.1f}s")
                    else:
                        print("   ❌ No response detected")
                else:
                    print("   ❌ Submission failed")
                
                # Short delay between prompts
                if i < len(prompts):
                    delay_time = random.uniform(self.delay, self.delay + 2)
                    print(f"   ⏳ Quick delay: {delay_time:.1f}s...")
                    time.sleep(delay_time)
            
            # Final results
            total_time = time.time() - start_time
            print(f"\n🎉 BRAND MENTION SCRAPING COMPLETE!")
            print(f"   ✅ Success rate: {successful_extractions}/{len(prompts)}")
            print(f"   ⏱️ Total time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
            print(f"   📈 Average per prompt: {total_time/len(prompts):.1f}s")
            
            if successful_extractions > 0:
                self.processor.print_detailed_summary()
                filename = f"brand_mentions_results_{int(time.time())}.json"
                self.processor.save_to_json(filename)
                print(f"💾 Saved: {filename}")
            
            return successful_extractions > 0
            
        finally:
            if self.driver:
                print("\n🔒 Keeping browser open for inspection...")
                input("Press Enter to close browser...")
                self.driver.quit()


def main():
    """Main function to start the brand mention scraping process"""
    print("🎯 CHATGPT BRAND MENTION SCRAPER")
    print("=" * 50)
    print("🚀 Automated extraction of sportswear brand mentions from ChatGPT")
    print("📊 Analyzes responses for Nike, Adidas, Hoka, New Balance, Jordan")
    print()
    
    choice = input("Start brand mention scraping? (y/n): ").strip().lower()
    
    if choice == 'y':
        scraper = GPTScrapper(delay=3)
        scraper.run_brand_mention_scraping()
    else:
        print("👋 Goodbye!")


if __name__ == "__main__":
    main() 