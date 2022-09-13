FROM node

# Create app directory
RUN mkdir -p /usr/app

WORKDIR /usr/app
COPY . .

RUN npm install

