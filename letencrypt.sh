#apt install certbot python3-certbot-nginx
##apt install python3-certbot-apache

#https://hyperhost.ua/tools/ru/ssl-checker?domain=used.1x1.com.ua
#https://www.baeldung.com/linux/letsencrypt-renew-ssl-certificate-automatically

service nginx stop
certbot certonly --standalone -d 1x1.com.ua
#certbot renew
service nginx start

