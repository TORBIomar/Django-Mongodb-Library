import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import books_col
import json

b = books_col.find_one()
if not b:
    print('NO_DOCS')
else:
    print('KEYS:', list(b.keys()))
    for k in ['title','authors','isbn','year','publisher','image_large','image_medium','image_small','rating','fame','_rating_val','rating_val','Image-URL-L','Image-URL-M','Image-URL-S']:
        print(f"{k}:", b.get(k))
    print('\nFULL_DOC (truncated):')
    print(json.dumps(b, default=str)[:2000])
