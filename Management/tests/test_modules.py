import json
import uuid

import pytest
from httpx import AsyncClient

from app.models.user import UserRole

pytestmark = pytest.mark.anyio


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def test_execution_and_collection_modules(
    client: AsyncClient, create_test_user, get_token, monkeypatch
):
    await create_test_user("op", UserRole.OPERATOR)
    token = await get_token("op")

    async def fake_get_connections():
        return []

    async def fake_get_connection(agent_id: str):
        return {}

    monkeypatch.setattr(
        "app.controllers.agent_controller.remote_get_connections",
        fake_get_connections,
    )
    monkeypatch.setattr(
        "app.controllers.agent_controller.remote_get_connection",
        fake_get_connection,
    )

    resp = await client.post(
        "/agents/",
        json={"host_name": "host", "os": "linux"},
        headers=_auth(token),
    )
    agent_id = resp.json()["agent_id"]

    async def fake_remote_send_command(**kwargs):
        from darkscryc2server.models.messages import AgentResponse, CommandIdentifiers

        if kwargs.get("action_id") == CommandIdentifiers.SNAP_FULL_DIRECTORY:
            snapshot = {"Files": [], "Directories": {"Items": []}, "RootPath": "/"}
            return AgentResponse(
                success=True, data={"directory_snapshot": json.dumps(snapshot)}
            )
        return AgentResponse(success=True, data={"result": "ok"})

    monkeypatch.setattr(
        "darkscryc2server.utils.remote_manager.remote_send_command",
        fake_remote_send_command,
    )
    monkeypatch.setattr(
        "app.services.modules.execution.remote_send_command",
        fake_remote_send_command,
    )
    monkeypatch.setattr(
        "app.services.modules.collection.remote_send_command",
        fake_remote_send_command,
    )

    class DummyExecutor:
        async def enqueue_job(self, *args, **kwargs):
            class Job:
                job_id = str(uuid.uuid4())

            return Job()

    async def fake_get_executor():
        return DummyExecutor()

    monkeypatch.setattr(
        "app.utils.tasks.get_task_executor",
        fake_get_executor,
    )
    monkeypatch.setattr(
        "app.services.modules.execution.get_task_executor",
        fake_get_executor,
    )
    monkeypatch.setattr(
        "app.services.modules.collection.get_task_executor",
        fake_get_executor,
    )

    resp = await client.post(
        f"/agents/{agent_id}/modules/execution/shell/run_command",
        json={"command": "whoami"},
        headers=_auth(token),
    )
    assert resp.status_code == 200
    assert resp.json()["success"] is True

    resp = await client.post(
        f"/agents/{agent_id}/modules/execution/shell/start_shell",
        json={},
        headers=_auth(token),
    )
    assert resp.status_code == 200
    assert "task_id" in resp.json()

    resp = await client.get(
        f"/agents/{agent_id}/modules/collection/machine/basic_machine_info",
        headers=_auth(token),
    )
    assert resp.status_code == 200
    assert "task_id" in resp.json()

    resp = await client.post(
        f"/agents/{agent_id}/modules/collection/files/files_explorer_task",
        json={"path": "/"},
        headers=_auth(token),
    )
    assert resp.status_code == 200
    assert "task_id" in resp.json()

    resp = await client.post(
        f"/agents/{agent_id}/modules/collection/files/files_explorer_stream",
        json={"path": "/"},
        headers=_auth(token),
    )
    assert resp.status_code == 200
    assert resp.json()["RootPath"] == "/"

    resp = await client.post(
        f"/agents/{agent_id}/modules/collection/files/get_file_base64",
        json={"path": "/tmp/file.txt"},
        headers=_auth(token),
    )
    assert resp.status_code == 200
    assert "task_id" in resp.json()

    resp = await client.post(
        f"/agents/{agent_id}/modules/collection/files/upload_base64",
        json={"path": "/tmp/file.txt", "file_base64": "Zg==", "file_name": "f.txt"},
        headers=_auth(token),
    )
    assert resp.status_code == 200
    assert "task_id" in resp.json()

    resp = await client.get(
        f"/agents/{agent_id}/modules/collection/passwords/wifi_basic_info",
        headers=_auth(token),
    )
    assert resp.status_code == 200
    assert "task_id" in resp.json()

    resp = await client.get(
        f"/agents/{agent_id}/modules/collection/process/enumerate_processes",
        headers=_auth(token),
    )
    assert resp.status_code == 200
    assert "task_id" in resp.json()
