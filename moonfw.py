# Get every single module, or library needed

import pygame, os
import modules.player as player
import modules.ghost as ghost
import modules.sound as Sound
import modules.skinsMenu as SkinsMenu
import copy
import math
import threading, time
import modules.powerups as powerups
from modules.uihandler import Button

import random

from board import boards

# Set up the game's icon & caption

pygame.display.set_icon(pygame.image.load('logo.webp'))
pygame.display.set_caption("Complexity | PACMAN")


PI = math.pi # get PI for circles

class Game:
    def __init__(self):
        # Set up the Screen's Size
        self.Screen_Size = {"Width" : 900, "Height" : 950}
        self.Screen = pygame.display.set_mode([900, 950])

        # Set up the game's Timer, the amount of FPS, the game not being paused, and the currency for winning not being given.

        self.Timer = pygame.time.Clock()
        self.FPS = 60
        self.Pause = False
        self.CurrencyGiven = False

        # Set up the fonts for the game & start the PLAYER class

        self.Font = pygame.font.Font('assets/fonts/Lumiare.otf', 20)
        self.Large_Font = pygame.font.Font('assets/fonts/Lumiare.otf', 50)
        self.Player = player.Player()

        # Set the game's color to blue, and having a stop live check for changing the game board's colors to False
       
        self.Game_Color = 'blue'
        self.Stop_Live_Check = False

        # If the player's image needs to currently change, and if the cursor is hovering over anything being false at the moment

        self.Flicker = False
        self.Cursor_Hover = False

        # Setting the game's state to currently opening the game, initializing the sound system, skins system and powerup system

        self.Game_State = "Open-Game"
        self.SoundSystem = Sound.SoundSystem()
        self.SkinsSystem = SkinsMenu.Skins_System(self)
        self.PowerupSystem = powerups.PowerupSystem(self)

        # Set the current skin's attribute onto the player

        self.SkinsSystem.set_skinattribute(self.Player.CurrentSkin)

        #  Set the game being won or lost to False, & Eaten Ghosts being all False

        self.Game_Over = False
        self.Game_Won = False
        self.Eaten_Ghosts = [False, False, False, False]

        # Set the startup counter to 0, the game running to true, and generally setting up lists for the game

        self.Startup_Counter = 0

        self.Running = True
        self.Move_Entities = False
        self.ButtonCD = False

        self.Main_Menu = {}
        self.Buttons = {}
        self.Animations_UI = {}
        self.Ghosts = {}

        self.Images = {

        }

        # Load in  the Go & Ready Images

        self.Images["Go"] = pygame.image.load(f'assets/misc/go.png')
        self.Images["Ready"] = pygame.image.load(f'assets/misc/ready.png')

        # Set the Ready & Go's Status to nothing

        self.Ready_Go_Status = ""

        # Load in all the menu background's and place them into the Main_Menu

        self.Main_Menu["Main_Image"] = pygame.image.load(f'assets/misc/mr bond main menu.png')
        self.Main_Menu["Exit_Image"] = pygame.image.load(f'assets/misc/exit_menu.png')
        self.Main_Menu["Skins_Image"] = pygame.image.load(f'assets/misc/skins_menu.png')
        self.Main_Menu["SkinsMenu"] = pygame.image.load(f'assets/misc/skins_menu2.png')
        self.Main_Menu["Walter"] = pygame.image.load(f'assets/misc/Walter White.png') # Easter Egg
        self.Main_Menu["wow"] = pygame.image.load(f'assets/misc/wow.jpg')

        # Set the menu's current image to be the main menu's image

        self.Main_Menu["Image"] = "Main_Image"

        # Set up the variables relative to it

        self.Main_Menu["Main_Button_Hovering"] = False
        self.Main_Menu["Override_Button_Hover"] = False

        self.ThreadStart = False

        # Set up the images for the cursor

        self.Pointer_Cursor = pygame.transform.scale(pygame.image.load(f'assets/cursor/cursor_1.png'),(64,64))

        Cursor_Image = pygame.transform.scale(pygame.image.load(f'assets/cursor/cursor_1.png'),(64,64))
        Cursor_2_Image = pygame.transform.scale(pygame.image.load(f'assets/cursor/cursor_2.png'),(64,64))

        # Set the images onto the cursor

        self.Pointer_Cursor = pygame.cursors.Cursor((Cursor_Image.get_width() // 2, Cursor_Image.get_height() // 2), Cursor_Image)
        self.Click_Cursor = pygame.cursors.Cursor((Cursor_2_Image.get_width() // 2, Cursor_2_Image.get_height() // 2), Cursor_2_Image)
        # Set the cursor
        pygame.mouse.set_cursor(self.Pointer_Cursor)

        self.set_level() # Set up the game's current level
        

    def open_game(self):
        # When the game is first opened

        def thread():
            time.sleep(4)

            self.set_up_mainmenu()
        # All of the quotes that can randomly appear

        quotes = [
            "a truly complex game",
            "do bagels taste good",
            "mr.bond vs superman",
            "banana",
            "the fastest guy alive",
            "there's pacman.. but it looks kinda complex idk",
            "so tuff bro",
            "prince lowkey: ",
            "do we start now.. or?"

        ]

        if not self.ThreadStart:
            # If the thread hasn't already started

            threading.Thread(target=thread).start() # After 4 seconds, start the game

            # Pick a random quote

            num = random.randint(0, len(quotes) - 1)
            Quote = quotes[num]
            self.Quote = quotes[num]

        self.ThreadStart = True # The thread started

        self.Screen.blit(self.Main_Menu["wow"], (450, 400)) # set up the minion image
        self.WalterClyde = False

        text = self.Large_Font.render(self.Quote, True, 'white')
        self.Screen.blit(text, (10, 600)) # draw the random quote

    def play_sound(self, sound_name):
        self.SoundSystem.play_sound(sound_name) # Fire the Sound's System Play Sound and send the Sound's Name

    def pause_game(self):
        self.Pause = True # Set Pause to True
        self.Past_Startup = self.Startup_Counter # get the past startup value
        self.Startup_Counter = 0 # set the current startup as 0
    
    def unpause_game(self):
        self.Pause = False # Set Pause to False

        if hasattr(self, "Past_Startup"): # If there is a Past Startup
            self.Startup_Counter = self.Past_Startup # Set it to the current startup
        else: # Otherwise
            self.Startup_Counter = 0 # Set it to 0

    def create_ghosts(self):
        # Create All of the Ghosts (Blinky, Inky, Pinky, Clyde)

        self.Ghosts["Blinky"] = ghost.Ghost("Blinky", self)
        self.Ghosts["Inky"] = ghost.Ghost("Inky", self)
        self.Ghosts["Pinky"] = ghost.Ghost("Pinky", self)
        self.Ghosts["Clyde"] = ghost.Ghost("Clyde", self)

    def draw_ghosts(self):
        # Draw every single ghost by iterating through each one

        for GhostName, Ghost in self.Ghosts.items():
            Ghost : ghost.Ghost

            Ghost.draw(self)

    def move_ghosts(self):
        for GhostName, Ghost in self.Ghosts.items():
            Ghost : ghost.Ghost

            Speed = 2

            if self.Player.Powerup:# When the player has a power up

                # Set the ghosts speeds to half

                Speed = 1
            else:# When the Player doesn't have a powerup

                # Set the ghosts speeds back to normal

                Speed = 2
            
            if self.Eaten_Ghosts[Ghost.id]: # If the ghost has been eaten
                Speed = 2

            if Ghost.dead: # If the ghost is dead
                Speed = 4
            
            if self.WalterClyde: # If it's the walter event
                Speed = 3


            Ghost.speed = Speed # Set the ghost's speed to the speeds found

            # Move the ghost

            self.move_ghost(Ghost)

    def move_ghost(self, Ghost : ghost.Ghost):
        # If there is a function within Ghosts to move the ghost itself by checking with it's name, then print if it's not there

        # If there is a function however, but it doesn't work, then print that we are confused

        FunctionName = "move_" + Ghost.Name

        if not hasattr(Ghost, FunctionName): return print("Ghost has no attribute to moving, uh oh")
        if not callable(getattr(Ghost, FunctionName)): return print("Huh?")

        # Update the Ghost's center position

        Ghost.center_x = Ghost.x_pos + 22
        Ghost.center_y = Ghost.y_pos + 22

        # Update the Ghost's collisions

        Ghost.check_collisions(self)

        if not Ghost.dead and not Ghost.in_box: # If the ghost isn't dead, nor in the box
            getattr(Ghost, FunctionName)() # Move the ghost normally
        else: # Otherwise
            Ghost.move_Clyde() # Move the ghost like Clyde

    def get_pygame_events(self):
        # Get all the events within pygame, and set up the event listener
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If the game is quit
                self.Running = False # Stop running the game

            self.event_listener(event) # Fire event listener


    def accumulate_startup(self):
        if self.Pause: return # If the game is paused, don't continue with this.

        self.get_pygame_events() # get the game's current events

        if self.Startup_Counter < 180 and not self.Game_Over and not self.Game_Won: # If it's been less than 180 frames for startup & the game is in normal state then don't move
            self.Move_Entities = False # Don't move ghosts & player
            self.Startup_Counter += 1 # Add to startup counter
        else: # Otherwise
            self.Move_Entities = True # Move the ghosts & player

    def draw_ready_go(self):
        # Timer function to clear the "Go" text after 1.5 seconds

        def thread():
            time.sleep(1.5)

            self.Ready_Go_Status = ""
        
        # Draw the "Ready" or "Go" image to the screen if active
        if self.Ready_Go_Status == "Go" or self.Ready_Go_Status == "Ready":
            self.Screen.blit(self.Images[self.Ready_Go_Status], (450, 475))
        
        # Trigger "Ready" state and sound at frame 30
        if self.Startup_Counter == 30:
            self.Ready_Go_Status = "Ready"
            self.play_sound("ready")

        # Trigger "Go" state, play sound, and start the clearance timer at frame 179, directly before startup

        if self.Startup_Counter == 179:
            self.Ready_Go_Status = "Go" 
            self.play_sound("go")

            threading.Thread(target=thread).start()


    def accumulate_powerup(self):
        Player = self.Player # Get the Player

        # If power-up is active and time remains, increment the counter
        if Player.Powerup and Player.Power_Counter < Player.Power_Counter_Duration:
            Player.Power_Counter += 1
        elif Player.Powerup and Player.Power_Counter >= Player.Power_Counter_Duration:
            # If power-up time runs out, reset counter, disable power-up, and reset eaten ghosts
            Player.Power_Counter = 0
            Player.Powerup = False
            self.Eaten_Ghosts = [False, False, False, False]

    def clean_up_mainmenu(self):
        # Set all the buttons to be gone

        self.Buttons = {}

    def set_up_mainmenu(self):
        # Reset game states and load lobby music

        self.Main_Menu["Override_Button_Hover"] = False

        self.clean_up_mainmenu()
        self.unpause_game()
        self.Player.Score = 0
        self.SoundSystem.change_soundtrack("Lobby")
        self.WalterClyde = False

        # Background timer to close the application after the exit "cutscene"
        def stop_running():
            time.sleep(8)

            self.Running = False

        # plays a fantastic cutscene
        def exitgame():
            if self.ButtonCD: return # If the game's buttons are on cooldown, stop.
            
            self.pause_game() # Pause the game

            self.play_sound("Please Don't Leave") # Announcer begs

            self.SoundSystem.change_soundtrack("Sad") # Change the soundtrack to sad
            self.Main_Menu["Override_Button_Hover"] = True
            self.Main_Menu["Image"] = "Exit_Image" # change it permanently to exit image
            threading.Thread(target=stop_running).start()

        # Hover effect: Updates menu background to Exit theme
        def set_image():
            if self.Pause: return # If the game is paused, stop

            self.Main_Menu["Image"] = "Exit_Image"
            self.Main_Menu["Main_Button_Hovering"] = True

        # Hover effect: Updates menu background to Skin theme

        def set_image_2():
            if self.Pause: return # If the game is paused, stop

            self.Main_Menu["Image"] = "Skins_Image"
            self.Main_Menu["Main_Button_Hovering"] = True

        # Hover effect: Updates menu background to Walter White theme

        def set_image_3():
            if self.Pause: return # If the game is paused, stop

            self.Main_Menu["Image"] = "Walter"
            self.Main_Menu["Main_Button_Hovering"] = True

        # Initializes and launches a new game

        def play_game():
            if self.ButtonCD: return # If the buttons are on cooldown, stop
            if self.Pause: return # If the game is paused, stop

            # Setup map color and player settings

            self.Player.Speed = 2
            self.Game_Color = 'blue'
            self.play_sound("Play_Announcer")
            self.set_level()

            # Position player at the starting tile

            self.Player.Position.x = 450
            self.Player.Powerup = False
            self.Player.Power_Counter = 0
            self.Player.Position.y = 663
            
            # Clear menu elements, reset intro counters, and spawn actors

            self.clean_up_mainmenu()
            self.Startup_Counter = 0 # Reset variable
        
            self.Game_State = "Game" # Set the game's state to play
            self.CurrencyGiven = False # Reset variable

            self.Player.setup_PlayerImages() # Set's up the player's current images
            self.create_ghosts() # Creates the ghosts

        # Opens the skins menu

        def skins_menu():
            if self.ButtonCD: return # If the buttons are on cooldown, stop
            if self.Pause: return # If the game is paused, stop

            self.play_sound("Skins_Announcer")
            self.set_up_skins()

        def easter_egg():
            if self.ButtonCD: return # If the buttons are on cooldown, stop
            if self.Pause: return # If the game is paused, stop

            self.SoundSystem.change_soundtrack("Walter")
            self.WalterClyde = True # starting the event
            self.Main_Menu["Override_Button_Hover"] = True
            self.Main_Menu["Image"] = "Walter" # change it permanently to exit image

        # Load specific UI textures for the Walter easter egg/mode

        self.VsWalter = pygame.image.load('assets/ui/theCook.png')
        self.VsWalter_Bought = pygame.image.load('assets/ui/theCook_Bought.png')


        # Set up all of the buttons for the main menu
        
        self.Buttons["VsWalter"] = Button(500,850, 370, 75, onclickFunction=easter_egg, hoverFunction = set_image_3)
        self.Buttons["ExitButton"] = Button(50,750, 370, 75, pygame.image.load('assets/ui/Exit_Button.png'), exitgame, imgoffset = (-16,-15), hoverFunction = set_image)
        self.Buttons["SkinsButton"] = Button(50,650, 370, 75, pygame.image.load('assets/ui/Skins_Button.png'), imgoffset = (-16,-15), hoverFunction = set_image_2, onclickFunction = skins_menu)
        self.Buttons["PlayButton"] = Button(50,550, 370, 75, pygame.image.load('assets/ui/Play_Button.png'), imgoffset = (-16,-15), onclickFunction = play_game)

        # Set up the game's logo & set the game's state to the main menu

        self.Animations_UI["TitleLogo"] = pygame.transform.scale(pygame.image.load(f'assets/ui/Title Logo.png'), (420*1.2, 240*1.2))

        self.Game_State = "Main Menu"

    def set_up_skins(self):
        self.clean_up_mainmenu() # clean up the main menu before starting
        self.SoundSystem.change_soundtrack("Skins") # Change the soundtrack to the skins menu soundtrack

        self.Game_State = "Skins Menu" # Set the game's state to the skins menu
        self.SkinsSystem.on_create() # start up the skins system to create the skins menu

    def main_menu(self):
        mousePos = pygame.mouse.get_pos()
        mousePos_x, mousePos_y = mousePos # Get the Mouse's current position

        # If nothing is currently being hovered
        if not self.Main_Menu["Main_Button_Hovering"] and not self.Main_Menu["Override_Button_Hover"]:
            self.Main_Menu["Image"] = "Main_Image" # Then it's just the main menu's normal image


        # Move the Main Menu's Background Image to the current image that is available & draw it
        self.Screen.blit(self.Main_Menu[self.Main_Menu["Image"]], (0 + (mousePos_x * 0.007), 0 + (mousePos_y * 0.007)))

        # 16:9 aspect ratio

        # Set up the game's title logo

        self.Screen.blit(self.Animations_UI["TitleLogo"], (50 + (mousePos_x * 0.025), 50 + (mousePos_y * 0.025)))

        if "VsWalter" in self.Buttons: # If Vs Walter is a button right now
            # If they already have Vs Walter, change the image accordingly to having it vs not

            if not self.Player.VsWalter:
                self.Screen.blit(self.VsWalter, ((self.Buttons["VsWalter"].x-16)  + (mousePos_x * 0.01), (self.Buttons["VsWalter"].y-15) + (mousePos_y * 0.01)))
            else:
                self.Screen.blit(self.VsWalter_Bought, ((self.Buttons["VsWalter"].x-16)  + (mousePos_x * 0.01), (self.Buttons["VsWalter"].y-15) + (mousePos_y * 0.01)))

        self.Main_Menu["Main_Button_Hovering"] = False

    def skins_menu(self):
        self.SkinsSystem.skins_menu() # Open the skin's menu

    def set_screen(self, Width : int = 900, Height : int = 950) -> None:
        # Change the screen's size to the new width & height

        self.Screen = pygame.display.set_mode([Width, Height]) # Change the display
        self.Screen_Size = {"Width" : Width, "Height" : Height} # Change that across the size dictonary




    def set_level(self):
        # set the game's level to a copy of boards, the actual game's level grid

        self.Level = copy.deepcopy(boards)

    def game_over(self):
        if not self.Game_Over: # If this hasn't yet happened: 
            self.play_sound("game-over") # Play the game over sound
            self.Player.Currency += 20 * (self.Player.Score * 0.003) # Add to the player's currency

        self.Game_Over = True # The game is over

        self.Move_Entities = False # Stop moving the entities
        self.Startup_Counter = 0 # Reset the startup counter
        self.pause_game() # Pause the game




    def draw_misc(self):
        # Render and display the current score UI

        self.score_text = self.Font.render(f'Score: {self.Player.Score}', True, 'white')
        self.Screen.blit(self.score_text, (10, 920))

        # Handle drawing the "Ready" and "Go" text states

        self.draw_ready_go() # Start up ready go


        

        if self.Player.Powerup: # If the player is currently powered up
            pygame.draw.circle(self.Screen, 'blue', (140, 930), 15) # Change the drawn circle on the bottom left for power up representation
        else: # Otherwise
            self.Stop_Live_Check = False # Do a live check
        for i in range(self.Player.Lives): # Iterate and draw all the player's lives
            self.Screen.blit(pygame.transform.scale(self.Player.Player_Images[0], (30, 30)), (650 + i * 40, 915))

        if self.Game_Over:
            # Draw red and black layered background boxes for the pop-up menu
            pygame.draw.rect(self.Screen, 'red', [50, 200, 800, 300],0, 10)
            pygame.draw.rect(self.Screen, 'black', [70, 220, 760, 260], 0, 10)

            # Display defeat message and instructions

            gameover_text = self.Font.render('You lost.. Space to go back.', True, 'red')

            self.Screen.blit(gameover_text, (100, 300))

            # Display coin reward based on final score

            text_2 = self.Font.render(f'You were given +{round(20 * (self.Player.Score * 0.003),2)} coins for your troubles..', True, 'green')

            self.Screen.blit(text_2, (100, 400))

        if self.Game_Won:
            # Draw green and black layered background boxes for the pop-up menu
            pygame.draw.rect(self.Screen, 'green', [50, 200, 800, 300],0, 10)
            pygame.draw.rect(self.Screen, 'black', [70, 220, 760, 260], 0, 10)

            # Display victory message and instructions

            gameover_text = self.Font.render('Victory.. Space to go back!', True, 'green')

            self.Screen.blit(gameover_text, (100, 300))

            # Display a more coin reward for winning

            text_2 = self.Font.render(f'You were given +{round(100 * (self.Player.Score * 0.007),2)} coins for your troubles!', True, 'green')

            self.Screen.blit(text_2, (100, 400))

            




    def check_collisions(self):
        # Calculate tile dimensions based on screen size

        num1 = (self.Screen_Size["Height"] - 50) // 32
        num2 = self.Screen_Size["Width"] // 30

        # Only check collisions if the player is within the main board boundaries (not in side tunnels)

        if 0 < self.Player.Position.x < 870:
            # Normal Pellet Collision

            if self.Level[int(self.Player.Center.y) // num1][int(self.Player.Center.x) // num2] == 1:
                self.Level[int(self.Player.Center.y) // num1][int(self.Player.Center.x) // num2] = 0 # Delete the pellet
                self.Player.addScore(10) # Add Score by 10


            # Power Pellet Collision

            if self.Level[int(self.Player.Center.y) // num1][int(self.Player.Center.x) // num2] == 2:
                self.Level[int(self.Player.Center.y) // num1][int(self.Player.Center.x) // num2] = 0 # Delete the pellet
                self.Player.addScore(50) # Add Score by 50




                self.Player.Powerup = True # Enable Powerup
                self.Player.Power_Counter = 0 # Reset Player Power Counter
                self.Eaten_Ghosts = [False, False, False, False] # Set Eaten Ghosts to not eaten yet
        return
   
   
    def draw_board(self):
        # Calculate tile dimensions based on screen size

        num1 = ((self.Screen_Size["Height"] - 50) // 32)
        num2 = (self.Screen_Size["Width"] // 30)

        # Loop through rows (i) and columns (j) of the map grid

        for i in range(len(self.Level)):
            for j in range(len(self.Level[i])):
                # 1: Normal pellet (small circle)

                if self.Level[i][j] == 1:
                    pygame.draw.circle(self.Screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
                
                # 2: Power pellet

                if self.Level[i][j] == 2 and not self.Flicker:
                    pygame.draw.circle(self.Screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
                
                # 3: Vertical wall line

                if self.Level[i][j] == 3:
                    pygame.draw.line(self.Screen, self.Game_Color, (j * num2 + (0.5 * num2), i * num1),
                                    (j * num2 + (0.5 * num2), i * num1 + num1), 3)
                
                # 4: Horizontal wall line

                if self.Level[i][j] == 4:
                    pygame.draw.line(self.Screen, self.Game_Color, (j * num2, i * num1 + (0.5 * num1)),
                                    (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
                
                # 5: Top-Left wall corner (arc)

                if self.Level[i][j] == 5:
                    pygame.draw.arc(self.Screen, self.Game_Color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                    0, PI / 2, 3)
                    
                # 6: Top-Right wall corner (arc)

                if self.Level[i][j] == 6:
                    pygame.draw.arc(self.Screen, self.Game_Color,
                                    [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
                    
                # 7: Bottom-Right wall corner (arc)

                if self.Level[i][j] == 7:
                    pygame.draw.arc(self.Screen, self.Game_Color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                    3 * PI / 2, 3)
                
                # 8: Bottom-Left wall corner (arc)

                if self.Level[i][j] == 8:
                    pygame.draw.arc(self.Screen, self.Game_Color,
                                    [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                    2 * PI, 3)
                
                # 9: Ghost house gate

                if self.Level[i][j] == 9:
                    pygame.draw.line(self.Screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                    (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
                    
    def Lives_Check(self):
        if self.Stop_Live_Check: return # If the game doesn't want us to change colors according to the lives, then stop.

        # Depending on which live the player is currently at, change accordingly

        Colors = {
            1: 'red',
            2: 'orange'

            }
        
        lowest = 10 # base value
        color = 'blue' # base color
        
        for LivesNeeded, Color in Colors.items(): # through all of the colors & lives needed for them
            if self.Player.Lives > LivesNeeded: continue # If the Player has more lives than the color's amount, then continue.


            if lowest >= LivesNeeded: # If the Lives is lower than the lowest
                lowest = LivesNeeded # set that as the lowest
                color = Color # set that as the concurrent color

        self.Game_Color = color # set that as the game's color


                   
   
   
    def check_position(self):
        # Set up the Height of the game according to grid size
        # Set the player's turns as all false

        turns = [False, False, False, False]
        num1 = (self.Screen_Size["Height"] - 50) // 32
        num2 = (self.Screen_Size["Width"] // 30)
        num3 = 15

        # check collisions based on center x and center y of player +/- fudge number


        # Get the Player's Center Position

        centerx = int(self.Player.Center.x)
        centery = int(self.Player.Center.y)
        
        if centerx // 30 < 29: # If they aren't at the edge of the map in terms of the grid
            if self.Player.Direction == 0: # If the player's current direction is RIGHT
                if self.Level[centery // num1][(centerx - num3) // num2] < 3: # If the ghost is concurrently colliding with any blocks left
                    # Set the LEFT Turn to be allowed
                    turns[1] = True
            if self.Player.Direction == 1: # If the player's current direction is LEFT
                if self.Level[centery // num1][(centerx + num3) // num2] < 3: # If the ghost is concurrently colliding with any blocks right
                    # Set the RIGHT Turn to be allowed
                    turns[0] = True

            if self.Player.Direction == 2: # If the player's current direction is UP
                if self.Level[(centery + num3) // num1][centerx // num2] < 3: # If the ghost is concurrently colliding with any blocks above
                    # Set the DOWN Turn to be allowed
                    turns[3] = True
            if self.Player.Direction == 3: # If the player's current direction is DOWN
                if self.Level[(centery - num3) // num1][centerx // num2] < 3: # If the ghost is concurrently colliding with any blocks below
                    # Set the UP Turn to be allowed
                    turns[2] = True




            if self.Player.Direction == 2 or self.Player.Direction == 3: # If the player's current direction is UP or DOWN
                if 12 <= centerx % num2 <= 18: # Check if the player is centered horizontally within the tile path
                    if self.Level[(centery + num3) // num1][centerx // num2] < 3: # Check tile BELOW and if they can walk 3 blocks from below
                        # Set the DOWN Turn to be allowed
                        turns[3] = True
                    if self.Level[(centery - num3) // num1][centerx // num2] < 3: # Check tile ABOVE and if they can walk 3 blocks from above
                        # Set the UP Turn to be allowed
                        turns[2] = True
                if 12 <= centery % num1 <= 18:
                    if self.Level[centery // num1][(centerx - num2) // num2] < 3:
                        # Set the LEFT Turn to be allowed
                        turns[1] = True
                    if self.Level[centery // num1][(centerx + num2) // num2] < 3:
                        # Set the RIGHT Turn to be allowed
                        turns[0] = True
            if self.Player.Direction == 0 or self.Player.Direction == 1: # If the player's current direction is RIGHT or LEFT
                if 12 <= centerx % num2 <= 18: # Check if the player is centered vertically within the tile path
                    if self.Level[(centery + num1) // num1][centerx // num2] < 3: # Check tile to the LEFT and if they can walk 3 blocks from left
                        # Set the DOWN Turn to be allowed
                        turns[3] = True
                    if self.Level[(centery - num1) // num1][centerx // num2] < 3: # Check tile to the RIGHT and if they can walk 3 blocks from right
                        # Set the UP Turn to be allowed
                        turns[2] = True
                if 12 <= centery % num1 <= 18: # Check if the player is centered vertically within the tile path
                    if self.Level[centery // num1][(centerx - num3) // num2] < 3: # Check tile to the LEFT using a targeted look-ahead offset
                        # Set the LEFT Turn to be allowed
                        turns[1] = True
                    if self.Level[centery // num1][(centerx + num3) // num2] < 3: # Check tile to the RIGHT using a targeted look-ahead offset
                        # Set the RIGHT Turn to be allowed
                        turns[0] = True
        else:
            # If not affected by grid's rules then set right & left turns to be allowed
            turns[0] = True
            turns[1] = True



        # Set the turns set up as the actual turns allowed for the Player
        self.Player.Turns_Allowed = turns

    def ripple(self):
        Mouse_Position = pygame.mouse.get_pos()

        # was suppose to be a ripple effect for clicking but I didn't want to do it after all

    def return_to_main(self):
        # Set that the game hasn't been won or lost

        self.Game_Over = False
        self.Game_Won = False

        # Return the player's lives back to normal

        self.Player.Lives = 3

        self.set_up_mainmenu() # Set up the main menu again

    def draw_currency(self):
        # Draw the coins of the Player's Currency

        # Draw it's shadow

        Text = self.Large_Font.render(f'Coins: {round(self.Player.Currency, 2)}', True, 'black') 
        self.Screen.blit(Text, (0,0))

        Text = self.Large_Font.render(f'Coins: {round(self.Player.Currency, 2)}', True, 'orange') # Render the coin's text & round it
        self.Screen.blit(Text, (3,3)) # Draw the coins


    def event_listener(self, event : pygame.event):
        if self.Game_Over or self.Game_Won: # If the game is won or is over
            if not self.Pause: # If the game isn't already paused
                self.pause_game() # Pause the game
        
        if self.Game_State == "Game": # If the game's current state is the game
            if event.type == pygame.KEYDOWN: # Then if the key is down

                # If it detects any directional keys, change the directional keybind for player to that direction

                if event.key == self.Player.Keybinds["Right"]:
                    self.Player.Direction_Keybind = 0

                if event.key == self.Player.Keybinds["Left"]:
                    self.Player.Direction_Keybind = 1

                if event.key == self.Player.Keybinds["Up"]:
                    self.Player.Direction_Keybind = 2

                if event.key == self.Player.Keybinds["Down"]:
                    self.Player.Direction_Keybind = 3

                # If the player presses space and the game is already won or lost

                if event.key == pygame.K_SPACE and (self.Game_Over or self.Game_Won):
                    self.return_to_main() # Then go back to the main menu
            
            if event.type == pygame.KEYUP: # Then if the key is up
                # Set that key to the direction derative from directional key if it's the key from before

                if event.key == self.Player.Keybinds["Right"] and self.Player.Direction_Keybind == 0:
                    self.Player.Direction_Keybind = self.Player.Direction
                if event.key == self.Player.Keybinds["Left"] and self.Player.Direction_Keybind == 1:
                    self.Player.Direction_Keybind = self.Player.Direction
                if event.key == self.Player.Keybinds["Up"] and self.Player.Direction_Keybind == 2:
                    self.Player.Direction_Keybind = self.Player.Direction
                if event.key == self.Player.Keybinds["Down"] and self.Player.Direction_Keybind == 3:
                    self.Player.Direction_Keybind = self.Player.Direction

    def draw_powerups(self):
        if hasattr(self.PowerupSystem, "draw_" + self.Player.PowerUpName): # If the power system has a draw event for that powerup
                getattr(self.PowerupSystem, "draw_" + self.Player.PowerUpName)() # Fire the draw event


    def run_powerup(self):
        self.PowerupSystem.run_Powerup() # Use PowerSystem to set up "Run_PowerUp"

        Player = self.Player # Get the player

        for GhostName, GhostData in self.Ghosts.items():
            # The Ghost is still alive

            if Player.Powerup and Player.Circle.colliderect(GhostData.rect) and self.Eaten_Ghosts[GhostData.id] and not GhostData.dead:
                if Player.Lives > 0:
                    # Remove a life from the player and restart the game

                    for _, Ghost in self.Ghosts.items():
                        x, y = Ghost.base_data["Position"] # Get the base position of the Ghost

                        Ghost.x_pos = x # Set the x position of the Ghost back to normal
                        Ghost.y_pos = y # Set the y position of the Ghost back to normal

                        Ghost.direction = Ghost.base_data["Direction"] # Set the Ghost's normal direction
                        Ghost.dead = False # Say that the Ghost isn't dead

                    Player.remove_life() # Remove A Life from the Player
                    self.Startup_Counter = 0 # Set the startup counter back to 0
                    # Set all ghosts positions & directions to default
                    # Set the ghost to not being dead
                    
                    self.Eaten_Ghosts = [False, False, False, False]
                else:
                    self.game_over()
                
            

    def run(self):
        self.Cursor_Hover = False

        # Get all the current buttons in the game

        for _, btn in self.Buttons.items():
            btn.process(self)

        # If the Mouse is currently hovering over a Button then change it's cursor accordingly

        if self.Cursor_Hover:
            pygame.mouse.set_cursor(self.Click_Cursor)
        else:
            pygame.mouse.set_cursor(self.Pointer_Cursor)


    