"""
Models module for Planetoids

This module contains the model classes for the Planetoids game. Anything that
you interact with on the screen is model: the ship, the bullets, and the
planetoids.

We need models for these objects because they contain information beyond the
simple shapes like GImage and GEllipse. In particular, ALL of these classes
need a velocity representing their movement direction and speed (and hence they
all need an additional attribute representing this fact). But for the most part,
that is all they need. You will only need more complex models if you are adding
advanced features like scoring.

You are free to add even more models to this module. You may wish to do this
when you add new features to your game, such as power-ups. If you are unsure
about whether to make a new class or not, please ask on Ed Discussions.

John Anim, ja857; Brendan Shek, bs863
12/09/24
"""
from consts import *
from game2d import *
from introcs import *
import math

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py. If you need extra information from Gameplay, then it should be a
# parameter in your method, and Wave should pass it as a argument when it calls
# the method.


class Bullet(GEllipse):
    """
    A class representing a bullet from the ship

    Bullets are typically just white circles (ellipses). The size of the bullet
    is determined by constants in consts.py. However, we MUST subclass GEllipse,
    because we need to add an extra attribute for the velocity of the bullet.

    The class Wave will need to look at this velocity, so you will need getters
    for the velocity components. However, it is possible to write this assignment
    with no setters for the velocities. That is because the velocity is fixed
    and cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set the
    starting velocity. This __init__ method will need to call the __init__ from
    GEllipse as a helper. This init will need a parameter to set the direction
    of the velocity.

    You also want to create a method to update the bolt. You update the bolt by
    adding the velocity to the position. While it is okay to add a method to
    detect collisions in this class, you may find it easier to process
    collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _velocity: represents the speed and direction of a bullet
    # Invariant: _velocity is a Vector2 object.
    #
    # Attribute _radius: represents the radius of a bullet
    # Invariant: _radius is a non-negative int or float.
    #
    # Attribute x: the x-position of the bullet
    # Invariant: x is a number (int or float)
    #
    # Attribute y: the y-position of the bullet
    # Invariant: y is a number (int or float)

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_velocity(self):
        """Returns the current velocity vector of the bullet."""
        return self._velocity

    def get_radius(self):
        """Returns the radius of the bullet."""
        return BULLET_RADIUS

    # INITIALIZER TO SET THE POSITION AND VELOCITY
    def __init__(self, position, velocity):
        """
        Initializes a new `Bullet` object with the given position and velocity.

        This constructor sets up the bullet's position, velocity, and
        visual representation. The bullet is represented as a colored
        circle with a predefined radius and color.

        Attributes:
        Parameter velocity: The velocity of the bullet, represented as a vector.
        Precondition: velocity is a Vector2 object.

        Parameter position: contains the x and y coordinates
        of the bullet's center
        Precondition: position is a list.
        """
        super().__init__(x=position[0],
                        y=position[1],
                        height = 2 * BULLET_RADIUS,
                        width = 2 * BULLET_RADIUS,
                        fillcolor = BULLET_COLOR)
        self._velocity = velocity

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def update(self):
        """
        Updates the bullet's position by applying velocity to the position.
        The position does not wrap around screen edges.
        """
        self.x += self._velocity.x
        self.y += self._velocity.y


class Ship(GImage):
    """
    A class to represent the game ship.

    This ship is represented by an image. The size of the ship is determined by
    constants in consts.py. However, we MUST subclass GEllipse, because we need
    to add an extra attribute for the velocity of the ship, as well as the facing
    vector (not the same) thing.

    The class Wave will need to access these two values, so you will need getters
    for them. But per the instructions,these values are changed indirectly by
    applying thrust or turning the ship. That means you won't want setters for
    these attributes, but you will want methods to apply thrust or turn the ship.

    This class needs an __init__ method to set the position and initial facing
    angle. This information is provided by the wave JSON file. Ships should
    start with a shield enabled.

    Finally, you want a method to update the ship. When you update the ship, you
    apply the velocity to the position. While it is okay to add a method to
    detect collisions in this class, you may find it easier to process collisions
    in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _facing: the current angle of the ship
    # Invariant: _facing is a Vector2 object
    #
    # Attribute x: position on x-axis
    # Invaraint: x is a component of position ( member of position list)
    #
    # Attribute y: position on y-axis
    # Invariant: y is a component of the position (member of position list)
    #
    # Attribute _velocity: velocity of object
    # Invariant: _velocity is a Vector2 object which has x and y components
    #
    # Attribute angle: angle of turn
    # Invariant: angle is an integer between 0 and 360

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_velocity(self):
        """Returns the current velocity vector of the ship."""
        return self._velocity

    def get_facing(self):
        """Returns the current facing vector of the ship."""
        return self._facing

    def get_radius(self):
        """Returns the radius of the ship."""
        return SHIP_RADIUS

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, x, y, angle):
        """
        Initializes a new `Ship` object with the given position and angle.

        This constructor sets up the ship's position, angle, velocity,
        and facing direction. It also initializes the ship's visual
        representation using a predefined image.

        Parameter x: The horizontal position of the ship's center.
        Precondtion: x is an int and the x-coordinate of the ship's center

        Parameter y: The vertical position of the ship's center.
        Precondition: y is an int and the y-coordinate of the ship's center.

        Parameter angle: directional angle of the ship used in calculating the
        facing angle
        Precondition:The angle of the ship in degrees, measured counterclockwise
        from the positive x-axis.
        """
        super().__init__(x=x, y=y, width=2 * SHIP_RADIUS,angle = angle,
                         height=2 * SHIP_RADIUS, source=SHIP_IMAGE)
        self.x = x
        self.y = y
        self._velocity = introcs.Vector2(0,0)
        self._facing = introcs.Vector2(math.cos(math.radians(self.angle)),
                                        math.sin(math.radians(self.angle)))

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def turn(self, turn_angle):
        """
        Calculates the change in angle of the ship's facing direction based
        on user input.

        Parameter turn_angle: The degree to which the ship turns, expressed as
        an angle.

        Precondition: turn_angle must be an int or float.
        """
        self.angle = (self.angle + turn_angle) % 360
        self._facing = introcs.Vector2(math.cos(math.radians(self.angle)),
                                       math.sin(math.radians(self.angle)))

    def shipImpulse(self):
        """Changes the speed (thrust) of the ship based on user input."""
        impulse = self._facing * SHIP_IMPULSE
        self._velocity += impulse
        if self._velocity.length() > SHIP_MAX_SPEED:
            self._velocity = self._velocity.normalize() * SHIP_MAX_SPEED

    def move(self):
        """Changes the position of the ship based on velocity."""
        self.x += self._velocity.x
        self.y += self._velocity.y

    def wrap(self):
        """Wraps the asteroid around the screen edges."""
        # Horizontal wrapping:
        if self.left < -DEAD_ZONE:
            self.x += GAME_WIDTH + 2 * DEAD_ZONE
        elif self.right > GAME_WIDTH + DEAD_ZONE:
            self.x -= GAME_WIDTH + 2 * DEAD_ZONE
        # Vertical wrapping:
        if self.top < -DEAD_ZONE:
            self.y += GAME_HEIGHT + 2 * DEAD_ZONE
        elif self.bottom > GAME_HEIGHT + DEAD_ZONE:
            self.y -= GAME_HEIGHT + 2 * DEAD_ZONE

    def update(self, dt):
        """
        Updates the ship's position by applying velocity.
        The position wraps around screen edges to ensure continuous movement.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self.x += self._velocity.x * dt
        self.y += self._velocity.y * dt


class Asteroid(GImage):
    """
    A class to represent a single asteroid.

    Asteroids are typically are represented by images. Asteroids come in three
    different sizes (SMALL_ASTEROID, MEDIUM_ASTEROID, and LARGE_ASTEROID) that
    determine the choice of image and asteroid radius. We MUST subclass GImage,
    because we need extra attributes for both the size and the velocity of the
    asteroid.

    The class Wave will need to look at the size and velocity, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for either of these. That is because they are fixed and cannot
    change when the asteroid is created.

    In addition to the getters, you need to write the __init__ method to set the
    size and starting velocity. Note that the SPEED of an asteroid is defined in
    const.py, so the only thing that differs is the velocity direction.

    You also want to create a method to update the asteroid. You update the
    asteroid by adding the velocity to the position. While it is okay to add a
    method to detect collisions in this class, you may find it easier to process
    collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute x: position on x-axis
    # Invaraint: x is a component of position ( member of position list)
    #
    # Attribute y: position on y-axis
    # Invariant: y is a component of the position (member of position list)
    #
    # Attribute _velocity: velocity of object
    # Invariant: _velocity is a Vector2 object which has x and y components
    #
    # Attribute _size: size of the asteroid
    # Invariant: _size is a string that's either small,medium, or large

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_velocity(self):
        """Returns the velocity vector of the asteroid."""
        return self._velocity

    def get_size(self):
        """Returns the size of the asteroid."""
        return self._size

    def get_radius(self):
        """Returns the radius of the asteroid based on its size."""
        if self._size == 'large':
            return LARGE_RADIUS
        elif self._size == 'medium':
            return MEDIUM_RADIUS
        elif self._size == 'small':
            return SMALL_RADIUS

    # INITIALIZER TO CREATE A NEW ASTEROID
    def __init__(self, size,position,direction):
        """
        Initializes a new `Asteroid` object with the given size,
        position, and direction.

        This constructor sets up the asteroid's size, velocity,
        and visual representation. The asteroid's image and dimensions are
        determined based on its size, and its velocity is calculated using a
        directional vector scaled by the asteroid's size.

        Parameter size:The size of the asteroid('small', 'medium', or 'large').
        Precondtion: size is a string

        Parameter position: contains the x and y coordinates of
        the asteroid's center
        Precondition: position is a list.

        Parameter direction: A one-dimensional list with two integer values,
        representing the x- and y- direction of the ship, respectively.
        Precondition: direction is a one-dimensional list with two int values.
        """
        self._size = size
        self._velocity = self._velocity_vector(direction,size)
        if size == 'small':
            image = SMALL_IMAGE
            width = SMALL_RADIUS * 2
            height = SMALL_RADIUS * 2
        elif size == 'medium':
            image = MEDIUM_IMAGE
            width = MEDIUM_RADIUS * 2
            height = MEDIUM_RADIUS * 2
        else:
            image = LARGE_IMAGE
            width = LARGE_RADIUS * 2
            height = LARGE_RADIUS * 2
        super().__init__(x=position[0], y=position[1],width=width,
                         height=height, source=image)

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def move(self):
        """Changes asteroid's position based on its velocity."""
        self.x += self._velocity.x
        self.y += self._velocity.y

    def _velocity_vector(self,direction,size):
        """
        Calculates the velocity of the asteroid based on its direction and
        size.

        Parameter direction: A one-dimensional list with two integer values,
        representing the x- and y- direction of the ship, respectively.
        Parameter size: A string that represents the size of the asteroid.

        Precondition: direction is a one-dimensional list with two int values.
        Precondition: size is a string with value either 'small', 'medium' or
        'large'.
        """
        if size == 'small':
            speed = SMALL_SPEED
        elif size == 'medium':
            speed = MEDIUM_SPEED
        else:
            speed = LARGE_SPEED
        if direction == [0, 0]:
            return Vector2(0, 0)
        direction_magnitude = math.sqrt(direction[0]**2 + direction[1]**2)
        unit_vector = [direction[0]/direction_magnitude,
                       direction[1]/direction_magnitude]
        return Vector2(unit_vector[0]*speed, unit_vector[1]*speed)

    def wrap(self):
        """
        Wraps the asteroid around the screen edges.
        """
        if self.x < -DEAD_ZONE:
            self.x += GAME_WIDTH + 2 * DEAD_ZONE
        elif self.x > GAME_WIDTH + DEAD_ZONE:
            self.x -= GAME_WIDTH + 2 * DEAD_ZONE
        if self.y < -DEAD_ZONE:
            self.y += GAME_HEIGHT + 2 * DEAD_ZONE
        elif self.y > GAME_HEIGHT + DEAD_ZONE:
            self.y -= GAME_HEIGHT + 2 * DEAD_ZONE

    def update(self, dt):
        """
        Updates the asteroid's position by applying velocity.
        The position wraps around screen edges to ensure continuous movement.

        Parameter dt: The time elapsed since the last update.

        Precondition: dt is a non-zero float.
        """
        self.x += self._velocity.x * dt
        self.y += self._velocity.y * dt

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
