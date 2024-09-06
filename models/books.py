from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

book_author_association = Table(
    'book_author', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id'), primary_key=True)
)

book_tag_association = Table(
    'book_tag', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


# Модель Книг
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

    # Связь с авторами и тегами: многие ко многим
    authors = relationship('Author', secondary=book_author_association, back_populates='books')
    tags = relationship('Tag', secondary=book_tag_association, back_populates='books')