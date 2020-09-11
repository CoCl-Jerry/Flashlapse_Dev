if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
	cd /home/pi/Documents/Flashlapse_Dev
	git pull
fi
cd /home/pi/Documents/Flashlapse_Dev/_python
sudo python3 Main.py
