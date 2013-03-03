from sqlalchemy import Table, Column, Integer, String, Date
import app.db as db

class SentSMS(db.Base):
    __tablename__ = 'sms_send'

    id = Column(Integer, primary_key=True)
    phone = Column(String(16))
    text = Column(String(1600))
    ts = Column(Date)
    owner = Column(String(200))
    state = Column(Integer, default=0)

    def __init__(self, phone, text):
        self.phone = phone
        self.text = text

    def __repr__(self):
        return '<User(%d, %s, %s, %s, %s, %d)>' % (self.id, self.phone,
                                               self.text, self.ts, self.owner,
                                               self.state)

    @staticmethod
    def get_unprocessed():
        return db.session.query(SentSMS).filter(SentSMS.state==0).all()

    @staticmethod
    def update_state(id, state):
        sms = db.session.query(SentSMS).filter(SentSMS.id==id).first()
        sms.state = state
