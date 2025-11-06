from datetime import datetime
import json
import logging
from typing import Dict, List
from app import db  # Import db from app.py

logger = logging.getLogger(__name__)

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    features = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_featured = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=4.5)
    review_count = db.Column(db.Integer, default=0)

    def apply_discount(self, discount_percent: float) -> float:
        """Apply a discount to the product price."""
        return round(self.price * (1 - discount_percent / 100), 2)

    def calculate_bulk_price(self, quantity: int) -> float:
        """Calculate bulk price based on quantity."""
        if quantity >= 10:
            return round(self.price * quantity * 0.85, 2)
        elif quantity >= 5:
            return round(self.price * quantity * 0.9, 2)
        else:
            return round(self.price * quantity, 2)

    def to_dict(self) -> Dict:
        """Convert the product to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'description': self.description,
            'features': json.loads(self.features) if self.features else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_featured': self.is_featured,
            'rating': self.rating,
            'review_count': self.review_count,
            'discount_price': self.apply_discount(10) if self.is_featured else None,
            'bulk_price_5': self.calculate_bulk_price(5),
            'bulk_price_10': self.calculate_bulk_price(10),
        }

class ProductVariant(db.Model):
    __tablename__ = 'product_variants'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(10), nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_paths = db.Column(db.Text)
    sku = db.Column(db.String(50), unique=True)

    product = db.relationship('Product', backref=db.backref('variants', lazy=True))

    def is_low_stock(self, threshold: int = 5) -> bool:
        """Check if stock is below a threshold."""
        return self.stock < threshold

    def days_until_stockout(self, daily_sales: float) -> float:
        """Estimate days until stock runs out."""
        if daily_sales <= 0:
            return float('inf')
        return round(self.stock / daily_sales, 2)

    def to_dict(self) -> Dict:
        """Convert the variant to a dictionary."""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'color': self.color,
            'size': self.size,
            'stock': self.stock,
            'image_paths': json.loads(self.image_paths) if self.image_paths else [],
            'sku': self.sku,
            'availability': 'In Stock' if self.stock > 0 else 'Out of Stock',
            'is_low_stock': self.is_low_stock(),
            'estimated_stockout_days': self.days_until_stockout(daily_sales=2),
        }

def init_db(app):
    """Initialize the database with sample data."""
    with app.app_context():
        try:
            logger.info("Dropping existing tables...")
            db.drop_all()

            logger.info("Creating new tables...")
            db.create_all()

            logger.info("Seeding database with sample products...")
            products = [
                Product(
                    name="PHOENIX ASCENDANT PRO",
                    category="basketball",
                    price=229.99,
                    description="Limited edition celestial basketball shoes with gold thread embroidery and advanced cushioning technology.",
                    features=json.dumps([
                        "Phoenix Feather Cushioning Pro",
                        "24K Gold Thread Embroidery",
                        "Cloud-Step Max Cushioning",
                        "Carbon Fiber Stability Plate",
                        "Anti-Gravity Traction System"
                    ]),
                    is_featured=True,
                    rating=4.8,
                    review_count=127
                ),
                Product(
                    name="DRAGON EMPEROR ELITE",
                    category="lifestyle",
                    price=199.99,
                    description="Imperial craftsmanship meets modern luxury with genuine leather and dragon scale texture.",
                    features=json.dumps([
                        "Genuine Italian Leather",
                        "Dragon Scale 3D Texture",
                        "Royal Silk Lining",
                        "Imperial Gold Accents",
                        "Comfort-Fit Memory Foam"
                    ]),
                    is_featured=True,
                    rating=4.7,
                    review_count=89
                ),
                Product(
                    name="TIGER SPIRIT ULTRA",
                    category="running",
                    price=189.99,
                    description="High-performance running shoes with tiger stripe dynamics and spirit animal cushioning.",
                    features=json.dumps([
                        "Tiger Stripe Dynamic Traction",
                        "Spirit Animal Cushioning",
                        "Warrior Agility Flex System",
                        "Breathable Mesh Upper",
                        "Energy Return Midsole"
                    ]),
                    rating=4.6,
                    review_count=156
                )
            ]
            db.session.bulk_save_objects(products)
            db.session.commit()

            logger.info("Seeding database with product variants...")
            variants = []
            color_map = {
                "PHOENIX ASCENDANT PRO": [
                    {"color": "gold", "sizes": ["US 8", "US 9", "US 10", "US 11", "US 12", "US 13"]},
                    {"color": "black", "sizes": ["US 7", "US 8", "US 9", "US 10", "US 11"]},
                    {"color": "red", "sizes": ["US 8", "US 9", "US 10", "US 11", "US 12"]}
                ],
                "DRAGON EMPEROR ELITE": [
                    {"color": "emerald", "sizes": ["US 7", "US 8", "US 9", "US 10", "US 11"]},
                    {"color": "midnight", "sizes": ["US 8", "US 9", "US 10", "US 11", "US 12"]},
                    {"color": "royal", "sizes": ["US 7", "US 8", "US 9", "US 10"]}
                ],
                "TIGER SPIRIT ULTRA": [
                    {"color": "sunset", "sizes": ["US 8", "US 9", "US 10", "US 11", "US 12"]},
                    {"color": "arctic", "sizes": ["US 7", "US 8", "US 9", "US 10", "US 11"]},
                    {"color": "ocean", "sizes": ["US 8", "US 9", "US 10", "US 11"]}
                ]
            }

            sku_counter = 1000
            for product in Product.query.all():
                for color_info in color_map[product.name]:
                    color = color_info["color"]
                    for size in color_info["sizes"]:
                        image_paths = [
                            f"/src/assets/shoes/{product.name.lower().replace(' ', '_')}/{color}/img{str(i).zfill(2)}.jpg"
                            for i in range(1, 7)
                        ]
                        variants.append(ProductVariant(
                            product_id=product.id,
                            color=color,
                            size=size,
                            stock=25,
                            image_paths=json.dumps(image_paths),
                            sku=f"GT{sku_counter}"
                        ))
                        sku_counter += 1
            db.session.bulk_save_objects(variants)
            db.session.commit()

            logger.info("Database initialization completed successfully.")
            logger.info(f"Created {len(products)} products and {len(variants)} variants.")

        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            db.session.rollback()
            raise
