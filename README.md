# World Stats API

One Paragraph of project description goes here

### Demo
[Front-end application](http://world-countries-api.s3-website.eu-west-3.amazonaws.com)

[GraphQL Endpoint](http://ec2-15-188-83-208.eu-west-3.compute.amazonaws.com/graphql/)

## Getting Started

To run this project locally, clone or download this repository in your prereferred directory.

### Prerequisites

You need to have [Docker](https://www.docker.com/get-started)  installed on your compose

[Clone the front-end application](https://github.com/ashermcoa/world-countries-ui)

## Running the application

### Initial steps
Create a `.env` and `.env.db` files as shown in the example files in the project root 

You may need to give executable rights to `entrypoint.sh` file in your project root directory.

Build docker images and spin up db and api containers
#### `$ docker-compose up -d --build`

Run django migrations
#### `$ docker-compose exec world-start-api python manage.py makemigrations api`
#### `$ docker-compose exec world-start-api python manage.py migrate`

Confirm that the 3 tables have been created
#### `$ docker-compose exec world-start-api-db psql -U docker -d world_stats`

```
$ docker-compose exec world-start-api-db psql -U docker -d world_stats
psql (12.2 (Debian 12.2-2.pgdg100+1))
Type "help" for help.

world_stats=# \d
                       List of relations
 Schema |               Name                |   Type   | Owner  
--------+-----------------------------------+----------+--------
 public | auth_group                        | table    | docker
 public | auth_group_id_seq                 | sequence | docker
 public | auth_group_permissions            | table    | docker
 public | auth_group_permissions_id_seq     | sequence | docker
 public | auth_permission                   | table    | docker
 public | auth_permission_id_seq            | sequence | docker
 public | auth_user                         | table    | docker
 public | auth_user_groups                  | table    | docker
 public | auth_user_groups_id_seq           | sequence | docker
 public | auth_user_id_seq                  | sequence | docker
 public | auth_user_user_permissions        | table    | docker
 public | auth_user_user_permissions_id_seq | sequence | docker
 public | city                              | table    | docker
 public | city_id_seq                       | sequence | docker
 public | country                           | table    | docker
 public | countrylanguage                   | table    | docker
 public | countrylanguage_id_seq            | sequence | docker
 public | django_admin_log                  | table    | docker
 public | django_admin_log_id_seq           | sequence | docker
 public | django_content_type               | table    | docker
 public | django_content_type_id_seq        | sequence | docker
 public | django_migrations                 | table    | docker
 public | django_migrations_id_seq          | sequence | docker
 public | django_session                    | table    | docker
(24 rows)

world_stats=# 
```

### Import sql data
There is `world.sql` file in `data/world.sql`
Export the data to the database. Copy the lines that begin with copy and enter the data them when you get this prompt. Do this for the
other 2 tables.
```
$ docker-compose exec world-start-api-db psql -U docker -d world_stats
psql (12.2 (Debian 12.2-2.pgdg100+1))
Type "help" for help.

world_stats=# COPY city (id, name, countrycode, district, population) FROM stdin;
Enter data to be copied followed by a newline.
End with a backslash and a period on a line by itself, or an EOF signal.
>> 1	Kabul	AFG	Kabol	1780000
2	Qandahar	AFG	Qandahar	237500
3	Herat	AFG	Herat	186800
4	Mazar-e-Sharif	AFG	Balkh	127800
5	Amsterdam	NLD	Noord-Holland	731200
6	Rotterdam	NLD	Zuid-Holland	593321
7	Haag	NLD	Zuid-Holland	440900
8	Utrecht	NLD	Utrecht	234323
...................................
...................................
...................................
4079	Rafah	PSE	Rafah	92020
\.
```
Once you are done, run the query below. This ensures that we can continue to add cities from the front-end.

`select setval('city_id_seq', 4080);`

### Accessing application endpoints 
Navigate to [http://localhost:8000/graphql/](http://localhost:80/graphql/) to open the GraphQL server

### Running tests
Run tests included in the project
#### `$ docker-compose exec world-start-api coverage run manage.py test`

View code coverage by opening `htmlcov/index.html` after running this command 
#### `$ docker-compose exec world-start-api coverage html              `

### Coding style tests

Pep8 Python styles have been used for formatting 


## Built With

- [Python 3](https://docs.python.org/3/) 
- [Django](https://docs.djangoproject.com/en/3.0) The backend framework
- [GraphQL](https://graphql.org/) - Used for building the API
