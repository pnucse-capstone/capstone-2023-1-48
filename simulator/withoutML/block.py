from config import *
from page import *

class Block:
    def __init__(self):
        self.page_per_block = PAGE_PER_BLOCK
        self.pages = [Page() for _ in range(PAGE_PER_BLOCK)]
        self.state_counts = {State.EMPTY: PAGE_PER_BLOCK, State.INVALID: 0, State.WRITTEN: 0}

    def get_pages_by_state(self, state):
        return self.state_counts[state]

    def reset_state_counts(self):
        self.state_counts = {State.EMPTY: PAGE_PER_BLOCK, State.INVALID: 0, State.WRITTEN: 0}

    def find_empty_page(self):
        for page_index, page in enumerate(self.pages):
            if page.state == State.EMPTY:
                return page_index  # 빈 페이지의 인덱스 반환
        return None  # 빈 페이지 없음

    def change_page_state(self, page_index, new_state):
        old_state = self.pages[page_index].get_state()
        self.state_counts[old_state] -= 1
        self.state_counts[new_state] += 1
        self.pages[page_index].set_state(new_state)
