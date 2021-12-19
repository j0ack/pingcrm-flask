"""Ping CRM routes utils."""

from typing import Any, Dict, Tuple

from flask import request, url_for


def get_search_filters() -> Tuple[int, str, str]:
    """Get search filters from request."""
    page = int(request.args.get("page", "1"))
    name_filter = request.args.get("search", "")
    trash_filter = request.args.get("trashed", "")

    return page, name_filter, trash_filter


def build_search_data(
    query,
    key: str,
    url_name: str,
    search_filter: str,
    trash_filter: str,
) -> Dict[str, Any]:
    """Build returned data for a search from query."""
    return {
        key: {
            "data": [item.to_dict() for item in query.items],
            "links": [
                {"url": url_for(url_name, page=page), "label": page}
                for page in range(1, query.pages + 1)
            ],
        },
        "filters": {
            "search": search_filter,
            "trashed": trash_filter,
        },
    }
