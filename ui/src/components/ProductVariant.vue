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
            return float('inf')  # No sales = no stockout
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
