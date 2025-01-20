# agents_api.py
from typing import List, Optional, Dict
from uuid import UUID, uuid4
from ninja.errors import HttpError
from asgiref.sync import sync_to_async

from ...services.view_base import ApiRouteV2
from application.models import Agent
from darkscryc2server.Utils.remote_utils.commands import (
    remote_get_connections,
)
from application.views.api.Schemas.agents import AgentIn, AgentOut
from application.views.api.Schemas.general import DeletedSuccessfully, EditedSuccessfully


class AgentsApi(ApiRouteV2):
    """
    Subclass for "Agents" endpoints.
    We handle GET and POST on the same path '/agents' with a single function.
    """

    def __init__(self):
        super().__init__(tags=["Agnets"])
        self.register_routes()


    async def get_agents(self, request, agent_id: Optional[UUID] = None) -> List[AgentOut]:        
        if agent_id:
            single_agent = await Agent.objects.filter(AgentId=agent_id).afirst()
            agents = [single_agent] if single_agent else []
        else:
            agents = await test()

        data = await remote_get_connections()
        if not data.success:
            raise HttpError(500, data.error)

        connections = data.data.get("connections", {})

        result = []
        for agent in agents:
            if not agent:
                continue
            agent_uuid_str = str(agent.AgentId)
            is_active = agent_uuid_str in connections
            address = connections.get(agent_uuid_str, {}).get("address", "Unknown")

            result.append(AgentOut(
                AgentId=agent.AgentId,
                HostName=agent.HostName,
                Os=agent.Os,
                LastTimeUpdate=agent.LastTimeUpdate,
                OnboardedTime=agent.OnboardedTime,
                is_active=is_active,
                address=address
            ))
        return result

    async def create_agent(self, request, payload: AgentIn) -> AgentOut:
        new_agent = await Agent.objects.acreate(
            AgentId=uuid4(),
            HostName=payload.HostName,
            Os=payload.Os
        )
        data = await remote_get_connections()
        connections = data.data.get("connections", {}) if data.success else {}
        agent_uuid_str = str(new_agent.AgentId)
        is_active = agent_uuid_str in connections
        address = connections.get(agent_uuid_str, {}).get("address", "Unknown")

        return AgentOut(
            AgentId=new_agent.AgentId,
            HostName=new_agent.HostName,
            Os=new_agent.Os,
            LastTimeUpdate=new_agent.LastTimeUpdate,
            OnboardedTime=new_agent.OnboardedTime,
            is_active=is_active,
            address=address
        )
    
    async def update_agent(self, request, agent_id: UUID, payload: AgentIn) -> AgentOut:
        agent = await Agent.objects.filter(AgentId=agent_id).afirst()
        if not agent:
            raise HttpError(404, "Agent not found")

        agent.HostName = payload.HostName
        agent.Os = payload.Os
        await agent.asave()

        data = await remote_get_connections()
        connections = data.data.get("connections", {}) if data.success else {}
        agent_uuid_str = str(agent.AgentId)
        is_active = agent_uuid_str in connections
        address = connections.get(agent_uuid_str, {}).get("address", "Unknown")

        return AgentOut(
            AgentId=agent.AgentId,
            HostName=agent.HostName,
            Os=agent.Os,
            LastTimeUpdate=agent.LastTimeUpdate,
            OnboardedTime=agent.OnboardedTime,
            is_active=is_active,
            address=address
        )

    async def delete_agent(self, request, agent_id: UUID):
        agent = await Agent.objects.filter(AgentId=agent_id).afirst()
        if not agent:
            raise HttpError(404, "Agent not found")

        await Agent.objects.filter(AgentId=agent_id).adelete()

        return DeletedSuccessfully(detail="Agent deleted successfully")


    def register_routes(self):
        self.register_route(
            path="/",
            methods=["GET"],
            view_func=self.get_agents,
            response={200: List[AgentOut]},
            summary="Get Agent/s details."
        )
        self.register_route(
            path="/",
            methods=["POST"],
            view_func=self.create_agent,
            response={200: AgentOut},
            permissions_req=["application.add_agent"],
            summary = "Create new onboarded agent"
        )
        self.register_route(
            path="/{agent_id}",
            methods=["PUT"],
            view_func=self.update_agent,
            response={200: AgentOut},
            permissions_req=["application.change_agent"],
            summary="Update an existing agent (HostName/Os only)"
        )

        self.register_route(
            path="/{agent_id}",
            methods=["DELETE"],
            view_func=self.delete_agent,
            response={200: DeletedSuccessfully},
            permissions_req=["application.delete_agent"],
            summary="Delete an existing agent"
        )

@sync_to_async
def test():
    return list(Agent.objects.all())