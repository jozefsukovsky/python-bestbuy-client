"""BestbuyClient is a small bestbuy.com api library you can use to 
collect data from bestbuy catalog. 

Supported are: Products API, Stores API, Reviews API, Categories API
Unsupported is: Recommendations API

It supports basic collections and search methods. For more 
information regarding Bestbuy API and instructions how to obtain 
your own API key, please visit 
following site: https://developer.bestbuy.com/documentation
"""

import json
import urllib2

__author__ = "Jozef Sukovsky"
__maintainer__ = "Jozef Sukovsky"
__email__ = "hi@factory84.com"


class BestbuyError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BestbuyClient(object):

    PRODUCTS = "products"
    STORES = "stores"
    REVIEWS = "reviews"
    CATEGORIES = "categories"

    def __init__(self, apikey,
                 products_fields=[],
                 stores_fields=[],
                 reviews_fields=[],
                 categories_fields=[],
                 ):
        """
        Variables and arguments:
        apikey: Bestbuy api key, can be obtained here: 
            https://remix.mashery.com/member/register
        url: current api url including version suffix
        page_size: number of elements per page. default bestbuy is 10
        any_fields: per api fields that will be collected. For more 
            information visit following 
            page:https://developer.bestbuy.com/documentation If you
            leav empty, all available fields will be downloaded
        total: Is number of all entries found. 
        pages: Is the number of pages API can return for particular 
            search
        current_page: Iterator. You can use it your own loops to 
            iterate through pages
        """
        self.url = "http://api.remix.bestbuy.com/v1"
        self.apikey = apikey
        self.page_size = 100
        self.products_fields = products_fields
        self.stores_fields = stores_fields
        self.reviews_fields = reviews_fields
        self.categories_fields = categories_fields
        self.total = 0
        self.pages = 1
        self.current_page = 1

    def _object_fields(self, param):
        """Will find api/fields pair and if you requested only 
        particular fields, will search for them. Otherwise 
        will search for all available fields
        """
        list_ = getattr(self, param + "_fields")
        if len(list_) == 0:
            return ''
        else:
            return '&show=%s' % ','.join(list_)

    def _merge_url(self, param, query=None, page=None):
        """Merge url parts into complete url to be requested"""
        if page is None:
            page = self.current_page
        else:
            self.current_page = page
        if query != None:
            query = '(%s)' % query.replace(' ', '%20')
        else:
            query = ''
        return '%(url)s/%(param)s%(query)s?format=json%(object_fields)s\
&pageSize=%(page_size)s&page=%(page)s&apiKey=%(apikey)s' % {
            'url': self.url,
            'param': param,
            'query': query,
            'object_fields': self._object_fields(param),
            'page_size': self.page_size,
            'page': page,
            'apikey': self.apikey
        }

    def _request(self, url):
        """Bare urllib2 Request. No much handling, will just catch
        error and you can handle it in your own code for now. 

        Also increments current_page variable after each successful
        request
        """
        try:
            request = urllib2.Request(url=url)
            d = urllib2.urlopen(request)
            response = d.read()
            self.current_page += 1
            return response
        except Exception, e:
            raise BestbuyError(e)

    def _get(self, param, query, page):
        r = self._request(self._merge_url(
            param,
            query=query,
            page=page,
        ))
        robject = json.loads(r)
        self.pages = robject['totalPages']
        self.total = robject['total']
        return robject[param]

    def products(self, page=None, query=None):
        """Search for products in Products API. If no query is provided, 
        whole collection will be returned. You can use standard querying
        as explained in bestbuy developers documentation
        """
        if page is None:
            page = self.current_page
        return self._get(self.PRODUCTS, query, page)

    def stores(self, page=None, query=None):
        """Search for stores in Stores API. If no query is provided, 
        whole collection will be returned. You can use standard querying
        as explained in bestbuy developers documentation
        """
        if page is None:
            page = self.current_page
        return self._get(self.STORES, query, page)

    def reviews(self, page=None, query=None):
        """Search for reviews in Reviews API. If no query is provided, 
        whole collection will be returned. You can use standard querying
        as explained in bestbuy developers documentation
        """
        if page is None:
            page = self.current_page
        return self._get(self.REVIEWS, query, page)

    def categories(self, page=None, query=None):
        """Search for categories in Categories API. If no query is provided, 
        whole collection will be returned. You can use standard querying
        as explained in bestbuy developers documentation
        """
        if page is None:
            page = self.current_page
        return self._get(self.CATEGORIES, query, page)
