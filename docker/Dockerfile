FROM mongo
RUN apt update && apt install -y python3 && apt install -y python3-pip
RUN pip install flask && pip install pymongo && pip install beautifulsoup4 && pip install requests

WORKDIR /var/flask
COPY [ "/src", "." ]