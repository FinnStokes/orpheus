import pygame, sys

class AudioManage:

    pygame.mixer.init()
    
    bgm = "snd/orpheusarrives.ogg"
 

    building_barks = { 
            "Manufactory" : pygame.mixer.Sound("snd/manubark.ogg"),
            "Reclamation Factory" : pygame.mixer.Sound("snd/reclaim.ogg"),
            "Fuel Extractor" : pygame.mixer.Sound("snd/fuelextract.ogg"),
            "Hydroponics Module" : pygame.mixer.Sound("snd/hydroponicbark.ogg")
    }
    
    unit_barks = {
            "Drone" : pygame.mixer.Sound("snd/dronebark.ogg"),
            "Transport" : pygame.mixer.Sound("snd/transportbark.ogg"),
            "Settler" : pygame.mixer.Sound("snd/settlerbark.ogg")
    }
        
    mine_bark = pygame.mixer.Sound("snd/minebark.ogg")
    

   
    def __init__(self, eventmanager):
        self.event = eventmanager

        self.event.register("built", self.sound_on_build)
        self.event.register("unit_built", self.sound_on_unit)
        self.event.register("mine_built", self.sound_on_mine)
     
        pygame.mixer.music.load(AudioManage.bgm)
        pygame.mixer.music.play(-1)

    def sound_on_build(self, thing, project):
        AudioManage.building_barks[project.name].play()
   
    def sound_on_unit(self,thing, project):
        AudioManage.unit_barks[project.name].play()
     
    def sound_on_mine(self, project):
        AudioManage.mine_bark.play() 
           
