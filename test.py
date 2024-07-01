import networkx as nx

# 创建有向图
G = nx.DiGraph()

# 添加边及其容量和费用
edges = [
    ('A1','B1',4,6), ('A2','B1',8,5),
 ('A2','B2',7,7), ('A3','B2',8,10),
 ('B1','C1',10,7),('B1','C2',3,3),
('B2','C1',4,5),('B2','C2',15,6),
('B1','B1',5,4),
]

for u, v, capacity, cost in edges:
    G.add_edge(u, v, capacity=capacity, weight=cost)

# 最小费用最大流算法
flow_cost, flow_dict = nx.network_simplex(G)

print("最小费用最大流的总费用：", flow_cost)
print("流量分配：")
for u, v, data in G.edges(data=True):
    print(f"{u} -> {v}: {flow_dict[u][v]} (cost: {data['weight']}, capacity: {data['capacity']})")

# 流量为22的最小费用
G.add_node('source', demand=-22)
G.add_node('sink', demand=22)

# 重新定义流量需求
for source in ['A1', 'A2', 'A3']:
    G.add_edge('source', source, capacity=float('inf'), weight=0)

for sink in ['C1', 'C2']:
    G.add_edge(sink, 'sink', capacity=float('inf'), weight=0)

flow_cost_22, flow_dict_22 = nx.network_simplex(G)

print("流量为22的最小费用：", flow_cost_22)
print("流量分配：")
for u, v, data in G.edges(data=True):
    if flow_dict_22[u][v] > 0:
        print(f"{u} -> {v}: {flow_dict_22[u][v]} (cost: {data['weight']}, capacity: {data['capacity']})")
