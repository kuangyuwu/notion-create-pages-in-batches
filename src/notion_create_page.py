import asyncio

import requests

from notion_api import NotionAPI
from notion_page import NotionPage

# Asynchronously create a batch of Notion pages
async def create_pages_batch(notion_api: NotionAPI, pages: list[NotionPage]) -> None:
    # Use asyncio.TaskGroup to manage asynchronous tasks
    async with asyncio.TaskGroup() as tg:
        # Iterate over each page and create a task to handle its creation
        for page in pages:
            tg.create_task(asyncio.to_thread(_create_page, notion_api, page))

# Create a single Notion page
def _create_page(notion_api: NotionAPI, page: NotionPage) -> None:
    print(f"Creating {page}...")
    # Send a POST request to the Notion API to create the page
    resp = requests.post(
        url="https://api.notion.com/v1/pages",
        headers=notion_api._headers("POST"),
        json=page.json(),
    )
    # Check the response status code to determine if the page was created successfully
    if resp.status_code == 200:
        print(f"Sucessfully created {page}!")
    else:
        # Print an error message if the page creation failed
        if "message" in resp.json():
            print(f"Failed to create {page}: {resp.status_code}: {resp.json()["message"]}")
        else:
            print(f"Failed to create {page}: {resp.status_code}")
    return