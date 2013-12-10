from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
review = Table('review', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('rec_id', Integer),
    Column('content', String),
    Column('created', DateTime),
    Column('rating', String),
)

review = Table('review', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('rec_id', Integer),
    Column('review', String(length=140)),
    Column('rating', String(length=120)),
    Column('created', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['review'].columns['content'].drop()
    post_meta.tables['review'].columns['review'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['review'].columns['content'].create()
    post_meta.tables['review'].columns['review'].drop()
