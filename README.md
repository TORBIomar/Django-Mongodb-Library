# 📚 Books Library — Django + MongoDB

*A fully-featured web application to browse, search, and discover books using Django and MongoDB.*

---

## 🚀 Quick Start

### Prerequisites

* Python 3.11+
* MongoDB running locally or remotely

### Installation

1. **Clone and navigate to the project**

```bash
cd mongo_library
```

2. **Create and activate a virtual environment**

> *Windows* (PowerShell / CMD) — **use the generic `activate` script**

```powershell
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
```

> *Mac / Linux*

```bash
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install django pymongo pandas python-dotenv
```

4. **Configure MongoDB connection** (optional)

Create a `.env` file in the project root:

```
MONGO_URI=mongodb://localhost:27017
MONGO_DB=bookstore_db
```

---

## 📥 Import Books Data

The project includes two CSV files:

* `library/books.csv` — Main book catalog (271k+ books)
* `library/ratings.csv` — User ratings (aggregated to compute average per ISBN)

**To import books:**

```bash
# Activate venv if not already
venv\Scripts\activate

# Run the import script
python import_books.py
```

This script will:

* Deduplicate books by ISBN or title+author
* Select the top 100,000 most popular/highest-rated books
* Merge user ratings from `ratings.csv` by ISBN
* Store everything in MongoDB

---

## 🔧 Create Text Index for Search (recommended)

For faster full-text search, create a MongoDB text index:

```bash
python manage.py create_text_index
```

---

## ▶️ Run the Development Server

```bash
venv\Scripts\activate
python manage.py runserver
```

Open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

---

## ✨ Features

* **First 5 pages (100 items):** Books with both **images** and **ratings**, alphabetically sorted
* **Remaining pages:** Full catalog sorted by year (newest first)
* **20 books per page** with clean pagination controls
* **Full-text search** (fallback to case-insensitive regex when text index is missing)
* **Book detail view** with large image fallback and aggregated rating (0–10 scale)
* Responsive UI with subtle animations and hover states

---

## 📁 Project Structure

```
mongo_library/
├── manage.py
├── import_books.py
├── db.py
├── README.md
│
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── library/
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│   ├── books.csv
│   ├── ratings.csv
│   └── templates/library/
│       ├── book_list.html
│       └── book_detail.html
└── scripts/
    └── inspect_doc.py
```

---

## 🔍 API Endpoints

| Endpoint           | Method | Description                                              |
| ------------------ | ------ | -------------------------------------------------------- |
| `/`                | GET    | Home page — list all books (prioritized by rating+image) |
| `/search/`         | GET    | Search results (query param: `q`)                        |
| `/book/<book_id>/` | GET    | Single book detail view                                  |

**Query Parameters:**

* `q` — Search query (e.g., `?q=harry+potter`)
* `page` — Page number (e.g., `?page=2`)

Example:

```
http://127.0.0.1:8000/
http://127.0.0.1:8000/?page=2
http://127.0.0.1:8000/search/?q=python
http://127.0.0.1:8000/book/507f1f77bcf86cd799439011/
```

---

## 🛠️ Management Commands

**Create MongoDB Text Index**

```bash
python manage.py create_text_index
```

This builds a text index on `title`, `authors`, and `publisher` fields for faster full-text search.

---

## 📊 Data Import Details (`import_books.py`)

* **Deduplication:** ISBN primary, title+author fallback; keeps highest-rated edition
* **Top 100k selection:** Ranks by occurrence (popularity proxy) and rating counts
* **Rating merge:** Computes average rating per ISBN from `ratings.csv`
* **Image handling:** Stores `image_large`, `image_medium`, `image_small` and UI falls back gracefully

Expected console output during import:

```
Reading CSV... (this can take some time for large files)
Columns found: [...]
Rows: 271360
Groups after deduplication: 271359
Found ratings file: library/ratings.csv — attempting to merge ratings by ISBN
Merged average ratings by ISBN; ...
Keeping top 100000 books (TOP_N=100000)
Valid records to import: 100000
Importing to MongoDB (titles collection)...
Cleared old data
✅ Imported: 100000 books
```

---

## 🐛 Troubleshooting

**`No module named 'pymongo'`**

```bash
pip install pymongo
```

**MongoDB connection fails**

* Ensure MongoDB is running (`mongod`) or update `MONGO_URI` in `.env`

**Books showing N/A for rating**

* Re-run `python import_books.py` to merge ratings
* Confirm `library/ratings.csv` has `ISBN` and `Book-Rating` columns

**Search not finding results**

* Create the text index: `python manage.py create_text_index`
* Or inspect the `titles` collection with `mongosh` or MongoDB Compass

---

## 📄 License

This project is provided as-is for educational and personal use.

---

**Happy reading!** 📚

*Edited: Windows activation instructions simplified to use `venv\\Scripts\\activate` (no `.ps1`).*
