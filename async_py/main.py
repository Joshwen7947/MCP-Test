#!/usr/bin/env python3
"""
Async Programming in Python - Simple Examples
Learning when and why to use async/await
"""

import asyncio
import time
import aiohttp
import requests

def sync_requests():
    """Make requests one after another - slow way"""
    print("Making requests the slow way...")
    
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1", 
        "https://httpbin.org/delay/1"
    ]
    
    start = time.time()
    
    for i, url in enumerate(urls):
        print(f"Request {i+1}: starting")
        r = requests.get(url)
        print(f"Request {i+1}: done")
    
    total = time.time() - start
    print(f"Total time: {total:.1f} seconds")
    print()

async def async_requests():
    """Make requests at the same time - fast way"""
    print("Making requests the fast way...")
    
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1"
    ]
    
    async def get_url(session, url, num):
        print(f"Request {num}: starting")
        async with session.get(url) as response:
            await response.text()
            print(f"Request {num}: done")
    
    start = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = [get_url(session, url, i+1) for i, url in enumerate(urls)]
        await asyncio.gather(*tasks)
    
    total = time.time() - start
    print(f"Total time: {total:.1f} seconds")
    print()

async def simple_example():
    """Basic async/await example"""
    print("Simple async example:")
    
    async def do_work(name, seconds):
        print(f"{name} starting")
        await asyncio.sleep(seconds)
        print(f"{name} finished")
        return f"{name} done"
    
    # Start all tasks at once
    task1 = asyncio.create_task(do_work("Task A", 2))
    task2 = asyncio.create_task(do_work("Task B", 1))
    task3 = asyncio.create_task(do_work("Task C", 1.5))
    
    # Wait for all to finish
    results = await asyncio.gather(task1, task2, task3)
    print(f"Results: {results}")
    print()

def when_to_use():
    """When should you use async?"""
    print("When to use async:")
    print("- Web requests")
    print("- File reading/writing") 
    print("- Database queries")
    print("- API calls")
    print("- Any I/O operation")
    print()
    print("When NOT to use async:")
    print("- Math calculations")
    print("- Image processing")
    print("- CPU intensive work")
    print()

async def web_scraper_example():
    """Real example: scrape multiple sites"""
    print("Web scraper example:")
    
    sites = [
        "https://httpbin.org/json",
        "https://httpbin.org/uuid",
        "https://httpbin.org/user-agent"
    ]
    
    async def scrape(session, url, num):
        print(f"Scraping site {num}")
        try:
            async with session.get(url) as response:
                data = await response.json()
                print(f"Site {num}: got data")
                return {"url": url, "success": True}
        except:
            print(f"Site {num}: failed")
            return {"url": url, "success": False}
    
    start = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = [scrape(session, url, i+1) for i, url in enumerate(sites)]
        results = await asyncio.gather(*tasks)
    
    total = time.time() - start
    success_count = sum(1 for r in results if r["success"])
    
    print(f"Scraped {len(sites)} sites in {total:.1f} seconds")
    print(f"Success: {success_count}/{len(sites)}")
    print()

async def main():
    """Run all examples"""
    print("Async Programming Examples")
    print("=" * 30)
    print()
    
    # Show the slow way
    sync_requests()
    
    # Show the fast way
    await async_requests()
    
    # Basic syntax
    await simple_example()
    
    # When to use
    when_to_use()
    
    # Real example
    await web_scraper_example()
    
    print("Summary:")
    print("- Use async for I/O operations")
    print("- Much faster than sync for multiple requests")
    print("- Easy to learn with async/await")
    print("- Essential for modern Python apps")

if __name__ == "__main__":
    asyncio.run(main())