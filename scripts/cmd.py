"""
@Name:        cmd
@Description: ''
@Author:      Lucas Yu
@Created:     2018/10/17
@Copyright:   ©GYENNO Technology,Shenzhen,Guangdong 2018
@Licence:
"""

from dl4FoG.my_fog.preparation import ParaConfig


graph = ParaConfig.appGraph()
sess = ParaConfig.appSession()
p1 = ParaConfig.signalMarkNode()
#p1.reset = False
graph.add_processor(p1)
print(p1.name)
sess.run(graph, p1.name, feed_dict={p1.name: ParaConfig.SIG_V_PATH})