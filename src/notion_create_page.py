import asyncio

import requests

from notion_api import NotionAPI
from notion_page import NotionPage

async def create_pages_batch(notion_api: NotionAPI, pages: list[NotionPage]) -> None:
    async with asyncio.TaskGroup() as tg:
        for page in pages:
            tg.create_task(asyncio.to_thread(create_page, notion_api, page))

def create_page(notion_api: NotionAPI, page: NotionPage) -> None:
    print(f"Creating {page}...")
    resp = requests.post(
        url="https://api.notion.com/v1/pages",
        headers=notion_api.headers("POST"),
        json=page.json(),
    )
    if resp.status_code == 200:
        print(f"Sucessfully created {page}!")
    else:
        if "message" in resp.json():
            print(f"Failed to create {page}: {resp.status_code}: {resp.json()["message"]}")
        else:
            print(f"Failed to create {page}: {resp.status_code}")
    return