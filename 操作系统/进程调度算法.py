class Process:
    def __init__(self, pid, priority):
        self.pid = pid
        self.priority = priority
        self.state = 'ready'  # 默认状态为就绪

class Scheduler:
    def __init__(self):
        # 初始化不同优先级的队列
        self.queues = {i: [] for i in range(5)}  # 假设有5个优先级，从0到4

    def add_process(self, process):
        # 将进程添加到对应优先级的队列中
        self.queues[process.priority].append(process)

    def schedule(self):
        # 执行调度逻辑
        for priority in sorted(self.queues.keys(), reverse=True):
            if self.queues[priority]:
                # 从最高优先级队列选择进程执行
                process = self.queues[priority].pop(0)
                return process  # 返回选中的进程
        return None  # 如果所有队列都空，则返回None

    def change_process_state(self, process, new_state):
        # 改变进程状态
        process.state = new_state

# 示例：创建进程并进行调度
scheduler = Scheduler()
scheduler.add_process(Process('P1', 2))
scheduler.add_process(Process('P2', 3))
scheduler.add_process(Process('P3', 1))

# 调度进程并输出结果
scheduled_process = scheduler.schedule()
if scheduled_process:
    print(f"调度进程: {scheduled_process.pid}，优先级: {scheduled_process.priority}")
else:
    print("无进程可调度")
