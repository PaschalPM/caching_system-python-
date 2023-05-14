from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
from dotenv import load_dotenv

load_dotenv()
mysql_conn = {
    'host': getenv('MYSQL_HOST'),
    'port': getenv('MYSQL_PORT'),
    'user': getenv('MYSQL_USER'),
    'password': getenv('MYSQL_PASSWORD'),
    'db': getenv('MYSQL_DB')
}
db_url = "{user}:{password}@{host}:{port}/{db}".format(**mysql_conn)
engine = create_engine('mysql+pymysql://{}'.format(db_url), echo=True, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
db_session = Session()

class DBStorage:
    def all(self, cls):
        with db_session as conn:
            records = conn.query(cls).all()
            
        return records
    
    def get(self, cls, id):    
        with db_session as conn:
            record = conn.query(cls).get(id)
            
            print(record)
        return record