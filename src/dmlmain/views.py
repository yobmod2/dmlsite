from __future__ import annotations

from typing import TYPE_CHECKING, Literal, cast

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django_user_agents.utils import get_user_agent
from user_agents.parsers import UserAgent

# from django.contrib.auth.models import User
from .forms import SignUpForm

if TYPE_CHECKING:
    from django.core.handlers.wsgi import WSGIRequest


def get_user_agent_wrapper(req: HttpRequest) -> UserAgent | Literal[""]:
    return cast(UserAgent | Literal[""], get_user_agent(req))  # type: ignore


def test(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Simple Django App with SQLite and WhiteNoise</h1>")


def home(request: WSGIRequest) -> HttpResponse:
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    if request.user.is_authenticated:
        text = f"Hello {request.user}"
    else:
        text = "Welcome visitor"
    context = {"text": text, "form": form, "user": request.user}

    user_agent = get_user_agent_wrapper(request)
    if isinstance(user_agent, UserAgent) and user_agent.is_mobile is True:
        # return render(request, 'dmlmain/homepage_mob.html', context)
        return HttpResponse("you are on a mobile")

    else:
        return render(request, "dmlmain/homepage.html", context)
