from fastapi import FastAPI
from . import routers as api_routes
from . import ws_manager
from ..Server import Server



def create_manager_app(server: Server) -> FastAPI:
    """
    Returns a FastAPI app that manages connections in `server.connection_manager`.
    """
    app = FastAPI(
        title="C2 Manager",
        version="1.0.0",
        description="FastAPI application for controlling and monitoring connections."
    )

    # 1) Include the HTTP router
    app.include_router(api_routes.router, prefix="/api", tags=["Manager"], 
                       dependencies=[],  # add security dependencies if needed
                       responses={404: {"description": "Not found"}})

    # 2) Attach the server instance so routers can access it
    app.state.server = server

    # 3) Add a simple health-check route
    @app.get("/health", tags=["Health"])
    def health_check():
        return {"status": "ok"}

    # 4) Add a WebSocket endpoint
    #    We'll define it in manager_ws.py for readability
    app.add_api_websocket_route("/manager_ws", ws_manager.manager_ws_endpoint, name="manager_ws")

    return app
