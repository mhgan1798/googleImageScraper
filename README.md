# Google image scraper

This script uses selenium to iterate through the image search results of a specific term and downloads the specified number of images sequentially. 

![scrapingProcessGif]()

## How to use
- If python is in your PATH, run the file in a terminal or command line using:
    ```
    python googleImageScraper.py
    ```

- Alternatively, you can run the file using the terminal built into VSCode, pyCharm, or any other IDE of your choice.

## Error Handling
The script uses error handling to ensure that there is sufficient time to download an image, where upon failure, the image would be skipped. This can be due to a slow internet connection or the image file simply being too big.

Every 25 iterations on the google image page, selenium runs into the "Related Searches" element. This element is removed before scraping because clicking on it would result in the desired image page being lost, as the browser navigates to a separate page.