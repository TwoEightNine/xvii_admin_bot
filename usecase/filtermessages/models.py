from typing import Callable


class FilterArgs:

    def __init__(self, filter_func: Callable):
        self.filter_func = filter_func
