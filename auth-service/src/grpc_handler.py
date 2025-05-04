import grpc
from grpc import StatusCode
import os
from .users_pb2 import BoolResponse, UserFull
from .users_pb2_grpc import UserServiceServicer, add_UserServiceServicer_to_server
from .database import AsyncSessionLocal
from .user_service import get_user, ban_user, is_banned

class UserServiceServicerImpl(UserServiceServicer):
    async def GetUser(self, request, context):
        async with AsyncSessionLocal() as db:
            user = await get_user(db, request.user_id)
        if not user:
            context.set_code(StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return UserFull()
        return UserFull(**user)

    async def BanUser(self, request, context):
        async with AsyncSessionLocal() as db:
            ok = await ban_user(db, request.user_id)
        return BoolResponse(ok=ok)

    async def IsBanned(self, request, context):
        async with AsyncSessionLocal() as db:
            ok = await is_banned(db, request.user_id)
        return BoolResponse(ok=ok)

def serve_grpc():
    import asyncio, jwt
    from .main import app  # assume app import for orchestrator
    server = grpc.aio.server()
    add_UserServiceServicer_to_server(UserServiceServicerImpl(), server)
    grpc_port = int(os.getenv('GRPC_PORT', 50051))
    server.add_insecure_port(f"[::]:{grpc_port}")
    loop = asyncio.get_event_loop()
    loop.create_task(server.start())