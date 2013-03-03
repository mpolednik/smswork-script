from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config.database import dbconf

dbconfstr = 'mysql+mysqldb://%s:%s@%s/%s'% (dbconf['user'], dbconf['pass'], 
                                            dbconf['host'], dbconf['name'])

engine = create_engine(dbstr)
Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
