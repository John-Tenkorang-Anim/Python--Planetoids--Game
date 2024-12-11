"""
Subcontroller module for Planetoids

This module contains the subcontroller to manage a single level (or wave) in
the Planetoids game. Instances of Wave represent a single level, and should
correspond to a JSON file in the Data directory. Whenever you move to a new
level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the asteroids, and any bullets on
screen. These are model objects. Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a
complicated issue. If you do not know, ask on Ed Discussions and we will answer.

John Anim, ja857; Brendan Shek, bs863
12/09/24
"""
from game2d import *
from consts import *
from models import *
import random
import datetime

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Level is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)

class Wave(object):
    """
    This class controls a single level or wave of Planetoids.

    This subcontroller has a reference to the ship, asteroids, and any bullets
    on screen. It animates all of these by adding the velocity to the position
    at each step. It checks for collisions between bullets and asteroids or
    asteroids and the ship (asteroids can safely pass through each other). A
    bullet collision either breaks up or removes a asteroid. A ship collision
    kills the player.

    The player wins once all asteroids are destroyed. The player loses if they
    run out of lives. When the wave is complete, you should create a NEW instance
    of Wave (in Planetoids) if you want to make a new wave of asteroids.

    If you want to pause the game, tell this controller to draw, but do not
    update. See subcontrollers.py from Lecture 25 for an example. This class
    will be similar to than one in many ways.

    All attributes of this class are to be hidden. No attribute should be
    accessed without going through a getter/setter first. However, just because
    you have an attribute does not mean that you have to have a getter for it.
    For example, the Planetoids app probably never needs to access the attribute
    for the bullets, so there is no need for a getter there. But at a minimum,
    you need getters indicating whether you one or lost the game.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # THE ATTRIBUTES LISTED ARE SUGGESTIONS ONLY AND CAN BE CHANGED AS YOU SEE FIT
    # Attribute _data: The data from the wave JSON, for reloading
    # Invariant: _data is a dict loaded from a JSON file
    #
    # Attribute _ship: The player ship to control
    # Invariant: _ship is a Ship object
    #
    # Attribute _asteroids: the asteroids on screen
    # Invariant: _asteroids is a list of Asteroid, possibly empty
    #
    # Attribute _bullets: the bullets currently on screen
    # Invariant: _bullets is a list of Bullet, possibly empty
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _firerate: the number of frames until the player can fire again
    # Invariant: _firerate is an int >= 0

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER (standard form) TO CREATE SHIP AND ASTEROIDS

    def __init__(self, save_level):
        """

        Parameter save_level: placeholder for the data attribute
        Precondition: save_level is a variable
        """
        self._data = save_level
        x = self._data['ship']['position'][0]
        y = self._data['ship']['position'][1]
        angle = self._data['ship']['angle']
        self._ship = Ship(x, y, angle)
        self._asteroids = []
        for asteroid in save_level['asteroids']:
            size = asteroid['size']
            position = asteroid['position']
            direction = asteroid['direction']
            self._asteroids.append(Asteroid(size,position,direction))
        self._bullets = []
        self._firerate = 0
        self.display_message = GLabel(text="", font_size=36, color='white')
        self.display_message.x = GAME_WIDTH / 2
        self.display_message.y = GAME_HEIGHT / 2
        self.display_message.visible = False
        self.display_message.font_name = MESSAGE_FONT

    # UPDATE METHOD TO MOVE THE SHIP, ASTEROIDS, AND BULLETS
    def update(self, input, dt):
        """
        This method handles the changes that take place when the game is
        continuing (in the STATE_ACTIVE)

        Parameter input: detects and performs keyboard and mouse activities
        based on user input
        Precondtion: input is an instance of GInput

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if not STATE_ACTIVE:
            return
        if self._ship is None:
            return
        self.handle_turning(input)
        if self._firerate >= BULLET_RATE and input.is_key_down('spacebar'):
            self.bullet_release()
            self._firerate = 0
        else:
            self._firerate += 1
        for bullet in self._bullets:
            bullet.update()
        self.bullets_to_use()
        self._ship.move()
        self._ship.update(dt)
        self._ship.wrap()
        self.process_collisions()
        for asteroid in self._asteroids:
            asteroid.update(dt)
            asteroid.move()
            asteroid.wrap()
        self.check_game_status()

    # DRAW METHOD TO DRAW THE SHIP, ASTEROIDS, AND BULLETS
    def draw(self, view):
        """
        Draws everything to the screen and makes everything visible to the
        player.

        Parameter view: the game view, used in drawing (see examples from class)
        Precondition: view is an instance of GView
        """
        if self._ship is not None:
            self._ship.draw(view)
        for asteroid in self._asteroids:
            asteroid.draw(view)
        for bullet in self._bullets:
            bullet.draw(view)
        if self.display_message.visible:
            self.display_message.draw(view)
    # RESET METHOD FOR CREATING A NEW LIFE

    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def handle_turning(self, input):
        """"
        This method handles the movement of the ship using the user input

        Parameter input: detects and performs keyboard and mouse activities
        based on user input
        Precondtion: input is an instance of GInput
        """
        turn_angle = 0
        if input.is_key_down('left'):
            turn_angle += SHIP_TURN_RATE
        if input.is_key_down('right'):
            turn_angle -= SHIP_TURN_RATE
        if turn_angle != 0:
            self._ship.turn(turn_angle)
        if input.is_key_down('up'):
            self._ship.shipImpulse()

    def bullets_to_use(self):
        """
        This method is a procedure that updates the bullets left to use after
        some bullets have been fired.
        """
        new_bullets = []
        for bullet in self._bullets:
            if (-DEAD_ZONE < bullet.x < GAME_WIDTH + DEAD_ZONE
                and -DEAD_ZONE < bullet.y < GAME_HEIGHT + DEAD_ZONE):
                new_bullets.append(bullet)
        self._bullets = new_bullets

    def bullet_release(self):
        """
        This method is a procedure that handles the release of a bullet
        """
        facing_vector = self._ship.get_facing()
        facing_x = facing_vector.x
        facing_y = facing_vector.y
        position = (self._ship.x + (facing_x * SHIP_RADIUS), self._ship.y +
                   (facing_y* SHIP_RADIUS))
        velocity = Vector2(facing_x * BULLET_SPEED, facing_y * BULLET_SPEED)
        generated_bullet = Bullet(position, velocity)
        self._bullets.append(generated_bullet)

    def process_collisions(self):
        """
        This method is a procedure that processes all the collisions
        that happens in the game. Asteroid-Ship collision, bullet-asteroid
        collision.
        """
        if self._ship is None:
            return
        bullets_to_remove = []
        asteroids_to_remove = []
        new_asteroids = []
        for asteroid in self._asteroids[:]:
            for bullet in self._bullets[:]:
                if self._collides(asteroid, bullet):
                    bullets_to_remove.append(bullet)
                    asteroids_to_remove.append(asteroid)
                    if asteroid.get_size() in ['large', 'medium']:
                        new_asteroids.extend(self._break_asteroid(asteroid,
                                             bullet.get_velocity()))
        for asteroid in self._asteroids[:]:
            if self._ship is not None and self._collides(asteroid, self._ship):
                asteroids_to_remove.append(asteroid)
                ship_velocity = self._ship.get_velocity()
                self._ship = None
                if asteroid.get_size() in ['large', 'medium']:
                    new_asteroids.extend(self._break_asteroid(asteroid,
                                         ship_velocity))
        for bullet in bullets_to_remove:
            if bullet in self._bullets:
                self._bullets.remove(bullet)
        for asteroid in asteroids_to_remove:
            if asteroid in self._asteroids:
                self._asteroids.remove(asteroid)
        self._asteroids.extend(new_asteroids)

    def _collides(self, object1, object2):
        """
        Returns True if distance is less than sum of radius from their centers

        This helper function calculates the possibility of collisions
        by computing the distance between colliding objects and the d

        Parameter object1: object involved in collision
        Precondition: object1 is either an object of Asteroid or Bullet or Ship

        Paramter object2: object involved in collision
        Precondition: object2 is either an object of Asteroid or Bullet or Ship
        """
        distance = math.sqrt((object1.x - object2.x)**2 +
                             (object1.y - object2.y)**2)
        radius_sum = object1.get_radius() + object2.get_radius()
        return distance < radius_sum

    def _break_asteroid(self, asteroid, collision_vector):
        """
        Returns a list of smaller asteroids resulting from a collision.

        This helper function is used to break the asteroid after collision.
        Large asteroid produces 3 medium asteroids, medium asteroid produces
        3 small asteroids after collision

        Parameter asteroid: asteroid collides with either ship or bullet
        Precondition: asteroid is an Asteroid object

        Parameter collision_vector: velocity component of object colliding with
        asteroid
        Precondition: collision_vector is a velocity vector of either ship
        or bullet
        """
        new_size = 'medium' if asteroid.get_size() == 'large' else 'small'
        new_radius = MEDIUM_RADIUS if new_size == 'medium' else SMALL_RADIUS

        angle = math.atan2(collision_vector.y, collision_vector.x)
        vectors = [
            (math.cos(angle), math.sin(angle)),
            (math.cos(angle + 2 * math.pi / 3),
             math.sin(angle + 2 * math.pi / 3)),
            (math.cos(angle - 2 * math.pi / 3),
             math.sin(angle - 2 * math.pi / 3))
        ]
        new_asteroids = []
        for vec in vectors:
            new_x = asteroid.x + new_radius * vec[0]
            new_y = asteroid.y + new_radius * vec[1]
            new_asteroids.append(Asteroid(new_size, (new_x, new_y), vec))
        return new_asteroids

    def check_game_status(self):
        """
        This is a procedure that checks the state of the game
        """
        if self._ship is None:
            self.display_message.text = "Game Over! You Lose!"
            self.display_message.visible = True
            self.state = STATE_COMPLETE
        elif len(self._asteroids) == 0:
            self.display_message.text = "Congratulations! You Win!"
            self.display_message.visible = True
            self.state = STATE_COMPLETE

    def display_message(self, message):
        """
        This is a method that displays a message

        Paramter message: The message to be displayed when you win or lose
        Precondtion: message is a string
        """
        self._title = GLabel(text = message)
        self._title.font_name = TITLE_FONT
        self._title.font_size = TITLE_SIZE
        self._title.fill_color = 'white'
        self._title.x = GAME_WIDTH/2
        self._title.y = GAME_HEIGHT/2
