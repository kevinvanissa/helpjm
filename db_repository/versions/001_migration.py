from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
contact_us = Table('contact_us', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=120), nullable=False),
    Column('email', String(length=120), nullable=False),
    Column('topic', String(length=120)),
    Column('message', String(length=140), nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['contact_us'].columns['topic'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['contact_us'].columns['topic'].drop()
