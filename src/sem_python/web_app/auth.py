from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar, cast

from flask import flash, redirect, session, url_for
from werkzeug.wrappers import Response

P = ParamSpec("P")
R = TypeVar("R")


def login_required(view: Callable[P, R]) -> Callable[P, R | Response]:
    @wraps(view)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> R | Response:
        if "user_id" not in session:
            flash("Войдите в систему, чтобы продолжить.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return cast(Callable[P, R | Response], wrapped)


def current_user_id() -> int:
    user_id = session.get("user_id")
    if not isinstance(user_id, int):
        raise RuntimeError("Current user is not authenticated")
    return user_id
