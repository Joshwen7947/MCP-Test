#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import csv
import time

def scrape_reddit_python_topics():
    
    subreddits = [
        "https://www.reddit.com/r/Python",
        "https://www.reddit.com/r/programming",
        "https://www.reddit.com/r/learnpython",
    ]
    all_data = []
    for url in subreddits:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        subreddit_name = url.split('/')[-1]
        print(f"Scraping r/{subreddit_name}...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            subreddit_data = {
                'subreddit': subreddit_name,
                'url': url,
                'title': soup.title.string if soup.title else 'No title',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            topics = []
            for heading in soup.find_all(['h1', 'h2', 'h3', 'h4']):
                text = heading.get_text(strip=True)
                if text and len(text) > 3:
                    if any(keyword in text.lower() for keyword in ['python', 'programming', 'code', 'developer', 'coding']):
                        topics.append({
                            'title': text,
                            'type': 'python_topic'
                        })
            discussions = []
            seen_urls = set()
            for link in soup.find_all('a', href=True):
                text = link.get_text(strip=True)
                href = link['href']
                if text and len(text) > 1 and '/comments/' in href and href not in seen_urls:
                    seen_urls.add(href)
                    discussions.append({
                        'title': text[:100] + '...' if len(text) > 100 else text,
                        'url': href,
                        'type': 'discussion'
                    })
            subreddit_data['python_topics'] = topics
            subreddit_data['discussions'] = discussions
            all_data.append(subreddit_data)
            time.sleep(2)
        except requests.RequestException as e:
            print(f"Error fetching r/{subreddit_name}: {e}")
        except Exception as e:
            print(f"Error parsing r/{subreddit_name}: {e}")
    return all_data

def save_python_data(data, filename_json='python_topics.json', filename_csv='python_topics.csv'):
    
    if not data:
        print("No data to save")
        return
    try:
        with open(filename_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Python topics data saved to {filename_json}")
    except Exception as e:
        print(f"Error saving JSON: {e}")
    try:
        with open(filename_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Subreddit', 'Type', 'Title', 'URL', 'Scraped At'])
            for subreddit_data in data:
                subreddit = subreddit_data['subreddit']
                scraped_at = subreddit_data['scraped_at']
                for topic in subreddit_data.get('python_topics', []):
                    writer.writerow([subreddit, topic['type'], topic['title'], '', scraped_at])
                for discussion in subreddit_data.get('discussions', []):
                    writer.writerow([subreddit, discussion['type'], discussion['title'], discussion['url'], scraped_at])
        print(f"Python topics data saved to {filename_csv}")
    except Exception as e:
        print(f"Error saving CSV: {e}")

def main():
    
    print("Reddit Python Topics Analyzer")
    print("=" * 40)
    data = scrape_reddit_python_topics()
    if data:
        print(f"\nAnalysis Results:")
        total_topics = 0
        total_discussions = 0
        for subreddit_data in data:
            topics_count = len(subreddit_data.get('python_topics', []))
            discussions_count = len(subreddit_data.get('discussions', []))
            total_topics += topics_count
            total_discussions += discussions_count
            print(f"r/{subreddit_data['subreddit']}: {topics_count} Python topics, {discussions_count} discussions")
        print(f"\nTotal: {total_topics} Python topics, {total_discussions} discussions across {len(data)} subreddits")
        save_python_data(data)
        print("\nPython topics analysis completed successfully!")
        print("Check python_topics.json and python_topics.csv for detailed results.")
    else:
        print("Analysis failed. Check your internet connection and try again.")

if __name__ == "__main__":
    main()  