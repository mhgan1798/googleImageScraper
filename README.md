# Google image scraper

This script uses selenium to iterate through the image search results of a specific term and downloads the specified number of images sequentially. 

![scrapingProcessGif](https://raw.githubusercontent.com/mhgan1798/googleImageScraper/master/gifs/2020-07-22%2019-21-59%204.gif)

## How to use
- If python is in your PATH, run the file in a terminal or command line using:
    ```
    python googleImageScraper.py
    ```

- Alternatively, you can run the file using the terminal built into VSCode, pyCharm, or any other IDE of your choice.

## Error Handling
The script tries to ensure that there is sufficient time to download an image. Upon failure to do so, the image would be skipped. These types of errors can arise due to a slow internet connection or when the image file is simply too big to download in time. The script can be modified accordingly by changing the sys.time() calls.

Every 25 iterations on the google image page, selenium runs into the "Related Searches" element. This element is removed before scraping because clicking on it would result in the desired image page being lost, as the browser navigates to a separate page.
