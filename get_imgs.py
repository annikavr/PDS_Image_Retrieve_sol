import csv
import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

######### ENTER DESIRED ZCAM IMAGE IDS HERE ###########
ids = ["zcam07114", "zcam07115"]

def find_items_with_ids(file_path, ids):
    found_ids = []

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if 'lma' not in row[1] or 'iof' in row[1]:
                continue
            if any(id_ in row[1] for id_ in ids):
                start_index = row[1].find("browse:") + len("browse:")
                end_index = row[1].find("::", start_index)
                extracted_portion = row[1][start_index:end_index]
                extracted_portion = extracted_portion.replace('lma', 'lmf')
                extracted_portion = extracted_portion.replace("_", "-")
                found_ids.append(extracted_portion)

    return found_ids

# Ensure that there is at least one ID provided
if not ids or len(ids) == 0:
    raise ValueError("You must include at least one ID in the 'ids' list.")

fol_name = "_".join(id_[4:] for id_ in ids)

def download_images(image_ids, base_url="https://mastcamz.asu.edu/galleries/", folder_name=fol_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    success_count = 0
    not_found_count = 0

    with tqdm(total=len(image_ids), desc="Downloading images", ncols=100, miniters=1) as progress_bar:
        for image_id in image_ids:
            page_url = f"{base_url}{image_id}"
            response = requests.get(page_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                download_button = soup.find('a', text='Download PNG')
                if download_button and 'href' in download_button.attrs:
                    image_url = download_button['href']
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        with open(os.path.join(folder_name, f"{image_id}.png"), 'wb') as file:
                            file.write(image_response.content)
                        success_count += 1
                    else:
                        not_found_count += 1
                else:
                    not_found_count += 1
            else:
                not_found_count += 1

            progress_bar.update(1)
            progress_bar.set_postfix(success=success_count, fail=not_found_count)

found_ids = find_items_with_ids("./inventory.csv", ids)
download_images(found_ids)