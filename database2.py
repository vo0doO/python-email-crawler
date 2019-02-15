import sqlalchemy

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Декларируем базуданных
Base = declarative_base()


class Link0(Base):
    __tablename__ = 'google_search_result'

    search_id = Column(Integer, primary_key=True)
    domain = Column(String(150), nullable=False)
    path = Column(String(250), nullable=True)
    query = Column(String(999), nullable=True)
    baseLinkcount = Column(Integer, nullable=True)
    externalLinkcount = Column(Integer, nullable=True)
    relativeLinkcount = Column(Integer, nullable=True)
    proportion_of_duplicates = Column(Integer, max(0, 100, 99, domain))

class Link(Base):
    __tablename__ = 'parse_level_1'

    id = Column(Integer, primary_key=True)
    url = Column(String(999), unique=True)
    domain = Column(String(150), nullable=False)
    path = Column(String(250), nullable=True)
    query = Column(String(999), nullable=True)
    keyword_tags = Column(String(250))
    emails = Column(String(999))
    baseLinkcount = Column(Integer)
    externalLinkcount = Column(Integer)
    google_search_id = Column(Integer, ForeignKey('Link0.search_id'))
    google_search_result = relationship(Link0)


class Link1(Base):
    __tablename__ = 'parse_level_2'

    id = Column(Integer, primary_key=True)
    domain = Column(String(250))
    path = Column(String(250))
    query = Column(String(999))
    keyword_tags = Column(String(250))
    emails = Column(String(999))
    baseLinkcount = Column(Integer)
    externalLinkcount = Column(Integer)
    one_level_req_id = Column(Integer, ForeignKey('Link.id'))
    parse_level_1 = relationship(Link)



engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
session = DBSession()
    
def get_all_Link():
    all_Link = session.query(Link).all()
    return all_Link


def new_Link_db(new_Linkaurant_name):
    new_Linkaurant = Link(name=new_Linkaurant_name)
    session.add(new_Linkaurant)
    session.commit()
    return


def get_Link_to_edit(Link_id, new_Link_name=None):
    this_Link = session.query(Link).get(Link_id)
    if new_Link_name is not None:
        this_Link.name = new_Link_name
        session.add(this_Link)
        session.commit()
    else:
        return this_Link

def get_Link_to_delete(Link_id, confirm_delete=None):
    this_Link = session.query(Link).get(Link_id)
    if confirm_delete is not None:
        session.delete(this_Link)
        session.commit()
    else:
        return this_Link