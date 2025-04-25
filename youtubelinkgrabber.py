from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

def get_links(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "ytd-item-section-renderer.style-scope")
            )
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        anchors = soup.find_all('a', class_=["yt-simple-endpoint style-scope ytd-playlist-video-renderer"])

        with open("links.csv", "w", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Video Link'])

            for anchor in anchors:
                href = anchor.get('href')
                title = anchor.get('title') or anchor.get_text(strip=True)

                if href:
                    full_link = f"https://www.youtube.com{href}"
                    writer.writerow([full_link])


    except Exception as e:
        print(f"Error scraping the page: {e}")
        return []

    finally:
        driver.quit()

def main():
    link = input("Enter the YouTube playlist link: ")
    links = get_links(link)

if __name__ == "__main__":
    main()
