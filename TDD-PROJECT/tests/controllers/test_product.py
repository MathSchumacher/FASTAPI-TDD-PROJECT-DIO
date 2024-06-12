import pytest
from typing import List
from tests.factories import product_data
from fastapi import status

async def test_controller_create_should_return_sucess(client, products_url):
    response = await client.post(products_url, json=product_data())

    content = response.json()
    del content['created_at']
    del content['updated_at']
    del content['id']
    assert response.status_code == status.HTTP_201_CREATED
    assert content == {'name': 'Iphone 14 pro Max', 'quantity': 10, 'price': '8.500', 'status': True}

async def test_controller_get_should_return_sucess(client, products_url, product_inserted):
    response = await client.get(f"{products_url}{product_inserted.id}")

    content = response.json()
    del content['created_at']
    del content['updated_at']

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {'id': str(product_inserted.id), 'name': 'Iphone 14 pro Max', 'quantity': 10, 'price': '8.500', 'status': True}

async def test_controller_get_should_return_not_found(client, products_url):
    response = await client.get(f"{products_url}bfaa1908-7056-4626-b477-fbe75093f1e8")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Product not found with filter: bfaa1908-7056-4626-b477-fbe75093f1e8'}

@pytest.mark.usefixtures("products_inserted")
async def test_controller_query_should_return_sucess(client, products_url):
    response = await client.get(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1

async def test_controller_patch_should_return_sucess(client, products_url, product_inserted):
    response = await client.patch(f"{products_url}{product_inserted.id}", json={"price": "7.500"})
    
    content = response.json()
    del content['created_at']
    del content['updated_at']

    assert response.status_code == status.HTTP_200_OK

async def test_controller_delete_should_return_no_content(client, products_url, product_inserted):
    response = await client.delete(f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

async def test_controller_delete_should_return_not_found(client, products_url):
    response = await client.delete(f"{products_url}bfaa1908-7056-4626-b477-fbe75093f1e8")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Product not found with filter: bfaa1908-7056-4626-b477-fbe75093f1e8'}