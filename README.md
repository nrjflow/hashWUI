# hashWUI
Web GUI to crack hashes using hashcat
## Requirements
```
Install WSGI_Mod
Load WSGI_Mod
Install Python3
Install Channels #(used for websockets)
Install Django
pip3 install channels_redis #(used for websockets and monitoring background jobs)
redis
apt-get install python3-dev libmysqlclient-dev
sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3
pip3 install mysqlclient
```

## Apache2 config:
```
<VirtualHost *:80>
	Alias /static/ /workspace/Dev/hashWUI/static/
	<Directory /workspace/Dev/hashWUI/static>
	Require all granted
	</Directory>
	WSGIScriptAlias / /workspace/Dev/hashWUI/hashWUI/wsgi.py
	WSGIPythonPath /workspace/Dev/hashWUI
	<Directory /workspace/Dev/hashWUI/hashWUI>
	<Files wsgi.py>
	Require all granted
	</Files>
	</Directory>
</VirtualHost>

RewriteEngine on
RewriteCond %{HTTP:UPGRADE} ^WebSocket$ [NC,OR]
RewriteCond %{HTTP:CONNECTION} ^Upgrade$ [NC]
RewriteRule .* ws://127.0.0.1:8080%{REQUEST_URI} [P,QSA,L]

```

## Activate modules:
```
a2enmod rewrite
a2enmod proxy
a2enmod proxy_http
a2enmov proxy_wstunnel
```

## Daphne as a service (used for websockets in channels) /etc/systemd/system/django-channels-daphne.service
```
[Unit]
Description=daphne server script for my project
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/workspace/Dev/hashWUI
ExecStart=/usr/local/bin/daphne -b 0.0.0.0 -p 8080 hashWUI.asgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

## Screenshots
Home
![Alt text](/Docs/screenshots/home.png?raw=true "Home")

List of tasks
![Alt text](/Docs/screenshots/list.png?raw=true "List of tasks")

New task
![Alt text](/Docs/screenshots/new_task.png?raw=true "New task")
