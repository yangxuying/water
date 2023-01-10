import numpy as np
import pandas as pd
from numpy import *


def data_clean(name_path, label_name):  # 数据预处理
    # df = pd.read_csv(name_path)
    df = name_path
    # 选择对应指标进行预处理
    series = df[label_name].values
    # series = series - np.mean(series)  # 中心化(非必须)
    # step1 嵌入
    windowLen = 90  # 嵌入窗口长度
    seriesLen = len(series)  # 序列长度
    K = seriesLen - windowLen + 1
    X = np.zeros((windowLen, K))
    for i in range(K):
        X[:, i] = series[i:i + windowLen]

    # step2: svd分解， U和sigma已经按升序排序
    U, sigma, VT = np.linalg.svd(X, full_matrices=False)
    for i in range(VT.shape[0]):
        VT[i, :] *= sigma[i]
    A = VT

    # 重组
    rec = np.zeros((windowLen, seriesLen))
    for i in range(windowLen):
        for j in range(windowLen - 1):
            for m in range(j + 1):
                rec[i, j] += A[i, j - m] * U[m, i]
            rec[i, j] /= (j + 1)
        for j in range(windowLen - 1, seriesLen - windowLen + 1):
            for m in range(windowLen):
                rec[i, j] += A[i, j - m] * U[m, i]
            rec[i, j] /= windowLen
        for j in range(seriesLen - windowLen + 1, seriesLen):
            for m in range(j - seriesLen + windowLen, windowLen):
                rec[i, j] += A[i, j - m] * U[m, i]
            rec[i, j] /= (seriesLen - j)
    refactoring_data = np.sum(rec[0:37, :], axis=0)
    # 返回最终预处理后的文件
    return refactoring_data


def water_predict1(data, indicator):  # 模型名：Online_ESN预测模型  indicator：水质指标

    # 设置训练集长度
    trainLen = len(data)
    initLen = 45

    if indicator == '溶解氧':
        inSize = 4  # inSize 输入维数 K
        outSize = 3
        resSize = 130  # 储备池规模 N
        a = 0.9600000000000001  # 可以看作储备池更新的速度，可不加，即设为1.
        sr = 0.45
        IS = 0.1
        proba_non_zero_connec_W = 0.01
    if indicator == '高锰酸盐指数':
        inSize = 4  # inSize 输入维数 K
        outSize = 3
        resSize = 130  # 储备池规模 N
        a = 0.9600000000000001  # 可以看作储备池更新的速度，可不加，即设为1.
        sr = 0.45
        IS = 0.1
        proba_non_zero_connec_W = 0.01
    if indicator == '总磷':
        inSize = 4  # inSize 输入维数 K
        outSize = 3
        resSize = 130  # 储备池规模 N
        a = 0.9600000000000001  # 可以看作储备池更新的速度，可不加，即设为1.
        sr = 0.45
        IS = 0.1
        proba_non_zero_connec_W = 0.01

    lamda = 1  # 遗忘因子
    alpha_coef = 1e-8

    train_in = data[:trainLen - outSize]
    train_out = data[inSize:trainLen]

    random.seed(42)
    Wfb = np.random.rand(resSize, outSize) - 0.5
    Win = (np.random.rand(resSize, 1 + inSize) - 0.5) * IS
    W = (np.random.rand(resSize, resSize) - 0.5)
    mask = np.random.rand(resSize, resSize)
    W[mask > proba_non_zero_connec_W] = 0
    p_wr = max(abs(linalg.eig(W)[0]))  # Spectral radius of W
    W = (sr * W) / p_wr
    Wout = np.zeros((outSize, Win.shape[1] + resSize))
    P = np.asmatrix(np.eye(resSize + Win.shape[1])) / alpha_coef
    x = zeros((resSize, 1))
    y0 = np.zeros((outSize, 1))

    for t in range(len(train_in) - inSize + 1):
        u = train_in[t:t + inSize]
        u = u.reshape(inSize, 1)
        x = (1 - a) * x + a * tanh(dot(Win, np.vstack((1, u))) + dot(W, x) + dot(Wfb, y0))
        state = np.vstack((1, x, u))
        if t >= initLen:
            y = train_out[t:t + outSize]
            y = y.reshape(outSize, 1)
            y0 = dot(Wout, state)
            e = y - y0  # 计算误差
            xTP = state.T @ P
            P = P - (P @ state @ xTP) / (lamda + np.dot(xTP, state))
            Wout = Wout + e * np.dot(P, state).T

        if t == (len(train_in) - inSize + 1):
            u = data[trainLen - inSize:trainLen]
            u = u.reshape(inSize, 1)
            x = (1 - a) * x + a * tanh(dot(Win, np.vstack((1, u))) + dot(W, x) + dot(Wfb, y0))
            state = np.vstack((1, x, u))
            y0 = dot(Wout, state)

    return y0


def water_predict2(data, indicator):  # 模型名：Offline_ESN预测模型
    # 设置训练集
    trainLen = len(data)
    initLen = 45

    # 设置超参数
    if indicator == '溶解氧':
        inSize = 6
        outSize = 3
        resSize = 140
        sr = 1.35
        a = 0.97
        reg = 0.001
        IS = 0.05
        proba_non_zero_connec_W = 0.1
    if indicator == '高锰酸盐指数':
        inSize = 6
        outSize = 3
        resSize = 140
        sr = 1.35
        a = 0.97
        reg = 0.001
        IS = 0.05
        proba_non_zero_connec_W = 0.1
    if indicator == '总磷':
        inSize = 6
        outSize = 3
        resSize = 140
        sr = 1.35
        a = 0.97
        reg = 0.001
        IS = 0.05
        proba_non_zero_connec_W = 0.1

    # 设置训练集
    train_in = data[:trainLen - outSize]

    # 随机初始化 Win 和 W
    np.random.seed(42)
    Win = (np.random.rand(resSize, 1 + inSize) - 0.5) * IS
    W = np.random.rand(resSize, resSize) - 0.5
    # 对W进行防缩，以满足稀疏的要求。
    mask = np.random.rand(resSize, resSize)
    W[mask > proba_non_zero_connec_W] = 0
    rhoW = max(abs(np.linalg.eig(W)[0]))
    W = W * sr / rhoW
    X = np.zeros((1 + inSize + resSize, len(train_in) - inSize + 1 - initLen))
    Y = np.vstack((data[inSize + initLen:trainLen - outSize + 1], data[1 + inSize + initLen:trainLen - outSize + 2],
                   data[2 + inSize + initLen:trainLen - outSize + 3]))

    x = np.zeros((resSize, 1))
    for t in range(len(train_in) - inSize + 1):
        u = train_in[t:t + inSize]
        u = u.reshape(inSize, 1)
        x = (1 - a) * x + a * np.tanh(np.dot(Win, np.vstack((1, u))) + np.dot(W, x))
        if t >= initLen:
            X[:, t - initLen] = np.vstack((1, x, u))[:, 0]
    X_T = X.T
    Wout = np.dot(np.dot(Y, X_T), np.linalg.inv(np.dot(X, X_T) + \
                                                reg * np.eye(
        1 + inSize + resSize)))
    u = data[trainLen - inSize:trainLen]
    u = u.reshape(inSize, 1)
    x = (1 - a) * x + a * np.tanh(np.dot(Win, np.vstack((1, u))) + np.dot(W, x))
    y = np.dot(Wout, np.vstack((1, x, u)))
    return y

# if __name__ == "__main__":
#     import datetime
#     now = datetime.datetime.now()
#     date1 = now + datetime.timedelta(days=1)
#     date2 = now + datetime.timedelta(days=2)
#     date3 = now + datetime.timedelta(days=3)
#
#     path = '重构数据.csv'
#     data1 = data_clean(path,'溶解氧')
#     predict_value11 = water_predict1(data1)
#     data2 = data_clean(path,'高锰酸盐')
#     predict_value21 = water_predict1(data2)
#     data3 = data_clean(path,'总磷,')
#     predict_value31 = water_predict1(data3)
#
#     data1 = data_clean(path,'溶解氧')
#     data2 = data_clean(path,'高锰酸盐')
#     data3 = data_clean(path,'总磷,')
#     predict_value12 = water_predict2(data1)
#     predict_value22 = water_predict2(data2)
#     predict_value32 = water_predict2(data3)
