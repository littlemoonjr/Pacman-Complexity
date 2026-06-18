import pygame

class SoundSystem:
    def __init__(self):
        # Set up the sound's library and use pygame.mixer to get every single sound and place them into here manually

        self.SoundLibrary = {
            "Play_Announcer" : pygame.mixer.Sound("audio/Play_Announcer.mp3"),
            "Please Don't Leave" : pygame.mixer.Sound("audio/Don_t_Leave.mp3"),
            "Skins_Announcer" : pygame.mixer.Sound("audio/Skins_Announcer.mp3"),
            "go" : pygame.mixer.Sound("audio/go_Announcer.mp3"),
            "ready" : pygame.mixer.Sound("audio/ready_Announcer.mp3"),
            "game-over" : pygame.mixer.Sound("audio/pacman-die.mp3"),
            "click" : pygame.mixer.Sound("audio/mouseclick.mp3"),
            "shot" : pygame.mixer.Sound("audio/shot.mp3"),
        }

        # Set up the soundtrack's library and use pygame.mixer to get every single soundtrack and place them into here manually

        self.SoundtrackLibrary = {
            "Lobby" : pygame.mixer.Sound("audio/Lobby.mp3"),
            "Sad" : pygame.mixer.Sound("audio/pretty_sad.mp3"),
            "Skins" : pygame.mixer.Sound("audio/Skins_Soundtrack.mp3"),
            "bond" : pygame.mixer.Sound("audio/mrbondtheme.mp3"),
            "jamesbond" : pygame.mixer.Sound("audio/jamesbond.mp3"),
            "Walter" : pygame.mixer.Sound("audio/breakingbad.mp3"),
        }

        self.MainSoundTrack = None # Set the MainSoundTrack to nothing so we could place in it later and set up the variable

    def play_sound(self, sound_name):
        if sound_name in self.SoundLibrary: # If the sound is in the library
            self.SoundLibrary[sound_name].play() # Play the sound from the library
        else:
            print(f"Sound '{sound_name}' not found!") # In case there is ever a mistake, print that the sound isn't there.

    def change_soundtrack(self, soundtrack_name):
        if soundtrack_name in self.SoundtrackLibrary: # If the soundtrack is in the library
            if self.MainSoundTrack != None: # If MainSoundTrack isn't nothing..
                self.MainSoundTrack.fadeout(1) # Delete/Fadeout the last soundtrack

            self.MainSoundTrack = self.SoundtrackLibrary[soundtrack_name] # Set the new MainSoundTrack as the soundtrack that was found
            self.MainSoundTrack.set_volume(0.25) # Set the volume to 25%
            self.MainSoundTrack.play(-1) # Play the song endlessly
        else:
            print(f"Soundtrack '{soundtrack_name}' not found!") # In case there is ever a mistake, print that the soundtrack isn't there.