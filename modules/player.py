import pygame, time, threading
from pygame.math import Vector2
import json, os

# 0 - Right
# 1 - Left
# 2 - Up
# 3 - Down




class Player:
    def __init__(self):
        # Set up the Player's x and y position to the spawn location (center of the screen roughly)

        self.Position = Vector2(450, 663)
        self.Center = Vector2(self.Position.x + 23, self.Position.y + 24)


        # Set up the necessary variables [Circle : Player's Hitbox, Currency, ...]

        self.Circle = None
        self.Currency = 0
        self.CurrentSkin = "Default"
        self.PowerUpName = "Default"
        self.Skins = []

        self.Direction = 0
        self.Speed = 2
        self.Lives = 3
        self.Score = 0
        self.Remove_Live_CD = False

        self.Power_Counter = 0
        self.Power_Counter_Duration = 600
        self.Powerup = False
        self.Currently_Moving = False

        self.Player_Images = []

        # Set up the Player's Keybinds

        self.Keybinds = {}

        self.Keybinds["Up"] = pygame.K_w
        self.Keybinds["Down"] = pygame.K_s
        self.Keybinds["Left"] = pygame.K_a
        self.Keybinds["Right"] = pygame.K_d

        self.VsWalter = False

        # Set the current direction keybind as RIGHT

        self.Direction_Keybind = 0

        # If there is a save file, apply the JSON Encode into the saved variables

        if os.path.exists("save_data.json"):
            with open("save_data.json", "r") as file:
                loaded_data = json.load(file)

                for Index, Value in loaded_data.items():
                    if hasattr(self, Index):
                        setattr(self, Index, Value)

        # Set up the Player's Images

        self.setup_PlayerImages()

        # Set the current allowed Turns as all False

        self.Turns_Allowed = [False, False, False, False]




   
    def setup_PlayerImages(self) -> None:
        self.Player_Images = []

        for i in range(1, 5): # From 1 to 4, add all of the found file from the current skins as the Player's Images
            self.Player_Images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{self.CurrentSkin}/movement/{i}.png'), (45, 45)))
        
        # Set the Last Player's Image as the first one as a base

        self.Last_PlayerImage = self.Player_Images[0]




    def move_player(self):
        # r, l, u, d
        moving = False

        # According to which Turns are allowed, set the Direction accordingly, and apply to x & y positions


        if self.Direction == 0 and self.Turns_Allowed[0]: # MOVING RIGHT
            self.Position.x += self.Speed

            moving = True
        elif self.Direction == 1 and self.Turns_Allowed[1]: # MOVING LEFT
            self.Position.x -= self.Speed

            moving = True
        if self.Direction == 2 and self.Turns_Allowed[2]: # MOVING UP
            self.Position.y -= self.Speed

            moving = True
        elif self.Direction == 3 and self.Turns_Allowed[3]: # MOVING DOWN
            self.Position.y += self.Speed

            moving = True
        
        self.Currently_Moving = moving

        

        




    def draw_player(self, Screen, counter):
        # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN

        self.Circle = pygame.draw.circle(Screen, 'black', (self.Center.x, self.Center.y), 17, 2)

        # Get the current sprite of the player

        PlayerImage = self.Player_Images[counter // 5]

        if not self.Currently_Moving: # If the Player isn't moving, set the Player's Image as the Last Player's Image
            PlayerImage = self.Last_PlayerImage

        # Draw the Player's Sprite according to the Direction & if the Player is currently moving

        if self.Direction == 0:
            Screen.blit(PlayerImage, (self.Position.x, self.Position.y))
        elif self.Direction == 1:
            Screen.blit(pygame.transform.flip(PlayerImage, True, False), (self.Position.x, self.Position.y))
        elif self.Direction == 2:
            Screen.blit(pygame.transform.rotate(PlayerImage, 90), (self.Position.x, self.Position.y))
        elif self.Direction == 3:
            Screen.blit(pygame.transform.rotate(PlayerImage, 270), (self.Position.x, self.Position.y))

        # Set the last player image as the current one

        self.Last_PlayerImage = PlayerImage




    def addScore(self, amount): # Add Score to the Player
        self.Score += amount




    def remove_life(self, amount = 1):
        if self.Remove_Live_CD: # If removing a life is currently on cooldown, then stop.
            return
        
        def thread():
            time.sleep(3)

            self.Remove_Live_CD = False

        # Reset some of the Player's variables
        
        self.Powerup = False
        self.Power_Counter = 0
        
        self.Position.x = 450
        self.Position.y = 663

        self.Lives -= amount # Remove the amount asked or 1

        self.Direction = 0

        self.Remove_Live_CD = True # Set the cooldown on

        threading.Thread(target=thread).start() # Set the Cooldown for Removing Lifes to off after 1 second