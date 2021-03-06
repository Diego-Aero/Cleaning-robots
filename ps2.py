# 6.00.2x Problem Set 2: Simulating robots

import math
import random

import ps2_visualize
import pylab

##################
## Comment/uncomment the relevant lines, depending on which version of Python you have
##################

# For Python 3.5:
#from ps2_verify_movement35 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.5 

# For Python 3.6:
from ps2_verify_movement38 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.6


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
#También se podría hacer sin recurrir a un diccionario
class RectangularRoom(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cleanTiles = set()

    def cleanTileAtPosition(self, pos):
        m = int(pos.x)
        n = int(pos.y)
        self.cleanTiles.add((m, n))

    def isTileCleaned(self, m, n):
        return (m, n) in self.cleanTiles

    def getNumTiles(self):
        return self.width * self.height

    def getNumCleanedTiles(self):
        return len(self.cleanTiles)

    def getRandomPosition(self):
        x = self.width * random.random()
        y = self.height * random.random()
        return Position(x, y)

    def isPositionInRoom(self, pos):
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

# === Problem 2
class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room=room
        pos=room.getRandomPosition()
        self.position=pos
        #self.position = self.room.getRandomPosition()
        room.cleanTileAtPosition(pos)
        #self.room.cleanTileAtPosition(self.position)
        self.speed=speed
        self.direction=random.randint(0, 359)
        

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position=position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction=direction

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!


# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        pos=self.getRobotPosition()
        newPos=pos.getNewPosition(self.getRobotDirection(), self.speed)
        room=self.room
        if room.isPositionInRoom(newPos):
            room.cleanTileAtPosition(newPos)
            self.setRobotPosition(newPos)
        else:
            self.setRobotDirection(random.randint(0, 359))


# Uncomment this line to see your implementation of StandardRobot in action!
#testRobotMovement(StandardRobot, RectangularRoom)


# === Problem 4
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """

    #Hay que inicializarlo para cada trial
    #Podríamos establecer las mismas condiciones iniciales en cada trial (posicion de los robots)
    time_steps=[]
    for i in range(num_trials):
        room=RectangularRoom(width, height)
        robots=[]
        time_step=0.0
        for i in range(num_robots):
            #Creamos una lista de robots
            robots.append(robot_type(room, speed))
            
        while room.getNumCleanedTiles()/room.getNumTiles()<min_coverage:
            #Mientras no se haya limpiado el porcentaje indicado
            for r in robots:
                #Vamos moviendo cada robot
                r.updatePositionAndClean()
            time_step+=1.0
        time_steps.append(time_step)

    return sum(time_steps)/num_trials

# Uncomment this line to see how much your simulation takes on average
print(runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot))


# === Problem 5
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        pos=self.getRobotPosition()
        newPos=pos.getNewPosition(self.getRobotDirection(), self.speed)
        room=self.room
        if room.isPositionInRoom(newPos):
            room.cleanTileAtPosition(newPos)
            self.setRobotPosition(newPos)
            # The proposed new robots differ in that they change direction randomly after every time step, rather than just when they run into walls.
        self.setRobotDirection(random.randint(0, 359))
            
# Uncomment this line to see how much your simulation takes on average
print(runSimulation(1, 1.0, 5, 5, 1.0, 30, StandardRobot))
print(runSimulation(1, 1.0, 5, 5, 1.0, 30, RandomWalkRobot))
#print(runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot))
#print(runSimulation(1, 1.0, 10, 10, 0.9, 30, StandardRobot))
#print(runSimulation(1, 1.0, 20, 20, 1.0, 30, StandardRobot))
#print(runSimulation(3, 1.0, 20, 20, 1.0, 30, StandardRobot))


def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

    
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    

# === Problem 6
# NOTE: If you are running the simulation, you will have to close it 
# before the plot will show up.

#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
showPlot1('Time It Takes 1 - 10 Robots To Clean 80% Of A Room', 'Number of Robots', 'Time-steps')
#

#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
showPlot2('Time It Takes Two Robots To Clean 80% Of Variously Shaped Rooms', 'Aspect Ratio', 'Time-steps')
#
