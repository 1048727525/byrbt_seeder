import argparse
import json
import os
import time
import pandas as pd
import shutil
import csv
import udp_client
import train
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

def del_space(str):
    str = str.rstrip()
    str = str.lstrip()
    return str

def del_r_l(str, del_l, del_r):
    str = str.rstrip(del_r)
    str = str.lstrip(del_l)
    return str

def get_transmission_list(args):
    now_path = os.getcwd()
    print("[transmission]updating state.txt")
    os.system("transmission-remote -n '{}:{}' -l>{}/state.txt".format(args.rpc_username, args.rpc_password, now_path))
    txt_lines = []
    with open('state.txt', 'r') as file:
        txt_lines = file.readlines()
    keys = list(filter(None, txt_lines[0].split(" ")))
    keys[-1] = keys[-1].rstrip('\n')
    sum_line_list = list(filter(None, txt_lines[-1].split(" ")))
    sum_line_list[-1] = sum_line_list[-1].rstrip('\n')
    info_dic = {}
    for i in keys:
        info_dic[i] = []
    for i in txt_lines[1:-1]:
        tmp_list = list(filter(None, i.split("  ")))
        tmp_list[-1] = tmp_list[-1].rstrip('\n')
        info_dic[keys[0]].append(del_space(tmp_list[0]))
        info_dic[keys[1]].append(del_space(tmp_list[1]))
        info_dic[keys[2]].append(del_space(tmp_list[2]))
        info_dic[keys[3]].append(del_space(tmp_list[3]))
        info_dic[keys[4]].append(del_space(tmp_list[4]))
        info_dic[keys[5]].append(del_space(tmp_list[5]))
        info_dic[keys[6]].append(del_space(tmp_list[6]))
        info_dic[keys[7]].append(del_space(tmp_list[7]))
        info_dic[keys[8]].append(del_space(tmp_list[8]))
    return info_dic

if __name__ == '__main__':
    print("[initialize]data in time.py is initializing")
    start = time.time()
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_download_space', type=float, default=50)
    parser.add_argument('--update_seed_queue_time', type=float, default=12)
    parser.add_argument('--seed_select_strategy', type=int, default=0)
    parser.add_argument('--max_seed_selected_num', type=int, default=5)
    parser.add_argument('--rpc_username', type=str, default='transmission')
    parser.add_argument('--rpc_password', type=str, default='123456')
    parser.add_argument('--download_prices', type=str, default='123456')
    parser.add_argument('--update_seed_num', type=int, default=100)
    parser.add_argument('--username', type=str)
    parser.add_argument('--password', type=str)
    args = parser.parse_args()
    with open('transmission_settings.json', 'r') as file:
        info = json.load(file)
    init_time = 0
    if "init_time" in info.keys():
        init_time = info["init_time"]
    if "stop_label" in info.keys():
        info["stop_label"] = 0
    with open('transmission_settings.json', 'w') as file:
        json.dump(info, file, indent=4, sort_keys=True)
    max_seed_selected_num = args.max_seed_selected_num
    seed_select_strategy = args.seed_select_strategy
    max_download_space = args.max_download_space
    download_prices = args.download_prices
    update_seed_queue_time = args.update_seed_queue_time
    rpc_username = args.rpc_username
    rpc_password = args.rpc_password
    update_seed_num = args.update_seed_num
    print("[initialize]data initialization in time.py has finished, costing {}s".format(time.time()-start))
    print("[info]max_download_space={}GB".format(max_download_space))
    print("[info]update_seed_queue_time={}h".format(update_seed_queue_time))
    print("[info]seed_select_strategy={}".format(seed_select_strategy))
    print("[info]max_seed_selected_num={}".format(max_seed_selected_num))
    print("[info]rpc_username={}".format(rpc_username))
    print("[info]rpc_password={}".format(rpc_password))
    print("[info]download_prices={}".format(download_prices))
    print("[info]update_seed_num={}".format(update_seed_num))
    print("[info]init_time={}s".format(info["init_time"]))
    while True:
        with open('transmission_settings.json', 'r') as file:
            info = json.load(file)
        if "stop_label" in info.keys() and info["stop_label"] == 1:
            info["init_time"] = time.time()-start_time+init_time
            print("******programmer is quited at {}******".format(time.strftime("%Y-%m-%d/%H:%M:%S", time.localtime(time.time()))))
            break
        time.sleep(1)
        if time.time()-start_time+init_time - args.update_seed_queue_time * 3600>0:
            start = time.time()
            print("[update]update seeds...")
            init_time = 0
            start_time = time.time()
            #正式使用时，请将下一句的注释去除。测试代码时为了节约时间可将下行代码注释掉
            ##hit.main(args.update_seed_num, args.username, args.password)
            #更新种子至文件夹./torrent_tmp
            print("[grade]grading is starting")
            with open('torrent_information.csv', encoding='UTF-8') as csvfile:
                data_list = pd.read_csv("torrent_information.csv", usecols=['seed_name', 'torrent_name', 'size', 'price'])
            ##评分策略
            if seed_select_strategy==0:
                print("[grade]the strategy is default")
                data_list = data_list.to_dict(orient='records')
                print("[grade]grade list is {}".format(len(data_list)))
                for i,item in enumerate(data_list):
                    data_list[i]['score'] = 0
            #nn
            elif seed_select_strategy==1:
                print("[grade]the strategy is neural network")
                if os.path.exists("./models/nn_model.pkl")==False:
                    raise RuntimeError("error:there is not nn_model.pkl in models")
                else:
                    data_list = data_list.to_dict(orient='records')
                    piece_range_over = len(data_list)
                    scores = train.nn_test("./models/nn_model.pkl", 0, piece_range_over)
                    print("[grade]grade list is {}".format(len(data_list)))
                    max_score = max(scores)
                    print("[grade]grading is finished, max_score={}, costing{}".format(max_score, time.time()-start))
                    for i, item in enumerate(data_list):
                        data_list[i]['score'] = float(scores[i] / max_score * 100)
            #SVC
            elif seed_select_strategy==2:
                print("[grade]the strategy is SVC")
                if os.path.exists("./models/svr_model.pkl")==False:
                    raise RuntimeError("error:there is not svr_model.pkl in models")
                else:
                    data_list = data_list.to_dict(orient='records')
                    piece_range_over = len(data_list)
                    scores = train.svr_test("./models/svr_model.pkl", 0, piece_range_over)
                    print("[grade]grade list is {}".format(len(data_list)))
                    max_score = max(scores)
                    print("[grade]grading is finished, max_score={}, costing{}".format(max_score, time.time()-start))
                    for i, item in enumerate(data_list):
                        data_list[i]['score'] = float(scores[i]/max_score*100)
            #更新完成，抛出信号
            print("[udp]throw signal, update successfully")
            udp_client.main('127.0.0.1', 8888, 'update successfully')
            with open('scored_torrent_information.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
                torrentwriter = csv.writer(csvfile, dialect='excel')
                torrentwriter.writerow(['rank']+['seed_name']+['torrent_name']+['size']+['price']+['score'])
                for i, item in enumerate(data_list):
                    torrentwriter.writerow([i+1]+[item['seed_name']]+[item['torrent_name']]+[item['size']]+[item['price']]+[item['score']])
            used_space = 0
            res_seeds_name = []
            res_seeds = []
            _res_id = []
            _sizes = []
            for i, item in enumerate(data_list):
                if used_space + transform_to_GB(item['size']) < max_download_space and str(item["price"]) in download_prices:
                    res_seeds.append(item["torrent_name"])
                    res_seeds_name.append(item["torrent_name"][8:-8])
                    _res_id.append(i)
                    _sizes.append(transform_to_GB(item['size']))
                    used_space = used_space + transform_to_GB(item['size'])
                if len(res_seeds_name) == max_seed_selected_num:
                    break
            seeds_info = get_transmission_list(args)
            for i, src in enumerate(seeds_info["Name"]):
                if (src in res_seeds_name) == False:
                    print("[update]removing ID={}".format(seeds_info["ID"][i]))
                    os.system("transmission-remote -n '{}:{}' -t {} --remove-and-delete".format(args.rpc_username, args.rpc_password, del_r_l(seeds_info["ID"][i], "", "*")))
            #seeds_info = get_transmission_list(args)
            print("[info]res_seeds={}".format(res_seeds_name))
            print("[info]seeds_info={}".format(seeds_info["Name"]))
            seeds_info = get_transmission_list(args)
            for i, src in enumerate(res_seeds_name):
                #print(src in seeds_info["Name"])
                if (src in seeds_info["Name"]) == True:
                    print("[update]True, {} keeps downloading".format(src))
                if (src in seeds_info["Name"]) == False:
                    print("[update]False, {} needs to be removed".format(src))
                    shutil.copy("./torrent_tmp/{}".format(res_seeds[i]), "{}/{}".format(info["watch-dir"], res_seeds[i]))
            print("[update]updating has finished, costing {}s".format(time.time() - start))
    with open('transmission_settings.json', 'w') as file:
        json.dump(info, file, indent=4, sort_keys=True)


