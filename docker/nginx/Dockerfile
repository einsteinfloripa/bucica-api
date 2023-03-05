FROM nginx

RUN rm -r /etc/nginx/conf.d/default.conf

# Copy the nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

# # Copy the static files
# COPY dist /usr/share/nginx/html
