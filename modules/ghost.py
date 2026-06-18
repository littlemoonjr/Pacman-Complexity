import pygame
from pygame.math import Vector2
import modules.powerups as powerups

# Get all of the image's of the ghosts, along with them being powered up or dead

spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/Powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45, 45))


# Get if the powerup is on image for ghosts

shaky = [
    pygame.transform.scale(pygame.image.load(f'assets/ghost_images/shaky_1.png'), (45, 45)),
    pygame.transform.scale(pygame.image.load(f'assets/ghost_images/shaky_2.png'), (45, 45)),
]

# Get the ghost's data and set it up as a table for usage and all the information necessary

Ghost_Data = {
    "Blinky" : {
        "Position" : (56,58),
        "Direction": 0,
        "Speed" : 2,

        "Image" : pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45, 45)),
         "ID" : 0
    },

    "Inky" : {
        "Position" : (440, 388),
        "Direction": 2,
        "Speed" : 2,

        "Image" : pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (45, 45)),
        "ID" : 1
    },

    "Pinky" : {
        "Position" : (440, 438),
        "Direction": 2,
        "Speed" : 2,

        "Image" : pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45, 45)),
        "ID" : 2
    },

    "Clyde" : {
        "Position" : (440, 438),
        "Direction": 2,
        "Speed" : 2,

        "Image" : pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45, 45)),
        "ID" : 3
    },

    "Walter" : {
        "Position" : (440, 438),
        "Direction": 2,
        "Speed" : 7,

        "Image" : pygame.transform.scale(pygame.image.load(f'assets/ghost_images/walter white.png'), (45, 45)),
        "ID" : 3
    },
}

class Ghost:
    def __init__(self, GhostName : str, Local_Game):
        # Get the Ghost's Base Data

        GhostTable = Ghost_Data[GhostName]
        ID = GhostTable["ID"]

        if Local_Game.WalterClyde: # If the event for walter is active then..
            GhostTable = Ghost_Data["Walter"]

        
        self.Name = GhostName

        x_coord, y_coord = Ghost_Data[GhostName]["Position"] # Unpack the tuple for x & y coordinates from the Ghost's Data

        self.x_pos = x_coord
        self.y_pos = y_coord

        self.base_data = GhostTable # Set the base_data as the Ghost's Base Data
        

        # Set up the center position for the Ghost

        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22

        # Set the current target for the Ghost as nothing

        self.target = None

        # Set up the Ghost's Speed, Image, & Direction based on data

        self.speed = GhostTable["Speed"]
        self.img = GhostTable["Image"]
        self.direction = GhostTable["Direction"]

        # Set up the variables for the ghost being dead, how many times they shook when power up is on, and if the ghost is in the box

        self.dead = False

        self.in_box = False
        self.shake_number = 0
        self.current_shake = 0

        self.id = ID # Set the Ghost's ID from Base Data

        self.check_collisions(Local_Game) # Set up the ghost's turns
        self.rect = self.draw(Local_Game) # Set up the ghost's hitbox




    def draw(self, Local_Game):
        Player = Local_Game.Player

        if self.dead: # If the ghost is dead
            Local_Game.Screen.blit(dead_img, (self.x_pos, self.y_pos)) # Draw them as dead at the position
        elif Player.Powerup and not Local_Game.Eaten_Ghosts[self.id] and powerups.Powerups[Player.PowerUpName]["Danger"]:
            # If the power up poses a danger, and the ghost hasn't been eaten yet, as well as the powerup being on

            if Player.Power_Counter > 450: # If it's been more than 450 frames since the power up
                # Make the ghost shake their boots

                # Shake the ghost every 8 frames

                self.shake_number += 1

                if self.shake_number >= 8:
                    self.current_shake += 1
                    self.shake_number = 0

                Local_Game.Screen.blit(shaky[self.current_shake - 1], (self.x_pos, self.y_pos)) # Set it according to what shake the ghost is currently at

                if self.current_shake >= 2:
                    self.current_shake = 0
                
            else: # Otherwise if it hasn't been more than 450 frames
                Local_Game.Screen.blit(spooked_img, (self.x_pos, self.y_pos)) # Set the ghost as just scared
            
        else: # Otherwise set them as normal
            Local_Game.Screen.blit(self.img, (self.x_pos, self.y_pos))
        
         # Set the ghost's rect based off of the center position and set the size as by 36

        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        self.rect = ghost_rect




    def check_collisions(self, Local_Game):
       # R, L, U, D

       # Set up the Height of the game according to grid size

        num1 = ((Local_Game.Screen_Size["Height"] - 50) // 32) 
        num2 = (Local_Game.Screen_Size["Width"] // 30) 
        num3 = 15

        # Set the ghost's turns as all false

        self.turns = [False, False, False, False]

        if 0 < self.center_x // 30 < 29: # If they aren't at the edge of the map in terms of the grid
            if Local_Game.Level[(self.center_y - num3) // num1][self.center_x // num2] == 9: # If the ghost is concurrently colliding with any blocks above
                # Set the UP turn allowed
                self.turns[2] = True
            # If the ghost is in the box or currently dead

            if Local_Game.Level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (Local_Game.Level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)): # If the ghost is concurrently colliding with any blocks to the left & closest to box
                # Set the LEFT turn allowed
                self.turns[1] = True
            if Local_Game.Level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (Local_Game.Level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):  # If the ghost is concurrently colliding with any blocks to the right  & closest to box
                # Set the RIGHT turn allowed
                self.turns[0] = True
            if Local_Game.Level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (Local_Game.Level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)): # If the ghost is concurrently colliding with any blocks below & closest to box
                # Set the DOWN turn allowed
                self.turns[3] = True
            if Local_Game.Level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (Local_Game.Level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)): # If the ghost is concurrently colliding with any blocks below & closest to box
                # Set the UP turn allowed
                self.turns[2] = True


            if self.direction == 2 or self.direction == 3: # If the ghost is currently looking either up or down
                # Check if the ghost is centered vertically to allow a horizontal turn
                if 12 <= self.center_x % num2 <= 18:
                    # Check tile BELOW: Valid if tile value < 3, or if it's the ghost house gate (9) and ghost can enter/leave

                    if Local_Game.Level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (Local_Game.Level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)): # Check tile to the 
                        self.turns[3] = True # Allow turning DOWN
                    if Local_Game.Level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (Local_Game.Level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)): # Check tile to the LEFT
                        self.turns[2] = True # Allow turning UP
                if 12 <= self.center_y % num1 <= 18: # Check if the ghost is centered vertically to allow a horizontal turn
                    if Local_Game.Level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (Local_Game.Level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)): # Check left tile
                        # Set the LEFT turn allowed
                        self.turns[1] = True
                    if Local_Game.Level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (Local_Game.Level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)): # Check right tile
                        # Set the RIGHT turn allowed
                        self.turns[0] = True




            if self.direction == 0 or self.direction == 1: # If the ghost is currently looking either right or left
                if 12 <= self.center_x % num2 <= 18: # Check if the ghost is centered horizontally to allow a vertical turn
                    # Same Logic as before


                    if Local_Game.Level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (Local_Game.Level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if Local_Game.Level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (Local_Game.Level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                
                if 12 <= self.center_y % num1 <= 18: # Check if the ghost is centered vertically to allow a horizontal turn
                    # Same Logic as before


                    if Local_Game.Level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (Local_Game.Level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if Local_Game.Level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (Local_Game.Level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            # If not affected by grid's rules then set right & left turns to be allowed

            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480: # Check if the ghost is at the box
            self.in_box = True # The Ghost is at the box [in_box]
        else:
            self.in_box = False # The Ghost isn't at the box [in_box]




    def move_Clyde(self):
        # r, l, u, d

        # [ Main Comment ]

        # According to direction, Clyde will turn to whatever turn is currently available

        if self.direction == 0:
            if self.target.x > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target.y > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target.y < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target.x < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target.y > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target.y < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target.y > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target.x < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target.y > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target.y < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target.x > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target.y > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target.y < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target.x < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target.y < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target.x > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target.x < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target.y > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target.x > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target.x < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target.y > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target.x > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target.x < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target.y < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target.x > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target.x < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30: # If the Ghost is currently in a tunnel, then teleport them to the other part of the tunnel
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30


    def move_Blinky(self):
        # r, l, u, d

        # [ Main Comment ]

        # According to direction, Blinky will turn whenever they collide with walls, otherwise they will keep going straight

        if self.direction == 0:
            if self.target.x > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target.y > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target.y < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target.x < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target.x < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target.y > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target.y < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target.x > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target.y < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target.x > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target.x < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target.y > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target.y > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target.x > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target.x < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target.y < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30: # If the Ghost is currently in a tunnel, then teleport them to the other part of the tunnel
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30


    def move_Inky(self):
        # r, l, u, d
        # inky turns up or down at any point to pursue, but left and right only on collision

         # [ Main Comment ]

        # According to direction, Inky will turn up or down at any point to pursue, but only left and right on collision

        if self.direction == 0:
            if self.target.x > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target.y > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target.y < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target.x < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target.y > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target.y < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target.y > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target.x < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target.y > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target.y < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target.x > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target.y > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target.y < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target.y < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target.x > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target.x < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target.y > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target.y > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target.x > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target.x < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target.y < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30: # If the Ghost is currently in a tunnel, then teleport them to the other part of the tunnel
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30

    def move_Pinky(self):
        # r, l, u, d

         # [ Main Comment ]

        # According to direction, Pinky will turn left or right whenever they can, but only up or down on collisions

        if self.direction == 0:
            if self.target.x > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target.y > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target.y < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target.x < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target.y > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target.x < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target.y > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target.y < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target.x > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target.x < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target.y < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target.x > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target.x < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target.y > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target.y > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target.x > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target.x < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target.y < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target.x > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target.x < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30: # If the Ghost is currently in a tunnel, then teleport them to the other part of the tunnel
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30





