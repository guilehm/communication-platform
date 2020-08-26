# Communication Platform

## Required
* Docker
* Docker Compose

## Installation


Clone this repository

    git@github.com:Guilehm/communication-platform.git
    
Enter the repository

    cd communication-platform


Copy `env.sample` to `.env`

    cp env.sample .env
    

Build and start the app

    make run
    
Now the server is running and you may access the app at this url: [http://localhost:8000/](http://localhost:8000/)


## Use guide

**Create a Scheduling:**

- POST Create at [http://localhost:8000/scheduling/](http://localhost:8000/scheduling/) with the following payload:
```json
{
    "addressee": {
        "name": "Bilbo Baggins",
        "email": "bilbo@gmail.com",
        "mobileNumber": "+55 11 99988-9080",
        "deviceToken": "8e335894 9b7c25d4 bebcf74f 740f4707"
    },
    "message": "Bilbo has always been frustrated with several of the more famous tales of Elvish history",
    "sendingTime": "2020-08-30T02:05:00.472Z",
    "type": "email",
    "sent": false
}
```

*Addressee data is not required. But if you want to create one `scheduling` with type `email`, be sure to set addressee email field, otherwise you will receive error 400 from the API.*

**Create a Scheduling for an existing addressee**
- POST Create at [http://localhost:8000/scheduling/](http://localhost:8000/scheduling/) with the following payload:
```json
{
    "addressee": {
        "id": 1
    },
    "message": "Bilbo has always been frustrated with several of the more famous tales of Elvish history",
    "sendingTime": "2020-08-30T02:05:00.472Z",
    "type": "email",
    "sent": false
}
```
**Retrieve Scheduling data**
- GET at `http://localhost:8000/scheduling/<uuid>/` where `<uuid>` is the ID of the `scheduling` you want see.

**Update the status for a Scheduling**
- PATCH at `http://localhost:8000/scheduling/<uuid>/` where `<uuid>` is the ID of the `scheduling` you want to update.

```json
{
  "sent": true
}
```

**Delete a Scheduling**
- DELETE at  `http://localhost:8000/scheduling/<uuid>/` where `<uuid>` is the ID of the `scheduling` you want to delete.


## API Docs

- Swagger [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- Redoc [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## Running tests

```bash
make test
```


## Containers
- Stopping containers
```bash
make stop 
```


- Remove containers and database volume
```bash
make down
```

## Running without Docker
#### Required
* Python 3.8
* Postgres

Install Pipenv
```bash
pip install pipenv
```

Create the virtual environment


```bash
pipenv install
```

Edit your `.env` file and set the `DATABASE_URL` environment variable for your local database
```bash
vim .env
```

Create the database.
If running on linux:
```bash
sudo su
```
```bash
su postgres
```
```bash
psql
```

```bash
create database communication;
```

Run migrations
```bash
python manage.py migrate
```

Start server
```bash
python manage.py runserver
```

### Extra


The entire process of developing this project is documented on Github Issues and Pull Requests.
    
Thanks!
