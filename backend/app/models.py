from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class SystemParameter(Base):
    __tablename__ = "system_parameters"
    
    id = Column(Integer, primary_key=True, index=True)
    parameter_name = Column(String, unique=True, index=True) # e.g., 'lab_sample_rod_gm'
    value = Column(Float)
    unit = Column(String) # 'grams', 'INR/kg', '%'
    last_updated = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

class SilverLedger(Base):
    __tablename__ = "silver_ledger"
    
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(String, index=True)
    stage = Column(String) # 'Melting', 'Drawing', etc.
    input_weight = Column(Float)
    output_weight = Column(Float)
    sample_loss = Column(Float) # The 1g/4g editable value
    purity = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class DailyJournal(Base):
    __tablename__ = "daily_journal"
    
    id = Column(Integer, primary_key=True, index=True)
    entry_type = Column(String) # 'SILVER_SALE' or 'EXPENSE'
    head = Column(String)       # 'Salary', 'Electricity', 'Stock_Liquidation'
    cash_amount = Column(Float)
    silver_weight_sold = Column(Float, nullable=True) # Only for sales
    spot_price = Column(Float, nullable=True)         # Price/gm at time of sale
    timestamp = Column(DateTime(timezone=True), server_default=func.now())    