python-bestbuy-client
=====================

Small bestbuy.com API client library written in Python

Example usage:
```
#!/usr/bin/env python

import time

from bestbuy import *

bb = BestbuyClient("YOUR_API_KEY")
bb.products_fields = ['sku', 'name']
bb.categories_fields = ['name']
fails = 0
max_fails = 10
while True:
    t = time.time()
    try:
        products = bb.products()
    except:
        if fails >= max_fails:
            break
        time.sleep(0.5)
        fails += 1
        bb.current_page -= 1
        products = bb.products()
    
    tt = time.time() 
    if tt - t < 0.2:
        time.sleep(tt - t)
     
    #print [x['sku'] for x in products]
    if bb.current_page >= 10:
        break

bb.current_page = 1
bb.total = 0
print bb.reviews(query='sku in('+','.join([str(x['sku']) for x in products])+')')
print bb.reviews(query='rating>4', page=1)
```
