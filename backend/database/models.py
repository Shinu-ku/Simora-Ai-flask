import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.database.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    business = relationship("Business", back_populates="owner", uselist=False)


class Business(Base):
    __tablename__ = "businesses"

    id = Column(String, primary_key=True, default=generate_uuid)
    owner_id = Column(String, ForeignKey("users.id"), unique=True)
    name = Column(String, nullable=False)
    business_type = Column(String)
    industry = Column(String)
    location = Column(String)
    currency = Column(String, default="USD")
    timezone = Column(String, default="UTC")
    business_start_date = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="business")
    products = relationship("Product", back_populates="business")
    # Will add other relationships as needed


class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=generate_uuid)
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    name = Column(String, nullable=False)
    sku = Column(String, nullable=False)
    category = Column(String)
    price = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    reorder_threshold = Column(Integer, default=0)
    status = Column(String, default="active") # active, inactive

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    business = relationship("Business", back_populates="products")
    sales_records = relationship("SalesRecord", back_populates="product")
    inventory_records = relationship("InventoryRecord", back_populates="product")

class SalesRecord(Base):
    __tablename__ = "sales_records"

    id = Column(String, primary_key=True, default=generate_uuid)
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    unit_cost = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    revenue = Column(Float, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    business = relationship("Business")
    product = relationship("Product", back_populates="sales_records")

class InventoryRecord(Base):
    __tablename__ = "inventory_records"

    id = Column(String, primary_key=True, default=generate_uuid)
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    stock_level = Column(Integer, nullable=False)
    restock_amount = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="inventory_records")

class DigitalTwinSnapshot(Base):
    __tablename__ = "digital_twin_snapshots"

    id = Column(String, primary_key=True, default=generate_uuid)
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    model_version = Column(String, nullable=False)
    data_range_start = Column(DateTime, nullable=False)
    data_range_end = Column(DateTime, nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    # JSON field containing all calculated features (elasticity, seasonality, etc)
    features = Column(JSON, nullable=False)
    confidence = Column(Float, nullable=False)
    data_quality = Column(String, nullable=False) # High, Medium, Low, Insufficient

    business = relationship("Business")

class Decision(Base):
    __tablename__ = "decisions"

    id = Column(String, primary_key=True, default=generate_uuid)
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    
    # Strategy details
    action_type = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    duration_days = Column(Integer, nullable=False)
    
    # Workflow status
    status = Column(String, default="PENDING") # PENDING, APPROVED, REJECTED, EXECUTED, FAILED
    
    # Predictions
    predicted_units = Column(Integer, nullable=False)
    predicted_revenue = Column(Float, nullable=False)
    predicted_profit = Column(Float, nullable=False)
    
    # Actuals (Populated later in Phase 11)
    actual_units = Column(Integer, nullable=True)
    actual_revenue = Column(Float, nullable=True)
    actual_profit = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    business = relationship("Business")
    product = relationship("Product")

class Memory(Base):
    """Stores business insights, observations, and past outcomes."""
    __tablename__ = "memories"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    
    memory_type = Column(String, nullable=False) # e.g. "OBSERVATION", "CALIBRATION", "PREFERENCE"
    content = Column(String, nullable=False)
    
    # Store dynamic metadata (e.g., error rates, calibration factors)
    metadata_json = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class Calibration(Base):
    """Stores learned calibration factors for the simulation engine."""
    __tablename__ = "calibrations"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    
    action_type = Column(String, nullable=False) # e.g., "discount"
    
    sample_count = Column(Integer, default=0)
    average_error = Column(Float, default=0.0)
    calibration_factor = Column(Float, default=1.0) # Multiply predicted outcome by this
    
    version = Column(Integer, default=1)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

