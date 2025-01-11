import asyncio

async def background_task():
    while True:
        print("task is running")
        await asyncio.sleep(1)

async def exec_after_delay(callback, delay):
    await asyncio.sleep(delay)
    await callback

def timer(callback, delay):
    asyncio.create_task(exec_after_delay(callback, delay))

