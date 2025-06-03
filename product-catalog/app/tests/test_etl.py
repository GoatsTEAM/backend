import pytest
import asyncio
from app.services.etl import etl_sync, sync_to_search_engine

@pytest.mark.asyncio
async def test_etl_sync():
    await etl_sync()

@pytest.mark.asyncio
async def test_sync_to_search_engine():
    await sync_to_search_engine(-1)
