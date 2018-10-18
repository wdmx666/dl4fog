"""
@Name:        scheduler
@Description: ''
@Author:      Lucas Yu
@Created:     2018/9/13
@Copyright:   ©GYENNO Technology,Shenzhen,Guangdong 2018
@Licence:
"""

import networkx as nx
import path


class AppGraph(object):
    def __init__(self):
        self.para = dict()
        self.node_gen_result_path_map = {}
        self.processors = dict()
        self.di_graph = nx.DiGraph()

    def set_para_with_prop(self, my_props):
        self.para.update(my_props)

    def remove_processor(self, processor):
        """同时删除掉依赖于processor存在的hooker"""
        self.processors.pop(processor.name)
        self.di_graph.remove_node(processor.name)
        return self

    def add_processor(self, processor, url=None):
        self.processors.update({processor.name: processor})
        # 添加图节点
        self.di_graph.add_node(processor.name)
        # 添加图边缘线
        if processor.dependencies:
            for dp in processor.dependencies:
                self.di_graph.add_edge(dp, processor.name)
        # 若节点路径在表中则使用，否则默认方式创建
        if url:
            self.node_gen_result_path_map[processor.name] = path.Path(url)
        else:
            self.node_gen_result_path_map[processor.name] = path.Path('../data').abspath().joinpath(processor.name)
        # 检查路径是否存在，否则创建
        _pn = self.node_gen_result_path_map[processor.name]
        if not _pn.exists():
                _pn.makedirs_p()
        # 设置节点输出位置，节点只接受会话的调度
        processor.set_output_destination(_pn)
        return self


class AppSession(object):
    def __init__(self, parallel_num=4):
        pass

    @staticmethod
    def __find_node_dependencies(di_graph, node, near_mode):
        if near_mode:
            sg = nx.subgraph(di_graph, list(nx.ancestors(di_graph, node)) + [node])
        else:
            sg = nx.subgraph(di_graph, list(di_graph.predecessors(node)) + [node])
        return nx.topological_sort(sg)

    @staticmethod
    def __reset_node(app_graph, processor):
        # 设置重置，清空
        if processor.reset:
            pn = path.Path(app_graph.node_gen_result_path_map[processor.name])
            for item in pn.listdir():
                if item.isdir():
                    item.rmtree_p()
                else:
                    item.remove_p()

    def run(self, app_graph, node, feed_dict={}, near_mode=False):
        sorted_nodes = self.__find_node_dependencies(app_graph.di_graph, node, near_mode)
        for node in sorted_nodes:
            processor = app_graph.processors[node]
            self.__reset_node(app_graph, processor)
            predecessors = app_graph.di_graph.predecessors(node)
            data = {'predecessors': predecessors, 'feed_dict': feed_dict}
            print("==============================================")
            processor.accept(data)
            print("==========================================")
            processor.prepare()
            print("=======================================")
            processor.process()
            print("------------------------------")





