# budgeting-app
Budgeting app for SE670

tree -I 'virtualenv|__pycache__'

There are 2 directories in this repository.
1. backend
2. my-budget-web

backend:
Backend is built using FastApi python framework. It implements REST API endpoints to perform budget CRUD operations.
It uses MySql as database hosted in AWS EC2 instance to store user data.
It uses Redis service for API rate limiting and database cacheing. Redis is in-memory database which caches the freqeuntly used database operations.
Redis sits between backend and database. 
API rate limiting is on the basis of IP.

Authentication is done at the server level using JWT bearer token which expires every 30 minutes.



my-budget-web:
Front-end is developed using Svelte which is an open-source web application framework. It makes requests to backend server using API endpoints and retrieves the responses.



