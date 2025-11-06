from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goldentiger.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import models to register them with SQLAlchemy
from models import Product, ProductVariant

# Add a simple route for testing
@app.route('/')
def home():
    return "Golden Tiger Shoes Backend is running!"

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)
