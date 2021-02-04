#!/usr/bin/python
import os
import time
from datetime import datetime

def daemon():
	while True:
		print("{0} - deamon tick" .format(getCurrentTime()))
		time.sleep(100)
def getCurrentTime():
	d = datetime.now()
	ds = d.strftime("%Y-%m-%d - %H:%M:%S")
	return ds
def runServer(adres=os.environ.get("ADDRESS"),port=os.environ.get("PORT")):
    print("{0} - Executing django server...".format(getCurrentTime()))
    return os.system("python3 ./app/manage.py runserver {0}:{1}" .format(adres,port))
def makeMigrations(params=""):
    print("{0} - Preparing migrations...".format(getCurrentTime()))
    return os.system("python3 ./app/manage.py makemigrations {0}" .format(params))
def migrate(params=""):
    print("{0} - Migrating to db...".format(getCurrentTime()))
    return os.system("python3 ./app/manage.py migrate {0}" .format(params))
def prints():
    print("="*40)
    print("Python machine for Django 3+")
    print("Author: Mateusz I")
    print("Website: mign.pl")
    print("Server: {0}:{1}".format(os.environ.get("ADDRESS"),os.environ.get("PORT")))
    print("DB engine: {0}".format(os.environ.get("DB_ENGINE")))
    print("DB: {0} - {1}:{2}".format(os.environ.get("DB_NAME"),os.environ.get("DB_ADDRESS"),os.environ.get("DB_PORT")))
    print("="*40)
    print("{0} - Executing deamon now!" .format(getCurrentTime()))
def is_up(host,port,count,sleep):
    cmd = "ping -i 0.1 -c 1 {0} -p {1}  > /dev/null".format(host,port)
    print("{0} - Checking host availability... {1}:{2}".format(getCurrentTime(),host,port))
    flag = False
    while flag == False:
        for x in range(count):
            time.sleep(sleep)
            host_up = True if os.system(cmd) == 0 else False
            if host_up:
                flag = True
                break
            else:
                print("{0} - Failed to connect...".format(getCurrentTime()))
    else:
        print("{0} - Host {1}:{2} znaleziony!".format(getCurrentTime(),host,port))
    return flag
def tests(app=""):
    print("{0} - Running tests...".format(getCurrentTime()))
    return os.system("python3 ./app/manage.py test {0}".format(app))
def cover(app=""):
    print("{0} - Covering tests...".format(getCurrentTime()))
    return os.system("coverage run app/manage.py test {0}".format(app))
def cover_raport():
    return os.system("coverage report")       
if __name__ == "__main__":
    prints()
    if is_up(host=os.environ.get("DB_ADDRESS"),port=os.environ.get("DB_PORT"),count=3,sleep=1):
        makeMigrations()
        cover("app")
        cover_raport()
        migrate()
        runServer()
