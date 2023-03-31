# TTM - Time Table Managment
### Describe
TTM is a web service for creating schedules at universities, and in the future at other educational institutions. TTM, unlike table processors, tends to take into account all factors when making a schedule, for example, so that a teacher can spend a couple of hours, we check whether he has a working day, taking into account vacations/business trips, etc. You can also create events in TTM - they are also activities in the admin panel.

### Technology
Python 3.9

Django 3.2

DRF 3.12.4

PyJWT 2.6.0

drf-yasg 1.21.5

SQLite

React 18.2.0

NodeJs 18.15.0

### Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`

### Start in dev mode
- Install and set environment
```
python -m venv env
```
- Activate the environment
Linux/MacOS:
```
source venv/bin/activate
```
Windows:
```
.\venv\Scripts\activate
```
- Install dependencies from requirements.txt
```
pip install -r requirements.txt
```
- In dir with manage.py make migrations
```
python manage.py makemigrations
python manage.py migrate
```
- In the folder with manage.py run next command:
```
python manage.py runserver
```

## API Reference
To begin working with the API, you need to register a user and create a jwt token for him. How to do this will be demonstrated in the example. You can find all the information about the API on the website after its launch on the /api/swagger/ page.
#### User register

```http
  POST /api/v1/users/
```

| Parameter  | Type     | Description                 |
| :--------  | :------- | :-------------------------  |
| `username` | `string` | **Required**. Your username |
| `password` | `string` | **Required**. Your password |
| `email`    | `string` | **Required**. Your email    |

#### Get JWT

```http
  POST /api/v1/jwt/create/
```

| Parameter  | Type     | Description                 |
| :--------  | :------- | :-------------------------- |
| `username` | `string` | **Required** Your username  |
| `password` | `string` | **Required** Your password  |



## Models description
A brief description of the project models, detailed methods and fields can be found
[here](/TimeTableManagment/timetables/models.py)

### User
The basic user model with a name, password, etc,
to which role models (Student, Teacher, Methodist) are later connected.

### Student
A role model that serves only to relate itself to the group and display the corresponding schedule.

### Teacher
A role model that serves only to relate yourself to teachers to display the appropriate schedule and your appointment as a teacher for lessons and activities

### Methodist
A role model that allows you to fully edit the schedule.

### Group
A group model whose objects are used in Student, Lesson, Activity.

### LessonType
The model serving only as a list of items is specified in the Lesson.

### Classroom
The model serving only as a list of cabinets is specified in Lesson, Activity.

### Lesson
Lesson model with teacher, groups and so on fields.

### Activity
Activity model with teacher, groups and so on fields.
## Authors

- [@Alexey](https://github.com/Alexey-zaliznuak)
- [@maxi-q](https://github.com/maxi-q)