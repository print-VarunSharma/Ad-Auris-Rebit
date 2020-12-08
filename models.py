from app import db
from sqlalchemy.dialects.postgresql import JSON
from manage import db 

class Log(db.Model):
    __tablename__ = 'ad-auris-narrations-audiowidget-logs'
    id = db.Column(db.Integer, primary_key=True) # auto incrementing
    logger = db.Column(db.String(100)) # the name of the logger. (e.g. myapp.views)
    level = db.Column(db.String(100)) # info, debug, or error?
    trace = db.Column(db.String(4096)) # the full traceback printout
    msg = db.Column(db.String(4096)) # any custom log you may have included
    created_at = db.Column(db.DateTime, default=db.func.now()) # the current timestamp

    def __init__(self, logger=None, level=None, trace=None, msg=None):
        self.logger = logger
        self.level = level
        self.trace = trace
        self.msg = msg

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Log: %s - %s>" % (self.created_at.strftime('%m/%d/%Y-%H:%M:%S'), self.msg[:50])

if __name__ == '__main__':
    db.create_all()