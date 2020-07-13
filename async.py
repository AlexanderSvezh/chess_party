import random
import asyncio
from selenium import webdriver


async def get_browser(time_to_sleep):
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get(f'http://google.com/{time_to_sleep}')
    await asyncio.sleep(time_to_sleep)
    driver.quit()


async def waiter(name):
    for _ in range(4):
        time_to_sleep = random.randint(2, 10)
        await get_browser(time_to_sleep)
        print("{} waited {} seconds""".format(name, time_to_sleep))


async def main():
    await asyncio.wait([waiter("foo"),
                        waiter("bar"),
                        waiter('three')])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
