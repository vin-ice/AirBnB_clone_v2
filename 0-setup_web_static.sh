#!/usr/bin/env bash
# install nginx if not installed
apt-get -y update
apt-get -y install -y nginx

# create /data/ folder
mkdir -p /data/web_static/releases/test/ /data/web_static/shared
chown -R $USER:$USER /data/

# create index.html
echo -e "<html>\n  <head>\n\t<title>Nginx Test</title>\n  </head>\n  <body>\n\t<p>This is a dummy file to test Nginx<p>\n  </body>\n</html>" > /data/web_static/releases/test/index.html
# symbolic link
rm -f /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

# configure location
sudo sed -i '38i\\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t\tautoindex off;\n\t}\n' /etc/nginx/sites-available/default

# restart nginx
sudo service nginx restart
exit 0
