from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey

metadata = MetaData()
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(50)),
              Column('fullname', String(50)),
              Column('password', String(12))
              )

meetings = Table('meetings', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('creator_id', None, ForeignKey('users.id')),
                 Column('title', String(50), nullable=False),
                 Column('time', String(23)),  # YYYY-MM-DD HH:MM:SS.SSS
                 Column('participants', Integer),
                 Column('map_id', None, ForeignKey('maps.id'))
                 )

maps = Table('maps', metadata,
             Column('id', Integer, primary_key=True)
             )
