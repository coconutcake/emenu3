FROM nginx

ADD /initial/nginx/nginx.conf /etc/nginx/nginx.conf
COPY /initial/nginx/certs /etc/nginx/conf.d/certs

RUN mkdir /resources

COPY /initial/nginx/run.sh /run.sh
COPY ./resources/wait-for-it.sh /resources/wait-for-it.sh
RUN chmod +x /resources/wait-for-it.sh
RUN chmod +x /run.sh


