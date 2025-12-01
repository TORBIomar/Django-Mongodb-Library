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
```
MONGO_URI=mongodb://localhost:27017
MONGO_DB=bookstore_db
```

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
