"""
@Name:        HAPPipeline
@Description: 定义一个流程逻辑
@Author:      Lucas Yu
@Created:     2018/9/13
@Copyright:   (c) GYENNO Science, Shenzhen, Guangdong 2018
@Licence:
"""
import joblib
import numpy as np
import pandas as pd

from dl4FoG.commons.common import MyProcessor


# 到了服务这个粒度上是否该使用return返回？
# 定义数据提供类
class DataSupplier(MyProcessor):
    def __init__(self, name=None, dependencies=None, reset=False):
        super().__init__(name, dependencies, reset)

    def set_para_with_prop(self, my_props):
        self.para.setdefault("SIGNALS", None)
        self.para.setdefault("DATADIR", None)
        self.para.update(my_props)

    def process(self, msg):
        """
        Obtain the dataset from multiple files. Returns: X_train, X_test, y_train, y_test
        """
        X_train, X_test = self.__load_signals('train'), self.__load_signals('test')
        y_train, y_test = self.__load_y('train'), self.__load_y('test')
        print(self.get_output_destination())
        joblib.dump((X_train, X_test, y_train, y_test), self.get_output_destination().joinpath('result'))

    def __load_signals(self, subset):
        signals_data = []
        for signal in self.para['SIGNALS']:
            DATADIR = self.para["DATADIR"]

            filename = f'{DATADIR}/{subset}/Inertial Signals/{signal}_{subset}.txt'
            print(self.para['SIGNALS'], DATADIR, signal,filename)
            signals_data.append(pd.read_csv(open(filename), delim_whitespace=True, header=None).as_matrix())
    # Transpose is used to change the dimensionality of the output,
    # aggregating the signals by combination of sample/timestep.
    # Resultant shape is (7352 train/2947 test samples, 128 timesteps, 9 signals)
        return np.transpose(signals_data, (1, 2, 0))

    def __load_y(self, subset):
        """
        The objective that we are trying to predict is a integer, from 1 to 6,
        that represents a human activity. We return a binary representation of
        every sample objective as a 6 bits vector using One Hot Encoding
        (https://pandas.pydata.org/pandas-docs/stable/generated/pandas.get_dummies.html)
        """
        DATADIR = self.para["DATADIR"]
        filename = f'{DATADIR}/{subset}/y_{subset}.txt'
        y = pd.read_csv(open(filename), delim_whitespace=True, header=None)[0]

        return pd.get_dummies(y).as_matrix()