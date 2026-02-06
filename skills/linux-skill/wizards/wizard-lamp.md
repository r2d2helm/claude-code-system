# Wizard: LAMP Stack

Assistant d'installation d'une stack LAMP (Linux, Apache/Nginx, MySQL/PostgreSQL, PHP).

## Questions

1. **Web server** : Apache ou Nginx
2. **Database** : MySQL 8, MariaDB 11, PostgreSQL 16
3. **PHP version** : 8.2, 8.3
4. **Application** : WordPress, Laravel, custom PHP
5. **SSL** : Certbot pour Let's Encrypt ?
6. **Domaine** : Nom de domaine

## Installation Nginx + PHP-FPM + PostgreSQL (Ubuntu)

```bash
# Nginx
sudo apt install -y nginx
sudo systemctl enable nginx

# PHP
sudo apt install -y php8.3-fpm php8.3-cli php8.3-common \
  php8.3-pgsql php8.3-mysql php8.3-curl php8.3-gd \
  php8.3-mbstring php8.3-xml php8.3-zip php8.3-intl

# PostgreSQL
sudo apt install -y postgresql postgresql-client
sudo systemctl enable postgresql

# Configurer Nginx vhost
sudo tee /etc/nginx/sites-available/app << 'EOF'
server {
    listen 80;
    server_name example.com;
    root /var/www/app/public;
    index index.php;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_pass unix:/run/php/php8.3-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
EOF
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# SSL avec Certbot
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d example.com
```
