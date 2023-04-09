#!/usr/bin/env bash
# install nginx if not installed
if [ ! -x /usr/sbin/nginx ]; then
    sudo apt-get -y update
    sudo apt-get -y upgrade
    sudo apt-get install -y nginx
fi

# create /data/ folder
if [ ! -d /data ]; then
    sudo mkdir -p /data
    sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared
fi

# create index.html
echo -e "<html>\n  <head>\n\t<title>Nginx Test</title>\n  </head>\n  <body>\n\t<p>This is a dummy file to test Nginx<p>\n  </body>\n</html>" > /data/web_static/releases/test/index.html

# symbolic link
if [ -h /data/web_static/current ]; then
    sudo rm -f /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test /data/web_static/current
sudo chown -R $USER:$USER /data

# configure location
sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n' /etc/nginx/sites-available/default

# restart nginx
sudo service nginx restart
