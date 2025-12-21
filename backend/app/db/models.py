from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Agency(Base):
    __tablename__ = "agencies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    location = Column(String(100))
    contact_info = Column(String(100))
    
    users = relationship("User", back_populates="agency")
    datasets = relationship("Dataset", back_populates="agency")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False) # 'admin', 'agency', 'public' (public might not need user)
    
    agency_id = Column(Integer, ForeignKey("agencies.id"), nullable=True)
    agency = relationship("Agency", back_populates="users")
    activity_logs = relationship("ActivityLog", back_populates="user")

class Dataset(Base):
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    agency_id = Column(Integer, ForeignKey("agencies.id"), nullable=False)
    agency = relationship("Agency", back_populates="datasets")
    
    training_logs = relationship("TrainingLog", back_populates="dataset")

class TrainingLog(Base):
    __tablename__ = "training_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    status = Column(String(50), default="Pending") # Pending, Success, Failed
    accuracy = Column(Float, nullable=True)
    feature_importance = Column(Text, nullable=True) # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    
    dataset = relationship("Dataset", back_populates="training_logs")


class ActivityLog(Base):
    """Tracks user activities: logins, uploads, training triggers, etc."""
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(50), nullable=False)  # 'login', 'logout', 'upload', 'train', 'delete'
    details = Column(Text, nullable=True)  # JSON with additional context
    status = Column(String(20), default="success")  # 'success', 'failed'
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="activity_logs")

