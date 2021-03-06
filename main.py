#This Image Scraper finds 10 images from Google and gathers them into a folder.
#Reference used: https://towardsdatascience.com/image-scraping-with-python-a96feda8af2d
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

# Specify the Google Chrome Driver path below
PATH = "C:\\Users\\user\\Desktop\\Python\\Scraper\\chromedriver.exe"

wd = webdriver.Chrome(PATH)

#Function for getting the link
def get_imgs_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
    # Enter the Google Image Search URL below
    url = "https://www.google.com/search?q=top+rated+album+all+time+imagesize%3A1600x1600&tbm=isch&ved=2ahUKEwjt9M-BpZj0AhUO9aQKHWUmDH0Q2-cCegQIABAA&oq=top+rated+album+all+time+imagesize%3A1600x1600&gs_lcp=CgNpbWcQA1DPCVi-E2CqFGgAcAB4AIAB0QKIAYoIkgEHNy4yLjAuMZgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=XzuRYa3JFo7qkwXlzLDoBw&bih=827&biw=1613"
    wd.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if image.get_attribute("src") in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute("src") and "http" in image.get_attribute("src"):
                    image_urls.add(image.get_attribute("src"))
                    print(f"Found {len(image_urls)}")
    return image_urls

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print(f"Error - Could not Download Image {url} -", e)

urls = get_imgs_google(wd, 1, 10)

for i, url in enumerate(urls):
    download_image("images/", url, str(i) + ".jpg")

wd.quit()
