# APEKSUI
UI For APEKS Build using Flask Framework Python
**[WARNING] Bad Implementation Code Inside**

Dependency:
- PySerial
- bluepy
- Flask

Installation:
1) Just like ordinary simple flask
2) Add "apeksui.service on /etc/systemd/system
3) Run sudo "systemctl enable apeksui" then "systemctl start apeksui" (As Root/Sudo)

[NGINX Configuration]
1) Copy "apeksui_proxy" to "/etc/nginx/sites-available"
2) Make symlink by run "sudo ln -s /etc/nginx/sites-available/apeksui_proxy /etc/nginx/sites-enabled"
3) Remember to Restart Nginx "systemctl restart nginx"

[Running App For Debug]
1) "cd" to APEKS Dir
2) Run "/usr/local/bin/uwsgi --ini /home/pi/APEKS/uwsgi.ini"

Thanks For Everyone's Help in Everyway Possible ^_^
