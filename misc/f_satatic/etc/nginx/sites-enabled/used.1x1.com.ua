server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name used.1x1.com.ua;
    client_max_body_size 200M;

    error_log /var/log/nginx/used.1x1.com.ua.log;
    access_log /var/log/nginx/used.1x1.com.ua.log_access.log;

    ssl_certificate /etc/letsencrypt/live/used.1x1.com.ua/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/used.1x1.com.ua/privkey.pem;

    location /img/ {
        proxy_pass http://127.0.0.1:8083;
    }

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

server {
    listen 80;
    server_name used.1x1.com.ua;
    return 301 https://$host$request_uri;
}
