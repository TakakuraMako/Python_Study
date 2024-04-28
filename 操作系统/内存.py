class Page:
    def __init__(self, page_number=None, physical_block_number=None,accessed = False, modified=False, present=False):
        self.page_number = page_number
        self.physical_block_number = physical_block_number
        self.accessed = accessed
        self.modified = modified
        self.present = present

class PageTable:
    def __init__(self):
        self.entries = {}  # 页面表，使用字典来存储，键为页面号，值为Page对象

    def get_physical_address(self, logical_address, page_size):
        page_number = logical_address // page_size  # 计算页面号
        offset = logical_address % page_size  # 计算页内偏移
        if page_number in self.entries and self.entries[page_number].present:
            page = self.entries[page_number]
            physical_address = page.physical_block_number * page_size + offset  # 计算物理地址
            page.accessed = True  # 更新访问位
            return physical_address
        else:
            return None  # 如果页面不在内存中，则返回None表示缺页


def access_memory(page_table, logical_address, page_size):
    physical_address = page_table.get_physical_address(logical_address, page_size)
    if physical_address is not None:
        print(f"访问物理地址: {physical_address}")
    else:
        print("发生缺页中断")
        handle_page_fault(page_table, logical_address, page_size)

def handle_page_fault(page_table, logical_address, page_size):
    page_number = logical_address // page_size
    # 假设现在通过某种算法找到一个可用的物理块（这里未展示具体算法）
    new_physical_block_number = find_free_physical_block()
    # 将新页面加载到内存中
    page_table.entries[page_number] = Page(page_number, new_physical_block_number, present=True)
    print(f"页面 {page_number} 被加载到物理块 {new_physical_block_number}")

def find_free_physical_block():
    # 这个函数是假设的，实际应用中应有具体实现
    return 1  # 返回一个可用的物理块号

PAGE_SIZE = 4096  # 页面大小为4KB
page_table = PageTable()
logical_address = 12345

access_memory(page_table, logical_address, PAGE_SIZE)
