from get_imgs import find_items_with_ids, download_images

######### ENTER DESIRED ZCAM IMAGE IDS HERE ###########
ids = ["zcam07114", "zcam07115"]

# Ensure that there is at least one ID provided
if not ids or len(ids) == 0:
    raise ValueError("You must include at least one ID in the 'ids' list.")

found_ids = find_items_with_ids("./collection_browse_inventory.csv", ids)
if found_ids:
    download_images(found_ids, ids)
else:
    print("No images found for the specified IDs.")

from get_imgs import find_items_with_ids, download_images
import re

# ######### ENTER ZCAM IMAGE IDS OR PATTERNS HERE ###########
# # You can mix exact matches and patterns
# ids = ["zcam07114", "zcam07115", "zcam08***"]  # Supports both exact IDs and wildcard

# # Validate input
# if not ids or len(ids) == 0:
#     raise ValueError("You must include at least one ID or pattern in the 'ids' list.")

# # Convert wildcards like zcam08*** to regex patterns
# regex_patterns = []
# for id_ in ids:
#     if '*' in id_:
#         # Convert wildcard pattern to regex
#         regex = id_.replace('*', r'\d')  # Replace * with digit match
#         regex_patterns.append(rf'{regex}')
#     else:
#         # Escape exact match as regex
#         regex_patterns.append(rf'{id_}')

# # Find images
# found_ids = find_items_with_ids("./collection_browse_inventory.csv", regex_patterns)

# # Download if found
# if found_ids:
#     download_images(found_ids, regex_patterns)
# else:
#     print("No images found for the specified IDs or patterns.")

#to find intersection between certain sols and ids, create set probably of the images across values and then see intersection (not sure if you can apply function to both)
