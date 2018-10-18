"""
@Name:        app2
@Description: ''
@Author:      Lucas Yu
@Created:     2018/10/17
@Copyright:   ©GYENNO Technology,Shenzhen,Guangdong 2018
@Licence:
"""

f1=r'E:\my_proj\fog_recognition\fog_opt\SignalETL4FoG'
f2=r'E:\my_proj\fog_recognition\fog_opt\VideoMark'
import path
from collections import OrderedDict
fn1=path.Path(f1)
fn2=path.Path(f2)
fn2=path.Path(f2).files()
fn1=path.Path(f1).files()

f=open(r'E:\my_proj\fog_recognition\fog_opt\tmp2.txt','w')

li=[]

f=open(r'E:\my_proj\fog_recognition\fog_opt\tmp3.txt','w')

c=0
for k,v in zip(fn1,fn2):
    c+=1
    d=[]

    d.extend(['id:pd{:0>6d}'.format(c),'signal:${SIGNAL_PATH}/'+path.Path(k).basename(),'video:${VIDEO_PATH}/'+path.Path(v).basename()])
    print('{'+', '.join(d)+'}')
    f.write(str(d))
    f.write('\n')


