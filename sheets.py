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
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('uselessFolderINeedBecauseOfWindoof/creds.json', scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open("ow2stats").sheet1

    def removeGame(self, rowIndex: int):
        self.sheet.delete_row(index=rowIndex)

    def openGame(self, row) -> Game:
        row_index = "A" + str(row) + ":N" + str(row)
        gameList = self.sheet.get(row_index)[0]
        game = Game()
        game.player = player.Player(gameList[0])
        game.player.socketName = gameList[1]
        game.date = gameList[2]
        game.groupSize = int(gameList[3])
        game.role = gameList[4]
        game.roleQueue = gameList[5]
        game.gameMode = gameList[6]
        game.mapPlayed = gameList[7]
        game.team = gameList[8]
        game.voice = gameList[9]
        game.ownVoice = gameList[10]
        game.result = gameList[11]
        game.comment = gameList[12]

        game.roleIsChosen = True
        game.mapIsSelected = True
        game.teamIsChosen = True
        game.resultIsChosen = True

        return game

    def addGame(self, game):
        gameArray = [game.player.username, game.player.socketName, str(game.date), game.groupSize, game.role.name,
                     ''.join(game.roleQueue), game.gameMode.name, game.mapPlayed.name, game.team.name, game.voice,
                     game.ownVoice, game.result.name, game.comment]
        self.sheet.insert_row(gameArray, 2)

    def openLastGame(self):
        game = self.openGame(2)
        self.removeGame(2)
        return game
