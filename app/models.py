import db
from sqlalchemy import Column,Integer,String
class BaseModel(db.Model):
    __abstract__ = True
    # define here __repr__ and json methods or any common method
    # that you need for all your models

class TestModel(BaseModel):
    __tablename__ = 'test_table'
    # define your model
    id = Column(Integer, primary_key=True)
    name = Column(String(256))