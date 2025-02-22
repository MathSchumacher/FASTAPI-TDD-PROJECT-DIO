from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
import pymongo
from store.db.mongo import db_client
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundException
from store.models.product import ProductModel

class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection: AsyncIOMotorCollection = self.database.get_collection("products")
    
    async def create(self, body:ProductIn) -> ProductOut:
        product_model=ProductModel(**body.model_dump())
        await self.collection.insert_one(product_model.model_dump())

        return ProductOut(**product_model.model_dump())

    async def get(self, id:UUID) ->ProductOut:
        result= await self.collection.find_one({"id":id})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)
    
    async def query(self) ->List[ProductOut]:
        return [ProductOut(**item) async for item in self.collection.find()]
    
    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        product= ProductUpdate(**body.model_dump(exclude_none=True))

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": body.model_dump(exclude_none=True)},
            #update={"$set": product.model_dump(exclude_none=True)},
            return_document=pymongo.ReturnDocument.AFTER,
        )
        return ProductUpdateOut(**result)
    
    async def delete(self, id: UUID) ->bool:
        product= await self.collection.find_one({"id":id})
        if not product:
            raise NotFoundException(message=f"Product Not Found with filter: {id}")
        result= await self.collection.delete_one({"id":id})

        return True if result.deleted_count > 0 else False

product_usecase = ProductUsecase()