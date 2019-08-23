#!/bin/bash

# prompt for domain and other variables
read -p "enter the domain name, no www: "  DOMAIN
read -p "enter your SSL contact email: "  SSLEMAIL
read -p "enter a custom word to display later: "  CUSTOM_WEB_WORD

# write repsonses to file
sed -i "s/dormer.mansard.net/${DOMAIN}/g" cert.sh data/nginx/app.conf
sed -i "s/sslemail@mansard.net/${SSLEMAIL}/g" cert.sh
sed -i "s/CUSTOM_WEB_WORD/${CUSTOM_WEB_WORD}/g" data/web/templates/hello.html

echo "all done!"