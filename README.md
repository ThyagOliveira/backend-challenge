# Backend Challenge

## Description

In this technical challenge, you will build a fullstack web application that processes and manages a
collection of book records. The application should handle file ingestion, provide administrative tools
for managing the records, and offer a user-friendly interface for external users to search and view
book details. The challenge will test your ability to work with backend technologies (Python or
Node.js), frontend frameworks (Vue.js or React), and relational databases (PostgreSQL or MySQL).

[Frontend](https://github.com/ThyagOliveira/frontend-challenge)

## Instructions

Install [Docker](https://docs.docker.com/get-docker/)

##### Start container
```shell
$ docker-compose up --build
```

##### Create Super User
```shell
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
```

##### Request to upload csv
```shell
curl -X POST -F "file=@books.csv" http://localhost:8000/api/books/upload/
```


## Design Patterns

### 1. **Template Method**
Models, View classes, serializers, implement the template pattern, which provides a base for something and we only need to provide/override the implementation for things we need to customize.

### 2. **Service Layer**
Instead of writing logic directly in views or serializers, create a service layer to encapsulate the logic. This helps maintain separation of concerns and allows for more organized and reusable code.

### 3. **Serializer DTO**
Use DRF serializers to facilitate data validation and transformation.

### 4. **Serializer Composite**
Combining serializers to reuse code and have more flexibility
