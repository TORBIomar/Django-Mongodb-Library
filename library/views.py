from django.shortcuts import render
from db import books_col
from django.core.paginator import Paginator
import re
from bson import ObjectId


def book_list(request):
    # show all books, paginated, with the first 5 pages reserved for books
    # that have both images and a non-null rating.
    page_number = int(request.GET.get('page', 1))
    # sort by year descending, then title ascending as a tie-breaker
    projection = {"title": 1, "authors": 1, "year": 1, "publisher": 1, "image_medium": 1, "image_large": 1, "image_small": 1, "fame": 1, "isbn": 1, "rating": 1, "rating_val": 1, "_rating_val": 1}

    # Pagination settings
    PAGE_SIZE = 20
    PRIORITY_PAGES = 5
    priority_limit = PAGE_SIZE * PRIORITY_PAGES

    # Build queries: first select books that have an image AND a rating, sorted alphabetically
    image_q = {"$or": [
        {"image_large": {"$exists": True, "$ne": None, "$ne": ""}},
        {"image_medium": {"$exists": True, "$ne": None, "$ne": ""}},
        {"image_small": {"$exists": True, "$ne": None, "$ne": ""}},
    ]}
    # require rating to be present (not null) for prioritized pages
    rating_q = {"rating": {"$exists": True, "$ne": None}}

    try:
        top_cursor = books_col.find({"$and": [rating_q, image_q]}, projection).sort([("title", 1)]).limit(priority_limit)
        top_list = list(top_cursor)
    except Exception:
        top_list = []

    top_ids = [d.get('_id') for d in top_list]

    # Then get the remaining books (exclude those already in top_list), keep previous fallback ordering (newest first)
    if top_ids:
        rest_cursor = books_col.find({"_id": {"$nin": top_ids}}, projection).sort([("year", -1), ("title", 1)])
    else:
        rest_cursor = books_col.find({}, projection).sort([("year", -1), ("title", 1)])

    rest_list = list(rest_cursor)

    # Combine prioritized list then the rest; convert _id to string `id` for templates
    combined = top_list + [d for d in rest_list if d.get('_id') not in top_ids]
    for b in combined:
        b['id'] = str(b.get('_id'))

    paginator = Paginator(combined, PAGE_SIZE)
    page_obj = paginator.get_page(page_number)

    return render(request, 'library/book_list.html', {'page_obj': page_obj})


def book_search(request):
    query = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    projection = {"title": 1, "authors": 1, "year": 1, "publisher": 1, "image_medium": 1, "image_large": 1, "image_small": 1, "fame": 1, "isbn": 1}

    books = []
    if query:
        # Prefer MongoDB text search (requires a text index on relevant fields).
        # If text search fails (no index), fall back to a case-insensitive regex search across common fields.
        try:
            # include text score in projection and sort by score then year desc
            proj_with_score = projection.copy()
            proj_with_score["score"] = {"$meta": "textScore"}
            cursor = books_col.find({"$text": {"$search": query}}, proj_with_score).sort([("score", {"$meta": "textScore"}), ("year", -1)])
            books = list(cursor)
        except Exception:
            # fallback: regex search on title, authors, publisher
            regex = re.compile(re.escape(query), re.IGNORECASE)
            q = {"$or": [{"title": regex}, {"authors": regex}, {"publisher": regex}]}
            # sort results by year descending (newest first)
            cursor = books_col.find(q, projection).sort([("year", -1), ("title", 1)])
            books = list(cursor)
        # convert ObjectId to string for template links
        for b in books:
            b['id'] = str(b.get('_id'))
    else:
        # if no query, behave like book_list (newest first)
        books = list(books_col.find({}, projection).sort([("year", -1), ("title", 1)]))
        for b in books:
            b['id'] = str(b.get('_id'))

    paginator = Paginator(books, 20)
    page_obj = paginator.get_page(page_number)

    return render(request, 'library/book_list.html', {'page_obj': page_obj, 'query': query})


def book_detail(request, book_id):
    """Show a single book with image and rating."""
    try:
        obj_id = ObjectId(book_id)
    except Exception:
        return render(request, 'library/book_detail.html', {'error': 'Invalid book id'})

    projection = {"title": 1, "authors": 1, "year": 1, "publisher": 1, "image_medium": 1, "image_large": 1, "image_small": 1, "fame": 1, "isbn": 1, "rating": 1, "rating_val": 1, "_rating_val": 1}
    book = books_col.find_one({"_id": obj_id}, projection)
    if not book:
        return render(request, 'library/book_detail.html', {'error': 'Book not found'})

    # Provide a friendly rating value if available
    # Preference: explicit `rating` inserted on import -> `fame` -> `_rating_val` -> merged `rating_val`
    rating = None
    if book.get('rating') is not None:
        rating = book.get('rating')
    elif book.get('fame') is not None:
        rating = book.get('fame')
    elif book.get('_rating_val') is not None:
        rating = book.get('_rating_val')
    elif book.get('rating_val') is not None:
        rating = book.get('rating_val')

    # Convert _id to str for template (if needed elsewhere)
    book['id'] = str(book.get('_id'))

    return render(request, 'library/book_detail.html', {'book': book, 'rating': rating})
