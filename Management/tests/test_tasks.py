import uuid
from datetime import datetime

import pytest
from arq.jobs import JobStatus
from httpx import AsyncClient

from app.models.user import UserRole
from app.schemas.tasks import TaskResultOut

pytestmark = pytest.mark.anyio


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def test_task_routes(
    client: AsyncClient, create_test_user, get_token, monkeypatch
):
    await create_test_user("admin", UserRole.ADMIN)
    token = await get_token("admin")

    task_id = uuid.uuid4()

    async def fake_get_status(self, t_id):
        assert t_id == task_id
        return JobStatus.complete

    async def fake_get_result(self, t_id):
        assert t_id == task_id
        return TaskResultOut(
            success=True,
            result={"ok": True},
            start_time=datetime.utcnow(),
            finish_time=datetime.utcnow(),
            action=None,
            job_id=task_id,
        )

    async def fake_revoke(self, t_id):
        assert t_id == task_id

    async def fake_delete(self, t_id):
        assert t_id == task_id

    monkeypatch.setattr(
        "app.services.task_service.TaskService.get_status", fake_get_status
    )
    monkeypatch.setattr(
        "app.services.task_service.TaskService.get_result", fake_get_result
    )
    monkeypatch.setattr(
        "app.services.task_service.TaskService.revoke_task", fake_revoke
    )
    monkeypatch.setattr(
        "app.services.task_service.TaskService.delete_task", fake_delete
    )

    headers = _auth(token)

    resp = await client.get(f"/tasks/{task_id}/status", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == JobStatus.complete.value

    resp = await client.get(f"/tasks/{task_id}/result", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["success"] is True

    resp = await client.put(f"/tasks/{task_id}/revoke", headers=headers)
    assert resp.status_code == 200

    resp = await client.delete(f"/tasks/{task_id}", headers=headers)
    assert resp.status_code == 200
