import csv
import os
import requests
from tqdm import tqdm

def parse_filename(filename):
    """Extract sol, time, product type, thumbnail flag, and sequence ID."""
    parts = filename.split("_")
    if len(parts) < 6:
        return None

    sol = parts[1]
    time = parts[2]
    product_type = parts[3][-3:]  # e.g., RAD
    thumb_flag = parts[4][0]      # N (non-thumbnail) or T (thumbnail)
    seq_id = [p for p in parts if p.startswith("ZCAM")]
    seq_id = seq_id[0] if seq_id else None

    return {
        "sol": sol,
        "time": time,
        "product_type": product_type,
        "thumb_flag": thumb_flag,
        "seq_id": seq_id,
        "filename": filename
    }

def find_items_with_ids(file_path, ids, max_sol=None):
    """Filter RAD+N images by sequence IDs (and optionally max_sol)."""
    found_items = []

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 2:
                continue

            filename = row[1].split("browse:")[-1].split("::")[0].upper()
            meta = parse_filename(filename)
            if not meta:
                continue

            # Only accept images that match the given IDs
            if not any(id_.upper() in filename for id_ in ids):
                continue

            # Apply filters
            if meta["product_type"] != "RAD":
                continue
            if meta["thumb_flag"] != "N":
                continue
            if not meta["seq_id"]:
                continue
            if max_sol and int(meta["sol"]) > max_sol:
                continue

            found_items.append(meta)

    print(f"\n****** Found {len(found_items)} RAD+N images with the given IDs ******\n")
    return found_items

def download_images(image_entries, in_ids, base_url="https://planetarydata.jpl.nasa.gov/img/data/mars2020/mars2020_mastcamz_ops_raw/browse/sol/"):
    """Download into /solXXXXX/sequence_id/ structure."""
    success_count, fail_count = 0, 0

    with tqdm(total=len(image_entries), desc="Downloading", unit="file", ncols=100) as pbar:
        for img in image_entries:
            sol_folder = f"sol{img['sol'].zfill(4)}"
            seq_folder = img["seq_id"]
            out_dir = os.path.join(sol_folder, seq_folder)
            os.makedirs(out_dir, exist_ok=True)

            image_url = f"{base_url}{img['sol'].zfill(5)}/ids/edr/zcam/{img['filename']}"
            image_path = os.path.join(out_dir, img["filename"])

            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(image_path, "wb") as f:
                    for chunk in response.iter_content(128):
                        f.write(chunk)
                success_count += 1
            else:
                fail_count += 1

            pbar.update(1)
            pbar.set_postfix_str(f"✓ {success_count} ✗ {fail_count}")

    print(f"\nDownload finished: {success_count} succeeded, {fail_count} failed.")
