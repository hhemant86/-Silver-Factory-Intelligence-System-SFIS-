from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func  # <--- Use this instead of 'import sum'
from typing import List
from . import models, schemas
from .database import engine, get_db
# Initialize Database Tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Silver Factory Intelligence System")

@app.get("/")
def read_root():
    return {
        "status": "Active",
        "objective": "Industrial Intelligence & Capital Control",
        "date": "2026-01-02"
    }

# --- Parameter Endpoints (Settings) ---

@app.post("/parameters/", response_model=schemas.ParameterResponse)
def create_parameter(param: schemas.ParameterCreate, db: Session = Depends(get_db)):
    db_param = models.SystemParameter(**param.model_dump())
    db.add(db_param)
    db.commit()
    db.refresh(db_param)
    return db_param

@app.get("/parameters/", response_model=list[schemas.ParameterResponse])
def get_parameters(db: Session = Depends(get_db)):
    return db.query(models.SystemParameter).all()


# --- Ledger Endpoints (Manufacturing) ---

@app.post("/ledger/", response_model=schemas.LedgerResponse)
def create_ledger_entry(entry: schemas.LedgerCreate, db: Session = Depends(get_db)):
    db_entry = models.SilverLedger(**entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@app.get("/ledger/", response_model=List[schemas.LedgerResponse])
def get_ledger(db: Session = Depends(get_db)):
    return db.query(models.SilverLedger).all()

# --- Quant Analytics Endpoint (Stage 1: Anomaly Detection Prep) ---

@app.get("/analytics/wastage/{batch_id}")
def get_wastage_analysis(batch_id: str, db: Session = Depends(get_db)):
    entry = db.query(models.SilverLedger).filter(models.SilverLedger.batch_id == batch_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    actual_loss = entry.input_weight - entry.output_weight - entry.sample_loss
    wastage_percentage = (actual_loss / entry.input_weight) * 100
    
    return {
        "batch_id": batch_id,
        "actual_loss_gm": round(actual_loss, 4),
        "wastage_percent": round(wastage_percentage, 4),
        "status": "Flagged" if wastage_percentage > 0.5 else "Normal" 
    }
@app.post("/journal/", response_model=schemas.JournalResponse)
def create_journal_entry(entry: schemas.JournalCreate, db: Session = Depends(get_db)):
    db_entry = models.DailyJournal(**entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@app.get("/journal/", response_model=List[schemas.JournalResponse])
def get_journal(db: Session = Depends(get_db)):
    return db.query(models.DailyJournal).all()


@app.get("/analytics/summary")
def get_factory_summary(db: Session = Depends(get_db)):
    # We use func.sum to call the database's internal addition logic
    total_produced = db.query(func.sum(models.SilverLedger.output_weight)).scalar() or 0
    total_sold = db.query(func.sum(models.DailyJournal.silver_weight_sold)).scalar() or 0
    total_cash = db.query(func.sum(models.DailyJournal.cash_amount)).scalar() or 0
    
    net_silver_balance = total_produced - total_sold
    
    return {
        "factory_status": "Operational",
        "net_silver_balance_gm": round(net_silver_balance, 2),
        "total_liquidated_gm": round(total_sold, 2),
        "cash_on_hand_inr": round(total_cash, 2)
    }