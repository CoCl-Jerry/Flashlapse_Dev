
if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
	cd /home/pi/COSE_FLASHLAPSE
	git pull
fi

cd /home/pi/COSE_FLASHLAPSE/_python
sudo python3 Main.py