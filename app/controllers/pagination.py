from flask import request
from flask import current_app as app
from app import schema as s


def create_pagination(total: int, page_size: int = 0) -> s.Pagination:
    """create instance Pagination for current request"""
    q = request.args.get("q", type=str, default="")
    page = request.args.get("page", type=int, default=1)
    page_size = page_size or app.config["DEFAULT_PAGE_SIZE"]
    PAGE_LINKS_NUMBER: int = app.config["PAGE_LINKS_NUMBER"]

    pages = (total // page_size + 1) if (total % page_size) else (total // page_size)

    pages_for_links: list[int] = []
    if pages > PAGE_LINKS_NUMBER:
        if page <= PAGE_LINKS_NUMBER // 2:
            pages_for_links = [n + 1 for n in range(PAGE_LINKS_NUMBER)]
        elif pages - page <= PAGE_LINKS_NUMBER // 2:
            pages_for_links = [n + 1 for n in range(pages - PAGE_LINKS_NUMBER, pages)]
        else:
            pages_for_links = list(
                range(page - PAGE_LINKS_NUMBER // 2, page + PAGE_LINKS_NUMBER // 2)
            )
    else:
        pages_for_links = [n + 1 for n in range(pages)]

    return s.Pagination(
        page=page,
        pages=pages,
        total=total,
        query=q,
        per_page=page_size,
        skip=(page - 1) * page_size,
        pages_for_links=pages_for_links,
    )
