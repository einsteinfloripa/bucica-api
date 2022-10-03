FROM nginx

# Copy the nginx configuration file
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# SSL
COPY ssl/certificate.pem /etc/nginx/certs/certificate.pem
COPY ssl/key.pem /etc/nginx/certs/key.pem

