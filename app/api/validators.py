from typing import Union
from fastapi import HTTPException, status

from app.models.urls import UrlModel, UrlCollection
from app.models.collection import Collection
from app.models.user import User


def is_url_exist(object: Union[UrlModel, None]) -> None:
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


def is_objects_exist_and_user_author_collection(
        collection: Union[Collection, None],
        url: Union[UrlModel, None],
        user: User
) -> None:
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такой коллекции не существует.'
        )
    if url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такой ссылки не существует.'
        )
    if collection.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='У вас нет доступа к этой коллекции.'
        )


def is_collection_exist_and_available(
    collection: Union[Collection, None],
    user: User
) -> None:
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такой коллекции не существует.'
        )
    if collection.user != user and collection.is_public is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='У вас нет доступа к этой коллекции.'
        )


def is_relation_exist(
        relation: Union[UrlCollection, None]
) -> None:
    if relation is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Ссылка уже добавлена в коллекцию.'
        )
