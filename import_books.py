import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import numpy as np
from db import books_col

# Configuration: change TOP_N if you want fewer/more books
TOP_N = 100000

# CSV location
CSV_FILE = "library/books.csv"

print("Reading CSV... (this can take some time for large files)")
df = pd.read_csv(CSV_FILE, encoding='ISO-8859-1', sep=';', on_bad_lines='skip', low_memory=False)

print("Columns found:", df.columns.tolist())
print("Rows:", len(df))

# Rename columns to match your data (non-destructive)
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

# Basic cleaning
df = df.where(pd.notnull(df), None)

# Ensure we have at least a title column
if 'title' not in df.columns:
    print("❌ No `title` column found. Aborting.")
    raise SystemExit(1)

# Build a deduplication key: prefer ISBN when available, otherwise title+author
df['isbn_str'] = df.get('isbn', pd.Series([None]*len(df))).fillna('').astype(str).str.strip()
df['title_norm'] = df['title'].fillna('').astype(str).str.strip().str.lower()
df['authors_norm'] = df.get('authors', pd.Series([None]*len(df))).fillna('').astype(str).str.strip().str.lower()
df['dedupe_key'] = np.where(df['isbn_str']!='', 'ISBN::'+df['isbn_str'], 'TA::'+df['title_norm']+'||'+df['authors_norm'])

# Detect a fame/rating column (common names)
rating_candidates = [c for c in df.columns if any(k in c.lower() for k in ['rating','book-rating','avg','average','num_ratings','ratings_count'])]
rating_col = None
for c in rating_candidates:
    # pick first numeric-like candidate
    try:
        pd.to_numeric(df[c].dropna().iloc[:10])
        rating_col = c
        break
    except Exception:
        continue

if rating_col:
    print(f"Using rating/fame column: {rating_col}")
    df['_rating_val'] = pd.to_numeric(df[rating_col], errors='coerce').fillna(0)
    # pick representative record per dedupe_key by highest rating, tie-break by year (if present)
    if 'year' in df.columns:
        # prefer higher rating, then newest year
        df['_year_val'] = pd.to_numeric(df['year'], errors='coerce').fillna(-9999)
        df_sorted = df.sort_values(by=['dedupe_key','_rating_val','_year_val'], ascending=[True,False,False])
        rep = df_sorted.groupby('dedupe_key', as_index=False).first()
        rep['fame'] = rep['_rating_val']
    else:
        idx = df.groupby('dedupe_key')['_rating_val'].idxmax()
        rep = df.loc[idx].reset_index(drop=True)
        rep['fame'] = rep['_rating_val']
else:
    print("No explicit rating column found — using occurrence counts as a proxy for fame.")
    counts = df.groupby('dedupe_key').size().rename('popularity')
    # choose a representative row using group.first (keeps first occurrence)
    rep = df.groupby('dedupe_key', as_index=False).first()
    rep = rep.merge(counts.reset_index(), on='dedupe_key', how='left')
    rep['fame'] = rep['popularity'].fillna(0)

print("Groups after deduplication:", len(rep))

# Optionally merge ratings from a separate CSV (e.g., library/ratings.csv)
RATINGS_CSV = "library/ratings.csv"
if os.path.exists(RATINGS_CSV):
    try:
        print(f"Found ratings file: {RATINGS_CSV} — attempting to merge ratings by ISBN")
        # ratings.csv in this dataset uses semicolon separator and quoted fields
        ratings_df = pd.read_csv(RATINGS_CSV, sep=';', encoding='ISO-8859-1', on_bad_lines='skip', low_memory=False)
        print("Ratings columns:", ratings_df.columns.tolist())

        # find isbn/rating columns in ratings file
        isbn_candidates = [c for c in ratings_df.columns if 'isbn' in c.lower()]
        rating_candidates_r = [c for c in ratings_df.columns if 'rating' in c.lower()]

        if isbn_candidates and rating_candidates_r:
            isbn_col = isbn_candidates[0]
            rating_col_r = rating_candidates_r[0]
            ratings_df['isbn_str'] = ratings_df[isbn_col].fillna('').astype(str).str.strip()
            ratings_df['rating_val'] = pd.to_numeric(ratings_df[rating_col_r], errors='coerce')
            # compute average rating per ISBN (many user ratings per ISBN)
            ratings_map = ratings_df.groupby('isbn_str', as_index=False)['rating_val'].mean().set_index('isbn_str')

            # ensure rep has isbn_str
            if 'isbn' in rep.columns:
                rep['isbn_str'] = rep['isbn'].fillna('').astype(str).str.strip()
            else:
                rep['isbn_str'] = ''

            rep = rep.merge(ratings_map, left_on='isbn_str', right_index=True, how='left')
            # merged rating_val may be NaN; we'll use it as fallback
            print("Merged average ratings by ISBN; any non-null 'rating_val' will be used when explicit rating is absent.")
        else:
            print("Ratings file found but couldn't detect ISBN or rating columns — skipping merge.")
    except Exception as e:
        print("Failed to read/merge ratings file:", e)

# Sort groups by fame and keep top N
rep_sorted = rep.sort_values(by='fame', ascending=False).head(TOP_N).reset_index(drop=True)

# Normalize/attach an explicit numeric `rating` field when available
# Preference order: existing detected _rating_val (from main CSV) -> merged rating_val (from ratings CSV) -> None
if '_rating_val' in rep_sorted.columns:
    rep_sorted['rating'] = rep_sorted.get('_rating_val')
elif 'rating_val' in rep_sorted.columns:
    rep_sorted['rating'] = rep_sorted.get('rating_val')
else:
    rep_sorted['rating'] = None

print(f"Keeping top {len(rep_sorted)} books (TOP_N={TOP_N})")

# Prepare records to insert
records = rep_sorted.to_dict(orient='records')

print(f"Valid records to import: {len(records)}")

if records:
    print("Importing to MongoDB (titles collection)...")
    books_col.delete_many({})
    print("Cleared old data")
    result = books_col.insert_many(records)
    print("✅ Imported:", len(result.inserted_ids), "books")
else:
    print("❌ No valid records to import!")