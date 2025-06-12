from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from django.contrib.auth.models import AbstractUser
from django.db import models

Base = declarative_base()

class Owner(Base):
    __tablename__ = 'gallery_owner'

    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    art_pieces = relationship("ArtPiece", back_populates="owner")

class ArtPiece(Base):
    __tablename__ = 'gallery_artpiece'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    image_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    owner_id = Column(Integer, ForeignKey('gallery_owner.id'))
    owner = relationship("Owner", back_populates="art_pieces")