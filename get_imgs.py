import csv
import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def find_items_with_ids(file_path, ids):
    found_ids = []

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            # enforce colored image
            if 'eby' not in row[1]:
                continue
            if any(id_ in row[1] for id_ in ids):
                start_index = row[1].find("browse:") + len("browse:")
                end_index = row[1].find("::", start_index)
                end_num = '0' + str(row[1][end_index + len('::'):])[0]
                extracted_portion = row[1][start_index:end_index]
                extracted_portion = extracted_portion.upper()[:-4] + end_num + '.png'
                found_ids.append(extracted_portion)

    print(f'\n****** Found {len(found_ids)} images with the corresponding ids ******\n')
    return found_ids

def download_images(image_entries, in_ids, base_url="https://planetarydata.jpl.nasa.gov/img/data/mars2020/mars2020_mastcamz_ops_raw/browse/sol/"):
    fol_name = "_".join(id_[4:] for id_ in in_ids)
    if not os.path.exists(fol_name):
        os.makedirs(fol_name)

    success_count = 0
    fail_count = 0

    # Initialize tqdm progress bar
    with tqdm(total=len(image_entries), desc="Downloading images", unit="file", ncols = 100) as pbar:
        for entry in image_entries:
            # Extract the "sol" number, which is the number after the first underscore and before the second
            parts = entry.split('_')
            sol = '0' + parts[1]  # Append leading zero

            # Construct the URL
            image_url = f"{base_url}{sol}/ids/edr/zcam/{entry}"

            # Download the image
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                image_path = os.path.join(fol_name, f"{entry}")
                with open(image_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=128):
                        file.write(chunk)
                success_count += 1
            else:
                fail_count += 1

            # Update tqdm progress bar
            pbar.update(1)
            pbar.set_postfix_str(f"Successes: {success_count}, Fails: {fail_count}")