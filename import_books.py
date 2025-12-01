import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from db import books_col

# CSV location 
CSV_FILE = "library/books.csv"

print("Reading CSV...")
df = pd.read_csv(CSV_FILE, encoding='ISO-8859-1', sep=';', on_bad_lines='skip', low_memory=False)

print("Columns found:", df.columns.tolist())
print("Rows:", len(df))

# Rename columns to match your data
mapping = {
    "Book-Title": "title",
    "Book-Author": "authors",
    "ISBN": "isbn",
    "Year-Of-Publication": "year",
    "Publisher": "publisher",
    "Image-URL-S": "image_small",
    "Image-URL-M": "image_medium",
    "Image-URL-L": "image_large",
}

df.rename(columns=mapping, inplace=True)

print("Columns after rename:", df.columns.tolist())

# Clean empty values
df = df.where(pd.notnull(df), None)

# Convert to dictionaries
records = df.to_dict(orient="records")

# Remove records without title
records = [b for b in records if b.get("title")]

print(f"Valid records to import: {len(records)}")

if records:
    print("Importing to MongoDB (titles collection)...")
    
    books_col.delete_many({})
    print("Cleared old data")
    
    result = books_col.insert_many(records)
    print("✅ Imported:", len(result.inserted_ids), "books")
else:
    print("❌ No valid records to import!")