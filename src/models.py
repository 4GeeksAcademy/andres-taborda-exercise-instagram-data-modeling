import enum
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique= True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique= True)

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    followers = relationship(
        "User", secondary="follower", 
        primaryjoin="User.id==follower.user_from_id", 
        secondaryjoin="User.id==follower.user_to_id", 
        back_populates="following"
    )
    following = relationship(
        "User", 
        secondary="follower", 
        primaryjoin="User.id==follower.user_to_id", 
        secondaryjoin="User.id==follower.user_from_id", 
        back_populates="followers"
    )

    

class Follower(Base):
    __tablename__ = "fallower"

    user_from_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)
    user_to_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)

class Post(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    author = relationship("User", back_populates="posts")

    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    media = relationship("Media", back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    comment_text = Column(String(500), nullable=False)

    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    author = relationship("User", back_populates="comments")

    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    post = relationship("Post", back_populates="comments")

    

class MediaType(enum.Enum):
    VIDEO = "video"
    IMAGE = "image"
    

class Media(Base):
    __tablename__= "media"

    id = Column(Integer, primary_key=True)
    type = Column(Enum(MediaType), nullable=False)
    ulr= Column(String(300), nullable=False)

    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    post = relationship("Post", back_populates="media")




    





## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
