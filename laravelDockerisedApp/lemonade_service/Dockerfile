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
