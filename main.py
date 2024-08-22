import asyncio
import threading

import uvicorn
from grpc import aio

from function.config_manager import ConfigManager
from app.app_init import create_app, create_connection
from server.proto import system_log_pb2_grpc
from server.server import SystemLogService

conn_all = create_connection(ConfigManager)
app = create_app(*conn_all)
def start_fastapi_server():
    uvicorn.run(app="main:app", host='0.0.0.0', port=ConfigManager.server.port,
                log_level="info", limit_concurrency=1000)

async def start_grpc_server():
    server = aio.server()
    server.add_insecure_port(f'[::]:{ConfigManager.server.g_port}')
    system_log_pb2_grpc.add_SystemLogServiceServicer_to_server(SystemLogService(*conn_all), server)
    await server.start()
    print(f"gRPC server running on port {ConfigManager.server.g_port}...")
    await server.wait_for_termination()


def run_servers():
    fastapi_thread = threading.Thread(target=start_fastapi_server)
    fastapi_thread.start()
    asyncio.run(start_grpc_server())


if __name__ == "__main__":
    run_servers()
