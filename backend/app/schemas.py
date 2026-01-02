from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# --- Parameter Schemas (For Dynamic Settings) ---
class ParameterBase(BaseModel):
    parameter_name: str
    value: float
    unit: str

class ParameterCreate(ParameterBase):
    pass

class ParameterResponse(ParameterBase):
    id: int
    last_updated: datetime
    
    model_config = ConfigDict(from_attributes=True)


# --- Ledger Schemas (For Metal Movement) ---
class LedgerBase(BaseModel):
    batch_id: str
    stage: str # e.g., Melting, Drawing, Soldering
    input_weight: float
    output_weight: float
    sample_loss: float # The 1g or 4g variable
    purity: float

class LedgerCreate(LedgerBase):
    pass

class LedgerResponse(LedgerBase):
    id: int
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

class JournalBase(BaseModel):
    entry_type: str
    head: str
    cash_amount: float
    silver_weight_sold: Optional[float] = None
    spot_price: Optional[float] = None

class JournalCreate(JournalBase):
    pass

class JournalResponse(JournalBase):
    id: int
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)    