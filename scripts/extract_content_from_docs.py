#!/usr/bin/env python3
"""
Script to extract content from Docusaurus markdown files and prepare for embedding.
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any


def extract_content_from_mdx_file(file_path: str) -> Dict[str, Any]:
    """
    Extract content from an MDX file, removing frontmatter and component tags.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove frontmatter (content between ---)
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # Remove component tags like <InteractiveLesson> and </InteractiveLesson>
    content = re.sub(r'<InteractiveLesson.*?>', '', content)
    content = re.sub(r'</InteractiveLesson>', '', content)

    # Remove import statements
    content = re.sub(r'^import.*?\n', '', content, flags=re.MULTILINE)

    # Get the title from the first H1 header
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else os.path.basename(file_path)

    # Clean up extra whitespace
    content = re.sub(r'\n\s*\n', '\n\n', content).strip()

    # Create URL based on file path
    relative_path = os.path.relpath(file_path, './docs')
    url = f"https://zoyaafzal.github.io/humanoid_robotic_book/docs/{relative_path.replace(os.sep, '/').replace('.mdx', '').replace('.md', '')}"

    return {
        "url": url,
        "title": title,
        "content": content,
        "headings": extract_headings(content),
        "chunk_index": 0,
        "source_document": relative_path
    }


def extract_headings(content: str) -> List[str]:
    """
    Extract headings from markdown content.
    """
    headings = []
    # Match markdown headings (##, ###, etc.)
    heading_pattern = r'^(#{2,6})\s+(.+)$'
    for line in content.split('\n'):
        match = re.match(heading_pattern, line.strip())
        if match:
            headings.append(match.group(2).strip())
    return headings


def scan_docs_directory(docs_dir: str) -> List[Dict[str, Any]]:
    """
    Scan the docs directory and extract content from all MD and MDX files.
    """
    content_list = []

    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(('.md', '.mdx')):
                file_path = os.path.join(root, file)
                try:
                    content_data = extract_content_from_mdx_file(file_path)
                    content_list.append(content_data)
                    print(f"Processed: {content_data['title'][:50]}... from {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")

    return content_list


def main():
    docs_dir = "./docs"

    print("Scanning documentation directory...")
    content_list = scan_docs_directory(docs_dir)

    print(f"Extracted content from {len(content_list)} files")

    # Save to JSON file
    output_file = "extracted_content.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(content_list, f, indent=2, ensure_ascii=False)

    print(f"Content extracted and saved to {output_file}")

    # Print a summary
    print("\nContent Summary:")
    for i, item in enumerate(content_list[:10]):  # Show first 10 items
        print(f"{i+1}. {item['title']} - {len(item['content'])} chars - {item['url']}")

    if len(content_list) > 10:
        print(f"... and {len(content_list) - 10} more items")


if __name__ == "__main__":
    main()