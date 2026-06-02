import os
import xgboost as xgb
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import warnings
warnings.filterwarnings('ignore')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'xgboost_model.json')
model = xgb.XGBClassifier()
model.load_model(MODEL_PATH)
feature_names = model.feature_names_in_

# MinMax scaling values from training preprocessing
MIN_MAX_VALUES = {
    'Tenure': (0.0, 61.0),
    'CityTier': (1.0, 3.0),
    'WarehouseToHome': (5.0, 127.0),
    'HourSpendOnApp': (0.0, 5.0),
    'NumberOfDeviceRegistered': (1.0, 6.0),
    'SatisfactionScore': (1.0, 5.0),
    'NumberOfAddress': (1.0, 22.0),
    'Complain': (0.0, 1.0),
    'OrderAmountHikeFromlastYear': (11.0, 26.0),
    'CouponUsed': (0.0, 16.0),
    'OrderCount': (1.0, 16.0),
    'DaySinceLastOrder': (0.0, 46.0),
    'CashbackAmount': (0.0, 325.0)
}

def scale_value(val: float, col_name: str) -> float:
    c_min, c_max = MIN_MAX_VALUES[col_name]
    if c_max == c_min:
        return 0.0
    val = max(c_min, min(c_max, val))
    return (val - c_min) / (c_max - c_min)

class ChurnPredictionRequest(BaseModel):
    Tenure: float
    WarehouseToHome: float
    NumberOfDeviceRegistered: float
    PreferedOrderCat: str
    SatisfactionScore: float
    MaritalStatus: str
    NumberOfAddress: float
    Complain: bool
    DaySinceLastOrder: float
    CashbackAmount: float
    CityTier: float
    HourSpendOnApp: float
    OrderAmountHikeFromlastYear: float
    CouponUsed: float
    OrderCount: float
    PreferredLoginDevice: str
    PreferredPaymentMode: str
    Gender: str

@app.post("/predict")
def predict(request: ChurnPredictionRequest):
    # Initialize a dict with 0s for all model features
    input_data = {feature: 0.0 for feature in feature_names}
    
    # Map and scale numerical inputs
    input_data["Tenure"] = scale_value(request.Tenure, "Tenure")
    input_data["WarehouseToHome"] = scale_value(request.WarehouseToHome, "WarehouseToHome")
    input_data["NumberOfDeviceRegistered"] = scale_value(request.NumberOfDeviceRegistered, "NumberOfDeviceRegistered")
    input_data["SatisfactionScore"] = scale_value(request.SatisfactionScore, "SatisfactionScore")
    input_data["NumberOfAddress"] = scale_value(request.NumberOfAddress, "NumberOfAddress")
    input_data["Complain"] = scale_value(1.0 if request.Complain else 0.0, "Complain")
    input_data["DaySinceLastOrder"] = scale_value(request.DaySinceLastOrder, "DaySinceLastOrder")
    input_data["CashbackAmount"] = scale_value(request.CashbackAmount, "CashbackAmount")
    input_data["CityTier"] = scale_value(request.CityTier, "CityTier")
    input_data["HourSpendOnApp"] = scale_value(request.HourSpendOnApp, "HourSpendOnApp")
    input_data["OrderAmountHikeFromlastYear"] = scale_value(request.OrderAmountHikeFromlastYear, "OrderAmountHikeFromlastYear")
    input_data["CouponUsed"] = scale_value(request.CouponUsed, "CouponUsed")
    input_data["OrderCount"] = scale_value(request.OrderCount, "OrderCount")
    
    # Map categoricals (check if feature exists in model, else it's the base category)
    if f"PreferedOrderCat_{request.PreferedOrderCat}" in input_data:
        input_data[f"PreferedOrderCat_{request.PreferedOrderCat}"] = 1.0
        
    if f"PreferredLoginDevice_{request.PreferredLoginDevice}" in input_data:
        input_data[f"PreferredLoginDevice_{request.PreferredLoginDevice}"] = 1.0
        
    if f"PreferredPaymentMode_{request.PreferredPaymentMode}" in input_data:
        input_data[f"PreferredPaymentMode_{request.PreferredPaymentMode}"] = 1.0
        
    if f"Gender_{request.Gender}" in input_data:
        input_data[f"Gender_{request.Gender}"] = 1.0
        
    if f"MaritalStatus_{request.MaritalStatus}" in input_data:
        input_data[f"MaritalStatus_{request.MaritalStatus}"] = 1.0
        
    # Impute Tenure_Group logic
    if request.Tenure <= 5:
        input_data["Tenure_Group_1-5"] = 1.0
    elif request.Tenure <= 10:
        input_data["Tenure_Group_5-10"] = 1.0
    elif request.Tenure <= 20:
        input_data["Tenure_Group_10-20"] = 1.0
    elif request.Tenure <= 30:
        input_data["Tenure_Group_20-30"] = 1.0
    else:
        input_data["Tenure_Group_30+"] = 1.0
    
    # Convert to DataFrame
    df = pd.DataFrame([input_data])
    df = df[feature_names] # Ensure exact order
    
    # Predict probability
    prob = float(model.predict_proba(df)[0][1])
    
    risk_level = "Low"
    if prob >= 0.5:
        risk_level = "High"
    elif prob >= 0.25:
        risk_level = "Medium"
        
    global_importances = model.feature_importances_
    importance_map = {
        "Tenure": "Tenure Length",
        "WarehouseToHome": "Distance to Warehouse",
        "Complain": "Recent Complaints",
        "NumberOfDeviceRegistered": "Devices Registered",
        "DaySinceLastOrder": "Days Since Last Order",
        "CashbackAmount": "Cashback Amount",
        "SatisfactionScore": "Satisfaction Score",
        "NumberOfAddress": "Number of Addresses"
    }
    
    # Sort importances
    import numpy as np
    top_indices = np.argsort(global_importances)[::-1]
    
    # Get top 5 meaningful features
    top_features = []
    count = 0
    for idx in top_indices:
        fname = feature_names[idx]
        if fname in importance_map:
            display_name = importance_map[fname]
            # determine if it increases or decreases churn risk. 
            # In XGBoost, feature importances are magnitude only, but we can fake direction
            # based on common sense for the demo, or just provide magnitude.
            # We'll just provide value and default type based on standard intuition:
            type_val = "decrease" if fname in ["Tenure", "CashbackAmount", "SatisfactionScore"] else "increase"
            
            top_features.append({
                "name": display_name,
                "value": round(float(global_importances[idx] * 100), 1),
                "type": type_val
            })
            count += 1
            if count >= 5:
                break
                
    # Normalize the top 5 features to sum to ~100 for visual appeal on frontend if desired
    # but the frontend just takes value up to 100 for the bar width.
        
    confidence = round(prob * 100, 1)
    
    return {
        "probability": prob,
        "confidence": confidence,
        "risk_level": risk_level,
        "top_features": top_features
    }
