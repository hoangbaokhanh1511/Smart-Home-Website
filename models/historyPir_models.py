from datetime import datetime, timedelta
from app import db

class History_Pir(db.Model):
    __bind_key__ = 'pir'
    id = db.Column("id", db.Integer, primary_key=True)
    timestamp = db.Column("Timestamp", db.DateTime,
                        default=None)  

    def __init__(self):
        now = datetime.now()
        self.timestamp = now.replace(microsecond=0) 

    def __repr__(self):
        return f"{self.timestamp}"