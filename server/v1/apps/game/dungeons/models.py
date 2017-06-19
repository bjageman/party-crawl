from v1.apps import db


door = db.Table(
    'doors', db.Model.metadata,
    db.Column('room_id', db.Integer, db.ForeignKey('room.id'), index=True),
    db.Column('door_id', db.Integer, db.ForeignKey('room.id')),
    db.UniqueConstraint('room_id', 'door_id', name='unique_door'))

class Dungeon(db.Model):
    __tablename__ = 'dungeon'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(32))

class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(32))
    dungeon_id = db.Column(db.Integer, db.ForeignKey('dungeon.id'))
    dungeon = db.relationship('Dungeon', backref=db.backref('rooms', lazy='dynamic'))
    doors = db.relationship('Room',
                           secondary=door,
                           primaryjoin=id==door.c.room_id,
                           secondaryjoin=id==door.c.door_id)
