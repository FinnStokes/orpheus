import pygame, sys

class AudioManage:
     
    def __init__(self, eventmanager):
        self.event = eventmanager

        self.event.register("build_project", self.sound_on_build)


    def sound_on_build(self, project_id):
        pass
   
    def usedrone(self, drone_id):
        pass

    def transport(self, succes):
        pass
