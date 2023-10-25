from state import *

class Page:
    def __init__(self):
        self.logical_page_address = None
        self.state = State.EMPTY

    def get_logical_page_address(self):
        return self.logical_page_address

    def set_logical_page_address(self, logical_page_address):
        self.logical_page_address = logical_page_address

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def reset(self):
        self.logical_page_address = None
        self.state = State.EMPTY
