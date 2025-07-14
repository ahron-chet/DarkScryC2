from django.shortcuts import render
from application.services.view_base import BaseAsyncView

class IndexView(BaseAsyncView):

    async def get(self, request, *args, **kwargs):
        return render(request, 'index.html')