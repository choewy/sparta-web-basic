# Docker Mongo-Flask

### docker build

```
$ docker build -t {IMAGE_TAG}
```

### docker run

```
$ docker run -it --name {CONTAINER_NAME} -p {PORT_flask:5000} -p {PORT_mongo:27017} -v {MONGO_DATA_PATH:/data/db} {IMAGE_TAG} 
```

### create dummy data

```
/var/flask# python3 dummy.py
```

### run flask server

```
/var/flask# python3 app.py
```
