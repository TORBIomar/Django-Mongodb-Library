# Books Library Data

📚 **Books_Library_Data** — A simple Django + MongoDB project that lists and searches books.

## Summary

This project is a minimal Django web app that uses MongoDB as a backend to store and search books data. The CSV dataset is included in the `library` folder as `books.csv` and an import script (`import_books.py`) converts and inserts this data into MongoDB.

The site exposes a small UI (`library/templates/library/book_list.html`) for listing books and searching them (text search) using MongoDB text indexes.

---

## Project structure (key files)

- `manage.py` — Django CLI
- `core/settings.py` — Django settings (Django 5.2.8 in this project)
- `library/` — Django app with views, URLs, tests, and templates
  - `library/books.csv` — the CSV dataset with all book records
  - `library/views.py` — business logic for listing & searching
  - `library/templates/library/book_list.html` — UI for listing and searching
- `db.py` — MongoDB connection wrapper (creates `books_col` / `titles` collection)
- `import_books.py` — script for importing CSV to MongoDB using pandas

---

## Prerequisites

- Python 3.11+ (or a compatible 3.x version). The project uses Django 5.2.
- MongoDB (local or cloud). Provide connection details in `.env` or rely on defaults.
- (Optional) Virtual environment for dependency isolation.

---

## Environment variables

You can create a `.env` file in the project root with the following variables (these are optional; defaults exist in `db.py`):

```
MONGO_URI=mongodb://localhost:27017
MONGO_DB=bookstore_db
```

`db.py` uses `MONGO_URI` and `MONGO_DB` to connect to the database and uses a timeout value to avoid long waits.

---

## Required Python packages

If the project doesn't have `requirements.txt` yet, the following packages are commonly required:

- Django (5.2.x)
- pymongo
- pandas
- python-dotenv

Install (example):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install django pymongo pandas python-dotenv
```

---

## Importing data into MongoDB

This repository includes a CSV with the book dataset at `library/books.csv`. The import script is `import_books.py`, which relies on `db.books_col` to insert into the `titles` collection (name used in `db.py`).

To import the CSV:

```powershell
# Activate your venv first
venv\Scripts\Activate.ps1
python import_books.py
```

Notes:

- `import_books.py` uses `pandas.read_csv` with `ISO-8859-1` encoding and `sep=';'` in case the CSV uses semicolons as separators.
- The script clears the `titles` collection before inserting new data (see `books_col.delete_many({})`).
- Records missing `title` are filtered out.

---

## Using the app

Run the Django development server:

```powershell
venv\Scripts\Activate.ps1
python manage.py runserver
```

Open your browser to `http://127.0.0.1:8000/` to view the book list. Use the search box to query titles, authors, or publishers. The search route is `http://127.0.0.1:8000/search/?q=<your-query>`.

---

## Text search index (if you want better search)

`library/views.py` uses MongoDB text search (`{"$text": {"$search": query}}`). To ensure this works, you must create a text index on relevant fields in the `titles` collection, for example (`mongo` shell / Compass / connection script):

```js
db.titles.createIndex({ title: "text", authors: "text", publisher: "text" });
```

If a text index is not created, searches will default to showing all books or require query changes.

---

## Notes & Troubleshooting

- If `import_books.py` prints `WARNING: Cannot connect to MongoDB: ...` then verify `MONGO_URI` and that MongoDB is running.
- The CSV might be large — if you run into memory issues, consider streaming or chunking the import.
- Pagination is controlled by `django.core.paginator.Paginator` in `library/views.py` and shows 20 books per page by default.

---

## Development & Contribution

- Add model(s) to `library/models.py` if you want to use Django ORM; currently the app uses MongoDB directly through `pymongo`.
- Add a `requirements.txt` file if you have specific dependency versions.
- Add tests into `library/tests.py` if you plan to add Django ORM code, or add integration tests for the DB/HTTP features.

---

## License

Add your preferred license file if needed.

---

If you'd like, I can also:

- Add a `requirements.txt` file.
- Add a `.env.example` sample file.
- Add instructions to create a virtualenv automatically (PowerShell & Bash variants).
- Add a Dockerfile / docker-compose for MongoDB + Django.

If you want a shorter or more verbose README, or to include more features (e.g., API endpoints, Docker, CI), tell me and I'll update it!
