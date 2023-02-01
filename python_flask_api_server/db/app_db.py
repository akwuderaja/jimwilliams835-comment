from sqlite3 import Timestamp
from sqlalchemy import Column, ForeignKey, Integer, String, LargeBinary, \
    DateTime, Boolean, TIMESTAMP, Float, INT, Date, BIGINT, func, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
#engine = create_engine("mysql+pymysql://root@localhost:8080/smartstoreng_db")
#For local Host
# engine = create_engine("mysql+pymysql://root@localhost/smartstoreng_db", echo=True, future=True)
engine = create_engine("mysql+pymysql://irbegvav_investuser:InvestTemp@localhost/irbegvav_comments")


class comment(Base):
    __tablename__ = "comments"
    id = Column(String(6), primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    comment = Column(String(1500), nullable=False)
    article_id = Column(String(100), nullable=False)
    time_posted = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(INT())
    

    def __repr__(self):
        return f"property(id={self.id!r}, name={self.name!r}, \
            address={self.address!r}, comment={self.comment!r}, \
            article_id={self.article_id!r}, \
            time_posted={self.time_posted!r}, \
            time_updated={self.time_updated!r}, \
            status={self.status!r}\
        )"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "comment": self.comment,
            "article_id": self.article_id,
            "time_posted": self.time_posted,
            "time_updated": self.time_updated,
            "status": self.status,
        }


Base.metadata.create_all(engine)
conn = engine.connect()
