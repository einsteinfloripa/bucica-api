FROM nginx

ENV TZ=America/Sao_Paulo

RUN rm -r /etc/nginx/conf.d/default.conf

# Copy the nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf
