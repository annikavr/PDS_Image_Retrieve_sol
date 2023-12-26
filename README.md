# Mars2020 MastcamZ Image Downloader

## Project Overview

Automate the fetching of high-resolution, color-calibrated images from the Mars2020 rover's Mastcam-Z instrument. Utilizing the rich datasets available from NASA's Planetary Data System and the Arizona State University's MastcamZ galleries, this script streamlines the process of downloading curated images of the Martian surface, making it an invaluable resource for researchers, educators, and space enthusiasts alike.

This project leverages the CSV files provided by the [JPL Planetary Data System](https://planetarydata.jpl.nasa.gov/img/data/mars2020/mars2020_mastcamz_sci_calibrated/) to extract image IDs. These IDs are then used to locate and download the corresponding full-color images from the [ASU MastcamZ website](https://mastcamz.asu.edu/mars-images/images-videos/).

## Prerequisites

Before running the `get_imgs.py` script, users are required to:

1. Download the latest csv file containing the image metadata from the bottom of the [Mastcam-Z Calibrated Images Data](https://planetarydata.jpl.nasa.gov/img/data/mars2020/mars2020_mastcamz_sci_calibrated/browse/) page.
2. Place the downloaded file in the same directory as the `get_imgs.py` script.
3. Rename the file to `inventory.csv`

## Setup

To tailor the script to your needs, you must specify the Mastcam-Z image IDs of interest. At the top of the `get_imgs.py` script, locate and adjust the following section:

```python
######### ENTER DESIRED ZCAM IMAGE IDS HERE ###########
ids = ["zcam07114", "zcam07115"]  # Example format
```

Ensure that the image IDs are formatted correctly, following the `zcamxxxxx` pattern where `xxxxx` represents the numerical part of the image ID.

## Usage

Once the `inventory.csv` file is in place and the desired image IDs are specified, run the script with the following command:

```shell
python3 get_imgs.py
```

The script will then:

- Parse the CSV file to find the specified image IDs.
- Display a progress bar with the download status and counts of successful and failed downloads.
- Download the images to a newly created folder named according to the specified image IDs in the format `xxxxx_xxxxx_...`.

If any of the web pages do not contain a "Download PNG" button, the script will log this as 'not found' and proceed with the next image.

## Contributing

We welcome contributions to this project! Whether you're fixing bugs, improving the documentation, or proposing new features, your help is appreciated. Submit your pull requests or open an issue to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Enjoy exploring the Red Planet with the Mars2020 MastcamZ Image Downloader!
