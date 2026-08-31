from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.models import Product, ProductPage
from app.repository import SortBy, SortOrder, get_product, search_products

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=ProductPage)
def read_products(
    q: Annotated[str | None, Query(description="Case-insensitive partial match on name or category")] = None,
    sort: Annotated[SortBy | None, Query(description="Sort by name or price")] = None,
    order: Annotated[SortOrder, Query(description="Sort order: asc or desc")] = "asc",
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=20)] = 20,
) -> ProductPage:
    items, total = search_products(
        q=q,
        sort_by=sort,
        order=order,
        page=page,
        page_size=page_size,
    )
    total_pages = max(1, -(-total // page_size))
    return ProductPage(items=items, total=total, page=page, page_size=page_size, total_pages=total_pages)


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int) -> Product:
    product = get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product
