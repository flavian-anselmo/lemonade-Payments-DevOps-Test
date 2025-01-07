<p align="center"><a href="https://laravel.com" target="_blank"><img src="https://raw.githubusercontent.com/laravel/art/master/logo-lockup/5%20SVG/2%20CMYK/1%20Full%20Color/laravel-logolockup-cmyk-red.svg" width="400" alt="Laravel Logo"></a></p>

<p align="center">
<a href="https://github.com/laravel/framework/actions"><img src="https://github.com/laravel/framework/workflows/tests/badge.svg" alt="Build Status"></a>
<a href="https://packagist.org/packages/laravel/framework"><img src="https://img.shields.io/packagist/dt/laravel/framework" alt="Total Downloads"></a>
<a href="https://packagist.org/packages/laravel/framework"><img src="https://img.shields.io/packagist/v/laravel/framework" alt="Latest Stable Version"></a>
<a href="https://packagist.org/packages/laravel/framework"><img src="https://img.shields.io/packagist/l/laravel/framework" alt="License"></a>
</p>

## How to run via docker 

```bash 
docker compose build 
docker compose up -d 
```

## Here is the docker file 
```bash
FROM php:8.2-fpm

WORKDIR /var/www

# system dependencies
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zip \
    unzip \
    curl

RUN docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd pdo pdo_mysql bcmath

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# Copy application files
COPY . .

# Install application dependencies
RUN composer install

# Change ownership and permissions
RUN chown -R www-data:www-data /var/www \
    && chmod -R 755 /var/www

    EXPOSE 9000
CMD ["php-fpm"]

```

## Here is the compose file and all the services to run 
- Nginx
- Msql 
- laravel service 


```bash
version: '3.8'

services:
  lemonade:
    build:
      context: .
      dockerfile: Dockerfile
    image: sample-laravel-app
    container_name: sample-laravel-app
    ports:
      - "9000:9000"
    volumes:
      - .:/var/www
    networks:
      - laravel

  webserver:
    image: nginx:stable
    container_name: sample-laravel-nginx
    ports:
      - "8000:80"
    volumes:
      - .:/var/www
      - ./nginx:/etc/nginx/conf.d
    networks:
      - laravel
    depends_on:
      - lemonade

  db:
    image: mysql:8.0
    container_name: sample-laravel-db
    ports:
      - "3306:3306"
    environment:
      MYSQL_DATABASE: laravel
      MYSQL_ROOT_PASSWORD: root
    networks:
      - laravel

networks:
  laravel:
    driver: bridge 
```
