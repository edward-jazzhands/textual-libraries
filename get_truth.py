import requests
from requests import Response
import time
import re
from pathlib import Path
import json
import yaml

from rich.console import Console
from rich import traceback
traceback.install(show_locals=True)
console = Console()
starting_time = time.time()

url = 'https://github.com/Textualize/transcendent-textual/raw/refs/heads/main/README.md'

class SpacedDumper(yaml.Dumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if self.indent == 0:  # Add a blank line between top-level entries
            super().write_line_break()


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


def normalize_lib_data(lib_dict: dict, official: bool) -> dict:

    new_libraries_dict = {}
    for key, value in lib_dict.items():
        new_libraries_dict[key] = {
            "author": "John Doe",
            "website": value[0],
            "img": f"libraries/{key}.png",
            "tags": [],
            "description": value[1],
            "official": official
        }
    return new_libraries_dict


def merge_with_existing_data(libraries_dict: dict) -> None:

    # json_file_path = Path("_data/libraries.json")
    yaml_file_path = Path("_data/libraries.yml")        

    added_count = 0
    if yaml_file_path.exists():
        with open(yaml_file_path, "r") as f:
            existing_data = yaml.load(f, Loader=yaml.FullLoader)
            for k, v in libraries_dict.items():
                if k in existing_data:
                    continue                  # skip libraries that are already in the file
                else:
                    existing_data.append(v)
                    added_count += 1
    else:
        existing_data = libraries_dict
        added_count = len(libraries_dict)
        console.print(f"File {yaml_file_path} does not exist. Creating new file...")

    with open(yaml_file_path, "w") as f:
        yaml.dump(existing_data, f, Dumper=SpacedDumper, indent=2)

    console.print(f"Added {added_count} libraries to the file {yaml_file_path}.")
    

def write_markdown_list(lib1: dict, lib2: dict) -> None:

    with open("libraries_list.md", "w") as f:
        f.write("""# Libraries list

This file is auto-generated from `get_truth.py`.
It is not used directly, but it shows the data that is fetched.
This list will match the contents of `_data/libraries.yml`.

## Textualize libraries and tools
                
| Name | URL | Description |
| --- | --- | --- |
""")
        for key, value in lib1.items():
            f.write(f"| {key} | {value[0]} | {value[1]} |\n")

        f.write("""
## Third-party libraries
                
| Name | URL | Description |
| --- | --- | --- |
""")
        for key, value in lib2.items():
            f.write(f"| {key} | {value[0]} | {value[1]} |\n")


###########################
# Main script starts here #
###########################

response = None
try:
    response = requests.get(url)
except Exception as e:
    raise Exception(f"Error while fetching the URL: {url}. Error: {e}")

if response.status_code == 200:
    console.print("\nSuccessfully fetched the README.md file. Next stage... \n")
    textualize_libraries_dict, third_party_libraries_dict = convert_response_to_dicts(response)
else:
    raise Exception(f"Get request passed but returned wrong code. Status code: {response.status_code}")

normalized_textualize_libraries = normalize_lib_data(textualize_libraries_dict, True)
normalized_third_party_libraries = normalize_lib_data(third_party_libraries_dict, False)

merged_dict = {**normalized_textualize_libraries, **normalized_third_party_libraries}
merge_with_existing_data(merged_dict)

write_markdown_list(textualize_libraries_dict, third_party_libraries_dict)

console.print(f"\nFinished successfully. Script took {time.time() - starting_time} seconds. \n")