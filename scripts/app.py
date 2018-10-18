"""
@Name:        app
@Description: 编写一个启动命令
@Author:      Lucas Yu
@Created:     2018/9/13
@Copyright:   (c) GYENNO Science,Shenzhen,Guangdong 2018
@Licence:
"""
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import networkx as nx
from dl4FoG.commons.scheduler import AppGraph
from dl4FoG.commons.common import MyProcessor

p0 = MyProcessor(name='p0', dependencies=None, reset=False)
p1 = MyProcessor(name='p1', dependencies=None, reset=False)
p2 = MyProcessor(name='p2', dependencies=['p0', 'p1'], reset=False)
p3 = MyProcessor(name='p3', dependencies=['p1', 'p2'], reset=False)
p4 = MyProcessor(name='p4', dependencies=['p2', 'p3'], reset=False)
p5 = MyProcessor(name='p5', dependencies=['p3'], reset=False)

graph = AppGraph()

graph.add_processor(p1)
graph.add_processor(p2)
graph.add_processor(p3)
graph.add_processor(p4)
graph.add_processor(p5)


print('============')
print(list(graph.di_graph.edges()))
print(list(graph.di_graph.nodes()))
print(graph.di_graph.predecessors('p4'))
for k, v in graph.node_gen_result_path_map.items():
    print(k, v)

print(list(nx.bfs_predecessors(graph.di_graph,'p3')))
print(list(nx.dfs_successors(graph.di_graph, 'p3')))
print('------')
print(list(nx.predecessor(graph.di_graph, 'p4')))
print(nx.ancestors(graph.di_graph, 'p4'))
print(nx.descendants(graph.di_graph, 'p2'))
print('--------')
G=graph.di_graph
print('-->', nx.ancestors(G,'p1'))
print(G.predecessors('p4'),G.successors('p2'))
sg = nx.subgraph(G, list(nx.ancestors(graph.di_graph, 'p4'))+['p4'])
print(nx.topological_sort(nx.subgraph(G,list(G.predecessors('p4'))+['p4'])))
print(nx.topological_sort(sg))
print(nx.topological_sort(G))
print('======================')

for node in ['p0','p1','p2','p3','p4','p5']:
    print(G.predecessors(node))
#print(list(nx.descendants(graph.di_graph,'p1')))
#print(list(graph.di_graph.successors_iter('p1')))
#nx.descendants()
plt.subplot(121)



nx.draw(sg, nx.spring_layout(sg),font_weight='bold', with_labels=True)

plt.show()

#nx.draw(graph.di_graph, font_weight='bold', with_labels=True)
plt.show()
