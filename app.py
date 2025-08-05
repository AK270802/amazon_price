from flask import Flask
from extensions import db
from config import Config
from routes import product_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(product_blueprint)

    with app.app_context():
        db.create_all()
        from scheduler import start_scheduler
        start_scheduler(app)  # <----- pass the actual app

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
