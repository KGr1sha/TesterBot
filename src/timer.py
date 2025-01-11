from threading import Timer
import asyncio

def call_async(function):
    asyncio.run(function)

def call(function, delay) -> Timer:
    t = Timer(delay, call_async, args=(function,))
    t.run()
    return t

async def async_function():
    await asyncio.sleep(1)
    print("done")

if __name__ == "__main__":
    call(async_function(), 3)

