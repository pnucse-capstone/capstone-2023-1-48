from block import *
from state import *

class SSD:
    def __init__(self):
        self.blocks = [Block() for _ in range(BLOCK_PER_SSD)]
        self.address_table = {}
        self.requested_write = 0
        self.additional_write = 0
        self.memory_space = BLOCK_PER_SSD * BLOCK_SIZE / MB
        self.total_gc_threshold = TOTAL_GC_THRESHOLD


    def __str__(self):
        return "SSD size : {:.0f}MB".format(self.memory_space)


    def write_request(self, logical_page_address):
        self.requested_write += 1

        # address_table에 page_id가 존재한다면, 이전에 할당된 주소를 찾아 'invalid'로 상태 변경
        if logical_page_address in self.address_table:
            self.change_state(logical_page_address, State.INVALID)

        # 새로운 데이터를 쓰기 위해 가장 좋은 블록과 페이지 찾고, 쓰기
        block_index, page_index = self.find_best_block_and_page()
        self.write(logical_page_address, block_index, page_index)

        # if self.is_gc_triggered_for_block(block_index) or self.is_gc_triggered_for_ssd():
        #     self.garbage_collection()

        if self.is_gc_triggered_for_ssd():
            self.garbage_collection()

    def write(self, logical_page_address, block_index, page_index):
        # AddressTable 업데이트, page 상태 업데이트
        self.update_address_table(logical_page_address, block_index, page_index)

        block_index, page_index = self.address_table[logical_page_address]
        self.blocks[block_index].pages[page_index].set_logical_page_address(logical_page_address)

        self.change_state(logical_page_address, State.WRITTEN)


    def erase(self, block_index):
        for page in self.blocks[block_index].pages:
            page.reset()
        self.blocks[block_index].reset_state_counts()


    def find_block_index_by_state(self, target_state):
        most_pages = 0
        most_pages_block_index = None
        for block_index, block in enumerate(self.blocks):
            pages = block.get_pages_by_state(target_state)
            if pages > most_pages:
                most_pages = pages
                most_pages_block_index = block_index

        if most_pages_block_index is None:
            raise Exception("There is No Remaining Memory Space.\n" +
                            "Memory Space: {using}/{total}".format(using=self.calculate_using_memory(), total=self.memory_space))

        return most_pages_block_index


    def find_best_block_and_page(self):
        # 가장 Empty Page가 많은 블록 찾기
        best_block_index = self.find_block_index_by_state(State.EMPTY)
        best_page_index = self.blocks[best_block_index].find_empty_page()
        return best_block_index, best_page_index


    def garbage_collection(self):
        # 가장 많은 invalid 페이지가 있는 블록 찾기
        victim_block_index = self.find_block_index_by_state(State.INVALID)
        self.relocate_block(victim_block_index)
        self.erase(victim_block_index)


    def is_gc_triggered_for_block(self, block_index):
        # 블록 내부의 GC Trigger
        block = self.blocks[block_index]
        return block.state_counts[State.EMPTY] / PAGE_PER_BLOCK < self.block_gc_threshold


    def is_gc_triggered_for_ssd(self):
        # 전체 Empty Page의 GC Trigger
        total_empty_pages = sum([block.state_counts[State.EMPTY] for block in self.blocks])
        total_pages = len(self.blocks) * PAGE_PER_BLOCK
        return total_empty_pages / total_pages < self.total_gc_threshold


    def relocate_block(self, block_index):
        block = self.blocks[block_index]
        written_pages = [page for page in block.pages if page.get_state() == State.WRITTEN]
        for page in written_pages:
            self.additional_write += 1
            best_block_index, best_page_index = self.find_best_block_and_page()
            self.write(page.get_logical_page_address(), best_block_index, best_page_index)


    def update_address_table(self, logical_page_address, block_index, page_index):
        self.address_table[logical_page_address] = (block_index, page_index)


    def change_state(self, logical_page_address, new_state):
        block_index, page_index = self.address_table[logical_page_address]
        block = self.blocks[block_index]
        block.change_page_state(page_index, new_state)


    def calculate_using_memory(self):
        memory = 0
        for block in self.blocks:
            for page in block.pages:
                if page.get_state() == State.WRITTEN:
                    memory += PAGE_SIZE
        return memory / MB
