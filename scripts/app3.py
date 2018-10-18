"""
@Name:        app3
@Description: ''
@Author:      Lucas Yu
@Created:     2018/10/18
@Copyright:   ©GYENNO Technology,Shenzhen,Guangdong 2018
@Licence:
"""

import time


def show(data):
    time.sleep(4)
    return data


from concurrent import futures

if __name__ == '__main__':
    #freeze_support()
    executor0 = futures.ProcessPoolExecutor(max_workers=3)


    with futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(pow, 323, 1235)



        print(future.result())


    #future = executor0.submit(pow, 323, 1235)
    #print(future.result())

    with futures.ProcessPoolExecutor(max_workers=3) as executor:
        fts=[]

        for i in range(10):
            fts.append(executor.submit(show,i))
            print('->',i)
        for ft in futures.as_completed(fts):
            print(ft.result())
            #print(ft.result())
