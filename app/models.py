from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import  relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    accounts = relationship("Account", back_populates="user")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    website = Column(String, nullable=False)
    account_name = Column(String, nullable=False)
    account_username = Column(String, nullable=False)
    account_password = Column(String, nullable=False)
    encryption_key = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="accounts")

    def __repr__(self):
        return f"<Account(website='{self.website}', account_name='{self.account_name}', account_username='{self.account_username}')>"
