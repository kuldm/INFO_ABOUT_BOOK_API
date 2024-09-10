from fastapi import Request, Depends
from jose import jwt, JWTError, ExpiredSignatureError

from config import settings
from exceptions import TokenAbsentException, IncorrectTokenFormatException, TokenExpiredException, \
    UserIsNotPresentException
from services.user_service import UserService
from logger_config import logger
from utils.elasticsearch_utils import index_document

es_index = 'auth_logs_2'


def get_token(request: Request):
    """Извлекает токен из куки запроса."""
    token = request.cookies.get('user_access_token')
    if not token:
        logger.error("Token is absent in the request cookies")
        index_document(es_index, 'token_check', None, {'status': 'failed', 'reason': 'token_absent'})
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    """Получает текущего пользователя на основе токена."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM,
        )
    except ExpiredSignatureError:
        index_document(es_index, 'token_check', None, {'status': 'failed', 'reason': 'token_expired'})
        raise TokenExpiredException

    except JWTError:
        index_document(es_index, 'token_check', None, {'status': 'failed', 'reason': 'invalid_token'})
        raise IncorrectTokenFormatException

    # Извлечение user_id из payload
    user_id: str = payload.get('sub')
    if not user_id:
        logger.error("User ID not found in token payload")
        index_document(es_index, 'token_check', None, {'status': 'failed', 'reason': 'user_id_missing'})
        raise UserIsNotPresentException

    # Поиск пользователя в базе данных
    user = await UserService.find_user(id=int(user_id))
    if not user:
        logger.error(f"User with ID {user_id} not found in the database")
        index_document(es_index, 'token_check', None,
                       {'status': 'failed', 'reason': 'user_not_found', 'user_id': user_id})
        raise UserIsNotPresentException

    index_document(es_index, 'token_check', user_id, {'status': 'success', 'user_id': user_id})
    return user
