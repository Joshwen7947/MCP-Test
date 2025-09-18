#!/usr/bin/env python3
"""
Substack Notes Automation Tool
Automatically posts notes to your Substack at scheduled times

This tool demonstrates web automation using Selenium to interact with Substack's web interface.
It can post pre-written notes on a schedule, making it perfect for consistent content delivery.

Author: Automation Project
Purpose: Automated Substack Notes posting
"""

import time
import random
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import schedule

# Load environment variables from .env file
load_dotenv()

class SubstackNotesPoster:
    """
    A class to automate posting notes to Substack.
    
    This class handles:
    - Browser automation using Selenium
    - Login to Substack
    - Posting notes with content
    - Scheduling posts
    - Error handling and logging
    """
    
    def __init__(self):
        """
        Initialize the Substack Notes Poster.
        
        Sets up browser configuration and loads credentials from environment variables.
        """
        # Load credentials from environment variables
        self.email = os.getenv('SUBSTACK_EMAIL')
        self.password = os.getenv('SUBSTACK_PASSWORD')
        self.substack_url = os.getenv('SUBSTACK_URL', 'https://thenerdnook.substack.com')
        
        # Validate that required credentials are provided
        if not self.email or not self.password:
            raise ValueError("Please set SUBSTACK_EMAIL and SUBSTACK_PASSWORD in your .env file")
        
        # Initialize browser driver
        self.driver = None
        self.wait = None
        
        # Load notes from JSON file
        self.notes = self.load_notes()
        
    def setup_browser(self):
        """
        Set up Chrome browser with appropriate options for automation.
        
        Configures Chrome to run in headless mode (no GUI) for server deployment,
        but can be configured to show browser for debugging.
        """
        # Chrome options for automation
        chrome_options = Options()
        
        # Uncomment the next line to run in headless mode (no browser window)
        # chrome_options.add_argument("--headless")
        
        # Additional Chrome options for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Set user agent to avoid detection
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Automatically download and set up ChromeDriver
        service = Service(ChromeDriverManager().install())
        
        # Initialize the Chrome driver
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set up explicit wait for elements (waits up to 10 seconds for elements to appear)
        self.wait = WebDriverWait(self.driver, 10)
        
        print("Browser setup completed successfully")
    
    def load_notes(self):
        """
        Load notes from a JSON file.
        
        Returns:
            list: List of note dictionaries containing content and metadata
        """
        notes_file = 'notes.json'
        
        # Check if notes file exists
        if not os.path.exists(notes_file):
            # Create a sample notes file if it doesn't exist
            sample_notes = [
                {
                    "content": "Just learned something amazing about Python! 🐍\n\nDid you know that Python's list comprehensions are not only more readable but often faster than traditional loops? Here's a quick example:\n\n# Traditional way\nsquares = []\nfor i in range(10):\n    squares.append(i**2)\n\n# Pythonic way\nsquares = [i**2 for i in range(10)]\n\nBoth do the same thing, but the list comprehension is more concise and Pythonic!",
                    "tags": ["python", "programming", "tips"],
                    "category": "programming"
                },
                {
                    "content": "Automation tip of the day! 🤖\n\nInstead of manually checking websites for updates, you can use Python to automate the process. A simple web scraper can save you hours of manual work.\n\nWhat's your favorite automation tool? Let me know in the comments!",
                    "tags": ["automation", "python", "productivity"],
                    "category": "automation"
                },
                {
                    "content": "Quick productivity hack! ⚡\n\nUse the Pomodoro Technique for focused work sessions:\n• 25 minutes of focused work\n• 5-minute break\n• Repeat 4 times\n• Take a longer 15-30 minute break\n\nThis technique helps maintain focus and prevents burnout. Try it out!",
                    "tags": ["productivity", "focus", "tips"],
                    "category": "productivity"
                }
            ]
            
            # Save sample notes to file
            with open(notes_file, 'w', encoding='utf-8') as f:
                json.dump(sample_notes, f, indent=2, ensure_ascii=False)
            
            print(f"Created sample notes file: {notes_file}")
            return sample_notes
        
        # Load existing notes
        try:
            with open(notes_file, 'r', encoding='utf-8') as f:
                notes = json.load(f)
            print(f"Loaded {len(notes)} notes from {notes_file}")
            return notes
        except Exception as e:
            print(f"Error loading notes: {e}")
            return []
    
    def login_to_substack(self):
        """
        Log in to Substack using provided credentials.
        
        This method navigates to the login page, enters credentials,
        and waits for successful login.
        """
        try:
            print("Navigating to Substack login page...")
            
            # Navigate to Substack login page
            self.driver.get("https://substack.com/sign-in")
            
            # Wait for and fill email field
            email_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_field.clear()
            email_field.send_keys(self.email)
            
            # Wait for and fill password field
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(self.password)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for login to complete (look for dashboard or profile elements)
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "dashboard")),
                    EC.presence_of_element_located((By.CLASS_NAME, "profile")),
                    EC.url_contains("dashboard")
                )
            )
            
            print("Successfully logged in to Substack!")
            return True
            
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    
    def navigate_to_notes(self):
        """
        Navigate to the Notes section of Substack.
        
        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            print("Navigating to Notes section...")
            
            # Navigate to the notes page
            notes_url = f"{self.substack_url}/notes"
            self.driver.get(notes_url)
            
            # Wait for notes page to load
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "notes"))
            )
            
            print("Successfully navigated to Notes section")
            return True
            
        except Exception as e:
            print(f"Failed to navigate to Notes: {e}")
            return False
    
    def post_note(self, note_content):
        """
        Post a note to Substack.
        
        Args:
            note_content (str): The content of the note to post
            
        Returns:
            bool: True if posting successful, False otherwise
        """
        try:
            print("Starting to post note...")
            
            # Look for the "Write a note" button or text area
            # Substack's interface may vary, so we'll try multiple selectors
            note_selectors = [
                "//button[contains(text(), 'Write a note')]",
                "//button[contains(text(), 'New note')]",
                "//textarea[@placeholder*='note']",
                "//div[@contenteditable='true']"
            ]
            
            note_element = None
            for selector in note_selectors:
                try:
                    note_element = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except:
                    continue
            
            if not note_element:
                print("Could not find note input element")
                return False
            
            # Click the note input area
            note_element.click()
            time.sleep(1)
            
            # Type the note content
            note_element.send_keys(note_content)
            time.sleep(2)
            
            # Look for and click the publish button
            publish_selectors = [
                "//button[contains(text(), 'Publish')]",
                "//button[contains(text(), 'Post')]",
                "//button[@type='submit']"
            ]
            
            publish_button = None
            for selector in publish_selectors:
                try:
                    publish_button = self.driver.find_element(By.XPATH, selector)
                    if publish_button.is_enabled():
                        break
                except:
                    continue
            
            if publish_button:
                publish_button.click()
                time.sleep(3)
                print("Note posted successfully!")
                return True
            else:
                print("Could not find publish button")
                return False
                
        except Exception as e:
            print(f"Error posting note: {e}")
            return False
    
    def post_random_note(self):
        """
        Post a random note from the loaded notes.
        
        Returns:
            bool: True if posting successful, False otherwise
        """
        if not self.notes:
            print("No notes available to post")
            return False
        
        # Select a random note
        note = random.choice(self.notes)
        note_content = note['content']
        
        print(f"Posting note with category: {note.get('category', 'general')}")
        print(f"Note content preview: {note_content[:100]}...")
        
        return self.post_note(note_content)
    
    def run_scheduled_post(self):
        """
        Execute a scheduled post (login, navigate, post, cleanup).
        
        This method is called by the scheduler and handles the complete
        posting workflow with error handling.
        """
        try:
            print(f"\n=== Starting scheduled post at {datetime.now()} ===")
            
            # Set up browser
            self.setup_browser()
            
            # Login to Substack
            if not self.login_to_substack():
                return False
            
            # Navigate to notes section
            if not self.navigate_to_notes():
                return False
            
            # Post a random note
            success = self.post_random_note()
            
            if success:
                print("Scheduled post completed successfully!")
            else:
                print("Scheduled post failed!")
            
            return success
            
        except Exception as e:
            print(f"Error in scheduled post: {e}")
            return False
        finally:
            # Always close the browser
            if self.driver:
                self.driver.quit()
                print("Browser closed")
    
    def setup_schedule(self, post_times=None):
        """
        Set up the posting schedule.
        
        Args:
            post_times (list): List of times to post (default: daily at 9 AM)
        """
        if post_times is None:
            post_times = ["09:00"]  # Default: daily at 9 AM
        
        # Clear any existing scheduled jobs
        schedule.clear()
        
        # Schedule posts for each specified time
        for post_time in post_times:
            schedule.every().day.at(post_time).do(self.run_scheduled_post)
            print(f"Scheduled daily post at {post_time}")
        
        print(f"Schedule setup complete. Posts scheduled for: {', '.join(post_times)}")
    
    def run_scheduler(self):
        """
        Run the scheduler to execute posts at scheduled times.
        
        This method runs indefinitely, checking for scheduled posts.
        """
        print("Starting scheduler...")
        print("Press Ctrl+C to stop the scheduler")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\nScheduler stopped by user")
        except Exception as e:
            print(f"Scheduler error: {e}")

def main():
    """
    Main function to run the Substack Notes automation.
    
    This function demonstrates different ways to use the automation:
    1. Post a single note immediately
    2. Set up scheduled posting
    3. Run the scheduler
    """
    print("Substack Notes Automation Tool")
    print("=" * 40)
    
    try:
        # Initialize the poster
        poster = SubstackNotesPoster()
        
        # Ask user what they want to do
        print("\nChoose an option:")
        print("1. Post a single note now")
        print("2. Set up scheduled posting")
        print("3. Run scheduler (for continuous operation)")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            # Post a single note immediately
            print("\nPosting a single note...")
            poster.setup_browser()
            
            if poster.login_to_substack() and poster.navigate_to_notes():
                poster.post_random_note()
            
            if poster.driver:
                poster.driver.quit()
                
        elif choice == "2":
            # Set up scheduled posting
            print("\nSetting up scheduled posting...")
            times_input = input("Enter posting times (comma-separated, e.g., '09:00,15:00'): ").strip()
            
            if times_input:
                post_times = [time.strip() for time in times_input.split(',')]
            else:
                post_times = ["09:00"]  # Default time
            
            poster.setup_schedule(post_times)
            
            # Run scheduler
            poster.run_scheduler()
            
        elif choice == "3":
            # Run scheduler with default schedule
            poster.setup_schedule()
            poster.run_scheduler()
            
        else:
            print("Invalid choice. Please run the program again.")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have set up your .env file with SUBSTACK_EMAIL and SUBSTACK_PASSWORD")

if __name__ == "__main__":
    main()
