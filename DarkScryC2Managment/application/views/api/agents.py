from application.services.view_base import BaseAsyncView
from django.http import JsonResponse



from darkscryc2server.Utils.remote_utils.commands import (
    remote_get_connections, 
    remote_send_command
)


async def get_connections(request):
    connections = await remote_get_connections()
    if not connections.success:
        return JsonResponse({"error": connections.error}, 500)

    

