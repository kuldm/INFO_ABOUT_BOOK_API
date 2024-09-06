from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base
from models.books import book_tag_association


# Модель Тегов
class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Связь с книгами: многие ко многим
    books = relationship("Book", secondary=book_tag_association, back_populates="tags")