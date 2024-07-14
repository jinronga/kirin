from src.models.db.account import Account
from src.repository.crud.base import BaseCRUDRepository
from src.models.schemas.dataset import DatasetCreate
from sqlalchemy.sql import functions as sqlalchemy_functions
from src.utilities.exceptions.database import EntityDoesNotExist
from src.models.db.dataset import DataSet
import sqlalchemy

import typing
class DataSetCRUDRepository(BaseCRUDRepository):

    async def init_dataset(self, dataset_name:str, account_username: str) -> DataSet:
        stmt = sqlalchemy.select(DataSet).where(DataSet.name == dataset_name)
        result = await self.async_session.execute(statement=stmt)
        dataset  = result.first()
        
        if dataset is None:
            dataset=DataSet(name=dataset_name)
            self.async_session.add(instance=dataset)
            await self.async_session.commit()
            await self.async_session.refresh(instance=dataset)
        
        update_stmt = sqlalchemy.update(table=Account).where(Account.username == account_username).values(updated_at=sqlalchemy_functions.now())
        update_stmt = update_stmt.values(current_dataset_id=dataset.id)
        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        return dataset
        
    async def create_dataset(self, dataset_create: DatasetCreate) -> DataSet:
        new_dataset=DataSet(name=dataset_create.dataset_name)

        self.async_session.add(instance=new_dataset)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_dataset)

        return new_dataset

    async def mark_loaded(self, name: str)->typing.Sequence[DataSet]:
        update_stmt = sqlalchemy.update(table=DataSet).where(DataSet.name == name).values(updated_at=sqlalchemy_functions.now())  # type: ignore
        update_stmt = update_stmt.values(is_uploaded=True)
        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()

    async def get_dataset_by_name(self,dataset_name: str)->typing.Sequence[DataSet]:
        stmt = sqlalchemy.select(DataSet).where(DataSet.name == dataset_name)
        result = await self.async_session.execute(statement=stmt)
        query = result.first()
        return query
    
    async def get_dataset_by_id(self, id: int) -> DataSet:
        stmt = sqlalchemy.select(DataSet).where(DataSet.id == id, DataSet.is_uploaded)
        query = await self.async_session.execute(statement=stmt)
        dataset = query.scalar()
        if dataset is None:
            raise EntityDoesNotExist("Dataset with id `{id}` does not exist!")

        return dataset
    
    async def get_load_status(self, id: int)->bool:
        stmt = sqlalchemy.select(DataSet).where(DataSet.id == id)
        result = await self.async_session.execute(statement=stmt)
        query = result.first()
        dataset = query.scalar()
        if dataset is None:
            return False
        return dataset.is_uploaded



    async def get_dataset_list(self)->typing.Sequence[DataSet]:
         stmt = sqlalchemy.select(DataSet).order_by(DataSet.updated_at.desc())
         query = await self.async_session.execute(statement=stmt) 
         return query.scalars().all()


