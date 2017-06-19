from v1.apps import db

from ..dungeons.models import Room


class Entity(db.Model):
    __tablename__ = 'entity'
    id = db.Column(db.Integer, primary_key= True)
    active = db.Column(db.Boolean, default=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', backref=db.backref('entities', lazy='dynamic'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character = db.relationship('Character', backref=db.backref('entities', lazy='dynamic'))
    trap_id = db.Column(db.Integer, db.ForeignKey('trap.id'))
    trap = db.relationship('Trap', backref=db.backref('entities', lazy='dynamic'))

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(32))
    theme = db.Column(db.String(32))
    hostile = db.Column(db.Boolean,default=False)
    current_health = db.Column(db.Integer, null = True)
    statistics = db.relationship("Statistics", uselist=False, backref="character_statistics")

class Trap(db.Model):
    __tablename__ = 'trap'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(32))
    statistics = db.relationship("Statistics", uselist=False, backref="trap_statistics")

class Statistics(db.Model):
    __tablename__ = 'statistics'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(32))
    level = db.Column(db.Integer, default=1)
    max_health = db.Column(db.Integer, default=1)
    damage_min = db.Column(db.Integer, default=1)
    damage_max = db.Column(db.Integer, default=4)
    armor_class = db.Column(db.Integer, default=10)
    strength = db.Column(db.Integer, default=8)
    dexterity = db.Column(db.Integer, default=8)
    consitution = db.Column(db.Integer, default=8)
    intelligence = db.Column(db.Integer, default=8)
    wisdom = db.Column(db.Integer, default=8)
    charisma = db.Column(db.Integer, default=8)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    trap_id = db.Column(db.Integer, db.ForeignKey('trap.id'))
    #player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
