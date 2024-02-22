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
    curl -o isfuckxui.py https://raw.githubusercontent.com/AriesEDGE/fuckxui/main/create.py
}

cvv(){
    python3 isfuckxui.py
    python3 create.py
}

upd
pyzt
echo "Enter your IP CIOR!"
read sbip
echo "ENTER YOUR MAX FUCKXUI RATE!"
read fucku
masscan -p54321 ${sbip} --max-rate ${fucku} -oG results.txt
cvv
