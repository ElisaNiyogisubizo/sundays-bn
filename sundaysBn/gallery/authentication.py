from sqlalchemy.orm import sessionmaker
from .db import get_sqlalchemy_engine
from .models import Owner

def authenticate_owner(username, password):
    engine = get_sqlalchemy_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    owner = session.query(Owner).filter_by(username=username, password=password).first()
    session.close()
    return owner