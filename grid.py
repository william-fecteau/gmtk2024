from queue import Queue

import numpy as np


class Grid:
    EMPTY = 0
    HEAD = 1
    APPLE = 2
    BODY = 3
    WALL = 4

    def __init__(self, nbRows: int, nbColumns: int, nbAppleOnScreen: int, initialSnakeLength: int):
        self.nbRows = nbRows
        self.nbColumns = nbColumns
        self.appleEaten = initialSnakeLength
        self.isDead = False
        self.nbAppleOnScreen = nbAppleOnScreen
        self.score = 0

        self.setupGrid()

        # Place player on the center
        self.headPos = (self.nbRows // 2, self.nbColumns // 2)
        self.grid[self.headPos] = Grid.HEAD
        self.direction: tuple[int, int] = (0, 1)
        self.queue = Queue()

    def setupGrid(self):
        self.grid = np.zeros((self.nbRows, self.nbColumns), dtype=np.int8)

        # Setup walls on every side
        self.grid[:, 0] = Grid.WALL
        self.grid[:, self.nbColumns - 1] = Grid.WALL
        self.grid[0, :] = Grid.WALL
        self.grid[self.nbRows - 1, :] = Grid.WALL

        for i in range(self.nbAppleOnScreen):
            self.placeApple()

    def placeApple(self):
        goodPos = False
        pos = (0, 0)
        maxIter = 69
        i = 0
        while not goodPos and i < maxIter:
            pos = (np.random.randint(1, self.nbRows - 1),
                   np.random.randint(1, self.nbColumns - 1))
            if self.grid[pos] == Grid.EMPTY:
                goodPos = True

            i += 1

        self.grid[pos] = Grid.APPLE

    def moveHead(self):
        # Add the current headPos to the body
        self.queue.put(self.headPos)
        self.grid[self.headPos] = Grid.BODY

        # Move head
        self.headPos = (self.headPos[0] + self.direction[0],
                        self.headPos[1] + self.direction[1])
        if (self.grid[self.headPos] == Grid.WALL or self.grid[self.headPos] == Grid.BODY):
            self.die()
            return

        # Eat apple if its present
        if self.grid[self.headPos] == Grid.APPLE:
            self.appleEaten += 1
            self.score += 1
            self.placeApple()
        self.grid[self.headPos] = Grid.HEAD

        # Make snake longer
        if self.appleEaten > 0:
            self.appleEaten -= 1
        # Remove last pos in the queue
        elif not self.queue.empty():
            lastPos = self.queue.get()
            self.grid[lastPos] = Grid.EMPTY

    def update(self):
        self.moveHead()

    def die(self):
        self.isDead = True
        print("You died - Score : {}".format(self.score))
