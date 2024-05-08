class PageTableEntry:
    def __init__(self, page_number, frame_number=None, access=False, modify=False, present=False):
        self.page_number = page_number
        self.frame_number = frame_number
        self.access = access
        self.modify = modify
        self.present = present

class MemoryManagementUnit:
    def __init__(self, size=4096):
        self.page_size = size  # 页面大小设为4KB
        self.page_table = {}

    def allocate_page(self, page_number, frame_number):
        # 分配页面
        self.page_table[page_number] = PageTableEntry(page_number, frame_number, present=True)

    def access_page(self, page_number):
        # 访问页面
        entry = self.page_table.get(page_number)
        if entry and entry.present:
            entry.access = True
            print(f"访问页面{page_number}，物理帧号为{entry.frame_number}")
        else:
            print(f"页面{page_number}未在内存中，触发缺页中断")
            self.handle_page_fault(page_number)

    def handle_page_fault(self, page_number):
        # 处理缺页中断
        print(f"处理页面{page_number}的缺页中断")
        # 在实际情况中，这里可以实现页面替换逻辑和加载页面到内存的逻辑

    def release_page(self, page_number):
        # 回收页面
        if page_number in self.page_table:
            del self.page_table[page_number]
            print(f"页面{page_number}已被回收")

# 示例：内存管理单元初始化和页面操作
mmu = MemoryManagementUnit()
mmu.allocate_page(1, 100)
mmu.access_page(1)
mmu.release_page(1)
