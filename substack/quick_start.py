#!/usr/bin/env python3
"""
Quick Start Script for Substack Notes Automation
A simplified version for immediate testing and setup
"""

import os
import json
from substack import SubstackNotesPoster

def create_env_file():
    """Create a .env file with user input."""
    print("Setting up your Substack automation...")
    print("=" * 40)
    
    email = input("Enter your Substack email: ").strip()
    password = input("Enter your Substack password: ").strip()
    substack_url = input("Enter your Substack URL (or press Enter for thenerdnook.substack.com): ").strip()
    
    if not substack_url:
        substack_url = "https://thenerdnook.substack.com"
    
    # Create .env file
    env_content = f"""SUBSTACK_EMAIL={email}
SUBSTACK_PASSWORD={password}
SUBSTACK_URL={substack_url}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    return True

def test_connection():
    """Test the connection and login."""
    print("\nTesting connection to Substack...")
    
    try:
        poster = SubstackNotesPoster()
        poster.setup_browser()
        
        if poster.login_to_substack():
            print("✅ Login successful!")
            poster.driver.quit()
            return True
        else:
            print("❌ Login failed. Please check your credentials.")
            poster.driver.quit()
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Quick setup and test."""
    print("Substack Notes Automation - Quick Start")
    print("=" * 40)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        if not create_env_file():
            return
    else:
        print("✅ .env file already exists")
    
    # Test connection
    if test_connection():
        print("\n🎉 Setup complete! You can now run:")
        print("python substack.py")
        print("\nChoose option 1 to post a test note immediately!")
    else:
        print("\n❌ Setup failed. Please check your credentials and try again.")

if __name__ == "__main__":
    main()
