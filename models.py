class Log(DB.Model):
    __tablename__ = 'ad-auris-narrations-audiowidget-logs'
    id = DB.Column(DB.Integer, primary_key=True) # auto incrementing
    logger = DB.Column(DB.String(100)) # the name of the logger. (e.g. myapp.views)
    level = DB.Column(DB.String(100)) # info, debug, or error?
    trace = DB.Column(DB.String(4096)) # the full traceback printout
    msg = DB.Column(DB.String(4096)) # any custom log you may have included
    created_at = DB.Column(DB.DateTime, default=DB.func.now()) # the current timestamp

    def __init__(self, logger=None, level=None, trace=None, msg=None):
        self.logger = logger
        self.level = level
        self.trace = trace
        self.msg = msg

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Log: %s - %s>" % (self.created_at.strftime('%m/%d/%Y-%H:%M:%S'), self.msg[:50])