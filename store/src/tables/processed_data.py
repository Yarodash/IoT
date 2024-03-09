from sqlalchemy import create_engine, MetaData, Column, Integer, String, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import PG_USER, PG_PASS, PG_HOST, PG_PORT, PG_DB

# SQLAlchemy setup
DATABASE_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"
engine = create_engine(DATABASE_URL, echo=True)
metadata = MetaData()

Base = declarative_base()


class ProcessedAgentDataSQL(Base):
    __tablename__ = 'processed_agent_data'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    road_state = Column(String)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime, default=func.now())


metadata.create_all(engine)

Session = sessionmaker(bind=engine)
