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
            logger.error("Database initialization failed: %s", str(e))
            db.session.rollback()
            raise
