#!/usr/bin/env bash
# installs nginx if absent
if [ ! -x "$(command -v nginx)" ]; then
    sudo apt-get -y update
    sudo apt-get -y nginx
fi
# data directory
sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
# change ownership
sudo chown -R "$USER":"$USER" /data/
echo -e "<html>\n <head>\n  <title>Test</title>\n <head>\n <body>\n  <p>Holberton School</p>\n </body>\n</html>" > /data/web_static/releases/test/index.html
# remove link
if [ -L "/data/web_static/current" ]; then
    rm -rf /data/web_static/current
fi
ln -s /data/web_static/releases/test/ /data/web_static/current
# sudo sed -i '38i\\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n' /etc/nginx/sites-available/default
sudo service nginx restart
exit 0
