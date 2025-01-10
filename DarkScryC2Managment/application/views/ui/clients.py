# application/routes/ui/views/alerts/views.py
from django.shortcuts import render
from application.services.view_base import BaseAsyncView


class ShowClients(BaseAsyncView):
    
    async def get(self, request, *args, **kwargs):
        return render(request, 'index.html', context={'section': 'clients'})

