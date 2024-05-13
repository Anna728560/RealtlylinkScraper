import time
from dataclasses import dataclass, fields

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


@dataclass
class Item:
    link_to_ad: str
    # title: str
    # region: str
    # address: str
    # description: str
    # img_array: list
    # date: str
    # price: float
    # count_room: int
    # size: float


ITEM_FIELDS = [field.name for field in fields(Item)]


class WebScraperService:
    BASE_URL = "https://realtylink.org/en/properties~for-rent?uc=0"

    def __init__(self) -> None:
        self.options = Options()
        self.driver = webdriver.Chrome(options=self._add_options())

    def _add_options(self) -> Options:
        # self.options.add_argument("--headless")
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        )

        return self.options

    def get_all_items(self):
        self.driver.get(self.BASE_URL)
        time.sleep(2)

        links = []

        while True:
            item_elements = self.driver.find_elements(By.CLASS_NAME, "property-thumbnail-item")
            for item_element in item_elements:
                link_to_ad = item_element.find_element(By.TAG_NAME, "a").get_attribute("href")
                links.append(link_to_ad)
                if len(links) == 30:
                    return links

            self.click_next_page()

    def click_next_page(self):
        pager = self.driver.find_element(By.CLASS_NAME, "pager")
        next_page_element = pager.find_element(By.CLASS_NAME, "next")
        if "inactive" not in next_page_element.get_attribute("class"):
            time.sleep(1)
            next_page_element.click()
            time.sleep(1)


def get_all_items():
    scraper = WebScraperService()
    links = scraper.get_all_items()
    print(links)
    print(len(links))


if __name__ == "__main__":
    get_all_items()
