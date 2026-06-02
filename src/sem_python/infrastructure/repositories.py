from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from sem_python.domain.entities import NewPredictionRecord, NewUser, PredictionRecord, User
from sem_python.domain.repositories import PredictionRepository, UserRepository
from sem_python.infrastructure.models import PredictionModel, UserModel


def _to_user(model: UserModel) -> User:
    return User(
        id=model.id,
        username=model.username,
        hashed_password=model.hashed_password,
        created_at=model.created_at,
    )


def _to_prediction(model: PredictionModel) -> PredictionRecord:
    return PredictionRecord(
        id=model.id,
        user_id=model.user_id,
        input_data=model.input_data,
        prediction=model.prediction,
        created_at=model.created_at,
    )


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, user_id: int) -> User | None:
        model = self._session.get(UserModel, user_id)
        return None if model is None else _to_user(model)

    def get_by_username(self, username: str) -> User | None:
        model = self._session.scalar(select(UserModel).where(UserModel.username == username))
        return None if model is None else _to_user(model)

    def add(self, user: NewUser) -> User:
        model = UserModel(username=user.username, hashed_password=user.hashed_password)
        self._session.add(model)
        self._session.flush()
        return _to_user(model)


class SqlAlchemyPredictionRepository(PredictionRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, prediction: NewPredictionRecord) -> PredictionRecord:
        model = PredictionModel(
            user_id=prediction.user_id,
            input_data=prediction.input_data,
            prediction=prediction.prediction,
        )
        self._session.add(model)
        self._session.flush()
        return _to_prediction(model)

    def list_for_user(self, user_id: int) -> list[PredictionRecord]:
        rows = self._session.scalars(
            select(PredictionModel)
            .where(PredictionModel.user_id == user_id)
            .order_by(PredictionModel.created_at.desc()),
        ).all()
        return [_to_prediction(row) for row in rows]
