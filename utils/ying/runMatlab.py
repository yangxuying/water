# -*- coding:utf-8 -*-
# import matlab.engine


def runQualityAnalysis(data, type):
    # neg = matlab.engine.start_matlab()
    if type == 'FCM':
        res = [[]]
        # res = neg.FCM(matlab.double(data), 5)
    elif type == 'FCE':
        res = [[]]
        # res = neg.FCE(matlab.double(data), nargout=1)
    elif type == 'WQI':
        res = [[]]
        # res = neg.WQI(matlab.double(data))
    elif type == 'SSO':
        res = [[]]
        # res = neg.SSO(matlab.double(data), matlab.double([0.98254, 0.80668, 0.87348, 0.99813, 0.99364]))
    else:
        res = None
    # neg.exit()
    res = [[1, 2, 3, 4, 5, 5, 4, 3, 2, 1]]
    return res[0]
