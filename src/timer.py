import asyncio

async def exec_after_delay(callback, delay, args=[]):
    await asyncio.sleep(delay)
    await callback(*args)

def timer(callback, delay, args=[]):
    return asyncio.create_task(exec_after_delay(callback, delay, args))

async def exec_every(callback, period, args=[]):
    while True:
        await asyncio.sleep(period)
        await callback(*args)

def background_task(callback, period, args=[]):
    return asyncio.create_task(exec_every(callback, period, args))

