from typing import Union
from fastapi import HTTPException, status

from app.models.urls import UrlModel


def is_object_exist(object: Union[UrlModel, None]) -> None:
    if object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такой ссылки не существует.'
        )


def is_short_url_exist(object: Union[UrlModel, None]) -> None:
    if object is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Такая короткая ссылка уже существует. Придумайте другую.'
        )
