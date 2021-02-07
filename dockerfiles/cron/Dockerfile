FROM gaafar/cron

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y curl
RUN mkdir /jobs
COPY ./initial/cron/job.sh /jobs
RUN chmod u+r+x /jobs/job.sh
COPY ./initial/cron/crontab /etc/cron.d/crontab
