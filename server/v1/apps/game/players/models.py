from v1.apps import db

from ..statistics.models import Statistics

class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('players', lazy='dynamic'))
    #statistics = db.relationship("Statistics", uselist=False, backref="player_statistics")
