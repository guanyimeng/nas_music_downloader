cd /home/dolphins22/Docs/Dev/dolphins22-docker
sudo chmod -R 770 ./db

sudo chown -R 33:33 ./wordpress   # www-data:www-data
sudo find ./wordpress -type d -exec chmod 755 {} \; 
sudo find ./wordpress -type f -exec chmod 644 {} \; 