import argparse
import os
import json
import time
import socket

def get_host_ip():
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    except:
        print("error:fall to get host ip")
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    print("******programmer begins at {}******".format(time.strftime("%Y-%m-%d/%H:%M:%S", time.localtime(time.time()))))
    print("[initialize]initialization in initialize.py is beginning")
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--watch_dir', type=str, default='watch')
    parser.add_argument('--download_dir', type=str, default='download')
    parser.add_argument('--rpc_enabled', type=bool, default=True)
    parser.add_argument('--rpc_username', type=str, default='transmission')
    parser.add_argument('--rpc_password', type=str, default='123456')
    parser.add_argument('--rpc_port', type=int, default=9091)
    parser.add_argument('--rpc_whitelist_enabled', type=bool, default=True)
    parser.add_argument('--rpc_whitelist', type=str, default='*')
    parser.add_argument('--upload_limit_enabled', type=int, default=0)
    parser.add_argument('--upload_limit', type=int, default=100)
    parser.add_argument('--download_limit_enabled', type=int, default=0)
    parser.add_argument('--download_limit', type=int, default=100)
    args = parser.parse_args()
    if os.path.exists(args.watch_dir)==False:
        os.mkdir(args.watch_dir)
    if os.path.exists(args.download_dir)==False:
        os.mkdir(args.download_dir)
    with open('transmission_settings.json', 'r') as file:
        info = json.load(file)
    info["watch-dir"] = args.watch_dir
    info["download-dir"] = args.download_dir
    info["rpc-enabled"] = args.rpc_enabled
    info["rpc-username"] = args.rpc_username
    info["rpc-password"] = args.rpc_password
    info["rpc-port"] = args.rpc_port
    info["rpc-whitelist-enabled"] = args.rpc_whitelist_enabled
    info["upload-limit-enabled"] = args.upload_limit_enabled
    info["upload-limit"] = args.upload_limit
    info["download-limit-enabled"] = args.download_limit_enabled
    info["download-limit"] = args.download_limit
    info["umask"] = 2
    info["rpc-authentication-required"] = False

    if args.rpc_whitelist == "all":
        info["rpc-whitelist"] = "*"
    else:
        info["rpc-whitelist"] = args.rpc_whitelist
    with open('transmission_settings.json', 'w') as file:
        json.dump(info, file, indent=4, sort_keys=True)
    if args.rpc_enabled == True:
        print("[initialize]rpc login is allowed")
        print("[initialize]remote login address : http://{}:{}/transmission/web/".format(get_host_ip(), args.rpc_port))
    else:
        print("[initialize]rpc login is closed")
    print("[initialize]initialization in initialize.py has finished, costing {}s".format(time.time()-start))



