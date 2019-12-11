import pandas as pd
import re
from sklearn.svm import SVR
import time
import numpy as np
import matplotlib.pyplot as plt
import pickle
import neuralNetwork

def transform_to_day(str):
    labels = ['年', '月', '天', '时']
    nums = []
    label_list = []
    str_tmp = ""
    for i in str:
        if i in labels:
            label_list.append(i)
            nums.append(str_tmp)
            str_tmp = ""
        else:
            str_tmp += i
    res_day = 0
    for i in range(len(nums)):
        if label_list[i] == '年':
            res_day += int(nums[i])*365
        elif label_list[i] == '月':
            res_day += int(nums[i])*30
        elif label_list[i] == '天':
            res_day += int(nums[i])
        else:
            res_day += int(nums[i])/24
    return res_day

def transform_to_GB(str):
    unit = str[-2]
    num = float(str[:-2])
    res_GB = 0
    if unit == 'T':
        res_GB += num*1024
    elif unit == 'G':
        res_GB += num
    else:
        res_GB += num/1024
    return res_GB

def transform_to_int(str):
    if str is str:
        nums = str.replace(',', '')
        return int(nums)
    else:
        return int(str)

def get_data(piece_range_start=50, piece_range_over=100):
    with open('torrent_information.csv', encoding='UTF-8') as csvfile:
        data_x = pd.read_csv("torrent_information.csv", usecols=['size', 'seeders', 'downloaders'])
        data_y = pd.read_csv("torrent_information.csv", usecols=['size', 'finished_num'])
        y_vector_train = []
        data_x_train = np.array(data_x[piece_range_start:piece_range_over])
        data_y_train = np.array(data_y[piece_range_start:piece_range_over])
        #type(data_x)=pandas DataFrame, type(data_x_train)=list
        row, _ = data_x_train.shape
        for i in range(row):
            data_x_train[i][0] = transform_to_GB(data_x_train[i][0])
            data_x_train[i][1] = int(data_x_train[i][1])
            data_x_train[i][2] = int(data_x_train[i][2])
            y_vector_train.append(int(data_y_train[i][1]) * transform_to_GB(data_y_train[i][0]))
        return data_x_train, y_vector_train

def svr_train(piece_range_start=50, piece_range_over=100):
    data_x_train, y_vector_train = get_data(piece_range_start, piece_range_over)
    svr = SVR(kernel='linear', degree=3, gamma='auto', coef0=0.0, tol=0.001, C=1.0, epsilon=0.1, shrinking=True,
            cache_size=200, verbose=False, max_iter=-1)
    svr.fit(data_x_train, y_vector_train)
    with open('./models/svr_model.pkl', 'wb') as f:
        print("[train]is saving the model as ./models/svr_model.pkl")
        pickle.dump(svr, f)
        print("[train]save successfully")

def svr_test(model_adress, piece_range_start=0, piece_range_over=10):
    data_x_test, y_vector_test = get_data(piece_range_start, piece_range_over)
    with open(model_adress, 'rb') as f:
        print("[model]is opening the model, {}".format(model_adress))
        model = pickle.load(f)
    y_test = model.predict(data_x_test)
    return y_test

def nn_train(piece_range_start=50, piece_range_over=100, input_nodes=3, hidden_nodes=7, output_nodes=1, learning_rate=0.03):
    start = time.time()
    data_x_train, y_vector_train = get_data(piece_range_start, piece_range_over)
    #print(data_x_train)
    max_value = [max(data_x_train[:, 0]), max(data_x_train[:, 1]), max(data_x_train[:, 2]), max(y_vector_train)]
    row, col = data_x_train.shape
    print("[train]data_x_train.shape={}".format(data_x_train.shape))
    print("[train]len(y_vector_train)={}".format(len(y_vector_train)))
    net = neuralNetwork.neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)
    for i in range(row):
        for m in range(col):
            data_x_train[i, m] = data_x_train[i, m] / max_value[m] * 0.99 + 0.01
        y_vector_train[i] = y_vector_train[i]/max_value[3]*0.99+0.01
        net.train(data_x_train[i], y_vector_train[i])
    print("[train]train spent", (time.time() - start), "s")
    save_nn_data = net.nn_dump()
    save_nn_data.append(max_value)
    with open('./models/nn_model.pkl', 'wb') as f:
        print("[train]is saving the model as ./models/nn_model.pkl")
        pickle.dump(save_nn_data, f)
        print("[train]save successfully")

def nn_test(model_adress, piece_range_start=0, piece_range_over=10):
    data_x_test, y_vector_test = get_data(piece_range_start, piece_range_over)
    net = neuralNetwork.neuralNetwork()
    with open(model_adress, 'rb') as f:
        print("[model]is opening the model, {}".format(model_adress))
        nn_para = pickle.load(f)
        net.nn_load(nn_para[0], nn_para[1], nn_para[2], nn_para[3], nn_para[4], nn_para[5])
        max_value = nn_para[6]
    y_test = []
    for x_test in data_x_test:
        x_test[0] = x_test[0]/max_value[0]*0.99+0.01
        x_test[1] = x_test[1]/max_value[1]*0.99+0.01
        x_test[2] = x_test[2]/max_value[2]*0.99+0.01
        y_test.append(net.query(x_test).tolist()[0][0])
    return y_test

if __name__ == '__main__':
    #svr
    '''''
    svr_train()
    print(test("./models/svr_model.pkl", 0, 10))
    '''''
    #nn
    nn_train()
    nn_test("./models/nn_model.pkl", 0, 10)