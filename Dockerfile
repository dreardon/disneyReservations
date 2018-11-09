FROM python:3.6-alpine3.7

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.7/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.7/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update
RUN apk add chromium chromium-chromedriver

LABEL author="Daniel Reardon <danreardon@gmail.com>"
COPY . /home/disneyReservation
WORKDIR /home/disneyReservation
RUN pip3 install -r requirements.txt
RUN adduser -D disney -H -h /home/disneyReservation && chown disney:disney /home/disneyReservation -R
USER disney
ENTRYPOINT ["python", "disneyReservations.py"]
