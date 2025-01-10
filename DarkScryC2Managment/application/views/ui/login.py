from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.handlers.asgi import ASGIRequest
from application.services.view_base import BaseAsyncView


class LoginPage(BaseAsyncView):
    login_required = False

    async def get(self, request:ASGIRequest, *args, **kwargs):
        user = await request.auser()
        if user.is_authenticated:
            return redirect('/index/')
        return render(request, 'login.html')
    
    

class Logout(BaseAsyncView):
    async def get(self, request:ASGIRequest, *args, **kwargs):
        await request.session.aflush()
        return redirect('/index/')

