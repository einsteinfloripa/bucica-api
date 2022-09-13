FROM node

# Create app directory
RUN mkdir -p /usr/app

WORKDIR /usr/app
COPY . .

EXPOSE 4000

RUN npm install

