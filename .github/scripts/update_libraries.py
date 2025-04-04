import requests
from requests import Response
import re
import os
from pathlib import Path
import yaml

# Load GitHub token from environment
token = os.environ.get('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}'} if token else {}

url = 'https://github.com/Textualize/transcendent-textual/raw/refs/heads/main/README.md'
yaml_file_path = Path("_data/libraries.yml")       

class SpacedDumper(yaml.Dumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if self.indent == 0:  # Add a blank line between top-level entries
            super().write_line_break()

def convert_response_to_dicts(response: Response) -> tuple[dict, dict]:

    split1 = response.text.split("## Textualize libraries and tools")   # split at top section
    split2 = split1[1].split("## Applications built with Textual")      # disregard top section, split at bottom section
    split3 = split2[0].split("## Third-party libraries")                # disregard bottom section, split at middle

    # split3 contains our 2 sections of interest:
        # split3[0] is official Textualize libraries and tools
        # split3[1] is third-party libraries

    textualize_libraries = split3[0].strip().split("\n")
    third_party_libraries = split3[1].strip().split("\n")

    def normalize_line(line: str, dict_to_update: dict, official: bool) -> None:
        name = re.findall(r'\[(.*?)\]', line)[0]
        name = name.replace(" ", "-").lower()
        url  = re.findall(r'\((.*?)\)', line)[0]
        description = line.split(") - ")[1]
        # dict_to_update[name] = [url, description]
        dict_to_update[name] = {
            "url": url,
            "img": f"libraries/{name}.png",
            "description": description,
            "official": official
        }

    textualize_libraries_dict = {}
    for line in textualize_libraries:
        normalize_line(line, textualize_libraries_dict, True)

    third_party_libraries_dict = {}
    for line in third_party_libraries:
        normalize_line(line, third_party_libraries_dict, False)

    return textualize_libraries_dict, third_party_libraries_dict

###########################
# Main script starts here #
###########################

try:
    response = requests.get(url, headers=headers)
except Exception as e:
    raise Exception(f"Error while fetching the URL: {url}. Error: {e}")

if response.status_code == 200:
    print("\nSuccessfully fetched the README.md file. Next stage... \n")
    textualize_libraries_dict, third_party_libraries_dict = convert_response_to_dicts(response)
else:
    raise Exception(f"Get request passed but returned wrong code. Status code: {response.status_code}")

merged_dict = {**textualize_libraries_dict, **third_party_libraries_dict}

try:
    with open(yaml_file_path, "w") as f:
        yaml.dump(merged_dict, f, Dumper=SpacedDumper, indent=2)
except Exception as e:
    raise Exception(f"Error while writing to yaml file: {e}")
else:
    print(f"Successfully wrote to {yaml_file_path} \n")
    print("Done update_libraries.py. \n")