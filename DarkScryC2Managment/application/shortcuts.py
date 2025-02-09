from application.Utils.arq_tasks_utils import get_task_executor

async def make_task(func_name:str, *args, **kargs):
    task_excutor = await get_task_executor()
    job = await task_excutor.enqueue_job(
        func_name,
        *args, **kargs
    )
    return job