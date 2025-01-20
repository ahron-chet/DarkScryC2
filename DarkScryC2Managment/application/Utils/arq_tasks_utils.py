from DarkScryC2Managment.arq_worker import WorkerSettings
from arq import create_pool




_redis_pool = None
async def get_task_executor():
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = await create_pool(WorkerSettings.redis_settings)
    return _redis_pool


async def close_task_executors():
    global _redis_pool
    if _redis_pool is not None:
        await _redis_pool.close()
        _redis_pool = None