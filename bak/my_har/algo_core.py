"""
@Name:        algo_core
@Description: pure algorithm stateless logic
@Author:      Lucas Yu
@Created:     2018/9/13
@Copyright:   (c) GYENNO Science, Shenzhen, Guangdong 2018
@Licence:
"""
import pandas as pd
import numpy as np


def confusion_matrix(Y_true, Y_pred):
    ACTIVITIES = {
        0: 'WALKING',
        1: 'WALKING_UPSTAIRS',
        2: 'WALKING_DOWNSTAIRS',
        3: 'SITTING',
        4: 'STANDING',
        5: 'LAYING',
    }
    Y_true = pd.Series([ACTIVITIES[y] for y in np.argmax(Y_true, axis=1)])
    Y_pred = pd.Series([ACTIVITIES[y] for y in np.argmax(Y_pred, axis=1)])

    return pd.crosstab(Y_true, Y_pred, rownames=['True'], colnames=['Pred'])