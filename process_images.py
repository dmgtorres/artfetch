#!/usr/bin/env python3
import sys
import subprocess
import urllib.request
import urllib.parse
import urllib.error
import json
import time
import argparse
from pathlib import Path

def get_wikimedia_url(filename, retries=3):
    encoded = urllib.parse.quote(filename)
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles=File:{encoded}&prop=imageinfo&iiprop=url&iiurlwidth=500&format=json"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0', 'Accept': 'application/json'}
    req = urllib.request.Request(url, headers=headers)

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read())
                pages = data['query']['pages']
            page = list(pages.values())[0]
            if 'imageinfo' in page:
                return page['imageinfo'][0].get('thumburl')
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_time = 5 * (attempt + 1)
                print(f"    [API Rate Limited] Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print(f"    Wikimedia API HTTP Error: {e.code}")
                break
        except Exception as e:
            print(f"    Wikimedia API Error for {filename}: {e}")
            break
    return None

def main():
    parser = argparse.ArgumentParser(description="Process images to ANSI art based on a JSON configuration file.")
    parser.add_argument("config", help="Path to the JSON configuration file")
    args = parser.parse_args()

    if not Path("/usr/bin/chafa").exists() and subprocess.call("command -v chafa", shell=True, stdout=subprocess.DEVNULL) != 0:
        print("Error: 'chafa' is required.")
        sys.exit(1)

    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Failed to load configuration file: {e}")
        sys.exit(1)

    category = config.get("category", "misc")
    category_name = config.get("category_name", "Miscellaneous")
    collection = config.get("collection", "default")
    collection_name = config.get("collection_name", "Default")
    prefix = config.get("prefix", "")

    resolution = config.get("resolution", "30x30")
    chafa_args_str = config.get("rendering_options", "--symbols=block")
    chafa_args = chafa_args_str.split()

    items = config.get("items", [])

    base_dir = Path.home() / ".artfetch"
    target_dir = base_dir / category / collection
    target_dir.mkdir(parents=True, exist_ok=True)
    collection_title = f"{category_name} > {collection_name}"

    print(f"Generating collection \"{collection_title}\" in {target_dir} using {resolution} size and styling '{chafa_args}'...")
    temp_png = base_dir / f"tmp_{collection}.png"

    for item in items:
        item_id = item.get("id")
        item_name = item.get("name")
        item_source_type = item.get("source_type")
        item_source_path = item.get("source_path")
        ansi_file = target_dir / f"{prefix}_{item_id.lower()}.ansi"
        
        item_title = f"{item_name} ({item_id})"

        if ansi_file.exists() and ansi_file.stat().st_size > 0:
            print(f"  Image already exists for \"{item_title}\". Skipping.")
            continue
            
        print(f"  Processing \"{item_title}\"...")

        url = None
        if item_source_type == "wikimedia":
            url = get_wikimedia_url(item_source_path)
        elif item_source_type == "direct_url":
            url = item_source_path
        else:
            print(f"    Unknown source type: '{item_source_type}'")
            continue

        if url:
            for attempt in range(3):
                try:
                    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}
                    req = urllib.request.Request(url, headers=headers)
                    
                    with urllib.request.urlopen(req, timeout=15) as response:
                        temp_png.write_bytes(response.read())

                    cmd = ['chafa', f'--size={resolution}', '--format=symbols'] + chafa_args + [str(temp_png)]
                    result = subprocess.run(cmd, capture_output=True, text=True)

                    if result.returncode == 0:
                        metadata_header = f"{collection_title}: {item_title})\n"
                        ansi_file.write_text(metadata_header + result.stdout)
                        break
                    else:
                        print(f"    Chafa error: {result.stderr}")
                        break
                except urllib.error.HTTPError as e:
                    if e.code == 429:
                        wait_time = 5 * (attempt + 1)
                        print(f"    [Image Rate Limited] Waiting {wait_time} s...")
                        time.sleep(wait_time)
                    else:
                        print(f"    HTTP Error: {e.code}")
                        break
                except Exception as e:
                    print(f"    Download/Conversion failed: {e}")
                    break
            
            time.sleep(1.5)
        else:
            print(f"    Failed to retrieve valid image URL.")

    if temp_png.exists():
        temp_png.unlink()

    print(f"\nCollection \"{collection_title}\" updated successfully.")

if __name__ == "__main__":
    main()
