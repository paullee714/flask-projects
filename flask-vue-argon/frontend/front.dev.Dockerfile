FROM node
MAINTAINER ba93love@gmail.com
WORKDIR /app
ADD . ./
CMD yarn install && yarn run serve
EXPOSE 8080