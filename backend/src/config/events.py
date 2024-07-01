import typing

import fastapi
import loguru

from src.repository.events import (
    dispose_db_connection, 
    initialize_db_connection,
    initialize_vectordb_collection,
    initialize_inference_client,
    initialize_anonymous_user
    )


def execute_backend_server_event_handler(backend_app: fastapi.FastAPI) -> typing.Any:
    async def launch_backend_server_events() -> None:
        await initialize_db_connection(backend_app=backend_app)
        await initialize_vectordb_collection()
        await initialize_inference_client()
        await initialize_anonymous_user()
    return launch_backend_server_events


def terminate_backend_server_event_handler(backend_app: fastapi.FastAPI) -> typing.Any:
    @loguru.logger.catch
    async def stop_backend_server_events() -> None:
        await dispose_db_connection(backend_app=backend_app)

    return stop_backend_server_events
