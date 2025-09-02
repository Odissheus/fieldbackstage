from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from .db import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class Tenant(Base):
    __tablename__ = "tenant"
    id = Column(String, primary_key=True, default=uuid_str)
    name = Column(String, nullable=False, unique=True)
    company_code = Column(String, nullable=True, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = "user"
    id = Column(String, primary_key=True)  # expected to match auth provider subject (sub)
    email = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    external_id = Column(String, nullable=True)  # optional mapping if needed
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LoginAccount(Base):
    __tablename__ = "login_account"
    id = Column(String, primary_key=True, default=uuid_str)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    # scope
    tenant_id = Column(String, nullable=True)  # null = landlord account
    user_id = Column(String, nullable=True)
    role = Column(String, nullable=False)  # super_admin, admin, editor, viewer
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserTenantRole(Base):
    __tablename__ = "user_tenant_role"
    id = Column(String, primary_key=True, default=uuid_str)
    user_id = Column(String, nullable=False)
    tenant_id = Column(String, nullable=False)
    # global roles example: super_admin (tenant-agnostic)
    # tenant roles example: admin, editor, viewer
    role = Column(String, nullable=False)
    # optional restriction of product lines the user can access inside this tenant
    product_line_ids = Column(JSON, nullable=True)  # list of strings
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InsightRaw(Base):
    __tablename__ = "insight_raw"
    id = Column(String, primary_key=True, default=uuid_str)
    tenant_id = Column(String, nullable=True)
    product_line_id = Column(String, nullable=False)
    territory_id = Column(String, nullable=True)
    type = Column(String, nullable=False)  # INSIGHT or CI
    text = Column(Text, nullable=True)
    audio_url = Column(Text, nullable=True)
    photo_url = Column(Text, nullable=True)
    ocr_text = Column(Text, nullable=True)
    extracted = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ProductLine(Base):
    __tablename__ = "product_line"
    id = Column(String, primary_key=True, default=uuid_str)
    tenant_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    active = Column(String, nullable=False, default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WeeklyReport(Base):
    __tablename__ = "weekly_report"
    id = Column(String, primary_key=True, default=uuid_str)
    tenant_id = Column(String, nullable=True)
    product_line_id = Column(String, nullable=False)
    week_id = Column(String, nullable=False)
    executive_summary = Column(Text, nullable=False)
    ci_summary = Column(Text, nullable=True)
    heatmap = Column(JSON, nullable=False)
    contributors = Column(JSON, nullable=False)  # list of names
    url_pdf = Column(Text, nullable=True)
    url_html = Column(Text, nullable=True)
    hash = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


