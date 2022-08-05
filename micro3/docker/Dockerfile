FROM python:3.6
EXPOSE 5000
RUN mkdir /hsapp
WORKDIR /hsapp
COPY ./hsdef/* /hsdef/
COPY ./hslib/* /hslib/
ADD ./micro3/ /hsapp/
RUN apt-get -y update
RUN apt-get upgrade -y
RUN apt-get install -y ffmpeg
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD ["python3",  "/hsapp/display.py"]
# CMD ["python3",  "/hsapp/main.py"]
# CMD tail -f /dev/null
