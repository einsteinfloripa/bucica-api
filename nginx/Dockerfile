FROM nginx:1.15.0


RUN rm -r /etc/nginx/conf.d/default.conf

# Copy the nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
# # Copy the static files
# COPY dist /usr/share/nginx/html
