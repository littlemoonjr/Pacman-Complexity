import pygame
import modules.uihandler
from modules.uihandler import Button
from threading import Thread
import time
from pygame.math import Vector2

# All of the skins data within the shop & outside of the shop for later usage

Skins_Data = {
    "Default" : {

    },

    "cool-dude" : {
        "Cost" : 250
    },

    "mario" : {
        "Cost" : 1200,
        "Powerup": "RAINBOW"
    },

    "superman" : {
        "Cost" : 2500,
        "Powerup": "Laser_Eyes"
    },

    "mr-bond" : {
        "Cost" : 5000,
        "Powerup": "MR_BOND",
        "PowerupDuration" : 4200
    }
}




class Skins_System():
    def __init__(self, Local_Game):
        # Get the Game's Class
        self.Local_Game = Local_Game

        # Set up the loaded assets, currentplayerimage, & frame

        self.Loaded_Assets = {}
        self.CurrentPlayerImage = 0
        self.Frame = 0

        # Load the images for Equipped, Equip, & Buy

        self.EquippedImg = pygame.transform.scale(pygame.image.load('assets/ui/Equipped.png'), (200,50))
        self.EquipImg = pygame.transform.scale(pygame.image.load('assets/ui/Equip.png'), (200,50))
        self.BuyImg = pygame.transform.scale(pygame.image.load('assets/ui/Buy.png'), (200,50))

    def on_create(self):
        def thread():
            time.sleep(0.5)
            self.Local_Game.ButtonCD = False # Set it off after 0.5 seconds

        def exit_menu(): # On Button Press
            Thread(target=thread).start()

            self.Local_Game.ButtonCD = True # Change the global button's cooldown to on to prevent double clicking

            self.Local_Game.set_up_mainmenu() # Set up  the game's main menu

        # Set up the exit button to leave the skin menu
        self.Local_Game.Buttons["ExitButton"] = Button(50,750, 370, 75, pygame.image.load('assets/ui/Exit_Button.png'), exit_menu, imgoffset = (-16,-15))


        # In the skin's data, load the images
        for SkinName, SkinData in Skins_Data.items():
            if SkinName in self.Loaded_Assets: continue # To prevent overlap of loading the images

            # Set the loaded assets for SkinName

            self.Loaded_Assets[SkinName] = {}
            self.Loaded_Assets[SkinName]["Background"] = pygame.transform.scale(pygame.image.load(f'assets/player_images/{SkinName}/background.png'), (3376/8, 2600/8))
            self.Loaded_Assets[SkinName]["Player_Images"] = []

            for i in range(1, 5): # Get the Player Images for this skin and place it in Loaded_Assets
                Image = pygame.transform.scale(pygame.image.load(f'assets/player_images/{SkinName}/movement/{i}.png'), (150, 150))
                self.Loaded_Assets[SkinName]["Player_Images"].append(pygame.transform.flip(Image, True, False))

    def set_skinattribute(self, SkinName : str):
        if "Powerup" in Skins_Data[SkinName]: # If the skin has a powerup
            self.Local_Game.Player.PowerUpName = Skins_Data[SkinName]["Powerup"] # Set it as the player's current powerup

            if "PowerupDuration" in Skins_Data[SkinName]: # If the skin has a custom duration
                self.Local_Game.Player.Power_Counter_Duration = Skins_Data[SkinName]["PowerupDuration"] # Set it as such
            else: # Otherwise
                self.Local_Game.Player.Power_Counter_Duration = 600 # Set it to normal
        else: # Otherwise
            self.Local_Game.Player.PowerUpName = "Default" # Set it to default
            self.Local_Game.Player.Power_Counter_Duration = 600 # Set it to normal

    def equip_skin(self, SkinName : str):
        self.set_skinattribute(SkinName)
        
        self.Local_Game.Player.CurrentSkin = SkinName # Equip the skin as the player's currentskin


    def buy_skin(self, SkinName : str, SkinData : dict):
        Cost = 0 # In case the skin's free

        if "Cost" in SkinData: # If the skin has a cost
            Cost = SkinData["Cost"]

        if self.Local_Game.Player.Currency >= Cost: # Check if the player has enough money
            self.Local_Game.Player.Currency -= Cost # Remove how much it costs

            self.Local_Game.Player.Skins.append(SkinName) # add that skin to their inventory
            print(f"Added {SkinName} to Inventory")

    def unequip_skin(self):
        self.Local_Game.Player.CurrentSkin = "Default" # unequipping just means it's going back to default, could use either function in this case

    def Check(self, SkinName, SkinData):
        if self.Local_Game.Player.CurrentSkin == SkinName: # Currently equipped then unequip
            print(f"Unequip {SkinName}")
            self.unequip_skin()
        elif SkinName in self.Local_Game.Player.Skins: # It's already bought, but not equipped then.
            print(f"Equip {SkinName}")
            self.equip_skin(SkinName)
        else:
            if SkinName != "Default": # Buy the skin if you don't already have it, only exception is the default.
                print(f"Buy {SkinName}")
                self.buy_skin(SkinName, SkinData)
            else: # It's the default
                print(f"Equip {SkinName}")
                self.equip_skin(SkinName)
                
    def draw_skins(self):
        # Draw the skins like a list

        Position = Vector2(0,125) # The starting position
        CurrentCell = 0 # How many has been made in that row
        self.Frame += 1

        if self.Frame >= 12: # Updating the player image's position of every pacman in the shop
            self.Frame = 0
            self.CurrentPlayerImage += 1

            if self.CurrentPlayerImage > 3:
                self.CurrentPlayerImage = 1

        for SkinName, SkinData in Skins_Data.items(): # Through all the skins
            CurrentCell += 1 # Add the current cell it's at

            if CurrentCell >= 4: # if 3 cells are already in a row, go to a different line
                Position.y += 350
                Position.x = 0
                CurrentCell = 1 # Reset the current cell it's at to 1

            self.Local_Game.Screen.blit(self.Loaded_Assets[SkinName]["Background"], (Position.x, Position.y)) # Draw the skin's background
            self.Local_Game.Screen.blit(self.Loaded_Assets[SkinName]["Player_Images"][self.CurrentPlayerImage], (Position.x + 70, Position.y + 170)) # Draw the skin's image according to CurrentPlayerImage

            if not (SkinName + "_Button" in self.Local_Game.Buttons):
                # Create a button for the skin at the top right
                self.Local_Game.Buttons[SkinName + "_Button"] = Button(Position.x + 32 + 240, Position.y + 30, 370/2, 75/2, onclickFunction= self.Check, clickargs=(SkinName, SkinData))

            Position.x += 240 # Move the column's position by 240 for the next one

            if "Cost" in SkinData: # If the Skin cost's something
                Text = self.Local_Game.Large_Font.render(f'Cost: {SkinData["Cost"]}', True, 'white') 

                self.Local_Game.Screen.blit(Text, (Position.x - 25, Position.y - 35)) # Add the cost as a text

            if self.Local_Game.Player.CurrentSkin == SkinName: # If the skin is equipped
                self.Local_Game.Screen.blit(self.EquippedImg, (Position.x, Position.y)) # Then set the skin's button as the equipped image
            elif SkinName in self.Local_Game.Player.Skins: # otherwise if they already bought the skin but it's not equipped
                self.Local_Game.Screen.blit(self.EquipImg, (Position.x, Position.y)) # Then set the skin's button as equip image
            else: # Otherwise if the skin's not bought
                if SkinName != "Default": # If the skin is not the default
                    self.Local_Game.Screen.blit(self.BuyImg, (Position.x, Position.y)) # set the skin's button to buy
                else: # otherwise
                    self.Local_Game.Screen.blit(self.EquipImg, (Position.x, Position.y)) # set the skin's button to equip
    
    def skins_menu(self):
        mousePos = pygame.mouse.get_pos()
        mousePos_x, mousePos_y = mousePos # Get the mouse's position

        # Draw the skin menu's background and move it according to the mouse's position

        self.Local_Game.Screen.blit(self.Local_Game.Main_Menu["SkinsMenu"], (0 + (mousePos_x * 0.007), 0 + (mousePos_y * 0.007)))

        # Draw the skins

        self.draw_skins()

        

