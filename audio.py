import pygame, sys

class AudioManage:

    pygame.mixer.init()
    
    bgm = "snd/orpheusarrives.ogg"
 
    barks = [

        #builds
         [
            pygame.mixer.Sound("snd/manubark.ogg"),
            pygame.mixer.Sound("snd/reclaim.ogg"),
            pygame.mixer.Sound("snd/fuelextract.ogg"),
            pygame.mixer.Sound("snd/hydroponicbark.ogg"),
         ],
        
        #units 
        [
            pygame.mixer.Sound("snd/dronebark.ogg"),
            pygame.mixer.Sound("snd/transportbark.ogg"),
            pygame.mixer.Sound("snd/settlerbark.ogg"),
            pygame.mixer.Sound("snd/scoutbark.ogg"),
        ],
        
        pygame.mixer.Sound("snd/minebark.ogg"),
    ]

   
    def __init__(self, eventmanager):
        self.event = eventmanager

        self.barks = AudioManage.barks
        self.event.register("build_project", self.sound_on_build)
        self.event.register("build_unit", self.sound_on_unit)
        self.event.register("build_mine", self.sound_on_build)
 

     
        pygame.mixer.music.load(AudioManage.bgm)
        pygame.mixer.music.play(-1)

    def sound_on_build(self, project_id):
        barks[0][project_id].play()
   
    def sound_on_unit(self, project_id):
        barks[1][project_id].play()
   
   
  
    def sound_on_mine(self):
        barks[2].play()
 
