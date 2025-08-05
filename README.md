
# Amazon Price Reminder

A Flask web application that tracks Amazon product prices and sends email notifications when prices drop below a user-specified target price. It employs Selenium for scraping Amazon product details and APScheduler for background scheduled price checks.

---

## Setup Instructions

### Prerequisites

- Python 3.8 or later
- Google Chrome installed
- ChromeDriver matching your Chrome version (auto-managed by `webdriver_manager` in the code)
- An SMTP email account for sending notification emails (e.g., Gmail, Outlook)
- Git (optional, for cloning the repository)

### Installation Steps

1. **Clone the repository** (or download the project files):

```

git clone https://github.com/yourusername/amazon-price-reminder.git
cd amazon-price-reminder

```

2. **Create and activate a virtual environment:**

```


# Windows

python -m venv venv
venv\Scripts\activate

# macOS/Linux

python3 -m venv venv
source venv/bin/activate

```

3. **Install required Python packages:**

```

pip install -r requirements.txt

```

4. **Create a `.env` file** in the project root directory with your SMTP and database settings:

```

SMTP_SERVER=smtp.yourmail.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASS=your-email-password
DATABASE_URI=sqlite:///amazon_price_reminder.db

```

5. **Run the application:**

```

python app_1.py

```

6. **Access the app** in your browser at [http://localhost:5000](http://localhost:5000).

---

## API Documentation

### Base URL
```

http://localhost:5000

```

### Endpoints

#### 1. Add a Product to Track

- **URL:** `/product/add`
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Request Body:**

```

{
"url": "https://www.amazon.com/dp/example_product",
"target_price": 29.99,
"email": "user@example.com"
}

```

- **Responses:**

  - Success (`200 OK`):

```

{
"status": "success",
"id": 1,
"name": "Product Name"
}

```

- Error (`400 Bad Request`):

```

{
"status": "error",
"message": "url, target_price and email required"
}

```

- Scraping or server error (`400 Bad Request`):

```

{
"status": "error",
"message": "Scraping error: <error details>"
}

```

#### 2. Get Status of All Tracked Products

- **URL:** `/product/status`
- **Method:** `GET`
- **Response:**

```

[
{
"id": 1,
"url": "https://www.amazon.com/dp/example_product",
"name": "Product Name",
"img_url": "https://image.url/product.jpg",
"target_price": 29.99,
"current_price": 27.49,
"met": true
},
{
"id": 2,
"url": "https://www.amazon.com/dp/another_product",
"name": "Another Product",
"img_url": null,
"target_price": 15.00,
"current_price": 18.50,
"met": false
}
]

```

---

## Assumptions Made

- The user inputs a valid Amazon product URL with a reachable product page.
- The server running this app has access to ChromeDriver and Google Chrome for Selenium-based scraping.
- SMTP credentials are correct and allow sending emails through the specified server/port.
- Price scraping logic assumes Amazon’s page HTML structure and selectors remain relatively stable; changes in Amazon’s site could cause scraping failures.
- Background price checks run every hour via APScheduler and process products marked as “not met” (i.e., target price not reached).
- The app uses SQLite as the default database; for production, a more robust DB is recommended.

---

## Project Structure Overview

```

amazon_price_reminder/
├── app_1.py              \# App factory and server entry point
├── config.py             \# Configuration + environment variables
├── extensions.py         \# Flask extensions, e.g., SQLAlchemy db instance
├── models/
│   └── product.py        \# Product SQLAlchemy model
├── scraper/
│   └── amazon.py         \# Selenium scraping logic
├── scheduler.py          \# Background scheduler and price check tasks
├── mailer.py             \# Email sending utilities
├── routes.py             \# Flask route blueprint and handlers
├── templates/
│   └── index.html        \# Frontend HTML template
├── static/               \# Static assets (JS, CSS, images)
├── requirements.txt      \# Python dependencies
└── .env                  \# Environment variables (excluded from VCS)

```

## License

This project is licensed under the MIT License.
```
