"""
@Name:        Controllers
@Description: 定义一个节点的功能，并供外界调用,节点功能具有独立性
@Description: 外界设置参数的接口，接受请求后的准备工作，处理接口，输出接口
@Author:      Lucas Yu
@Created:     2018/9/13
@Copyright:   (c) GYENNO Science, Shenzhen, Guangdong 2018
@Licence:
"""
import path
from collections import deque
from dl4FoG.commons.common import MyProcessor


# 类内方法共享属性-局部公共变量
class SignalMarkNode(MyProcessor):
    def __init__(self, name=None, dependencies=None, reset=False):
        super().__init__(name, dependencies, reset)

    def set_para_with_prop(self, my_props):
        self.para.setdefault("SignalMarker", None)
        self.para.update(my_props)

    def output(self, old_name, new_name=None, data_id=None):
        if not data_id:
            data_id = old_name.split('==')[0]
        result_name = path.Path(data_id).joinpath(new_name) if new_name else old_name
        return path.Path(self.get_output_destination()).joinpath(data_id+'=='+result_name)

    def prepare(self):
        # 相当于输入函数input_fn，准备数据之外，还可以做些其他工作
        from ..commons.helper import ProcessorHelper
        data = self.request['feed_dict'][self.name]
        data_tmp = [it for it in data if not ProcessorHelper.input_whose_output_exist(self, it.get('id'))]
        self.request['feed_dict'][self.name] = data_tmp

    def process(self):
        from concurrent import futures
        data = deque(self.request['feed_dict'][self.name])
        with futures.ThreadPoolExecutor(max_workers=self.para['max_workers']) as executor:
            future_to_it = {executor.submit(self.para["SignalMarker"].calculate, it): it for it in data}
            for future in futures.as_completed(future_to_it):
                it = future_to_it[future]
                future.result().to_csv(self.output(path.Path(it['signal']).basename(), data_id=it['id']),index=False)


