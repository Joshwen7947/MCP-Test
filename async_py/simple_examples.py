#!/usr/bin/env python3
"""
Simple Async Examples for Beginners
Easy-to-understand async programming examples

These examples are perfect for introducing async concepts
without overwhelming beginners with complex code.
"""

import asyncio
import time

async def simple_async_function():
    """
    The simplest possible async function.
    
    This demonstrates the basic async/await syntax.
    """
    print("🚀 Starting async function...")
    
    # asyncio.sleep() is the async equivalent of time.sleep()
    # It doesn't block the entire program, just this function
    await asyncio.sleep(2)
    
    print("✅ Async function completed!")

async def multiple_async_tasks():
    """
    Run multiple async tasks concurrently.
    
    This shows how async allows multiple operations
    to run at the same time.
    """
    print("🎯 Running multiple async tasks...")
    
    async def task(name, delay):
        print(f"   🏃 Starting {name}")
        await asyncio.sleep(delay)
        print(f"   ✅ {name} completed")
        return f"{name} result"
    
    # Create tasks that will run concurrently
    task1 = asyncio.create_task(task("Task A", 2))
    task2 = asyncio.create_task(task("Task B", 1))
    task3 = asyncio.create_task(task("Task C", 3))
    
    # Wait for all tasks to complete
    results = await asyncio.gather(task1, task2, task3)
    
    print("🎉 All tasks completed!")
    print(f"Results: {results}")

def synchronous_version():
    """
    The synchronous version for comparison.
    
    This shows how the same operations would work
    without async programming.
    """
    print("🔄 Running synchronous version...")
    
    def task(name, delay):
        print(f"   🏃 Starting {name}")
        time.sleep(delay)  # This blocks the entire program
        print(f"   ✅ {name} completed")
        return f"{name} result"
    
    # Tasks run one after another (sequentially)
    result1 = task("Task A", 2)
    result2 = task("Task B", 1)
    result3 = task("Task C", 3)
    
    print("🎉 All tasks completed!")
    print(f"Results: {[result1, result2, result3]}")

async def timing_comparison():
    """
    Compare the timing of async vs sync approaches.
    
    This demonstrates the performance difference
    between async and synchronous programming.
    """
    print("⏱️  TIMING COMPARISON")
    print("=" * 25)
    
    # Async version
    print("\n🚀 Async version:")
    start_time = time.time()
    await multiple_async_tasks()
    async_time = time.time() - start_time
    print(f"   Total time: {async_time:.2f} seconds")
    
    # Sync version
    print("\n🔄 Sync version:")
    start_time = time.time()
    synchronous_version()
    sync_time = time.time() - start_time
    print(f"   Total time: {sync_time:.2f} seconds")
    
    # Show the difference
    speedup = sync_time / async_time
    print(f"\n📊 Speed improvement: {speedup:.1f}x faster with async!")

async def main():
    """
    Run all the simple examples.
    
    This function demonstrates the progression from
    simple async concepts to more complex examples.
    """
    print("🎓 SIMPLE ASYNC EXAMPLES")
    print("=" * 30)
    
    # Example 1: Basic async function
    print("\n1️⃣  Basic Async Function:")
    await simple_async_function()
    
    # Example 2: Multiple async tasks
    print("\n2️⃣  Multiple Async Tasks:")
    await multiple_async_tasks()
    
    # Example 3: Timing comparison
    print("\n3️⃣  Timing Comparison:")
    await timing_comparison()
    
    print("\n🎯 Key Takeaways:")
    print("   • async def: Define an async function")
    print("   • await: Wait for an async operation")
    print("   • asyncio.create_task(): Create concurrent tasks")
    print("   • asyncio.gather(): Wait for multiple tasks")
    print("   • Async is faster for I/O-bound operations!")

if __name__ == "__main__":
    # Run the simple examples
    asyncio.run(main())

