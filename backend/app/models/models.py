import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(Text)
    phone = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    transactions = relationship("Transaction", back_populates="user")
    groups_created = relationship("Group", back_populates="creator")


class Group(Base):
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    description = Column(Text)
    goal_amount = Column(Numeric(12, 2))
    created_by = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    creator = relationship("Profile", back_populates="groups_created")
    members = relationship("GroupMember", back_populates="group")
    transactions = relationship("Transaction", back_populates="group")


class GroupMember(Base):
    __tablename__ = "group_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"))
    role = Column(Text, CheckConstraint("role IN ('admin', 'member')"))
    joined_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    group = relationship("Group", back_populates="members")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"), nullable=True)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(Text, default="ZAR")
    description = Column(Text, nullable=False)
    date = Column(Date, nullable=False)
    category = Column(Text)
    merchant = Column(Text)
    is_recurring = Column(Boolean, default=False)
    ai_categorized = Column(Boolean, default=False)
    ai_confidence = Column(Numeric(3, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("Profile", back_populates="transactions")
    group = relationship("Group", back_populates="transactions")


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    icon = Column(Text)
    color = Column(Text)
    is_system = Column(Boolean, default=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class BankStatement(Base):
    __tablename__ = "bank_statements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    filename = Column(Text, nullable=False)
    file_path = Column(Text, nullable=False)
    statement_date = Column(Date)
    bank_name = Column(Text)
    processed = Column(Boolean, default=False)
    transaction_count = Column(Numeric, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
