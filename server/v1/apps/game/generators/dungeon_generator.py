import random
from time import sleep

from v1.apps import db
from ..dungeons.models import Room, Dungeon
from ..entities.models import Entity, Character, Trap, Statistics


class Cell:
    x = 0
    y = 0
    visited = False
    room = None
    def __init__(self,x, y, dungeon):
        self.x = x
        self.y = y
        self.room = self.createRoom(dungeon)

    def __unicode__(self):
        return (self.x, self.y)

    def __str__(self):
        return "%s,%s" % (self.x, self.y)

    def createRoom(self, dungeon):
        room = Room(dungeon=dungeon)
        self.populateRoom(room)
        db.session.add(room)
        db.session.commit()
        return room

    def populateRoom(self, room, level=1, theme=None):
        characters = Character.query.join(Statistics).filter(Statistics.level==1).all()
        character = characters[random.randint(0,len(characters) - 1)]
        db.session.commit()
        for i in range(random.randint(0,3)):
            entity = Entity(character=character, room=room)
            db.session.add(entity)
        db.session.commit()

class DungeonGenerator():
    grid = []
    size = 0
    NORTH = [0,1]
    EAST = [1,0]
    SOUTH = [0,-1]
    WEST = [-1,0]
    dungeon = None

    def __init__(self, size=4):
        self.size = size
        self.createDungeon(self.size)

    def createDungeon(self, size=4):
        self.grid = []
        self.dungeon = Dungeon()
        db.session.add(self.dungeon)
        db.session.commit()
        for i in range(size):
            for j in range(size):
                cell = Cell(i, j, self.dungeon)
                self.grid.append(cell)

    def getDungeon(self):
        return self.dungeon

    def getCell(self, x, y):
        for cell in self.grid:
            if cell.x == x and cell.y == y:
                return cell

    def traverseDungeon(self, cell, prev_cell = None):
        print(cell)
        #sleep(1)
        x = cell.x
        y = cell.y
        cell.visited = True
        if prev_cell is not None and prev_cell.room not in cell.room.doors:
            cell.room.doors.append(prev_cell.room)
        paths = []
        if cell.y < self.size - 1   and self.getCell(x    , y + 1).visited is not True :
            paths.append(self.NORTH)
        if cell.x < self.size - 1   and self.getCell(x + 1, y    ).visited is not True :
            paths.append(self.EAST)
        if cell.y > 0               and self.getCell(x    , y - 1).visited is not True :
            paths.append(self.SOUTH)
        if cell.x > 0               and self.getCell(x - 1, y    ).visited is not True :
            paths.append(self.WEST)
        if len(paths) > 0:
            branches = 1
            if len(paths) > 1:
                branches = random.randint(1,len(paths))
            for i in range(branches):
                if i >= 1:
                    print(branches, "branches at", cell)
                direction = paths[random.randint(0,len(paths)-1)]
                next_cell = self.getCell(x + direction[0], y + direction[1])
                if next_cell.room not in cell.room.doors:
                    cell.room.doors.append(next_cell.room)
                self.traverseDungeon(next_cell, cell)

    def getVisited(self):
        visited_cells = []
        for cell in self.grid:
            if cell.visited:
                visited_cells.append(cell)
        return visited_cells

if __name__ == '__main__':
    dungeon = DungeonGenerator(5)
    cell = dungeon.getCell(0,0)
    dungeon.traverseDungeon(cell)
    cell = dungeon.getCell(0,0)
    print(len(dungeon.getVisited()))
