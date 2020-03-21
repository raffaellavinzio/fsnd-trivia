import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app)

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, DELETE, OPTIONS')
        return response

    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories')
    def get_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            formatted_categories = {
                category.id: category.type for category in categories}
            if (len(categories) == 0):
                raise Exception()
            result = {
                "success": True,
                "categories": formatted_categories
            }
            return jsonify(result)

        except:
            db.session.rollback()
            abort(404)

        finally:
            db.session.close()

    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for two pages.
  Clicking on the page numbers should update the questions.
  '''
    @app.route('/questions')
    def get_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            formatted_questions = [question.format() for question in questions]

            # pagination of 10 items per page
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * 10
            end = start + 10
            current_questions = formatted_questions[start:end]

            categories = Category.query.order_by(Category.id).all()
            formatted_categories = {
                category.id: category.type for category in categories}

            if (len(current_questions) == 0):
                raise Exception()

            result = {
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions),
                "categories": formatted_categories,
                "current_category": None}
            return jsonify(result)

        except:
            db.session.rollback()
            abort(404)

        finally:
            db.session.close()

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                raise Exception()

            question.delete()
            result = {'success': True,
                      'deleted_question': question.format(),
                      'total_questions': len(Question.query.all())}

            return jsonify(result)

        except:
            db.session.rollback()
            abort(404)

        finally:
            db.session.close()

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    # combining the 2 endpoints above into one decorator
    @app.route('/questions', methods=['POST'])
    def add_or_search_question():
        body = request.get_json()

        # add new question
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)
        # search questions text by term
        search = body.get('searchTerm', None)

        try:
            if search is not None:
                questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(search)))
                formatted_questions = [question.format()
                                       for question in questions]

                result = {
                    'success': True,
                    'questions': formatted_questions,
                    'total_questions': len(formatted_questions),
                    'current_category': None}
                return jsonify(result)

            else:
                if question == None or answer == None:
                    raise Exception()
                question = Question(question=question, answer=answer,
                                    difficulty=difficulty, category=category)
                question.insert()

                result = {'success': True,
                          'added_question': question.format(),
                          'total_questions': len(Question.query.all())}
                return jsonify(result)

        except:
            db.session.rollback()
            abort(422)

        finally:
            db.session.close()

    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        valid_category = (category_id <= len(
            Category.query.all()) and (category_id > 0))

        try:
            questions = Question.query.order_by(Question.id).filter(
                Question.category == category_id).all()
            formatted_questions = [question.format()
                                   for question in questions]

            if not valid_category:
                raise Exception()

            result = {
                "success": True,
                "questions": formatted_questions,
                "total_questions": len(formatted_questions),
                "current_category": None}
            return jsonify(result)

        except:
            db.session.rollback()
            if not valid_category:
                abort(400)
            else:
                abort(422)

        finally:
            db.session.close()

    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/quizzes', methods=['POST'])
    def get_questions_to_play():
        body = request.get_json()

        # add new question
        previous_questions = body.get('previous_questions', [])
        category = body.get('quiz_category', None)

        try:

            if int(category["id"]) != 0:
                questions = Question.query.order_by(Question.id).filter(
                    Question.category == int(category["id"])).all()
            else:
                questions = Question.query.order_by(Question.id).all()

            all_questions = [question.format()
                             for question in questions]
            available_questions = [
                q for q in all_questions if q["id"] not in previous_questions]

            if len(available_questions):
                return jsonify({"success": True, "question": random.choice(available_questions)})
            else:
                return jsonify({"success": True, "question": None})

        except:
            db.session.rollback()
            abort(422)

        finally:
            db.session.close()

    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server Error"
        }), 500

    return app
