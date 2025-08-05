from flask import Blueprint, request, jsonify, render_template
from extensions import db
from models import Product
from scraper import scrape_amazon
from mailer import send_email  # adjust import path if mailer in a package

product_blueprint = Blueprint('product', __name__)

@product_blueprint.route('/')
def index():
    return render_template('index.html')  # move your HTML_TEMPLATE to templates/index.html

@product_blueprint.route('/product/add', methods=['POST'])
def add_product():
    data = request.json or {}
    url = data.get('url')
    target_price = data.get('target_price')
    email = data.get('email')

    if not url or target_price is None or not email:
        return jsonify({"status": "error", "message": "url, target_price and email required"}), 400

    try:
        title, price, img_url = scrape_amazon(url)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Scraping error: {e}"}), 400

    product = Product.query.filter_by(url=url, target_price=target_price, met=False).first()
    if product:
        product.current_price = price
        product.name = title
        product.img_url = img_url
        product.email = email
    else:
        product = Product(
            url=url.strip(),
            name=title,
            img_url=img_url,
            target_price=float(target_price),
            current_price=price,
            met=False,
            email=email
        )
        db.session.add(product)

    db.session.commit()

    send_email(
        to_email=email,
        subject=f"Tracking started for {title[:40]}",
        body=f"You have successfully started tracking the product: {title}\nTarget price: ${target_price}\nYou will be notified when price drops."
    )

    return jsonify({"status": "success", "id": product.id, "name": product.name})

@product_blueprint.route('/product/status')
def product_status():
    products = Product.query.order_by(Product.id).all()
    return jsonify([p.to_dict() for p in products])
