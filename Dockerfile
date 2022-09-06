FROM node

# Create app directory
WORKDIR /usr/app
COPY . .

# Install app dependencies
RUN npm install
