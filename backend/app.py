from flask import Flask
from extensions import db
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goldentiger.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with app
db.init_app(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import models AFTER db is initialized
with app.app_context():
    from models import Product, ProductVariant
    db.create_all()  # Create tables

# Add a simple route for testing
@app.route('/')
def home():
    return "Golden Tiger Shoes Backend is running!"

@app.route('/api/products')
def get_products():
    products = Product.query.all()
    return {'products': [p.to_dict() for p in products]}

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)
