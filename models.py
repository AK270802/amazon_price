from extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    img_url = db.Column(db.String(500), nullable=True)
    target_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=True)
    met = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "name": self.name,
            "img_url": self.img_url,
            "target_price": self.target_price,
            "current_price": self.current_price,
            "met": self.met
        }
