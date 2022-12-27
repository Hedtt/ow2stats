import gspread
from oauth2client.service_account import ServiceAccountCredentials
from enum import Enum

import player
from game import Game
import datetime
from enums import *


class GDoc:
    def __init__(self):
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('uselessFolderINeedBecauseOfWindoof/creds.json',
                                                                      scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open("ow2stats").sheet1

    def removeGame(self, row_index: int):
        self.sheet.delete_row(index=row_index)

    def openGame(self, row) -> Game:
        row_index = "A" + str(row) + ":N" + str(row)
        game_list = self.sheet.get(row_index)[0]
        game = Game()
        game.player = player.Player(game_list[0])
        game.player.socketName = game_list[1]
        game.date = game_list[2]
        game.groupSize = int(game_list[3])
        game.role = game_list[4]
        game.roleQueue = game_list[5]
        game.gameMode = game_list[6]
        game.mapPlayed = game_list[7]
        game.team = game_list[8]
        game.voice = game_list[9]
        game.ownVoice = game_list[10]
        game.result = game_list[11]
        game.comment = game_list[12]

        game.roleIsChosen = True
        game.mapIsSelected = True
        game.teamIsChosen = True
        game.resultIsChosen = True

        return game

    @staticmethod
    def addGame(game):
        role_queued = ''.join(list(map(lambda x: x.name[0], game.roleQueue)))
        game_array = [game.player.username, game.player.socketName, str(game.date), game.groupSize, game.role.name,
                      role_queued, game.gameMode.name, game.mapPlayed.name, game.team.name, game.voice,
                      game.ownVoice, game.result.name, game.comment]
        # self.sheet.insert_row(game_array, 2)

    def openLastGame(self):
        game = self.openGame(2)
        self.removeGame(2)
        return game
