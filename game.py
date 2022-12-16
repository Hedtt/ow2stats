import datetime
from enums import *
from player import *


class Game:
    def __init__(self):
        self.role = None
        self.roleQueue = []
        self.player = None
        self.date = datetime.date.today()
        self.groupSize = 1
        self.gameMode = None
        self.mapPlayed = None
        self.team = None
        self.voice = 1
        self.ownVoice = 1
        self.result = None

        self.roleIsChosen = False
        self.mapIsSelected = False
        self.teamIsChosen = False
        self.resultIsChosen = False
        self.comment = None

    def dateChanged(self, date):
        if type(date) is not str:
            self.date = date.toString('yyyy-MM-dd')
        else:
            self.date = date

    def groupSizeChanged(self, groupsize: int):
        self.groupSize = groupsize

    def roleChosen(self, role: Role):
        self.role = role
        self.roleIsChosen = True

    def roleQueuedChanged(self, role: Role):
        text = role.name[0]
        if self.roleQueue is not None:
            if text in self.roleQueue:
                self.roleQueue.remove(text)
            else:
                self.roleQueue.append(text)

    def gameModeChosen(self, gameMode: GameMode):
        self.gameMode = gameMode

    def mapChosen(self, mapPlayed):
        self.mapPlayed = mapPlayed
        self.mapIsSelected = True

    def teamChosen(self, team: Team):
        self.team = team
        self.teamIsChosen = True

    def voiceChanged(self, voice: int):
        self.voice = voice

    def ownVoiceChanged(self, ownVoice: int):
        self.ownVoice = ownVoice

    def resultChanged(self, result: Result):
        self.result = result
        self.resultIsChosen = True

    def gameValid(self) -> bool:
        role_played_is_in_role_queued = True
        if len(self.roleQueue) > 0:
            role_played_is_in_role_queued = self.role in self.roleQueue
        return self.roleIsChosen and role_played_is_in_role_queued and self.mapIsSelected and self.teamIsChosen and self.resultIsChosen is True
