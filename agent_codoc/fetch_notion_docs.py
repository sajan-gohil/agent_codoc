import requests
import json
import os

NOTION_API_URL = "https://api.notion.com/v1/"
NOTION_API_KEY = "your_notion_api_key"
NOTION_PAGE_ID = "your_notion_page_id"
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2021-08-16",
    "Content-Type": "application/json"
}

def fetch_notion_page(page_id):
    url = f"{NOTION_API_URL}blocks/{page_id}/children"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def block_to_markdown(block):
    block_type = block['type']
    if block_type == 'paragraph':
        return block['paragraph']['text'][0]['plain_text']
    elif block_type == 'heading_1':
        return f"# {block['heading_1']['text'][0]['plain_text']}"
    elif block_type == 'heading_2':
        return f"## {block['heading_2']['text'][0]['plain_text']}"
    elif block_type == 'heading_3':
        return f"### {block['heading_3']['text'][0]['plain_text']}"
    elif block_type == 'bulleted_list_item':
        return f"- {block['bulleted_list_item']['text'][0]['plain_text']}"
    elif block_type == 'numbered_list_item':
        return f"1. {block['numbered_list_item']['text'][0]['plain_text']}"
    else:
        return f"Unsupported block type: {block_type}"

def notion_to_markdown(page_id):
    page_data = fetch_notion_page(page_id)
    blocks = page_data['results']
    markdown_blocks = [block_to_markdown(block) for block in blocks]
    return "\n\n".join(markdown_blocks)

if __name__ == "__main__":
    markdown_content = notion_to_markdown(NOTION_PAGE_ID)
    with open("notion_page.md", "w") as file:
        file.write(markdown_content)
