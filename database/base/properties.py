import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker


Base = declarative_base()
ENGINE = create_engine(settings.LINK_TO_DATABASE, echo=False)
Session = scoped_session(sessionmaker(bind=ENGINE))
