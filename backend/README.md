# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## API reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
  "error": 404,
  "message": "Not Found",
  "success": false
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500: Server Error

5. Create a POST endpoint to get questions based on category.
6. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
7. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.

### Endpoint Library

GET '/categories'

- General:

  - Returns an object with two keys, categories, a dictionary object of id: category_string key:value pairs, and success, a boolean for the query execution status.
  - Request Arguments: None

- Sample: `curl http://127.0.0.1:5000/categories`

```

{
"categories": {
"1": "Science",
"2": "Art",
"3": "Geography",
"4": "History",
"5": "Entertainment",
"6": "Sports"
},
"success": true
}

```

GET '/questions'

- General:

  - Returns an object with four keys: a list of question objects, a boolean success value, a total number of questions int value, a categories object and a current category value string which is set to None. Each question object contains five key:value pairs: "answer":answer_string, "category":category_string, "difficulty":difficulty_int, "id":id_int and "question":question_string. The categories object is a dictionary of id:category_string key:value pairs.
  - Results are paginated in groups of 10.
  - Request Arguments: include a request argument to choose page number, starting from 1. None given defaults to 1.

- Sample: `curl http://127.0.0.1:5000/questions` or `curl http://127.0.0.1:5000/questions?page=2`

```

{
"categories": {
"1": "Science",
"2": "Art",
"3": "Geography",
"4": "History",
"5": "Entertainment",
"6": "Sports"
},
"current_category": null,
"questions": [
{
"answer": "Apollo 13",
"category": 5,
"difficulty": 4,
"id": 2,
"question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
},
{
"answer": "Tom Cruise",
"category": 5,
"difficulty": 4,
"id": 4,
"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
},
{
"answer": "Maya Angelou",
"category": 4,
"difficulty": 2,
"id": 5,
"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
},
{
"answer": "Edward Scissorhands",
"category": 5,
"difficulty": 3,
"id": 6,
"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
},
{
"answer": "Muhammad Ali",
"category": 4,
"difficulty": 1,
"id": 9,
"question": "What boxer's original name is Cassius Clay?"
},
{
"answer": "Brazil",
"category": 6,
"difficulty": 3,
"id": 10,
"question": "Which is the only team to play in every soccer World Cup tournament?"
},
{
"answer": "Uruguay",
"category": 6,
"difficulty": 4,
"id": 11,
"question": "Which country won the first ever soccer World Cup in 1930?"
},
{
"answer": "George Washington Carver",
"category": 4,
"difficulty": 2,
"id": 12,
"question": "Who invented Peanut Butter?"
},
{
"answer": "Lake Victoria",
"category": 3,
"difficulty": 2,
"id": 13,
"question": "What is the largest lake in Africa?"
},
{
"answer": "The Palace of Versailles",
"category": 3,
"difficulty": 3,
"id": 14,
"question": "In which royal palace would you find the Hall of Mirrors?"
}
],
"success": true,
"total_questions": 19
}

```

POST '/questions/{question_id}'

- General:

  - Deletes the question of the given `id` if it exists.
  - Returns an object with three keys: the deleted question object, a success boolean value, the updated total number of questions integer
  - Request Arguments: question id

- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/21`

```

{
  "deleted_question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true,
  "total_questions": 23
}

```

POST '/questions'

- General:

  - Creates a new question using the submitted question string, answer string, difficulty integer value and category integer value.
  - Returns an object with three keys: the added question object, a success boolean value, the new total number of questions integer
  - Request Arguments: None

- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"question": "what is the color of the sky", "answer":"blue", "difficulty":"1", "category": "5"}' http://127.0.0.1:5000/questions`

```

{
  "added_question": {
    "answer": "blue",
    "category": 5,
    "difficulty": 1,
    "id": 28,
    "question": "what is the color of the sky"
  },
  "success": true,
  "total_questions": 24
}

```

POST '/questions'

- General:

  - Searches matching questions for a given search phrase, case insensitive
  - Returns any questions for whom the search term is a substring, that is a list of objects with three keys: the list of matching question objects, a success boolean value, the total number of matching questions found integer
  - Request Arguments: None

- Sample with results: `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}' http://127.0.0.1:5000/questions`

```

{
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}

```

- Sample without results: `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "pizza"}' http://127.0.0.1:5000/questions`

```

{
  "current_category": null,
  "questions": [],
  "success": true,
  "total_questions": 0
}

```

## Testing

To run the tests, run

```

dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py

```

```

```
