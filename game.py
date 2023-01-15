import datetime
from typing import List

from enums import *
from player import *
from boolStrAttributes import BoolStrAttributes


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

        self.roleIsChosen = BoolStrAttributes(error_str='Role was not chosen!')
        self.mapIsSelected = BoolStrAttributes(error_str='Map was not selected!')
        self.teamIsChosen = BoolStrAttributes(error_str='Team was not chosen!')
        self.resultIsChosen = BoolStrAttributes(error_str='Result was not chosen!')
        self.comment = None

    def dateChanged(self, date):
        if type(date) is not str:
            self.date = date.toString('yyyy-MM-dd')
        else:
            self.date = date

    def groupSizeChanged(self, group_size: int):
        self.groupSize = group_size

    def roleChosen(self, role: Role):
        self.role = role
        self.roleIsChosen.val = True

    def roleQueuedChanged(self, role: Role):
        if role not in self.roleQueue:
            self.roleQueue.append(role)
        else:
            self.roleQueue.remove(role)

    def gameModeChosen(self, game_mode: GameMode):
        self.gameMode = game_mode

    def mapChosen(self, map_played):
        self.mapPlayed = map_played
        self.mapIsSelected.val = True

    def teamChosen(self, team: Team):
        self.team = team
        self.teamIsChosen.val = True

    def voiceChanged(self, voice: int):
        self.voice = voice

    def ownVoiceChanged(self, own_voice: int):
        self.ownVoice = own_voice

    def resultChanged(self, result: Result):
        self.result = result
        self.resultIsChosen.val = True

    def gameValid(self) -> [bool, List[str]]:
        errors = []
        role_played_is_in_role_queued = BoolStrAttributes('Role played is not in role queued!')
        if len(self.roleQueue) > 0:
            role_played_is_in_role_queued.val = self.role in self.roleQueue

        vals = [self.roleIsChosen, role_played_is_in_role_queued, self.mapIsSelected,
                self.teamIsChosen, self.resultIsChosen]
        for cond in vals:
            if not cond.val:
                errors.append(cond.error)

        return [all(list(map(lambda x: x.val, vals))), errors]
