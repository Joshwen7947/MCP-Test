#!/usr/bin/env python3
"""
Reddit Python Topics Analyzer
A web scraper to analyze popular Python discussions on Reddit

This script demonstrates web scraping fundamentals by:
1. Making HTTP requests to Reddit subreddits
2. Parsing HTML content with BeautifulSoup
3. Extracting and filtering relevant data
4. Saving results in multiple formats (JSON, CSV)
5. Implementing respectful scraping practices (delays, headers)

Author: Web Scraping Tutorial
Purpose: Educational demonstration of web scraping concepts
"""

# Standard library imports for data handling and time management
import requests  # For making HTTP requests to web pages
from bs4 import BeautifulSoup  # For parsing HTML content and extracting data
import json  # For saving data in JSON format (structured, human-readable)
import csv  # For saving data in CSV format (spreadsheet-compatible)
import time  # For adding delays between requests and timestamping data

def scrape_reddit_python_topics() -> list[dict[str, Any]]:
    """
    Main scraping function that extracts Python-related content from multiple Reddit subreddits.
    
    This function demonstrates the core web scraping workflow:
    1. Define target URLs (subreddits to scrape)
    2. Loop through each URL and make HTTP requests
    3. Parse HTML content to extract relevant data
    4. Filter and structure the extracted data
    5. Return organized data for further processing
    
    Returns:
        list: A list of dictionaries, where each dictionary contains data from one subreddit.
              Each subreddit dictionary includes:
              - subreddit: Name of the subreddit (e.g., 'Python')
              - url: The URL that was scraped
              - title: Page title from HTML <title> tag
              - scraped_at: Timestamp when scraping occurred
              - python_topics: List of Python-related headings/topics found
              - discussions: List of discussion links found
    """
    
    # Define the target subreddits to scrape
    # These are Python-related communities on Reddit that likely contain relevant content
    subreddits = [
        "https://www.reddit.com/r/Python",        # Main Python subreddit - general Python content
        "https://www.reddit.com/r/programming",   # General programming subreddit - may contain Python discussions
        "https://www.reddit.com/r/learnpython",   # Learning-focused Python subreddit - beginner questions and resources
        # Additional URLs that could be uncommented for more comprehensive scraping:
        # "https://www.reddit.com/r/Python/hot/",  # Hot posts from r/Python
        # "https://www.reddit.com/r/Python/top/",  # Top posts from r/Python
        # "https://www.reddit.com/r/Python/new/",  # New posts from r/Python
    ]
    
    # Initialize empty list to store data from all subreddits
    # This will accumulate results as we scrape each subreddit
    all_data = []
    
    # Loop through each subreddit URL to scrape content
    for url in subreddits:
        # HTTP Headers: Critical for successful web scraping
        # Many websites block requests that don't look like they come from a real browser
        # The User-Agent header tells the server what browser/device is making the request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            # This User-Agent string mimics Chrome on Windows 10
            # Other common User-Agent strings:
            # - Firefox: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
            # - Safari: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15'
        }
        
        # Extract subreddit name from URL for display and data organization
        # Example: "https://www.reddit.com/r/Python" -> "Python"
        # The split('/') method splits the URL by forward slashes
        # [-1] gets the last element (the subreddit name)
        subreddit_name = url.split('/')[-1]
        print(f"Scraping r/{subreddit_name}...")  # User feedback during execution
        
        # Error handling: Wrap scraping logic in try-except to handle network issues gracefully
        try:
            # Make HTTP GET request to fetch the webpage
            # requests.get() parameters:
            # - url: The webpage URL to fetch
            # - headers: HTTP headers to send with the request (makes us look like a real browser)
            # - timeout: Maximum time to wait for response (prevents hanging on slow connections)
            response = requests.get(url, headers=headers, timeout=10)
            
            # Check if the request was successful
            # raise_for_status() raises an exception if HTTP status code indicates an error
            # Common HTTP status codes:
            # - 200: OK (success)
            # - 404: Not Found
            # - 403: Forbidden (blocked)
            # - 500: Internal Server Error
            response.raise_for_status()
            
            # Parse the HTML content using BeautifulSoup
            # BeautifulSoup converts raw HTML into a navigable tree structure
            # Parameters:
            # - response.content: Raw HTML content from the HTTP response (bytes)
            # - 'html.parser': Parser to use (built-in Python parser, good for most cases)
            # Alternative parsers: 'lxml' (faster), 'html5lib' (more lenient)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Create a dictionary to store all data for this subreddit
            # This structure makes it easy to organize and access different types of data
            subreddit_data = {
                'subreddit': subreddit_name,  # Store the subreddit name for identification
                'url': url,                   # Store the original URL for reference
                'title': soup.title.string if soup.title else 'No title',  # Extract page title from HTML <title> tag
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')  # Timestamp when scraping occurred
            }
            
            # Extract Python-related topics from HTML headings
            # HTML headings (h1, h2, h3, h4) often contain important content like post titles, section headers
            topics = []  # Initialize empty list to store found topics
            
            # Find all heading elements in the HTML
            # soup.find_all() searches for elements matching the given criteria
            # ['h1', 'h2', 'h3', 'h4'] means "find any h1, h2, h3, or h4 elements"
            for heading in soup.find_all(['h1', 'h2', 'h3', 'h4']):
                # Extract text content from the heading element
                # get_text(strip=True) gets the text content and removes leading/trailing whitespace
                text = heading.get_text(strip=True)
                
                # Filter out very short text (likely not meaningful content)
                if text and len(text) > 3:
                    # Apply keyword filtering to find Python-related content
                    # any() returns True if any of the keywords are found in the text
                    # text.lower() converts to lowercase for case-insensitive matching
                    # This helps identify relevant content even if keywords are capitalized differently
                    if any(keyword in text.lower() for keyword in ['python', 'programming', 'code', 'developer', 'coding']):
                        # If Python-related keywords are found, add to topics list
                        topics.append({
                            'title': text,           # The actual heading text
                            'type': 'python_topic'   # Categorize this as a Python topic
                        })
            
            # Extract discussion links from HTML anchor tags
            # Reddit discussion URLs contain '/comments/' in their path
            # This helps us identify actual discussion threads vs. other links
            discussions = []  # Initialize empty list to store discussion links
            seen_urls = set()  # Use a set to track URLs we've already seen (prevents duplicates)
            
            # Find all anchor tags (<a>) that have an href attribute
            # soup.find_all('a', href=True) finds all <a> tags with href attributes
            for link in soup.find_all('a', href=True):
                # Extract the link text (what users see) and the URL (where it points)
                text = link.get_text(strip=True)  # Link text, stripped of whitespace
                href = link['href']               # The href attribute (the URL)
                
                # Apply multiple filters to find relevant discussion links:
                # 1. text and len(text) > 1: Must have meaningful text content
                # 2. '/comments/' in href: Must be a Reddit discussion URL
                # 3. href not in seen_urls: Must not be a duplicate we've already processed
                if text and len(text) > 1 and '/comments/' in href and href not in seen_urls:
                    # Add URL to seen set to prevent future duplicates
                    seen_urls.add(href)
                    
                    # Add discussion to our list with truncated title for readability
                    discussions.append({
                        'title': text[:100] + '...' if len(text) > 100 else text,  # Truncate very long titles
                        'url': href,        # The full Reddit discussion URL
                        'type': 'discussion'  # Categorize this as a discussion
                    })
            
            # Store the extracted data in our subreddit dictionary
            subreddit_data['python_topics'] = topics      # Add the Python topics we found
            subreddit_data['discussions'] = discussions   # Add the discussion links we found
            
            # Add this subreddit's data to our overall results
            all_data.append(subreddit_data)
            
            # Implement respectful scraping: Add delay between requests
            # This prevents overwhelming the server with too many rapid requests
            # 2 seconds is a reasonable delay that's respectful but not too slow
            # Other common delays: 1 second (faster), 5 seconds (more conservative)
            time.sleep(2)
            
        # Handle specific types of errors that might occur during scraping
        except requests.RequestException as e:
            # This catches network-related errors (connection timeout, DNS failure, etc.)
            # requests.RequestException is the base class for all requests library exceptions
            # Common subclasses: ConnectionError, Timeout, HTTPError, TooManyRedirects
            print(f"Error fetching r/{subreddit_name}: {e}")
            # Continue to next subreddit instead of crashing the entire program
            
        except Exception as e:
            # This catches any other unexpected errors (parsing errors, data processing errors, etc.)
            # It's a broad catch-all that ensures the program doesn't crash on unexpected issues
            print(f"Error parsing r/{subreddit_name}: {e}")
            # Continue to next subreddit instead of crashing the entire program
    
    # Return all the data we've collected from all subreddits
    # This list contains dictionaries, one for each successfully scraped subreddit
    return all_data

def save_python_data(data, filename_json='python_topics.json', filename_csv='python_topics.csv'):
    """
    Save the scraped Python topic data to both JSON and CSV file formats.
    
    This function demonstrates data persistence - saving scraped data for later analysis.
    Two formats are used for different purposes:
    - JSON: Structured, hierarchical data format (good for programming/APIs)
    - CSV: Tabular format (good for spreadsheets, data analysis tools)
    
    Parameters:
        data (list): List of dictionaries containing scraped subreddit data
        filename_json (str): Name of the JSON output file (default: 'python_topics.json')
        filename_csv (str): Name of the CSV output file (default: 'python_topics.csv')
    
    Returns:
        None: This function saves files but doesn't return any data
    """
    
    # Validate that we have data to save
    if not data:
        print("No data to save")  # Early return if no data was scraped
        return
    
    # Save data in JSON format (structured, hierarchical)
    try:
        # Open file in write mode with UTF-8 encoding to handle international characters
        with open(filename_json, 'w', encoding='utf-8') as f:
            # json.dump() writes Python data structures to JSON format
            # Parameters:
            # - data: The Python data to convert to JSON
            # - f: The file object to write to
            # - indent=2: Pretty-print with 2-space indentation (makes it human-readable)
            # - ensure_ascii=False: Allow non-ASCII characters (emojis, accented letters, etc.)
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Python topics data saved to {filename_json}")
    except Exception as e:
        # Handle file I/O errors (permission denied, disk full, etc.)
        print(f"Error saving JSON: {e}")
    
    # Save data in CSV format (tabular, spreadsheet-compatible)
    try:
        # Open file in write mode with UTF-8 encoding and proper line ending handling
        with open(filename_csv, 'w', newline='', encoding='utf-8') as f:
            # Create a CSV writer object to handle proper CSV formatting
            writer = csv.writer(f)
            
            # Write the header row (column names)
            # These column names will appear in the first row of the CSV file
            writer.writerow(['Subreddit', 'Type', 'Title', 'URL', 'Scraped At'])
            
            # Loop through each subreddit's data to write rows
            for subreddit_data in data:
                # Extract common fields that will be used for all rows from this subreddit
                subreddit = subreddit_data['subreddit']    # Subreddit name (e.g., 'Python')
                scraped_at = subreddit_data['scraped_at']  # Timestamp when data was scraped
                
                # Write rows for Python topics (headings, rules, etc.)
                # subreddit_data.get('python_topics', []) safely gets the list or returns empty list if key doesn't exist
                for topic in subreddit_data.get('python_topics', []):
                    # Each row represents one topic found in the subreddit
                    # Format: [Subreddit, Type, Title, URL, Scraped At]
                    # Empty string for URL since topics don't have direct links
                    writer.writerow([subreddit, topic['type'], topic['title'], '', scraped_at])
                
                # Write rows for discussions (actual Reddit posts with URLs)
                for discussion in subreddit_data.get('discussions', []):
                    # Each row represents one discussion thread found in the subreddit
                    # Format: [Subreddit, Type, Title, URL, Scraped At]
                    writer.writerow([subreddit, discussion['type'], discussion['title'], discussion['url'], scraped_at])
        
        print(f"Python topics data saved to {filename_csv}")
    except Exception as e:
        # Handle file I/O errors (permission denied, disk full, etc.)
        print(f"Error saving CSV: {e}")

def main() -> None:
    """
    Main function that orchestrates the entire web scraping process.
    
    This function demonstrates the complete workflow:
    1. Display program information and user interface
    2. Execute the scraping process
    3. Process and summarize the results
    4. Save data to files
    5. Provide user feedback on completion
    
    This is the entry point of the program when run directly.
    """
    
    # Display program header and user interface
    print("Reddit Python Topics Analyzer")
    print("=" * 40)  # Create a visual separator line
    
    # Execute the main scraping function
    # This calls our scrape_reddit_python_topics() function which does all the heavy lifting
    data = scrape_reddit_python_topics()
    
    # Check if scraping was successful (data was returned)
    if data:
        # Process and display summary statistics
        print(f"\nAnalysis Results:")
        
        # Initialize counters for total statistics
        total_topics = 0      # Count of all Python topics found across all subreddits
        total_discussions = 0 # Count of all discussions found across all subreddits
        
        # Loop through each subreddit's data to calculate individual and total counts
        for subreddit_data in data:
            # Count topics and discussions for this specific subreddit
            # .get() method safely retrieves values, returning empty list if key doesn't exist
            topics_count = len(subreddit_data.get('python_topics', []))
            discussions_count = len(subreddit_data.get('discussions', []))
            
            # Add to running totals
            total_topics += topics_count
            total_discussions += discussions_count
            
            # Display per-subreddit statistics for user feedback
            print(f"r/{subreddit_data['subreddit']}: {topics_count} Python topics, {discussions_count} discussions")
        
        # Display overall summary statistics
        print(f"\nTotal: {total_topics} Python topics, {total_discussions} discussions across {len(data)} subreddits")
        
        # Save the scraped data to files using our save function
        save_python_data(data)
        
        # Provide completion feedback and next steps to the user
        print("\nPython topics analysis completed successfully!")
        print("Check python_topics.json and python_topics.csv for detailed results.")
        
    else:
        # Handle the case where scraping failed (no data returned)
        print("Analysis failed. Check your internet connection and try again.")


if __name__ == "__main__":
    main()