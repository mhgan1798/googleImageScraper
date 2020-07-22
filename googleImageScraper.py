# %% Set up the script
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import requests
import shutil
import os
import numpy as np


#### PLEASE NOTE THAT YOU WILL NEED TO SET UP AND INSTALL CHROMEDRIVER AS WELL AS SELENIUM FOR THE SCRIPT TO FUNCTION AS INTENDED. MORE INFORMATION CAN BE FOUND IN THE FOLLOWING URLS:
#### https://chromedriver.chromium.org/getting-started
#### https://chromedriver.chromium.org/home


# %% Get user input for the script
numberImages = int(input("How many images would you like to save? "))

inp = input("What images would you like to search for? ").replace(" ", "+")

folderName = input("What do you want to call the results folder? ")
directory = os.path.dirname(os.path.abspath(__file__)) + "/" + folderName

# Try to make the directory, else proceed
try:
    os.mkdir(directory)
    print("Results folder has been created in the same folder as the script directory!")
    time.sleep(0.5)
except FileExistsError:
    print("Folder already exists! Starting up the scraper now...")
    time.sleep(0.5)


# %% Functions
def removeElement(xpath):
    element = driver.find_element_by_xpath(xpath)
    driver.execute_script(
        """
    var element = arguments[0];
    element.parentNode.removeChild(element);
    """,
        element,
    )


def save_img(inp, img, i, directory):
    try:
        filename = inp.replace("+", "_") + str(i) + ".jpg"
        response = requests.get(img, stream=True)
        image_path = os.path.join(directory, filename)
        with open(image_path, "wb") as file:
            shutil.copyfileobj(response.raw, file)
        print("Image '" + str(filename) + "' has been saved to " + directory)
        print("")
        return 1

    except WebDriverException:
        pass


def find_urls(inp, url, driver, numberImages, directory):
    iterate = numberImages + numberImages // 25
    iterateRange = np.arange(1, iterate + 1)
    iterateRange = iterateRange[iterateRange % 25 != 0]

    driver.get(url)

    # Click on the "images" tab
    images_button_url = driver.find_element_by_xpath(
        "/html/body/div[5]/div[2]/div[3]/div/div/div[1]/div/div/div[1]/div/div[2]/a"
    )
    driver.execute_script("arguments[0].click();", images_button_url)

    time.sleep(0.5)

    # Loop through the range of images specified and save
    for j in iterateRange:
        # global imgurl
        imgurl = driver.find_element_by_xpath(
            "//div//div//div//div//div//div//div//div//div//div["
            + str(j)
            + "]//a[1]//div[1]//img[1]"
        )
        driver.execute_script("arguments[0].click();", imgurl)

        time.sleep(0.8)

        # Save data with error handling
        result = None
        attempts = 0
        while result is None:
            try:
                # Get the html element by the xpath (obtained via inspect element) then get the image/src attribute from it
                img = driver.find_element_by_xpath(
                    "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img"
                ).get_attribute("src")
                # Save the result in the directory
                result = save_img(inp, img, j, directory)
            except requests.exceptions.InvalidSchema:
                attempts += 1
                print(
                    "Image has not loaded yet! Giving some time for the image to load... Attempt: "
                    + str(attempts)
                )
                time.sleep(0.4)

                if attempts >= 10:
                    print(
                        "Failed to download an image after 10 waiting attempts. Skipping..."
                    )
                    break


# %% Run the scrape and saving process for good art
if "driver" in globals():
    del driver

# Initiate a driver
print("Opening up the chrome driver now.")
time.sleep(0.2)
driver = webdriver.Chrome(r"C:\Program Files\chromeDriver\chromedriver.exe")

# Generate url from search terms
url = "https://www.google.com/search?q=" + inp

# Find urls and save
find_urls(inp, url, driver, numberImages, directory)

# quit current session
if "driver" in globals():
    driver.quit()
