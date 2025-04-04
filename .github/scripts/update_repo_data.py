import os
import yaml
import requests
import datetime

# Load GitHub token from environment
token = os.environ.get('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}'} if token else {}

# Load current libraries data
with open('_data/libraries.yml', 'r') as file:
    libraries:dict = yaml.safe_load(file)

# Update each library with latest data
for name, lib_data in libraries.items():
    url = lib_data.get('url', '')
    
    # Skip if not a GitHub repo
    if 'github.com' not in url:
        continue
        
    # Extract owner/repo
    path = url.replace('https://github.com/', '').strip('/')
    if not path:     # this would only happen if the URL is malformed
        continue
    api_url = f'https://api.github.com/repos/{path}'        

    try:
        response = requests.get(api_url, headers=headers)   # Fetch repo data
        response.raise_for_status()
    except Exception as e:
        raise SystemExit(f"Error fetching data for {name}: {e}")       

    print(f"Fetch successful for {name}: {response.status_code}. Proceeding...")
    try:
        repo_data = response.json()
    except ValueError:
        raise SystemExit(f"Error parsing JSON for {name}: {response.text}")
    
    if 'pushed_at' in repo_data:                            
        lib_data['pushed_at'] = repo_data['pushed_at']
    if 'stargazers_count' in repo_data:
        lib_data['stars'] = repo_data['stargazers_count']
    if 'owner' in repo_data:
        lib_data['author'] = repo_data['owner']['login']

print("Fetched all libraries successfully. Writing to file...")

class SpacedDumper(yaml.Dumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if self.indent == 0:  # Add a blank line between top-level entries
            super().write_line_break()

# Save updated data
try:
    with open('_data/libraries.yml', 'w') as file:
        yaml.dump(libraries, file, Dumper=SpacedDumper, indent=2)
except Exception as e:
    raise SystemExit(f"Error writing to file: {e}")
else:
    print("File written successfully.")
    print(f"Finished time: {datetime.datetime.now()} \n")