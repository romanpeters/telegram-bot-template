import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE = "sqlite:///sqlite.db"
SQLAlchemyBase = declarative_base()
engine = sa.create_engine(DATABASE, echo=False)
Session = sessionmaker(bind=engine)


chat_members = sa.Table('chat_members', SQLAlchemyBase.metadata,
                        sa.Column('user_id', sa.ForeignKey('users.user_id'), primary_key=True),
                        sa.Column('chat_id', sa.ForeignKey('chats.chat_id'), primary_key=True))


class Chat(SQLAlchemyBase):
    __tablename__ = 'chats'
    chat_id = sa.Column(sa.Integer, primary_key=True)
    users = relationship('User',
                         secondary=chat_members,
                         back_populates='chats')

    def __repr__(self):
        return f"<Chat(chat_id='{self.chat_id}', users='{self.users}')>"



class User(SQLAlchemyBase):
    __tablename__ = 'users'
    user_id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(32))
    first_name = sa.Column(sa.String(32))
    last_name = sa.Column(sa.String(32))
    rank = sa.Column(sa.Integer)
    chats = relationship('Chat',
                         secondary=chat_members,
                         back_populates='users')

    def __repr__(self):
        return f"<User(user_id='{self.user_id}', username='{self.username}', first_name='{self.first_name}', " \
               f"last_name='{self.last_name}', chats='{self.chats}')>"


def user_to_db(user_id, chat_id, username=None, first_name=None, last_name=None, rank=None):
    session = Session()
    entry = User(user_id=user_id, username=username, first_name=first_name, last_name=last_name)
    if rank:
        entry.rank = rank
    entry.chats.append(Chat(chat_id=chat_id))
    session.merge(entry)
    session.commit()



SQLAlchemyBase.metadata.create_all(engine)