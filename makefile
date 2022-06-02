init:
	pip3 install -r requirements.txt
	
start:
	pm2 start main.py --name AUTO_VIDEO_NEW --interpreter python3

restart:
	pm2 restart AUTO_VIDEO_NEW

stop:
	pm2 stop AUTO_VIDEO_NEW
