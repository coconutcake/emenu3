FROM python:3.8-slim
LABEL maintainer = "mign.pl"

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
		gcc \
		curl \
		gettext \
        mariadb-client \
		default-mysql-client default-libmysqlclient-dev \
		libpq-dev \
		sqlite3 \
		nano \
		iputils-ping \
	--no-install-recommends apt-utils && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /requirements.txt

RUN mkdir /app
RUN mkdir /resources
COPY ./initial/django/run.py /run.py
COPY ./initial/django/run.sh /run.sh
COPY ./resources/wait-for-it.sh /resources/wait-for-it.sh
RUN chmod +x /run.py
RUN chmod +x /run.sh
RUN chmod +x /resources/wait-for-it.sh
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY ./app /app

RUN useradd -ms /bin/bash user
# RUN useradd -D user
RUN chown user -R /app/
# USER user
# EXPOSE 8000
# CMD [ "python", "manage.py migrate", "python", "manage.py runserver 0.0.0.0:8000" ]
# CMD ["/wait-for-it.sh", "db:3306", "--timeout=45", "--strict", "--", "./run.sh"]
#ENTRYPOINT ["python3","./entrypoint.py"]


