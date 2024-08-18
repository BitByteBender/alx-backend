#!/usr/bin/env python3
""" Hypermedia Pagination """
import csv
import math
from typing import List, Dict


def index_range(page: int, page_size: int) -> tuple:
    """ Calcs start and end index for pagination """
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    return start_idx, end_idx


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
        """
            Retrieves a page of data from the dataset method
        """
        WarnLog = "must be a signed integer"
        assert isinstance(page,
                          int) and page > 0,  "Page " + WarnLog
        assert isinstance(page_size,
                          int) and page_size > 0, "Page size " + WarnLog

        start_idx, end_idx = index_range(page, page_size)
        dataset = self.dataset()

        return [] if start_idx >= len(dataset) else dataset[start_idx:end_idx]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """
           Returns a dict containing pagination data
        """
        dt = self.get_page(page, page_size)
        datas = len(self.dataset())
        pages = math.ceil(datas / page_size)

        hyper_pagination = {
                'page_size': len(dt),
                'page': page,
                'data': dt,
                'next_page': (page + 1) if page < pages else None,
                'prev_page': (page - 1) if page > 1 else None,
                'total_pages': pages
        }

        return hyper_pagination
