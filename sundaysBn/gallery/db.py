from sqlalchemy import create_engine
from django.conf import settings

def get_sqlalchemy_engine():
    db_config = settings.DATABASES['default']
    db_url = f"postgresql://{db_config['USER']}:{db_config['PASSWORD']}@{db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}"
    return create_engine(db_url)