from apscheduler.schedulers.background import BackgroundScheduler
from extensions import db
from models import Product
from mailer import send_email
from scraper import extract_price
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

scheduler = BackgroundScheduler()

def price_check_task(app):
    with app.app_context():
        products = Product.query.filter_by(met=False).all()
        if not products:
            return
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
        try:
            for p in products:
                try:
                    driver.get(p.url)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "productTitle")))
                    title = driver.find_element(By.ID, "productTitle").text.strip()

                    price = extract_price(driver)

                    try:
                        img_tag = driver.find_element(By.ID, "landingImage")
                        img_url = img_tag.get_attribute("src")
                    except Exception:
                        img_url = "https://m.media-amazon.com/images/I/71o8Q5XJS5L._AC_SY355_.jpg"

                    p.name = title
                    p.current_price = price
                    p.img_url = img_url

                    if price <= p.target_price and not p.met:
                        p.met = True
                        db.session.commit()
                        send_email(
                            to_email=p.email,
                            subject=f"Price Alert: {title[:40]}",
                            body=f"The price for {title} has dropped to {price}.\nProduct link: {p.url}"
                        )
                    else:
                        db.session.commit()
                except Exception as e:
                    app.logger.warning(f"Failed to update product id={p.id}: {e}")
        finally:
            driver.quit()

def start_scheduler(app):
    scheduler.add_job(
        func=price_check_task,
        args=[app],  # pass app as argument here
        trigger="interval",
        seconds=3600,
        id='price_check',
        replace_existing=True
    )
    scheduler.start()

