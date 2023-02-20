from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, unique=True)
    answer = Column(String, nullable=False)
    category = Column(String, nullable=False)
    level = Column(String, nullable=False)
    wrong1 = Column(String, nullable=False)
    wrong2 = Column(String, nullable=False)
    wrong3 = Column(String, nullable=False)

    def generate_dictionary(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary
    