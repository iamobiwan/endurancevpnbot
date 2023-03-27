from sqlalchemy.orm import relationship
import sqlalchemy as sql
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()

engine = create_engine(f'postgresql://endurance:qwerty@127.0.0.1:5432/endurance_db', echo=True)

session_maker = sessionmaker(bind=engine)



Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
