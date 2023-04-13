from pydantic import BaseModel


class Pagination(BaseModel):
    """Pagination data"""

    page: int  # current page number
    total: int  # total items
    query: str | None  # query string
    per_page: int  # number items on the page
    skip: int  # number items on all previous pages
    pages: int  # total pages
    pages_for_links: list[int]  # number of links
