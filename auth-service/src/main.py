import os
from fastapi import FastAPI
import grpc
import asyncio
from .rest_handler import router as user_router
from .grpc_handler import UserServiceServicer
from .users_pb2_grpc import add_UserServiceServicer_to_server

app = FastAPI()
app.include_router(user_router)


async def serve_grpc():
    server = grpc.aio.server()
    add_UserServiceServicer_to_server(UserServiceServicer(), server)
    grpc_port = int(os.getenv("GRPC_PORT", 50051))
    server.add_insecure_port(f"[::]:{grpc_port}")
    await server.start()
    await server.wait_for_termination()


@app.on_event("startup")
async def on_startup():
    asyncio.create_task(serve_grpc())
