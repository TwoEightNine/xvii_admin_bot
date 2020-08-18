from typing import Optional

from usecase.logger import Logger
from tqdm import tqdm


class StdoutLogger(Logger):

    def __init__(self):
        self.pbar = None

    def log(self, message: str, exception: Optional[Exception] = None):
        print(message)
        if exception:
            print(exception)

    def progress(self, done: int, total: int):
        if not self.pbar:
            self.pbar = tqdm(total=total)

        self.pbar.update(done - self.pbar.n)

        if done == total:
            self.pbar.close()
            self.pbar = None
