from __future__ import annotations

import logging
from typing import Any, cast

from flask import Flask, flash, redirect, render_template, session, url_for
from requests import RequestException
from werkzeug.wrappers import Response

from sem_python.domain.exceptions import DomainError
from sem_python.infrastructure.repositories import (
    SqlAlchemyPredictionRepository,
    SqlAlchemyUserRepository,
)
from sem_python.infrastructure.security import WerkzeugPasswordHasher
from sem_python.services.auth import AuthService
from sem_python.services.history import PredictionHistoryService
from sem_python.web_app.auth import current_user_id, login_required
from sem_python.web_app.forms import LoginForm, PredictionForm, RegisterForm
from sem_python.web_app.http_client import MlApiClient

logger = logging.getLogger(__name__)


def _ml_client(app: Flask) -> MlApiClient:
    return cast(MlApiClient, app.extensions["ml_api_client"])


def register_routes(app: Flask) -> None:
    from sem_python.web_app.app import get_db_session

    @app.get("/")
    def index() -> Response:
        if "user_id" in session:
            return redirect(url_for("predict"))
        return redirect(url_for("login"))

    @app.route("/register", methods=["GET", "POST"])
    def register() -> str | Response:
        form = RegisterForm()
        if form.validate_on_submit():
            with get_db_session(app) as db:
                service = AuthService(SqlAlchemyUserRepository(db), WerkzeugPasswordHasher())
                try:
                    user = service.register(form.username.data or "", form.password.data or "")
                except DomainError as exc:
                    flash(str(exc), "danger")
                else:
                    session["user_id"] = user.id
                    session["username"] = user.username
                    logger.info("Registered user %s", user.username)
                    flash("Аккаунт успешно создан.", "success")
                    return redirect(url_for("predict"))
        return render_template("register.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login() -> str | Response:
        form = LoginForm()
        if form.validate_on_submit():
            with get_db_session(app) as db:
                service = AuthService(SqlAlchemyUserRepository(db), WerkzeugPasswordHasher())
                try:
                    user = service.authenticate(form.username.data or "", form.password.data or "")
                except DomainError as exc:
                    flash(str(exc), "danger")
                else:
                    session["user_id"] = user.id
                    session["username"] = user.username
                    logger.info("User %s signed in", user.username)
                    flash("Вход выполнен успешно.", "success")
                    return redirect(url_for("predict"))
        return render_template("login.html", form=form)

    @app.post("/logout")
    @login_required
    def logout() -> Response:
        username = session.get("username")
        session.clear()
        logger.info("User %s signed out", username)
        flash("Вы вышли из системы.", "info")
        return redirect(url_for("login"))

    @app.route("/predict", methods=["GET", "POST"])
    @login_required
    def predict() -> str | Response:
        form = PredictionForm()
        prediction: dict[str, Any] | None = None
        model_info: dict[str, Any] | None = None

        try:
            model_info = _ml_client(app).model_info()
        except (RequestException, ValueError) as exc:
            logger.error("Could not load model info: %s", exc)

        if form.validate_on_submit():
            features = {
                "sepal_length": float(form.sepal_length.data or 0),
                "sepal_width": float(form.sepal_width.data or 0),
                "petal_length": float(form.petal_length.data or 0),
                "petal_width": float(form.petal_width.data or 0),
            }
            try:
                prediction = _ml_client(app).predict(features)
            except (RequestException, ValueError) as exc:
                logger.error("Prediction failed: %s", exc)
                flash("ML API недоступен. Попробуйте позже.", "danger")
            else:
                with get_db_session(app) as db:
                    history = PredictionHistoryService(SqlAlchemyPredictionRepository(db))
                    history.save(
                        user_id=current_user_id(),
                        input_data=features,
                        prediction=prediction,
                    )
                logger.info("Saved prediction for user %s", current_user_id())
                flash("Предсказание сохранено в истории.", "success")

        return render_template(
            "predict.html",
            form=form,
            prediction=prediction,
            model_info=model_info,
        )

    @app.get("/history")
    @login_required
    def history() -> str | Response:
        with get_db_session(app) as db:
            service = PredictionHistoryService(SqlAlchemyPredictionRepository(db))
            records = service.list_for_user(current_user_id())
        return render_template("history.html", records=records)

    @app.after_request
    def add_security_headers(response: Response) -> Response:
        response.headers["Content-Security-Policy"] = "default-src 'self' https://cdn.jsdelivr.net"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response
