echo "restaring autoexpense_webapp SystemD Service"
cp /app/scripts/autoexpense_webapp.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable autoexpense_webapp.service
systemctl restart autoexpense_webapp.service
