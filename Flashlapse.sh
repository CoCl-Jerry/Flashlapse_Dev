
if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
	git pull
fi

cd _python
sudo python3 Main.py
