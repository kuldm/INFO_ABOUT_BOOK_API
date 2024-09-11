from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base
from models.books import book_author_association


# Модель Авторов
class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Связь с книгами: многие ко многим
    books = relationship("Book", secondary=book_author_association, back_populates="authors")
