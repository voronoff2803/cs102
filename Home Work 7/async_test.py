import asyncio
import requests


async def get_page(url):
    response = requests.get(url)
    return response