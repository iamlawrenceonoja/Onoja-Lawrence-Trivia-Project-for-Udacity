# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where I come in! I helped them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application includes the following features:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app helped me test my ability to structure plan, implement, and test an API - skills essential for enabling my future applications to communicate with others.

## Cloning the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) the forked repository to your machine. 

## About the Stack

The full stack application was started for me. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. I worked primarily in `__init__.py` to define endpoints and referenced models.py for DB and SQLAlchemy setup. These are the files I edited in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

I paid special attention to what data the frontend is expecting from each API response to help guide how I format my API. The places where I changed the frontend behavior, and where I looked for the above information, are marked with `TODO`. These are the files I edited in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, I practiced the core skill of being able to read and understand code and have a simple plan to follow to build out the endpoints of the backend API.

> View the [Frontend README](./frontend/README.md) for more details.

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return five error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Unprocessable 
- 405: Method Not Allowed
- 500: Unexpected Server Error

### Endpoints 
#### GET '/categories'

- Fetches and returns An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
- Request Arguments: None
- Sample: `curl http://127.0.0.1:5000/categories`

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}


#### GET '/questions'

- Fetches and returns a list of question objects, success value, total number of questions and a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category 
- Request Arguments: page number starting from 1
- Sample: `curl http://127.0.0.1:5000/questions?page=2`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
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
  "total_questions": 20
}

#### DELETE '/questions/{question_id}'

- Deletes the question of the given ID if it exists.
- Returns the id of the deleted question, success value, and total questions.
- Request Arguments: id integer
- Sample: `curl -X delete http://127.0.0.1:5000/questions/1`

```json
{
    "success": true,
    "deleted": 1,
    "total_questions": 19,
}

#### POST '/questions'
- Creates a new question using the submitted question, answer, category and difficulty OR searches for questions using the search term provided. 
- Either it returns the id of the created question, success value, and total questions or it returns the success value, list of question objects, total number of questions and current category.
- Request Arguments: question, answer, category, difficulty, search term
- Sample for creating question: `curl -X POST -H "Content-Type: application/json" -d "{\"question\":\"What is my name\", \"answer\":\"Larry\", \"category_id\":\"3\", \"difficulty\":\"2\"}"  http://127.0.0.1:5000/questions`
-Sample for searching questions: `curl -X POST -H "Content-Type: application/json" -d "{\"searchTerm\":\"title\"}"  http://127.0.0.1:5000/questions`

```json
{
    "success": true,
    "created": 30,
    "total_questions": 20,
}

OR

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

#### GET '/categories/{category_id}/questions'

- Fetches and returns a list of question objects, success value, total number of questions and a dictionary of the current category in which the keys are the ids and the value is the corresponding string of the category 
- Request Arguments: id integer
- Sample: `curl http://127.0.0.1:5000//categories/1/questions`

```json
{
  "current_category": {
    "1": "Science"
  },
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Priscilla",
      "category": 1,
      "difficulty": 1,
      "id": 39,
      "question": "Whio is Austin's first love"
    }
  ],
  "success": true,
  "total_questions": 4
}

####POST '/quizzes'
- Sends a post request in order to get the next question
- Request Body:
{
    "previous_questions": [1, 4, 20, 15]
    "quiz_category": current_category
}
 -Returns a single question object:
{
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
}