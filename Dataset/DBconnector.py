from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

db = r"sqlite:///C:\Users\carmi\PycharmProjects\DataMiningRepositorySoftware\Dataset\repositorydatabase.db"

Base = declarative_base()
engine = create_engine(db, echo=True)
Session = sessionmaker()
