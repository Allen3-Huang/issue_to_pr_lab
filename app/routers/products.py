from fastapi import APIRouter, HTTPException, Query, status

from app.models import Product, ProductPage
from app.repository import SortBy, SortOrder, get_product, search_products

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=ProductPage)
def read_products(
    q: str | None = Query(default=None, description="Case-insensitive partial name match"),
    sort_by: SortBy = "id",
    order: SortOrder = "asc",
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> ProductPage:
    items, total = search_products(
        q=q,
        sort_by=sort_by,
        order=order,
        page=page,
        page_size=page_size,
    )
    return ProductPage(items=items, total=total, page=page, page_size=page_size)


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int) -> Product:
    product = get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product
