#!/bin/bash

# 핫스팟 설정 자동화 스크립트

echo "Raspberry Pi 핫스팟 설정을 시작합니다."

# 1. 필요한 패키지 설치
echo "필요한 패키지를 설치 중입니다..."
sudo apt update
sudo apt install -y dnsmasq hostapd

# 2. Wi-Fi 서비스 중지
echo "Wi-Fi 서비스를 중지합니다..."
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq

# 3. 고정 IP 주소 설정
echo "고정 IP 주소를 설정합니다..."
sudo bash -c "cat >> /etc/dhcpcd.conf" <<EOF
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
EOF

sudo service dhcpcd restart

# 4. dnsmasq 설정
echo "dnsmasq를 설정합니다..."
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo bash -c "cat > /etc/dnsmasq.conf" <<EOF
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
EOF

# 5. hostapd 설정
echo "hostapd를 설정합니다..."
sudo bash -c "cat > /etc/hostapd/hostapd.conf" <<EOF
interface=wlan0
driver=nl80211
ssid=YourHotspotName
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=YourPassword
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
EOF

sudo sed -i 's|#DAEMON_CONF=".*"|DAEMON_CONF="/etc/hostapd/hostapd.conf"|' /etc/default/hostapd

# 6. IP 포워딩 활성화
echo "IP 포워딩을 활성화합니다..."
sudo sed -i 's|#net.ipv4.ip_forward=1|net.ipv4.ip_forward=1|' /etc/sysctl.conf
sudo sysctl -p

# 7. NAT 설정
echo "NAT를 설정합니다..."
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
sudo bash -c "grep -qxF 'iptables-restore < /etc/iptables.ipv4.nat' /etc/rc.local || sed -i '/^exit 0/i iptables-restore < /etc/iptables.ipv4.nat' /etc/rc.local"

# 8. 서비스 활성화 및 시작
echo "서비스를 활성화하고 시작합니다..."
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
sudo systemctl start hostapd
sudo systemctl start dnsmasq

echo "핫스팟 설정이 완료되었습니다!"
echo "SSID: YourHotspotName"
echo "Password: YourPassword"
