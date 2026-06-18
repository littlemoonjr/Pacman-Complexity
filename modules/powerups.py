import pygame
import random, copy

# Set up all the current power up's and their data associated as well as their images

Powerups = {
    "Default": {
        "Danger" : True,
        "OnGhost" : True
    },

    "Laser_Eyes": {
        "Danger" : True,
        "OnGhost": True,

        "Beam" : pygame.image.load('assets/misc/laser eye beam.png')
    },

    "RAINBOW" : {
        "Danger" : True,
        "OnGhost" : True
    },

    "MR_BOND": {
        "Danger" : True,

        "Gun" : pygame.transform.scale(pygame.image.load('assets/misc/gun.png'),(64,64)),
        "Logo": pygame.transform.scale(pygame.image.load('assets/misc/mrbondyyy.png'),(200,191)),
        "Complete": pygame.transform.scale(pygame.image.load('assets/misc/completethemission.png'),(327,36.5)),
    }
}

# Set up the gun

class Gun:
    def __init__(self, Local_Game):
        self.Frame = 0 # The current frame the gun is on
        self.Cooldown = 40 # The cooldown of the gun
        self.Local_Game = Local_Game # The Game Class
        self.Bullets = [] # The bullets the gun fired

    def fire(self):
        self.Frame += 1 # Add a frame every iteration

        if self.Cooldown <= self.Frame: # If the current frames passed is more than the cooldown
            self.Frame = 0 # Reset the Frame

            self.Bullets.append(Bullet(self.Local_Game)) # Send out a bullet every time the gun shoots
            self.Local_Game.SoundSystem.play_sound("shot") # Send out a shot sound every time the gun shoots

        for bullet in self.Bullets: # Update every bullet 
            bullet : Bullet
            bullet.update()

class Bullet(Gun):
    def __init__(self, Local_Game):
        Player = Local_Game.Player # The Player
        self.Local_Game = Local_Game # The Game

        self.Position = Player.Position # The Player's current position
        self.image = pygame.Surface((10, 5)) # Set up the bullet's size hozortionally
        self.image.fill((255, 255, 0)) # Yellow bullet
        self.rect = self.image.get_rect() # Get the rect of the surface

        self.rect.center = (self.Position.x, self.Position.y) # The center of the rect of the surface

        self.speed = 12 # The bullet's speed
        self.Frame = 0 # The current frame it's at

        self.Direction = copy.copy(self.Local_Game.Player.Direction)

        if self.Direction >= 2: # If the player is looking up or down
            self.image = pygame.Surface((5, 10)) # Set up the bullet's size vertically

            self.image.fill((255, 255, 0)) # Yellow bullet
            self.rect = self.image.get_rect()

            self.rect.center = (self.Position.x, self.Position.y)
            self.rect.x += 20
        else:
            self.rect.x += 10
            self.rect.y += 20



    def update(self):
        # Move the bullet forward on the X axis
        if self.Direction < 2:
            if self.Direction == 1:
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed
        else:
            if self.Direction == 3:
                self.rect.y += self.speed
            else:
                self.rect.y -= self.speed

        self.Local_Game.Screen.blit(self.image, (self.rect.x,self.rect.y))

        for _, Ghost in self.Local_Game.Ghosts.items():
            if self.rect.colliderect(Ghost.rect) and not Ghost.dead:
                Ghost.dead = True
                self.Local_Game.Eaten_Ghosts[Ghost.id] = True
                self.Local_Game.Player.addScore((2 ** self.Local_Game.Eaten_Ghosts.count(True)) * 100)

        
        self.Frame += 1
        # Delete if it goes off-screen to clear RAM memory
        if self.Frame >= 30:
            self.kill()
    
    def kill(self):
        del self


class PowerupSystem:
    def __init__(self, Local_Game):
        self.Local_Game = Local_Game
        self.Player = Local_Game.Player
        self.Enabled = True

    def Default(self, GhostData): # The Default for eating Ghosts
        Local_Game = self.Local_Game
        Player = self.Player

        if not Player.Powerup: return
        if GhostData.dead: return
        if Local_Game.Eaten_Ghosts[GhostData.id]: return

        if Player.Circle.colliderect(GhostData.rect):
                GhostData.dead = True
                Local_Game.Eaten_Ghosts[GhostData.id] = True
                Player.addScore((2 ** Local_Game.Eaten_Ghosts.count(True)) * 100)

    def Laser_Eyes(self, GhostData): # Detecting if the Hitbox's for the Laser Eye's hit a Ghost
        Local_Game = self.Local_Game
        Player = self.Player

        if not Player.Powerup: return
        if GhostData.dead: return
        #if Local_Game.Eaten_Ghosts[GhostData.id]: return

        LaserEye_Hitbox = Player.LaserEye_Hitbox

        if LaserEye_Hitbox.colliderect(GhostData.rect):
            GhostData.dead = True
            #Local_Game.Eaten_Ghosts[GhostData.id] = True
            Player.addScore((2 ** Local_Game.Eaten_Ghosts.count(True)) * 100)

    def establish_Laser_Eyes(self): # The Hitbox for the Laser Eye's
        Local_Game = self.Local_Game
        Player = self.Player

        if not Player.Powerup: return

        Direction = Player.Direction

        # Left by default
        x = Player.Position.x - 400
        y = Player.Position.y + 10
        BeamPos_x = Player.Position.x - 20
        BeamPos_y = Player.Position.y - 130

        Width = 400
        Height = 45

        if Direction == 0: # Right
            x = Player.Position.x + 50

        if Direction == 2: # Up
            x = Player.Position.x + 10
            y = Player.Position.y - 400

            Width = 45
            Height = 400


        if Direction == 3: # Down
            x = Player.Position.x - 10
            y = Player.Position.y + 50

            Width = 45
            Height = 400


        Player.LaserEye_Hitbox = pygame.Rect([x, y, Width, Height])

    def draw_Laser_Eyes(self):  # Drawing the laser eyes for the Player
        Local_Game = self.Local_Game
        Player = self.Player

        if not Player.Powerup: return

        Direction = Player.Direction

        # Left by default
        BeamPos_x = Player.Position.x - 20
        BeamPos_y = Player.Position.y - 130

        if Direction == 0: # Right
            Local_Game.Screen.blit(Powerups["Laser_Eyes"]["Beam"], (BeamPos_x, BeamPos_y))

        if Direction == 1:
            BeamPos_x = Player.Position.x - 425
            Local_Game.Screen.blit(pygame.transform.flip(Powerups["Laser_Eyes"]["Beam"], True, False), (BeamPos_x, BeamPos_y))

        if Direction == 2: # Up
            BeamPos_x = Player.Position.x - 130
            BeamPos_y = Player.Position.y - 425
            Local_Game.Screen.blit(pygame.transform.rotate(Powerups["Laser_Eyes"]["Beam"], 90), (BeamPos_x, BeamPos_y))

        if Direction == 3: # Down
            BeamPos_x = Player.Position.x - 106
            BeamPos_y = Player.Position.y - 30
            Local_Game.Screen.blit(pygame.transform.rotate(Powerups["Laser_Eyes"]["Beam"], 270), (BeamPos_x, BeamPos_y))

    def establish_RAINBOW(self): # The speed powerup for the RAINBOW Powerup
        Local_Game = self.Local_Game
        Player = self.Player

        if not Player.Powerup:
            Player.Speed = 2
            return

        ColorTable = [
            "red",
            'blue',
            'green',
            'purple',
            'yellow',
            'orange'
        ]

        Color_Int = random.randint(0,len(ColorTable) - 1)

        self.Local_Game.Game_Color = ColorTable[Color_Int]

        self.Player.Speed = 3

    def establish_MR_BOND(self): # Changing the soundtrack for Mr. Bond & giving him a pass to give a gun to the Player
        Local_Game = self.Local_Game
        Player = self.Player

        if not Player.Powerup:
            if Player.Lives == 1:
                return self.thereasonforthenamemrbond()
            
            if hasattr(Player, "BONDDY"):
                Local_Game.SoundSystem.change_soundtrack("Lobby")
                if hasattr(Player, "CountFinale"):
                    del Player.CountFinale
                del Player.BONDDY
                del Player.Gun
            return
        
        self.Local_Game.Game_Color = "black"


        if not hasattr(Player, "BONDDY"):
            Local_Game.SoundSystem.change_soundtrack("bond")
            Player.BONDDY = True

    def thereasonforthenamemrbond(self): # The Passive for Mr. Bond when he's on 1 life left
        Local_Game = self.Local_Game
        Player = self.Player

        if Local_Game.Game_Over or Local_Game.Game_Won:
            if hasattr(Player, "CountFinale"):
                del Player.CountFinale
                del Player.BONDDY

            return
        
        Player.Powerup = False
        
        self.Local_Game.Game_Color = "black"

        if not hasattr(Player, "CountFinale"):
            Player.CountFinale = 0
            Local_Game.SoundSystem.change_soundtrack("jamesbond")

        Player.CountFinale += 1
        if Player.CountFinale <= 5:
            Player.Speed = 1

        if Player.CountFinale == 1000:
            Player.Speed += 1
            Player.Gun.Cooldown /= 2
        
        if Player.CountFinale == 1900:
            Player.Speed += 1
            Player.Gun.Cooldown /= 2

        Player.BONDDY = True

        detectionradius = pygame.rect.Rect([Player.Position.x, Player.Position.y, 10, 10])

        for _, Ghost in self.Local_Game.Ghosts.items():
            if detectionradius.colliderect(Ghost.rect):
                if Ghost.direction == 0:
                    Player.Direction = 1

                if Ghost.direction == 1:
                    Player.Direction = 0

                if Ghost.direction == 2:
                    Player.Direction = 3
                
                if Ghost.direction == 3:
                    Player.Direction = 2

        if Player.CountFinale >= 6000 and not Player.Powerup:
            Player.remove_life()

            if hasattr(Player, "CountFinale"):
                del Player.CountFinale

    
    def draw_MR_BOND(self):
        Local_Game = self.Local_Game
        Player = self.Player

        if not hasattr(Player, "BONDDY"): return

        Direction = Player.Direction

        # Left by default

        if Direction == 0: # Right
            Local_Game.Screen.blit(Powerups["MR_BOND"]["Gun"], (Player.Position.x, Player.Position.y))

        if Direction == 1:
            Local_Game.Screen.blit(pygame.transform.flip(Powerups["MR_BOND"]["Gun"], True, False), (Player.Position.x, Player.Position.y))

        if Direction == 2: # Up
            Local_Game.Screen.blit(pygame.transform.rotate(Powerups["MR_BOND"]["Gun"], 90), (Player.Position.x, Player.Position.y))

        if Direction == 3: # Down
            Local_Game.Screen.blit(pygame.transform.rotate(Powerups["MR_BOND"]["Gun"], 270), (Player.Position.x, Player.Position.y))

        Local_Game.Screen.blit(Powerups["MR_BOND"]["Logo"], (Player.Position.x * 0.05, Player.Position.y * 0.05))

        if not hasattr(Player, "Gun"):
            Player.Gun = Gun(Local_Game)
        
        if hasattr(Player, "CountFinale"):
            Local_Game.Screen.blit(Powerups["MR_BOND"]["Complete"], (Player.Position.x * 0.9, Player.Position.y * 0.9))
            Player.Gun.Cooldown = 75

        Player.Gun.fire()


    def run_Powerup(self):
        if not self.Enabled: return

        Local_Game = self.Local_Game
        Player = self.Player

        if hasattr(self, "establish_" + Player.PowerUpName): # Every frame, update establish if there's a function for that powerup
            getattr(self, "establish_" + Player.PowerUpName)()

        for GhostName, GhostData in Local_Game.Ghosts.items(): # Through all the ghosts
            # The Ghost is running away

            if "OnGhost" in Powerups[Player.PowerUpName]: # If the ghost's are affected by the powerup
                if hasattr(self, Player.PowerUpName): # IF there's a function for it
                    getattr(self, Player.PowerUpName)(GhostData)
                else:
                    getattr(self, "Default")(GhostData) # Otherwise just make it the default
        

