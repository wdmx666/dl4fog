"""
@Name:        preparation
@Description: ''
@Author:      Lucas Yu
@Created:     2018/10/17
@Copyright:   (c) GYENNO Science,Shenzhen,Guangdong 2018
@Licence:
"""

from ..commons.common import MyConfig


import os
from pyhocon import ConfigFactory


# 相对静态的配置
# one code one appear
class ParaConfig(MyConfig):
    conf_path = "../dl4fog/my_fog/config/raw_input.conf"
    _d_conf = ConfigFactory.parse_file(os.path.abspath(conf_path))
    SIG_V_PATH = _d_conf['SIG_V_PATH']

# #####一些公共的服务对象##################################################################################
    @classmethod
    def appGraph(cls):
        from ..commons.scheduler import AppGraph
        graph = AppGraph()
        return graph

    @classmethod
    def appSession(cls):
        from ..commons.scheduler import AppSession
        sess = AppSession()
        return sess

    @classmethod
    def signalMarkNode(cls):
        from .controllers import SignalMarkNode
        from .services import SignalMarker
        node = SignalMarkNode(reset=True)
        node.set_para_with_prop({'SignalMarker': SignalMarker(),'max_workers':4})
        return node






