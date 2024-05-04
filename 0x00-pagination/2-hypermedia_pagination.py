#!/usr/bin/env python3
"""
This module contains a simple helper function
and a class to paginate a database of popular baby names.
The dataset is stored in a CSV file that is read at runtime.
"""

import csv
import math
from typing import Tuple, List


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Return a tuple of size two containing a start index and an end index."""
    return ((page - 1) * page_size, page * page_size)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """ Get the page with the pagination"""
        assert isinstance(page, int) and isinstance(page_size, int)
        assert page > 0 and page_size > 0
        dataSet = self.dataset()
        start_index, end_index = index_range(page, page_size)
        if start_index >= len(dataSet) or end_index >= len(dataSet):
            return []
        page_items = []
        for i in range(start_index, end_index):
            page_items.append(dataSet[i])
        return page_items

    def get_hyper(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Returns a dictionary containing the following key-value pairs:

        page_size: the length of the returned dataset page
        page: the current page number
        data: the dataset page (equivalent to return from previous task)
        next_page: number of the next page, None if no next page
        prev_page: number of the previous page, None if no previous page
        total_pages: the total number of pages in the dataset as an integer
        """
        data = self.get_page(page, page_size)
        next_page = prev_page = None
        total_pages = (len(self.dataset()) + page_size - 1) // page_size
        if page > 1:
            prev_page = page - 1
        if page < total_pages:
            next_page = page + 1
        return {
                  "page_size": page_size,
                  "page": page,
                  "data": data,
                  "next_page": next_page,
                  "prev_page": prev_page,
                  "total_pages": total_pages
              }
