. bt_auto.conf
if [ ! -d "./torrent_tmp" ]; then
mkdir ./torrent_tmp
fi
sudo service transmission-daemon stop
if [ "$print_log_or_not" = "0" ];then
    sudo python3 initialize.py --watch_dir $watch_dir --download_dir $download_dir --rpc_enabled $rpc_enabled --rpc_username $rpc_username --rpc_password $rpc_password --rpc_port $rpc_port --rpc_whitelist_enabled $rpc_whitelist_enabled --rpc_whitelist $rpc_whitelist --upload_limit_enabled $upload_limit_enabled --upload_limit $upload_limit --download_limit_enabled $download_limit_enabled --download_limit $download_limit>log.txt
else
    sudo python3 initialize.py --watch_dir $watch_dir --download_dir $download_dir --rpc_enabled $rpc_enabled --rpc_username $rpc_username --rpc_password $rpc_password --rpc_port $rpc_port --rpc_whitelist_enabled $rpc_whitelist_enabled --rpc_whitelist $rpc_whitelist --upload_limit_enabled $upload_limit_enabled --upload_limit $upload_limit --download_limit_enabled $download_limit_enabled --download_limit $download_limit
fi
sudo chmod 777 $download_dir
sudo cp transmission_settings.json /etc/transmission-daemon/settings.json
sudo service transmission-daemon start
if [ "$print_log_or_not" = "0" ];then
    sudo python3 timer.py --update_seed_queue_time $update_seed_queue_time --max_seed_selected_num $max_seed_selected_num --rpc_username $rpc_username --rpc_password $rpc_password --download_prices $download_prices --max_download_space $max_download_space --update_seed_num $update_seed_num --username $username --password $password --seed_select_strategy $seed_select_strategy>>log.txt
else
    sudo python3 timer.py --update_seed_queue_time $update_seed_queue_time --max_seed_selected_num $max_seed_selected_num --rpc_username $rpc_username --rpc_password $rpc_password --download_prices $download_prices --max_download_space $max_download_space --update_seed_num $update_seed_num --username $username --password $password --seed_select_strategy $seed_select_strategy
fi

#important orders
#transmission-remote -n 'transmission:123456' -l>state.txt
#transmission-remote -n 'transmission:123456' -t 2 --remove-and-delete   #remve seed and data
#transmission-remote -n 'transmission:123456' --exit   #Tell the transmission session to shut down
#transmission-remote -n $rpc_username:$rpc_password -S -t 3
#transmission-remote -n $rpc_username:$rpc_password --exit   #Tell the transmission session to shut down