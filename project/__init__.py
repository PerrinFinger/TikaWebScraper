from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#main_telescopes
#testing_telescopes

#testing_weather_stations


#testing_covers



file_name = "sqlite:///C:/Users/GGPC/sqlalchemytesting/TestingData/DBs/testing_weather_stations.db"
engine = create_engine(file_name, echo=False)
Session = sessionmaker(bind=engine)
