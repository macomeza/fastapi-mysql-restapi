from sqlalchemy import create_engine, MetaData

DATABASE_URL = "mysql+pymysql://usrMCU:M?eaSfd;Q9<*@mcu.calhasdfv17y.us-east-1.rds.amazonaws.com:3306/dbFastAPIDev"
engine = create_engine(DATABASE_URL)

meta = MetaData()

conn = engine.connect()

# Create tables (make sure your models are defined before this line)
meta.create_all(engine)