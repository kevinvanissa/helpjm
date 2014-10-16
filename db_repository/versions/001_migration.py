from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
event = Table('event', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String, nullable=False),
    Column('category', String),
    Column('description', String, nullable=False),
    Column('event_start_date', DateTime, nullable=False),
    Column('event_end_date', DateTime, nullable=False),
    Column('venue', String, nullable=False),
    Column('address', String, nullable=False),
    Column('parish', String, nullable=False),
    Column('longitude', Float),
    Column('latitude', Float),
    Column('flyer', String, nullable=False),
    Column('thumbnail', String, nullable=False),
    Column('youtube', String),
    Column('number_attending', Integer),
    Column('created_date', DateTime),
    Column('creator', Integer),
    Column('comment_counting', Integer),
    Column('featured', SmallInteger),
    Column('active', SmallInteger),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['event'].columns['latitude'].drop()
    pre_meta.tables['event'].columns['longitude'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['event'].columns['latitude'].create()
    pre_meta.tables['event'].columns['longitude'].create()
