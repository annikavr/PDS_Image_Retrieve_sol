from get_imgs_sol import find_items_with_ids, download_images

######### ENTER DESIRED ZCAM IMAGE IDS HERE ###########
ids = ["zcam07114", "zcam07115"]  # example IDs

# Limit sols for testing
max_sol = 30

# Ensure that there is at least one ID provided
if not ids or len(ids) == 0:
    raise ValueError("You must include at least one ID in the 'ids' list.")

# Find all matching images up to max_sol
found_items = find_items_with_ids("./collection_browse_inventory.csv", ids, max_sol=max_sol)

# Download the images into /solXXXX/sequence_id/ structure
if found_items:
    download_images(found_items, ids)
else:
    print("No images found for the specified IDs.")
