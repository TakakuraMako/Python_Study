class BankerAlgorithm:
    def __init__(self, available, max_demand, allocation):
        self.available = available
        self.max_demand = max_demand
        self.allocation = allocation
        self.need = [[max_demand[i][j] - allocation[i][j] for j in range(len(available))] for i in range(len(allocation))]

    def request_resources(self, process_id, request):
        # 检查请求是否超出了该进程的需求
        if any(request[j] > self.need[process_id][j] for j in range(len(request))):
            print(f"进程{process_id}的请求超出最大需求，请求被拒绝。")
            return False
        # 检查是否有足够的资源满足请求
        if any(request[j] > self.available[j] for j in range(len(request))):
            print(f"资源不足，进程{process_id}的请求被拒绝。")
            return False

        # 尝试分配资源
        for j in range(len(request)):
            self.available[j] -= request[j]
            self.allocation[process_id][j] += request[j]
            self.need[process_id][j] -= request[j]

        # 检查此次分配后是否安全
        is_safe, _ = self.is_safe()
        if not is_safe:
            # 如果不安全，回滚
            for j in range(len(request)):
                self.available[j] += request[j]
                self.allocation[process_id][j] -= request[j]
                self.need[process_id][j] += request[j]
            print(f"不能满足进程{process_id}的请求而保持系统安全，请求被拒绝。")
            return False
        print(f"进程{process_id}的请求被批准。")
        return True

    def is_safe(self):
        work = self.available[:]
        finish = [False] * len(self.allocation)
        safe_sequence = []

        while len(safe_sequence) < len(self.allocation):
            made_progress = False
            for i in range(len(self.allocation)):
                if not finish[i] and all(self.need[i][j] <= work[j] for j in range(len(work))):
                    for j in range(len(work)):
                        work[j] += self.allocation[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    made_progress = True

            if not made_progress:
                return False, safe_sequence
        return True, safe_sequence

    def try_to_fulfill_all(self):
        # 尝试满足所有进程的全部需求
        for process_id in range(len(self.need)):
            while not all(need == 0 for need in self.need[process_id]):
                request = self.need[process_id][:]
                if not self.request_resources(process_id, request):
                    print(f"无法安全地满足进程{process_id}的全部需求。")
                    return
        print("所有进程的需求已被安全满足。")

# 示例数据
available = [2, 1, 1]
max_demand = [
    [5, 5, 9],
    [5, 3, 6],
    [4, 0, 11],
    [4, 2, 5],
    [4, 2, 4]
]
allocation = [
    [2, 1, 2],
    [4, 0, 2],
    [4, 0, 5],
    [2, 0, 4],
    [3, 1, 4]
]

banker = BankerAlgorithm(available, max_demand, allocation)
banker.try_to_fulfill_all()