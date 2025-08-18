from get_imgs_sol import find_items_with_ids, download_images

######### ENTER DESIRED ZCAM IMAGE IDS HERE ###########
ids = ["zcam07114", "zcam07115"]

# Limit sols (example: up to sol 30)
max_sol = 30

# Ensure that there is at least one ID provided
if not ids or len(ids) == 0:
    raise ValueError("You must include at least one ID in the 'ids' list.")

found_ids = find_items_with_ids("./collection_browse_inventory.csv", ids, max_sol=max_sol)
if found_ids:
    download_images(found_ids, ids)
else:
    print("No images found for the specified IDs.")
