"""
@Name:        common
@Description: ''
@Author:      Lucas Yu
@Created:     2018/9/13
@Copyright:   ©GYENNO Technology,Shenzhen,Guangdong 2018
@Licence:
"""

import collections
import json, path


# 继承字典类，特异化成属性类，通过名字明确其在应用总的作用。
class MyProperties(collections.OrderedDict):
    def __init__(self):
        super().__init__()

    def parse(self, json_str):
        js_str = " ".join([i.strip() for i in filter(lambda x: x != "", json_str.split("\n"))])
        try:
            js = json.loads(js_str,object_pairs_hook=collections.OrderedDict)
            for key in js.keys():
                self.setdefault(key, js.get(key))
            return self
        except Exception as e:
            print("maybe exist solo quote in the json str!")
            js = json.loads(js_str.replace("\'","\""), object_pairs_hook=collections.OrderedDict)
            for key in js.keys():
                self.setdefault(key, js.get(key))
            return self


# 业务层
class MyProcessor(object):
    """在处理器之前或者之后做一些工作,不打算将其放入processor内，而是将其分割开来，尽量保证处理逻辑的单纯性。
    """
    def __init__(self, name=None, dependencies=None, reset=False):
        # 创建对象时赋值的参数，不会修改的
        self.class_name = self.__class__.__name__
        self.name = name if name is not None else self.class_name
        self.dependencies = []
        self.reset = reset
        # 由图调用接口方法赋值的参数
        self.output_destination = None
        # 由会话调用接口方法赋值的参数
        self.request = None
        # 外界通过设置接口修改的参数
        self.para = MyProperties()
        self.para['max_workers'] = 4
        if dependencies:
            if isinstance(dependencies, str):
                self.dependencies.append(dependencies)
            elif isinstance(dependencies, (list, tuple)):
                self.dependencies.extend(dependencies)
            else:
                raise Exception("输入正确依赖名，字符串或者列表")

    def set_output_destination(self, output_destination):
        """设置节点数据存储位置方法
        给图对象使用"""
        if not path.Path(output_destination).exists():
            path.Path(output_destination).makedirs_p()
        self.output_destination = path.Path(output_destination)

    def get_output_destination(self):
        if not self.output_destination:
            print("请输入输出地址！")
            return None
        else:
            return self.output_destination

    def accept(self, request):
        self.request = request

    def output(self, old_name, new_name):
        pass

    def prepare(self):
        pass

    def process(self):
        pass


class MyCalculator(object):
    def __init__(self, name=None):
        self.class_name = self.__class__.__name__
        self.name = name if name is not None else self.class_name
        self.para = MyProperties()

    def calculate(self, msg):
        pass


class MyConfig(object):

    def get_bean(self, name):
        print(self.__dir__())
        dic = self.__dir__()
        for attr in dic:
            if str(name).lower() in str(attr).lower():
                return getattr(self, attr)()
        else:
            raise Exception("not found you wanted! no this name object!")