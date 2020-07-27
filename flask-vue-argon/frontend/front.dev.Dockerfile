FROM node
MAINTAINER ba93love@gmail.com
WORKDIR /app
ADD . ./
RUN yarn install
CMD yarn run serve
EXPOSE 8080