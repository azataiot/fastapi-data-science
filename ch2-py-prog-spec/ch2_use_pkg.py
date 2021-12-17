import datetime

import asyncio

print(datetime.date.today())


async def main():
    print('Hello ...')
    await asyncio.sleep(2)
    print('....world!')


async def printer(name: str, times: int) -> None:
    for i in range(times):
        print(name)
        await asyncio.sleep(1)


async def again():
    await asyncio.gather(
        printer('A', 3),
        printer('B', 10),
    )


asyncio.run(again())
