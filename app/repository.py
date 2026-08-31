from typing import Literal

from app.models import Product

PRODUCTS = [
    Product(id=1, name="Zenbook 14 OLED", category="Laptop", price=42900),
    Product(id=2, name="ROG Zephyrus G14", category="Gaming Laptop", price=62900),
    Product(id=3, name="ProArt P16", category="Creator Laptop", price=79900),
    Product(id=4, name="TUF Gaming A15", category="Gaming Laptop", price=38900),
    Product(id=5, name="ROG Ally X", category="Handheld", price=26900),
    Product(id=6, name="ProArt Display PA279CRV", category="Monitor", price=15900),
]

SortBy = Literal["name", "price"]
SortOrder = Literal["asc", "desc"]


def search_products(
    q: str | None = None,
    sort_by: SortBy | None = None,
    order: SortOrder = "asc",
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Product], int]:
    """Return one page of matching products plus the total match count."""
    matches = list(PRODUCTS)
    if q:
        needle = q.casefold()
        matches = [
            product
            for product in matches
            if needle in product.name.casefold() or needle in product.category.casefold()
        ]

    if sort_by is not None:
        matches = sorted(
            matches,
            key=lambda product: getattr(product, sort_by),
            reverse=order == "desc",
        )

    start = (page - 1) * page_size
    return matches[start : start + page_size], len(matches)

    start = (page - 1) * page_size
    return matches[start : start + page_size], len(matches)


def list_products() -> list[Product]:
    return PRODUCTS.copy()


def get_product(product_id: int) -> Product | None:
    return next((product for product in PRODUCTS if product.id == product_id), None)
