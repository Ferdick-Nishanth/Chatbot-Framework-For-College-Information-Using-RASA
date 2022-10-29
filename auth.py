from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date


Base = declarative_base()

class Auth(Base):
    __tablename__ = 'auth'
    id = Column(Integer)
    password = Column(String)
    createdDate = Column(Date)
    modifiedDate = Column(Date)
    
    def __repr__(self):
        return "<auth(id='{}', password='{}', createdDate={}, modifiedDate={})>" \
            .format(self.id, self.password, self.createdDate, self.modifiedDate)             