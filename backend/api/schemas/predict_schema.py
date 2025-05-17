from pydantic import BaseModel

class PredictionInput(BaseModel):
    date: str
    location: str
    crop_type: str
    soil_type: str
    season: str
    area: float
    initial_moisture: float
    max_moisture: float
