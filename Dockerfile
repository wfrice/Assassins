FROM ubuntu:18.04
RUN apt-get update && apt-get upgrade -y
RUN apt-get install build-essential -y
RUN apt-get install cmake -y
RUN apt-get install python3 python3-pip python3-dev libmysqlclient-dev python3-mysql.connector -y
RUN apt-get install libmysqlclient-dev -y
RUN apt-get install mariadb-server -y
RUN apt-get install git -y
RUN pip3 install flask
RUN pip3 install flask-sqlalchemy
RUN pip3 install flask-login
RUN pip3 install passlib
RUN pip3 install pythonping
RUN pip3 install psutil
