# todo-backend
Backend for a todo app.

## Database
managed postgres sql database hosted on elephantsql.com (tiny turtle).

## Authentication
JWT based user authentication.

## Endpoints
```
POST /api/user/register/
POST /api/user/token/
POST /api/user/token/refresh/
POST /api/user/token/refresh/

GET /api/todo/todo/
GET /api/todo/todo/:id/
POST /api/todo/todo/
PATCH /api/todo/todo/:id/
DELETE /api/todo/todo/:id/
```
## Mangement commands
autodelete management command deletes any todo that is older than one week
`docker-compose run app sh -c "python manage.py autpdelete"`
