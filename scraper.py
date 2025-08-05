import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_price(driver):
    price = None
    try:
        price_container = None
        try:
            price_container = driver.find_element(By.ID, "corePriceDisplay_desktop_feature_div")
        except Exception:
            pass

        if price_container:
            whole_el = price_container.find_elements(By.CSS_SELECTOR, ".a-price-whole")
            fraction_el = price_container.find_elements(By.CSS_SELECTOR, ".a-price-fraction")
            whole = whole_el[0].text.replace(',', '') if whole_el else ''
            fraction = fraction_el[0].text if fraction_el else '00'
            if whole:
                price_str = whole + '.' + fraction
                price = float(price_str)
                return price

        fallback_selectors = [
            "priceblock_ourprice",
            "priceblock_dealprice",
            "priceblock_saleprice",
            "price_inside_buybox",
            "tp_price_block_total_price_ww",
            ".a-price .a-offscreen",
            ".priceToPay .a-offscreen",
        ]

        for sel in fallback_selectors:
            try:
                if sel.startswith("."):
                    elem = driver.find_element(By.CSS_SELECTOR, sel)
                else:
                    elem = driver.find_element(By.ID, sel)
                text = elem.text.strip()
                cleaned = text.replace(",", "").replace("$", "").replace("₹", "").strip()
                m = re.search(r"\d+(\.\d+)?", cleaned)
                if m:
                    return float(m.group())
            except Exception:
                continue
    except Exception:
        pass

    return 0.0


def scrape_amazon(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    )
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    title = "Unknown Product Title"
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "productTitle"))
        )
        title = driver.find_element(By.ID, "productTitle").text.strip()
    except Exception:
        pass

    price = extract_price(driver)

    try:
        img_tag = driver.find_element(By.ID, "landingImage")
        img_url = img_tag.get_attribute("src")
    except Exception:
        img_url = "https://m.media-amazon.com/images/I/71o8Q5XJS5L._AC_SY355_.jpg"

    driver.quit()
    return title, price, img_url
