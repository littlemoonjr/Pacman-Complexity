# Get the necessary libraries & modules

import copy
from board import boards
import pygame
import math, threading, time
from pygame.math import Vector2
import modules.powerups as powerups
import json

# Pre Initialize the Mixer/Sound to make sure the sound is completely initialized
# Initialized Pygame
# Initialized the Mixer/Sound afterwards

pygame.mixer.pre_init()
pygame.init()
pygame.mixer.init()


# IMPORT THE MAIN FRAMEWORK OF THE GAME, MOON FRAMEWORK (My creation)

import moonfw



# Set up the game class & Player Class

Local_Game = moonfw.Game()
Player = Local_Game.Player

counter = 0
Local_Game.Flicker = False
# R, L, U, D
# Set up Player's Powerup Stats & Eaten_Ghosts just in case if they were ever to be modified in another script, extra security.
Player.Powerup = False
Player.Power_Counter = 0
Local_Game.Eaten_Ghosts = [False, False, False, False]

def check_1(Ghost):
    if 340 < Ghost.x_pos < 560 and 340 < Ghost.y_pos < 500: # Check if Ghost is within boundaries
        Ghost.target = Vector2(400, 100) # go to corner
    else: # Otherwise just target the Player's Position
        Ghost.target = Player.Position

def get_targets():
    # Get All of the Ghosts

    blinky = Local_Game.Ghosts["Blinky"]
    inky = Local_Game.Ghosts["Inky"]
    clyde = Local_Game.Ghosts["Clyde"]
    pinky = Local_Game.Ghosts["Pinky"]

    # Checking if the player is on a BOUNDARY of under 450, and changing the coordinates to 900 or 0

    if Player.Position.x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if Player.Position.y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    
    # Return Target being "if there's nothing else" option, then return to 380, 400, the box

    return_target = Vector2(380, 400)

    if Player.Powerup and powerups.Powerups[Player.PowerUpName]["Danger"]: # When the player has a powerup..

        # RUN AWAYYYYY, unless your dead.

        if not blinky.dead and not Local_Game.Eaten_Ghosts[0]: # Check if Blinky is still alive and hasn't been eaten yet
            blinky.target = Vector2(runaway_x, runaway_y)
        elif not blinky.dead and Local_Game.Eaten_Ghosts[0]: # Check if Blinky still alive, but HAS already been eaten
            check_1(blinky)
        else: # Otherwise if they are just dead
            blinky.target = return_target # dude lemme go back to my box


        if not inky.dead and not Local_Game.Eaten_Ghosts[1]:
            inky.target = Vector2(runaway_x, Player.Position.y)
        elif not inky.dead and Local_Game.Eaten_Ghosts[1]:
            check_1(inky)
        else:# Otherwise if they are just dead
            inky.target = return_target # dude lemme go back to my box


        if not pinky.dead:
            pinky.target = Vector2(Player.Position.x, runaway_y)
        elif not pinky.dead and Local_Game.Eaten_Ghosts[2]:
            check_1(pinky)
        else:
            pinky.target = return_target # dude lemme go back to my box


        if not clyde.dead and not Local_Game.Eaten_Ghosts[3]:
            clyde.target = Vector2(450, 450)
        elif not clyde.dead and Local_Game.Eaten_Ghosts[3]:
            check_1(clyde)
        else:
            clyde.target = return_target # dude lemme go back to my box


    else:
        for _, Ghost in Local_Game.Ghosts.items():
            if not Ghost.dead:
                check_1(Ghost)
            else:
                Ghost.target = return_target # dude lemme go back to my box

def draw_game():
    Local_Game.Screen.fill('black')

    # Drawing all the assets in the game layer by layer

    Local_Game.draw_board()
    Player.draw_player(Local_Game.Screen, counter)
    Local_Game.draw_ghosts()
    Local_Game.draw_misc()
    Local_Game.draw_powerups()

def play_game():
    # Getting all the ghosts

    blinky = Local_Game.Ghosts["Blinky"]
    inky = Local_Game.Ghosts["Inky"]
    clyde = Local_Game.Ghosts["Clyde"]
    pinky = Local_Game.Ghosts["Pinky"]

    global counter

    # Change the sprite for the player by applying it every 20 frames or so as well as flickering the power up pellet
    
    if counter < 19:
        counter += 1 # Count up by 1 every frame
        if counter > 3:
            Local_Game.Flicker = False # If it's 3, then reset the Flicker
    else:
        counter = 0 # Restart all over again
        Local_Game.Flicker = True # Say that's it's flickered


    # Start acculumating for powerup & startup
    
    Local_Game.accumulate_powerup() 
    Local_Game.accumulate_startup()


    #Local_Game.Screen.fill('black')
    #Local_Game.draw_board()

    # Set the Player's Center Position

    Player.Center.x = int(Player.Position.x + 23)
    Player.Center.y = int(Player.Position.y + 24)

    
    # Since we already have the ghost's referenced, we are just manually changing the ghosts speeds.
    
    Local_Game.Game_Won = True
    
    for i in range(len(Local_Game.Level)):
        if 1 in Local_Game.Level[i] or 2 in Local_Game.Level[i]:
            Local_Game.Game_Won = False

    # If the game is won, but the currency wasn't given:

    if Local_Game.Game_Won and not Local_Game.CurrencyGiven:
        Local_Game.CurrencyGiven = True # Set that the currency was given

        Local_Game.Move_Entities = False # Stop moving the entities
        Local_Game.Startup_Counter = 0 # Set the startup counter to 0

        Local_Game.pause_game() # Pause the game

        Player.Currency += 100 * (Player.Score * 0.007) # Add the currency




    #Player.draw_player(Local_Game.Screen, counter)
    #Local_Game.draw_ghosts()
    
    blinky = Local_Game.Ghosts["Blinky"]
    inky = Local_Game.Ghosts["Inky"]
    clyde = Local_Game.Ghosts["Clyde"]
    pinky = Local_Game.Ghosts["Pinky"]
    
    #Local_Game.draw_misc()
    get_targets() # Gets all of the targets for the ghosts

    Local_Game.check_position() # Change the Player Turns Allowed by checking the grid

    if Local_Game.Move_Entities: # Check if the Player & Ghosts can move
        Player.move_player() # Move the Player
        Local_Game.move_ghosts() # Move the Ghosts

    Local_Game.check_collisions() # Check if the Player is colliding with a pellet
    Local_Game.Lives_Check() # Check the Player's Lives to change the color of the game board

    # add to if not Player.Powerup to check if eaten ghosts
    if not Player.Powerup: # IF THE PLAYER DOESN'T HAVE A POWERUP
        if (Player.Circle.colliderect(blinky.rect) and not blinky.dead) or \
                (Player.Circle.colliderect(inky.rect) and not inky.dead) or \
                (Player.Circle.colliderect(pinky.rect) and not pinky.dead) or \
                (Player.Circle.colliderect(clyde.rect) and not clyde.dead): # Check if the Player is colliding with any of the ghosts and the ghost is still alive
            if Player.Lives > 0:
                # Remove a life from the player and restart the game

                for _, Ghost in Local_Game.Ghosts.items():
                    x, y = Ghost.base_data["Position"] # Get the base position of the Ghost

                    Ghost.x_pos = x # Set the x position of the Ghost back to normal
                    Ghost.y_pos = y # Set the y position of the Ghost back to normal

                    Ghost.direction = Ghost.base_data["Direction"] # Set the Ghost's normal direction
                    Ghost.dead = False # Say that the Ghost isn't dead

                Player.remove_life() # Remove A Life from the Player
                Local_Game.Startup_Counter = 0 # Set the startup counter back to 0
               
                Player.Direction_Keybind = 0 # Set the player's keybind back to Right

                # Set all ghosts positions & directions to default
                # Set the ghost to not being dead

                # Say that the ghosts haven't already been eaten

                Local_Game.Eaten_Ghosts = [False, False, False, False]
            else: # The Player has no more lives
                Local_Game.game_over() # Game Over.

    # IF THE PLAYER HAS A POWERUP
    Local_Game.run_powerup() # Start the loop for running the power up
    
    Local_Game.get_pygame_events() # Check if the player is currently pressing anything

    for i in range(0, 4):
        if Player.Direction_Keybind == i and Player.Turns_Allowed[i]:
            Player.Direction = i


    # If the Player is in a Tunnel, or then teleport them accordingly

    if Player.Position.x > 900: 
        Player.Position.x = -47
    elif Player.Position.x < -50:
        Player.Position.x = 897



    # If the ghost is dead and in a box, then revive the ghost to get them ready to get out

    for _, Ghost in Local_Game.Ghosts.items():
        if Ghost.in_box and Ghost.dead:
            Ghost.dead = False


    pygame.display.flip() # Update the game display



while Local_Game.Running:
    Local_Game.Timer.tick(Local_Game.FPS) # 60 Frames a Second

    Local_Game.get_pygame_events()

    if Local_Game.Game_State == "Open-Game": # On the game's open
        Local_Game.open_game() # Fire the event

    if Local_Game.Game_State == "Main Menu": # On the game's menu
        Local_Game.main_menu() # Fire the event

    if Local_Game.Game_State == "Skins Menu": # On the game's skin shop
        Local_Game.skins_menu() # Fire the event

    if Local_Game.Game_State == "Game": # On the game's Game state
       draw_game() # draw the game
       threading.Thread(target=play_game).start() # Put the playing of the game on a seperate thread
    else: # Otherwise
        Local_Game.draw_currency() # Draw the game's currency

    Local_Game.run() # Run the game's "run" event

    pygame.display.flip() # Update the game's display

# Save the game's data with JSON Encoding into save_data.json file

with open("save_data.json", "w") as file:
    json.dump({"Skins" : Player.Skins, "Currency" : Player.Currency, "CurrentSkin" : Player.CurrentSkin, "VsWalter" : Player.VsWalter}, file, indent=4)
    
pygame.quit() # Stop pygame
