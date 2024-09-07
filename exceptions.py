from fastapi import HTTPException, status


class BookApiException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class TagAlreadyExistException(BookApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Тэг уже существует"


class TagAbsentException(BookApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Такого тэга не существует"


class AuthorAlreadyExistException(BookApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Автор уже существует"


class AuthorAbsentException(BookApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Такого автора не существует"


class BookAlreadyExistException(BookApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Книга уже существует"


class BookAbsentException(BookApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Такой книги не существует"


class AuthorsMissingException(BookApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Поле 'Автор' не может быть пустым"


class TagsMissingException(BookApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Поле 'Тэг' не может быть пустым"


class LinkM2MException(BookApiException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Невозможно удалить, поскольку на значение есть ссылка в другой таблице."


class UserAlreadyExistException(BookApiException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BookApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BookApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истёк"


class TokenAbsentException(BookApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BookApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(BookApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
