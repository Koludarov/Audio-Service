from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    token = Column(String)

    audio_records = relationship("AudioRecord", back_populates="user")


class AudioRecord(Base):
    __tablename__ = "audio_records"

    id = Column(Integer, primary_key=True)
    file_uuid = Column(String)
    filename = Column(String)
    wav_path = Column(String)
    mp3_path = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="audio_records")
