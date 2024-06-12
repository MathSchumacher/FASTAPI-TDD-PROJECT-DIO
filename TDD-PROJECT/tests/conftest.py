import asyncio
import uuid
from uuid import UUID
import pytest
from store.db.mongo import db_client
from store.schemas.product import ProductIn, ProductUpdate
from tests.factories import product_data, products_data
from tests.usecases.product import product_usecase
from httpx import AsyncClient
from typing import AsyncGenerator

@pytest.fixture(scope="session")
def event_loop():
    loop= asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
@pytest.fixture
def mongo_client():
    return db_client.get()

@pytest.fixture(autouse=True)
async def clear_collections(mongo_client):
    yield
    collections_names= await mongo_client.get_database().list_collection_names()
    for collection_name in collections_names:
        if collection_name.starswich("system"):
            continue

        #await mongo_client.get_database()[collection_name].delete_many({})


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    from store.main import app

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def product_url() -> str:
    return "/products/"

new_uuid = uuid.uuid4()
print(new_uuid)

@pytest.fixture
def product_id() -> UUID:
    return UUID(new_uuid)

@pytest.fixture
def product_in(product_id):
    ProductIn(**product_data(), id=product_id)

@pytest.fixture
def product_up(product_id):
    return ProductUpdate(**product_data(), id=product_id)

@pytest.fixture
async def product_inserted():
    return await product_usecase.create(body=product_in)

@pytest.fixture
def products_in():
    return [ProductIn(**product) for product in products_data()]

@pytest.fixture
async def products_inserted(products_in):
    return [await product_usecase.create(body=product_in) for product_in in products_in]