"""
@Name:        services
@Description: ''
@Author:      Lucas Yu
@Created:     2018/10/17
@Copyright:   (c) GYENNO Science,Shenzhen,Guangdong 2018
@Licence:
"""
import pandas as pd
import keras
import itertools
from ..commons.common import MyCalculator


STATUS_DEFINITION = {"fog":["A","B","C","D","F"],"normal":["H","I","J","K","N"]}
INFO_COLS = ["time10","label_start_time","label_end_time","gait_type",
             "label_confidence","stimulate_type","start_time","end_time","unit_confidence"]


def mark_signal_with_video(df_s, df_v):
    df_all = df_s.reindex(columns=list(df_s.columns)+list(df_v.columns))
    for i in df_v.index:
        v_it = df_v.loc[i,:]
        start = v_it['start_time']
        end = v_it['end_time']
        idx = df_all[(df_all['time10']>start)&(df_all['time10']<end)].index.tolist()
        df_all.loc[idx, v_it.index.tolist()]= v_it.tolist()
    return df_all


def drop_head_tail_na(df_all,col_name):
    start_id = 0
    for i in df_all.index:
        if pd.notna(df_all.loc[i,col_name]):
            start_id = i
            break
    end_id = len(df_all)
    for j in df_all.index[::-1]:
        if pd.notna(df_all.loc[j,col_name]):
            end_id = j
            break
    print(start_id, end_id)
    return df_all.loc[start_id:end_id, :]


def mark_status(it, STATUS_DEFINITION):
    status = 'normal'
    for k, lst in STATUS_DEFINITION.items():
        if it in lst:
            status = k
            break
    return status


class SignalMarker(MyCalculator):
    @staticmethod
    def __check(data):
        print(data)

    def calculate(self, msg):
        self.__check(msg)
        df_s = pd.read_csv(open(msg['signal']))
        df_v = pd.read_csv(open(msg['video']))
        df_all = mark_signal_with_video(df_s, df_v)
        df_res = drop_head_tail_na(df_all, 'end_time')
        gait_type = list(itertools.chain.from_iterable(STATUS_DEFINITION.values()))
        df_res.loc[:, 'gait_type'] = df_res['gait_type'].apply(lambda it: it if it in gait_type else 'N')
        df_res.loc[:, 'status'] = df_res['gait_type'].apply(mark_status, args=(STATUS_DEFINITION,))
        df_res.loc[:, 'status_code'] = df_res.loc[:, 'status'].apply(lambda it: 1 if it == 'fog' else 0)
        df_res.loc[:, 'one_hot'] = df_res.loc[:, 'status_code'].apply(keras.utils.to_categorical, args=(2,))

        self.__check(df_res['status_code'].value_counts())

        return df_res


