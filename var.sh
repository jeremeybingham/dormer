#!/bin/bash

# prompt for domain and other variables
read -p "what's this project called? no spaces. "  PROJ_NAME
read -p "enter the domain name, no www: "  DOMAIN
read -p "enter your SSL contact email: "  SSLEMAIL

# write repsonses to file
sed -i "s/dormer.mansard.net/${DOMAIN}/g" cert.sh data/nginx/app.conf
sed -i "s/ssl@mansard.net/${SSLEMAIL}/g" cert.sh
mv ../{dormer,${PROJ_NAME}}
cd
echo "all done!"
