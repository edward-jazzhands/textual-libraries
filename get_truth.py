import requests
from requests import Response
import time
import re
from pathlib import Path

from rich.console import Console
console = Console()
starting_time = time.time()

url = 'https://github.com/Textualize/transcendent-textual/raw/refs/heads/main/README.md'


def convert_response_to_dicts(response: Response) -> tuple[dict, dict]:

    split1 = response.text.split("## Textualize libraries and tools")   # split at top section
    split2 = split1[1].split("## Applications built with Textual")      # disregard top section, split at bottom section
    split3 = split2[0].split("## Third-party libraries")                # disregard bottom section, split at middle

    # split3 contains our 2 sections of interest
    # split3[0] is official Textualize libraries and tools
    # split3[1] is third-party libraries

    textualize_libraries = split3[0].strip().split("\n")
    third_party_libraries = split3[1].strip().split("\n")

    def normalize_line(line: str, dict_to_update: dict) -> None:
        name = re.findall(r'\[(.*?)\]', line)
        name = name[0].replace(" ", "-").lower()
        url  = re.findall(r'\((.*?)\)', line)
        url = url[0]
        description = line.split(") - ")[1]
        dict_to_update[name] = [url, description]

    textualize_libraries_dict = {}
    for line in textualize_libraries:
        normalize_line(line, textualize_libraries_dict)

    third_party_libraries_dict = {}
    for line in third_party_libraries:
        normalize_line(line, third_party_libraries_dict)

    return textualize_libraries_dict, third_party_libraries_dict


def create_files(lib_dict: dict, official: bool) -> None:

    for key, value in lib_dict.items():
        file_path = Path(f"_posts/1970-01-01-{key}.md")
        if file_path.exists():
            console.print(f"File {file_path} already exists. [red]Skipping...")
            continue
        else:
            console.print(f"[green]Creating file[/green] {file_path}...")
            with open(f"_posts/1970-01-01-{key}.md", "w") as f:
                f.write(f"""---
layout: post
title: {key}
author: ?
website: {value[0]}
img: posts/?
tags: [{key}, TUI, Terminal, Textual, Libraries, Tools, CLI, Python, Rich, Textualize, Plugins]
description: {value[1]}
official: {official}
---

## GITHUB
[{{ page.website }}]({{ page.website }})
"""
)


textualize_libraries_dict = {}
third_party_libraries_dict = {}

try:
    response = requests.get(url)
except Exception as e:
    console.print(f"\nAn error occurred making the get request: {e}")
else:
    if response.status_code == 200:
        console.print("\nSuccessfully fetched the README.md file. Next stage... \n")
        textualize_libraries_dict, third_party_libraries_dict = convert_response_to_dicts(response)
        console.print(f"\nFinished successfully. Operation took {time.time() - starting_time} seconds. \n")
    else:
        console.print(f"\nGet request passed but returned wrong code. Status code: {response.status_code}")

if textualize_libraries_dict == {}:
    raise ValueError("No data found in the response.")
   
create_files(textualize_libraries_dict, True)
create_files(third_party_libraries_dict, False)


with open("libraries_list.md", "w") as f:
    f.write("""# Libraries list

This file is auto-generated from `get_truth.py`.
It is not used directly, but it shows the data that is fetched.
This list should match the files in the `_posts` directory.     

## Textualize libraries and tools
| Name | URL | Description |
| --- | --- | --- |
""")
    for key, value in textualize_libraries_dict.items():
        f.write(f"| {key} | {value[0]} | {value[1]} |\n")

    f.write("""
## Third-party libraries
| Name | URL | Description |
| --- | --- | --- |
""")
    for key, value in third_party_libraries_dict.items():
        f.write(f"| {key} | {value[0]} | {value[1]} |\n")