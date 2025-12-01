from django.shortcuts import render
from db import books_col
from django.core.paginator import Paginator

def book_list(request):
    # show all books, paginated
    page_number = request.GET.get('page', 1)
    books = list(books_col.find({}, {"title":1, "authors":1, "year":1, "publisher":1}).sort("title", 1))
    
    paginator = Paginator(books, 20)  # 20 books per page
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'library/book_list.html', {'page_obj': page_obj})

def book_search(request):
    query = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)
    
    if query:
        # text search (requires text index)
        books = list(books_col.find({"$text": {"$search": query}}, {"score":{"$meta":"textScore"}, "title":1, "authors":1, "year":1, "publisher":1}).sort([("score", {"$meta": "textScore"})]))
    else:
        books = list(books_col.find({}, {"title":1, "authors":1, "year":1, "publisher":1}))
    
    paginator = Paginator(books, 20)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'library/book_list.html', {'page_obj': page_obj, 'query': query})
