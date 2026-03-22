from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from notes_rag.api.main import app


@pytest.fixture  # type: ignore[untyped-decorator]
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
