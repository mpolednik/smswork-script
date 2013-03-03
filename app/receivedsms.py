from sqlalchemy import Table, Column, Integer, String, Date
import app.db as db

class ReceivedSMS(db.Base):
    __tablename__ = 'sms_recv'

    id = Column(Integer, primary_key=True)
    phone = Column(String(16))
    text = Column(String(1600))
    ts = Column(Date)

    def __init__(self, phone, text, ts):
        self.phone = phone
        self.text = text
        self.ts = ts 

    def __repr__(self):
        return '<User(%d, %s, %s, %s)>' % (self.id, self.phone,
                                               self.text, self.ts)
