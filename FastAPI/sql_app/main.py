from fastapi import FastAPI, Request, status, HTTPException, Depends
from random import choice

from .base import AddModel, UpdateModel, ChangeModel
from sqlalchemy.orm import Session
from .models import Base, Question
from .database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


# ================================================= DEPENDENCY ======================================== #
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================ VARIABLES SECTION ======================================== #
LEVEL = ["easy", "medium", "hard"]
CATEGORY = ["flask", "django", "fastapi"]
OPERATOR = ["between", "more", "less"]

# ============================================ GET REQUESTS SECTION ======================================== #
@app.get("/")
def home_page():
    return {
        "Message": "Hello To Quiz REST API"
    }


@app.get("/all")
def all_page(request: Request, db: Session = Depends(get_db)):
    all_data = db.query(Question).all()
    return {
        "data": [item.generate_dictionary() for item in all_data]
    }


@app.get("/random")
def random_page(db: Session = Depends(get_db)):
    all_data = db.query(Question).all()
    return {
        "Question": choice(all_data).generate_dictionary()
    }


@app.get("/filter/category/{decision}")
def filter_category(decision: str, db: Session = Depends(get_db)):
    if decision.lower() not in CATEGORY:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="We Don't Have that Category!")
    else:
        if decision.lower() == "fastapi":
            answer = db.query(Question).filter_by(category="FastAPI").all()
        else:
            answer = db.query(Question).filter_by(category=decision.capitalize()).all()
        return {
            "data": [item.generate_dictionary() for item in answer]
        }


@app.get("/filter/level/{decision}")
def filter_level(decision: str, db: Session = Depends(get_db)):
    if decision.lower() not in LEVEL:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="We Don't Have that Level!")
    else:
        answer = db.query(Question).filter_by(level=decision.capitalize()).all()
        return {
            "data": [item.generate_dictionary() for item in answer]
        }


@app.get("/filter/id")
def filter_id(
    high: int,
    low: int,
    operator: str,
    db: Session = Depends(get_db)
):
    if operator.lower() not in OPERATOR:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Operator Name!")
    else:
        result = None
        if operator.lower() == "between":
            result = db.query(Question).filter(Question.id>=low, Question.id<=high).all()
        elif operator.lower() == "more":
            result = db.query(Question).filter(Question.id>low).all()
        elif operator.lower() == "less":
            result = db.query(Question).filter(Question.id<low).all()
    return {
        "data": [item.generate_dictionary() for item in result]
    }


# ============================================ POST REQUESTS SECTION ======================================== #
@app.post("/add", status_code=status.HTTP_201_CREATED)
def add_page(tool: AddModel, db: Session = Depends(get_db)):
    new_question = Question(
        question=tool.question,
        answer=tool.answer,
        category=tool.category,
        level=tool.level,
        wrong1=tool.wrong1,
        wrong2=tool.wrong2,
        wrong3=tool.wrong3
    )
    check_point = db.query(Question).filter_by(question=tool.question).first()
    if check_point is not None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Question Already Exists!")
    else:
        db.add(new_question)
        db.commit()
        return {
            "success": {
                "Message": "Congratulations New Questions Has Been Added Successfully!",
                "Status code": 200
            }
        }
    


# ============================================ PATCH REQUESTS SECTION ======================================== #
@app.patch("/update/{question_id}")
def update_page(question_id: int, tool: UpdateModel, db: Session = Depends(get_db)):
    record = db.query(Question).filter_by(id=question_id).first()
    if record is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Record with that ID doesn't exists!")
    else:
        if tool.api_key != "TommyShelby":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Api_Key is wrong!")
        else:
            if tool.field_name == "question":
                record.question = tool.new_value
            elif tool.field_name == "answer":
                record.answer = tool.new_value
            elif tool.field_name == "category":
                record.category = tool.new_value
            elif tool.field_name == "level":
                record.level = tool.new_value
            elif tool.field_name == "wrong1":
                record.wrong1 = tool.new_value
            elif tool.field_name == "wrong2":
                record.wrong2 = tool.new_value
            elif tool.field_name == "wrong3":
                record.wrong3 = tool.new_value
            db.commit()
            return {
                "success": {
                    "Message": "Congratulations, Question Has been Updated!",
                    "Status code": 200
                }
            }



# ============================================ PUT REQUESTS SECTION ======================================== #
@app.put("/change/{question_id}")
def change_page(question_id: int, tool: ChangeModel, db: Session = Depends(get_db)):
    record = db.query(Question).filter_by(id=question_id).first()
    if record is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Record with that ID doesn't exists!")
    else:
        if tool.api_key != "TommyShelby":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Api_Key is wrong!")
        else:
            record.question=tool.question
            record.answer=tool.answer
            record.category=tool.category
            record.level=tool.level
            record.wrong1=tool.wrong1
            record.wrong2=tool.wrong2
            record.wrong3=tool.wrong3
            db.commit()
            return {
                "success": {
                        "Message": "Congratulations, Question Has been Changed!",
                        "Status code": 200
                    }
            }


# ============================================ DELETE REQUESTS SECTION ======================================== #
@app.delete("/delete")
def delete_page(question_id: int, api_key: str, db: Session = Depends(get_db)):
    record = db.query(Question).filter_by(id=question_id).first()
    if record is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Record with that ID doesn't exists!")
    else:
        if api_key != "TommyShelby":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Api_Key is wrong!")
        else:
            db.delete(record)
            db.commit()
            return {
                "success": {
                    "Message": "Congratulations, Question Has been Deleted!",
                    "Status code": 200
                }
            }
