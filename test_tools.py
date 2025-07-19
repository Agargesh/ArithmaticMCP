import pytest
import json
from fastmcp import Client
from main import server

pytestmark = pytest.mark.asyncio  # marks all tests in this file as asyncio-compatible

async def test_calculate():
    async with Client(server) as client:
        result = await client.call_tool("calculate", {"expression": "2 + 3 * 4"})
        content = json.loads(result.content[0].text)  # ✅ Fix: parse JSON from text content
        assert content == {"result": 14}

async def test_power():
    async with Client(server) as client:
        result = await client.call_tool("power", {"base": 2, "exponent": 5})
        content = json.loads(result.content[0].text)
        assert content == {"result": 32}

async def test_square_root():
    async with Client(server) as client:
        result = await client.call_tool("square_root", {"value": 16})
        content = json.loads(result.content[0].text)
        assert content == {"result": 4.0}