<<<<<<< HEAD
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

=======
# 📚 Books Library - Django + MongoDB

A simple web application to browse and search books using Django and MongoDB.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- MongoDB running locally or remotely

### Installation

1. **Clone and navigate to the project**
```bash
cd mongo_library
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**
- Windows: `venv\Scripts\Activate.ps1`
- Mac/Linux: `source venv/bin/activate`

4. **Install dependencies**
```bash
pip install django pymongo pandas python-dotenv
```

5. **Configure MongoDB connection** (optional)

Create a `.env` file in the project root:
>>>>>>> e705b795369ce9b58afc4b55ee1207b3af357b8a
```
MONGO_URI=mongodb://localhost:27017
MONGO_DB=bookstore_db
```

<<<<<<< HEAD
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
=======
If not provided, defaults to `mongodb://localhost:27017` and `bookstore_db`.

### Import Book Data

```bash
python import_books.py
```

This imports all books from `library/books.csv` into MongoDB's `titles` collection.

### Create Search Index

Open a new terminal and run:
```bash
python manage.py shell
```

Then execute:
```python
from db import books_col

books_col.create_index([
    ("title", "text"),
    ("authors", "text"),
    ("publisher", "text")
])
exit()
```

### Run the Application

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** to browse books!

## 📁 Project Structure

```
mongo_library/
├── core/                    # Django project settings
│   ├── settings.py
│   └── urls.py
├── library/                 # Main Django app
│   ├── templates/
│   │   └── library/
│   │       └── book_list.html
│   ├── views.py            # Book list and search logic
│   └── books.csv           # Book dataset
├── db.py                   # MongoDB connection
├── import_books.py         # CSV import script
└── manage.py              # Django CLI
```

## 🔍 Features

- **Browse Books**: Paginated list of all books (20 per page)
- **Search**: Full-text search by title, author, or publisher
- **Modern UI**: Clean, responsive design with gradient colors

## 🛠️ MongoDB Commands

Access MongoDB shell:
```bash
mongosh
```

Useful commands:
```javascript
// Switch to database
use bookstore_db

// Count all books
db.titles.countDocuments()

// Find books by author
db.titles.find({ authors: "Amy Tan" })

// Find books by year
db.titles.find({ year: "2002" })

// View all indexes
db.titles.getIndexes()
```

## 📊 Database Schema

**Collection**: `titles`

Each book document contains:
- `isbn` - ISBN number
- `title` - Book title
- `authors` - Author name(s)
- `year` - Publication year
- `publisher` - Publisher name
- `image_small`, `image_medium`, `image_large` - Cover image URLs

## 🐛 Troubleshooting

**MongoDB connection error?**
- Ensure MongoDB is running
- Check your `.env` file or connection string

**Search not working?**
- Make sure you created the text index (see "Create Search Index" above)

**Import fails?**
- Check that `library/books.csv` exists
- Verify CSV encoding and delimiter (should be semicolon-separated)

## 📝 Notes

- Uses `pymongo` for direct MongoDB access (no Django ORM)
- Pagination set to 20 books per page
- Text search requires MongoDB text index
- CSV data cleared before each import

## 🤝 Contributing

Feel free to fork and submit pull requests!

## 📄 License

MIT License (or specify your preferred license)
>>>>>>> e705b795369ce9b58afc4b55ee1207b3af357b8a
