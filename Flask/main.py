from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)

# =================================== PREPARE SQL DATABASE =================================== #
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, unique=True, nullable=False)
    answer = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    level = db.Column(db.String, nullable=False)
    wrong1 = db.Column(db.String, nullable=False)
    wrong2 = db.Column(db.String, nullable=False)
    wrong3 = db.Column(db.String, nullable=False)

    # generate dictionary:
    def generate_dictionary(self):
        my_dictionary = {}
        for column in self.__table__.columns:
            my_dictionary[column.name] = getattr(self, column.name)
        return my_dictionary


# =================================== GET REQUEST SECTION =================================== #
@app.route("/")
def home_page():
    return jsonify(
        welcome={
            "Message": "Welcome this is Question REST API",
            "Status code": 200
        }
    )


@app.route("/all")
def all_page():
    question_list = db.session.query(Questions).all()
    return jsonify(
        Quiz=[question.generate_dictionary() for question in question_list]
    )


@app.route("/random")
def random_page():
    question = choice(db.session.query(Questions).all())
    return jsonify(
        Quiz=question.generate_dictionary()
    )


@app.route("/filter/category/<string:decision>")
def filter_category(decision):
    question_list = db.session.query(Questions).filter_by(category=decision).all()
    return jsonify(
        Quiz=[question.generate_dictionary() for question in question_list]
    )


@app.route("/filter/level/<string:decision>")
def filter_level(decision):
    question_list = db.session.query(Questions).filter_by(level=decision).all()
    return jsonify(
        Quiz=[question.generate_dictionary() for question in question_list]
    )


@app.route("/filter/multiple")
def filter_multiple():
    chosen_category = request.args.get("category")
    chosen_level = request.args.get("level")
    question_list = []
    available_categories = ["Django", "Flask", "Express"]
    available_levels = ["Easy", "Medium", "Hard"]

    if (chosen_category is not None) and (chosen_level is not None):
        chosen_category = chosen_category.capitalize()
        chosen_level = chosen_level.capitalize()
        if (chosen_category in available_categories) and (chosen_level in available_levels):
            question_list = db.session.query(Questions).filter_by(
                category=chosen_category,
                level=chosen_level
            ).all()
        else:
            return jsonify(
                error={
                    "Message": "Please Enter Category and Level values Correctly!",
                    "Available Categories": ["Django", "Flask", "Express"],
                    "Available Levels": ["Easy", "Medium", "Hard"]
                }
            )
    elif (chosen_category is not None) and (chosen_level is None):
        chosen_category = chosen_category.capitalize()
        if chosen_category in available_categories:
            question_list = db.session.query(Questions).filter_by(category=chosen_category).all()
        else:
            return jsonify(
                error={
                    "Message": "Category is not defined Correctly!",
                    "Available Categories": ["Django", "Flask", "Express"]
                }
            )

    elif (chosen_category is None) and (chosen_level is not None):
        chosen_level = chosen_level.capitalize()
        if chosen_level in available_levels:
            question_list = db.session.query(Questions).filter_by(level=chosen_level).all()
        else:
            return jsonify(
                error={
                    "Message": "Level is not defined Correctly!",
                    "Available Levels": ["Easy", "Medium", "Hard"]
                }
            )

    return jsonify(
        Quiz=[question.generate_dictionary() for question in question_list]
    )


# =================================== POST REQUEST SECTION =================================== #
@app.route("/add", methods=["POST"])
def add_page():
    available_category = ["Django", "Flask", "Express"]
    available_level = ["Easy", "Medium", "Hard"]
    data = {
        "question": request.json["question"],
        "answer": request.json["answer"],
        "category": request.json["category"],
        "level": request.json["level"],
        "wrong1": request.json["wrong1"],
        "wrong2": request.json["wrong2"],
        "wrong3": request.json["wrong3"]
    }
    if (data["category"].capitalize() in available_category) and (data["level"].capitalize() in available_level):
        new_question = Questions(
            question=data["question"].capitalize(),
            answer=data["answer"].capitalize(),
            category=data["category"].capitalize(),
            level=data["level"].capitalize(),
            wrong1=data["wrong1"].capitalize(),
            wrong2=data["wrong2"].capitalize(),
            wrong3=data["wrong3"].capitalize()
        )
        db.session.add(new_question)
        db.session.commit()
        return jsonify(
            success={
                "Message": "Congratulations New Questions Has Been Added Successfully!",
                "Status code": 200
            }
        )
    else:
        return jsonify(
            errorr={
                "Message": "We except restricted types of Categories and Levels!",
                "Available Categories": available_category,
                "Available Levels": available_level
            }
        )


# =================================== PATCH REQUEST SECTION =================================== #
@app.route("/update/<int:question_id>", methods=["PATCH"])
def update_page(question_id):
    valid_fields = ["question", "answer", "category", "level", "wrong1", "wrong2", "wrong3"]
    entered_key = request.args.get("api_key")
    chosen_field = request.args.get("field")
    new_value = request.args.get("value")
    chosen_question = db.session.query(Questions).filter_by(id=question_id).first()

    if entered_key == "TommyShelby":
        if (chosen_field.lower() in valid_fields) and (new_value is not None):
            if chosen_field.lower() == "question":
                chosen_question.question = new_value
            elif chosen_field.lower() == "answer":
                chosen_question.answer = new_value
            elif chosen_field.lower() == "category":
                chosen_question.category = new_value
            elif chosen_field.lower() == "level":
                chosen_question.level = new_value
            elif chosen_field.lower() == "wrong1":
                chosen_question.wrong1 = new_value
            elif chosen_field.lower() == "wrong2":
                chosen_question.wrong2 = new_value
            elif chosen_field.lower() == "wrong3":
                chosen_question.wrong3 = new_value
            db.session.commit()
            return jsonify(
                success={
                    "Message": "Congratulations, Question Has been Updated!",
                    "Status code": 200
                }
            )
        elif new_value is None:
            return jsonify(
                errorr={
                    "Message": "New Value is not defined!"
                }
            )
        else:
            return jsonify(
                errorr={
                    "Message": "Field name is wrong",
                    "Valid Fields": valid_fields
                }
            )
    else:
        return jsonify(
            errorr={
                "Message": "Api Key is Wrong - FORBIDDEN!",
                "Status code": 403
            }
        )


# =================================== PUT REQUEST SECTION =================================== #
@app.route("/change/<int:question_id>", methods=["PUT"])
def change_page(question_id):
    valid_categories = ["Django", "Flask", "Express"]
    valid_levels = ["Easy", "Medium", "Hard"]
    chosen_question = db.session.query(Questions).filter_by(id=question_id).first()
    if chosen_question is not None:
        entered_key = request.args.get("api_key")
        new_question = request.json["question"]
        new_answer = request.json["answer"]
        new_category = request.json["category"]
        new_level = request.json["level"]
        new_wrong1 = request.json["wrong1"]
        new_wrong2 = request.json["wrong2"]
        new_wrong3 = request.json["wrong3"]

        if entered_key == "TommyShelby":
            if (new_category.capitalize() in valid_categories) and (new_level.capitalize() in valid_levels):
                chosen_question.question = new_question
                chosen_question.answer = new_answer
                chosen_question.category = new_category
                chosen_question.level = new_level
                chosen_question.wrong1 = new_wrong1
                chosen_question.wrong2 = new_wrong2
                chosen_question.wrong3 = new_wrong3
                db.session.commit()
                return jsonify(
                    success={
                        "Message": "Congratulations, Question Has been Changed!",
                        "Status code": 200
                    }
                )
            else:
                return jsonify(
                    errorr={
                        "Message": "We except restricted types of Categories and Levels!",
                        "Available Categories": valid_categories,
                        "Available Levels": valid_levels
                    }
                )
        else:
            return jsonify(
                errorr={
                    "Message": "Api Key is Wrong - FORBIDDEN!",
                    "Status code": 403
                }
            )
    else:
        return jsonify(
            errorr={
                "Message": "Question ID not valid - CHANGE IT!"
            }
        )


# =================================== DELETE REQUEST SECTION =================================== #
@app.route("/delete/<int:question_id>", methods=["DELETE"])
def delete_page(question_id):
    chosen_question = db.session.query(Questions).filter_by(id=question_id).first()
    entered_key = request.args.get("api_key")
    if chosen_question is not None:
        if entered_key == "TommyShelby":
            db.session.delete(chosen_question)
            db.session.commit()
            return jsonify(
                success={
                    "Message": "Congratulations, Question Has been Deleted!",
                    "Status code": 200
                }
            )
        else:
            return jsonify(
                errorr={
                    "Message": "Api Key is Wrong - FORBIDDEN!",
                    "Status code": 403
                }
            )
    else:
        return jsonify(
            errorr={
                "Message": "Question ID not valid - CHANGE IT!"
            }
        )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
