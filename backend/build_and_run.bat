from typing import List

def calculate_revenue(variants: List, quantity_sold: int) -> float:
    """Calculate total revenue from a list of variants."""
    return sum(variant.price * quantity_sold for variant in variants)

def calculate_profit(variants: List, quantity_sold: int, cost_per_unit: float) -> float:
    """Calculate profit after subtracting cost."""
    revenue = calculate_revenue(variants, quantity_sold)
    cost = cost_per_unit * quantity_sold * len(variants)
    return round(revenue - cost, 2)
