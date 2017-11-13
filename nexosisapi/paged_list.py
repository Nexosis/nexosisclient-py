from nexosisapi.link import Link


class PagedList(list):
    def __init__(self, *args, **kwargs):
        super(PagedList, self).__init__(args[0])
        if kwargs is not None:
            self._page_number = kwargs['page_number'] if 'page_number' in kwargs else 0
            self._total_pages = kwargs['total_pages'] if 'total_pages' in kwargs else 0
            self._page_size = kwargs['page_size'] if 'page_size' in kwargs else 50
            self._item_total = kwargs['item_total'] if 'item_total' in kwargs else 0
            self._links = kwargs['links'] if 'links' in kwargs else []

    @property
    def page_number(self):
        return self._page_number

    @page_number.setter
    def page_number(self, value):
        self._page_number = value

    @property
    def total_pages(self):
        return self._total_pages

    @total_pages.setter
    def total_pages(self, value):
        self._total_pages = value

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        self._page_size = value

    @property
    def item_total(self):
        return self._item_total

    @item_total.setter
    def item_total(self, value):
        self._item_total = value

    @property
    def links(self):
        return self._links

    @links.setter
    def links(self, value):
        self._links = value

    @staticmethod
    def from_response(items, response_dict):
        return PagedList(items,
                         page_number=response_dict.get('pageNumber', 0),
                         page_size=response_dict.get('pageSize', 50),
                         item_total=response_dict.get('totalCount', 50),
                         total_pages=response_dict.get('totalPages', 1),
                         links=[Link(item['rel'],item['href']) for item in response_dict.get('links', [])])