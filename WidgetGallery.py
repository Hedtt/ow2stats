from PyQt5.QtCore import QObject, QDateTime, QDate
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QAbstractButton, QDateEdit, QButtonGroup)
import re
from sheets import *
from player import *
from game import *


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.comment = QLineEdit()
        self.doc = GDoc()
        self.currentPlayer = None

        self.voiceCombo = QComboBox()
        self.ownVoicechat = QComboBox()
        self.radioPushGroup = QButtonGroup()
        self.radioKothGroup = QButtonGroup()
        self.radioEscortGroup = QButtonGroup()
        self.radioHybridGroup = QButtonGroup()
        self.radioGroupTeam = QButtonGroup()
        self.radioGroupRole = QButtonGroup()
        self.checkGroupRoleQueue = QButtonGroup()
        self.generalBox = QGroupBox()
        self.error = None
        self.supportRoleImage = QLabel()
        self.dpsRoleImage = QLabel()
        self.tankRoleImage = QLabel()
        self.player = QLineEdit()
        self.resultDraw = QPushButton()
        self.mainScreen = QGroupBox('Overwatch 2 Stats')
        self.submitBox = QGroupBox()
        self.resultBox = QGroupBox('Result')
        self.compPlaying = QCheckBox()
        self.socialGroupBox = QGroupBox('Social')
        self.pushMapsBox = QGroupBox('Push')
        self.pushMapsBox.setVisible(False)
        self.kothMapsBox = QGroupBox('Koth')
        self.kothMapsBox.setVisible(False)
        self.hybridMapsBox = QGroupBox('Hybrid')
        self.hybridMapsBox.setVisible(False)
        self.escortMapsBox = QGroupBox('Escort')
        self.escortMapsBox.setVisible(False)

        self.teamGroupBox = QGroupBox('Team')
        self.modeGroupBox = QGroupBox('Mode')
        self.mapGroupBox = QGroupBox('Map')
        self.roleGroupBox = QGroupBox('Role')

        self.createMapGroupBox()
        self.createRoleGroupBox()
        self.createTeamGroupBox()
        self.createGeneralBox()
        self.createModeGroupBox()
        self.createEscortMapsBox()
        self.createHybridMapsBox()
        self.createKothMapsBox()
        self.createPushMapsBox()
        self.createSocialGroupBox()
        self.createResultBox()
        self.createSubmitBox()
        self.createMainScreen()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.mainScreen, 0, 0)
        mainLayout.addWidget(self.generalBox, 0, 0)
        mainLayout.addWidget(self.roleGroupBox, 1, 0)
        mainLayout.addWidget(self.modeGroupBox, 2, 0)
        mainLayout.addWidget(self.escortMapsBox, 2, 0)
        mainLayout.addWidget(self.hybridMapsBox, 2, 0)
        mainLayout.addWidget(self.kothMapsBox, 2, 0)
        mainLayout.addWidget(self.pushMapsBox, 2, 0)
        mainLayout.addWidget(self.teamGroupBox, 3, 0)
        mainLayout.addWidget(self.socialGroupBox, 4, 0)
        mainLayout.addWidget(self.resultBox, 5, 0)
        mainLayout.addWidget(self.submitBox, 6, 0)
        self.setLayout(mainLayout)

        self.initialize()

        self.setToStartScreen()

    def initialize(self):
        # create new game
        self.game = Game()
        self.game.player = self.currentPlayer

        # Role reset
        self.radioGroupRole.setExclusive(False)
        if self.radioGroupRole.checkedButton() is not None:
            self.radioGroupRole.checkedButton().setChecked(False)
        self.radioGroupRole.setExclusive(True)
        self.tankRoleImage.setVisible(False)
        self.dpsRoleImage.setVisible(False)
        self.supportRoleImage.setVisible(False)

        self.checkGroupRoleQueue.setExclusive(False)
        # if self.checkGroupRoleQueue.checkedButton() is not None:
        #     for button in self.checkGroupRoleQueue.checkedButton():
        #         button.setChecked(False)
        for button in self.checkGroupRoleQueue.buttons():
            button.setChecked(False)
        self.game.roleQueue = []

        # Team reset
        self.radioGroupTeam.setExclusive(False)
        if self.radioGroupTeam.checkedButton() is not None:
            self.radioGroupTeam.checkedButton().setChecked(False)
        self.radioGroupTeam.setExclusive(True)
        if self.compPlaying.isChecked():
            self.comp_clicked(state=QtCore.Qt.Checked)

        # Map reset
        self.mapSelect_back()

        # Social reset
        self.voiceCombo.setCurrentIndex(self.ownVoicechat.currentIndex() + 1)
        self.comment.setText('')

    def setToStartScreen(self):
        self.mainScreen.setVisible(True)
        self.generalBox.setVisible(False)
        self.roleGroupBox.setVisible(False)
        self.modeGroupBox.setVisible(False)
        self.escortMapsBox.setVisible(False)
        self.hybridMapsBox.setVisible(False)
        self.kothMapsBox.setVisible(False)
        self.pushMapsBox.setVisible(False)
        self.teamGroupBox.setVisible(False)
        self.socialGroupBox.setVisible(False)
        self.resultBox.setVisible(False)
        self.submitBox.setVisible(False)
        self.mainScreen.adjustSize()

    def setToStatsScreen(self):
        self.mainScreen.setVisible(False)
        self.generalBox.setVisible(True)
        self.roleGroupBox.setVisible(True)
        self.modeGroupBox.setVisible(True)
        self.teamGroupBox.setVisible(True)
        self.socialGroupBox.setVisible(True)
        self.resultBox.setVisible(True)
        self.submitBox.setVisible(True)

    def createGeneralBox(self):
        self.dateEdit = QDateEdit()
        self.dateEdit.setDate(QDate.currentDate())
        self.dateEdit.dateChanged.connect(lambda: self.game.dateChanged(self.dateEdit.date()))
        self.peoplePlaying = QComboBox()
        peoplePlayingStr = QLabel('# Group')
        peoplePlayingStr.setToolTip('How many people are in the group you\'re playing in?')
        self.peoplePlaying.addItems(map(str, range(1, 6)))
        self.peoplePlaying.currentIndexChanged.connect(
            lambda: self.game.groupSizeChanged(self.peoplePlaying.currentText()))
        self.peoplePlaying.currentIndexChanged.connect(
            lambda: self.groupSizeChanged(self.peoplePlaying.currentIndex() + 1))
        ownVoicechatStr = QLabel('# Voicechat')
        ownVoicechatStr.setToolTip('How many people of your group are in team voicechat?')
        self.ownVoicechat.addItems(map(str, range(0, 6)))
        self.ownVoicechat.currentIndexChanged.connect(
            lambda: self.game.ownVoiceChanged(self.ownVoicechat.currentText()))
        self.compPlaying.stateChanged.connect(self.comp_clicked)

        layout = QHBoxLayout()
        layout.addWidget(QLabel('Date:'))
        layout.addWidget(self.dateEdit)
        layout.addStretch()
        layout.addWidget(peoplePlayingStr)
        layout.addWidget(self.peoplePlaying)
        layout.addStretch()
        layout.addWidget(ownVoicechatStr)
        layout.addWidget(self.ownVoicechat)
        layout.addStretch()
        layout.addWidget(QLabel('Playing Comp:'))
        layout.addWidget(self.compPlaying)
        self.generalBox.setLayout(layout)

    def createRoleGroupBox(self):

        radioButtonTank = QRadioButton('Tank')
        radioButtonTank.clicked.connect(lambda: self.chooseRole(radioButtonTank.text()))
        radioButtonTank.clicked.connect(lambda: self.game.roleChosen(Role.Tank))
        radioButtonDps = QRadioButton('Dps')
        radioButtonDps.clicked.connect(lambda: self.game.roleChosen(Role.Dps))
        radioButtonDps.clicked.connect(lambda: self.chooseRole(radioButtonDps.text()))
        radioButtonSupport = QRadioButton('Support')
        radioButtonSupport.clicked.connect(lambda: self.game.roleChosen(Role.Support))
        radioButtonSupport.clicked.connect(lambda: self.chooseRole(radioButtonSupport.text()))

        self.radioGroupRole.addButton(radioButtonTank)
        self.radioGroupRole.addButton(radioButtonDps)
        self.radioGroupRole.addButton(radioButtonSupport)

        checkButtonQueuedTank = QCheckBox('Tank')
        checkButtonQueuedTank.stateChanged.connect(lambda: self.game.roleQueuedChanged(Role.Tank))
        checkButtonQueuedDps = QCheckBox('Dps')
        checkButtonQueuedDps.stateChanged.connect(lambda: self.game.roleQueuedChanged(Role.Dps))
        checkButtonQueuedSupport = QCheckBox('Support')
        checkButtonQueuedSupport.stateChanged.connect(lambda: self.game.roleQueuedChanged(Role.Support))

        self.checkGroupRoleQueue.addButton(checkButtonQueuedTank)
        self.checkGroupRoleQueue.addButton(checkButtonQueuedDps)
        self.checkGroupRoleQueue.addButton(checkButtonQueuedSupport)

        TankRolePixmap = QtGui.QPixmap('pictures/Tank_icon.svg')
        DpsRolePixmap = QtGui.QPixmap('pictures/Damage_icon.svg')
        SupportRolePixmap = QtGui.QPixmap('pictures/Support_icon.svg')
        self.tankRoleImage.resize(80, 80)
        self.dpsRoleImage.resize(80, 80)
        self.supportRoleImage.resize(80, 80)
        self.tankRoleImage.setPixmap(TankRolePixmap.scaled(self.tankRoleImage.size(), QtCore.Qt.KeepAspectRatio))
        self.dpsRoleImage.setPixmap(DpsRolePixmap.scaled(self.dpsRoleImage.size(), QtCore.Qt.KeepAspectRatio))
        self.supportRoleImage.setPixmap(
            SupportRolePixmap.scaled(self.supportRoleImage.size(), QtCore.Qt.KeepAspectRatio))

        TankRoleImageLayout = QGridLayout()
        TankRoleImageLayout.addWidget(self.tankRoleImage)
        self.tankRoleImage.setVisible(False)

        DpsRoleImageLayout = QGridLayout()
        DpsRoleImageLayout.addWidget(self.dpsRoleImage)
        self.dpsRoleImage.setVisible(False)

        SupportRoleImageLayout = QGridLayout()
        SupportRoleImageLayout.addWidget(self.supportRoleImage)
        self.supportRoleImage.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(radioButtonTank)
        layout.addWidget(radioButtonDps)
        layout.addWidget(radioButtonSupport)
        layoutQueue = QVBoxLayout()
        layoutQueue.addWidget(QLabel('Queued for:'))
        layoutQueue.addWidget(checkButtonQueuedTank)
        layoutQueue.addWidget(checkButtonQueuedDps)
        layoutQueue.addWidget(checkButtonQueuedSupport)
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(layout)
        mainLayout.addLayout(TankRoleImageLayout)
        mainLayout.addLayout(DpsRoleImageLayout)
        mainLayout.addLayout(SupportRoleImageLayout)
        mainLayout.addLayout(layoutQueue)
        self.roleGroupBox.setLayout(mainLayout)

    def createMapGroupBox(self):
        mapButtonGothenburg = QRadioButton('Gothenburg')
        mapButtonIndia = QRadioButton('India')
        mapButtonMonteCarlo = QRadioButton('Monte Carlo')

        # TODO: add new maps to mode

    def createModeGroupBox(self):
        self.modeButtonEscort = QPushButton('Escort')
        self.modeButtonEscort.clicked.connect(self.modeEscort_clicked)
        self.modeButtonEscort.clicked.connect(lambda: self.game.gameModeChosen(GameMode.Escort))
        self.modeButtonHybrid = QPushButton('Hybrid')
        self.modeButtonHybrid.clicked.connect(self.modeHybrid_clicked)
        self.modeButtonHybrid.clicked.connect(lambda: self.game.gameModeChosen(GameMode.Hybrid))
        self.modeButtonKoth = QPushButton('Koth')
        self.modeButtonKoth.clicked.connect(self.modeKoth_clicked)
        self.modeButtonKoth.clicked.connect(lambda: self.game.gameModeChosen(GameMode.Koth))
        self.modeButtonPush = QPushButton('Push')
        self.modeButtonPush.clicked.connect(self.modePush_clicked)
        self.modeButtonPush.clicked.connect(lambda: self.game.gameModeChosen(GameMode.Push))
        layout = QHBoxLayout()
        layout.addWidget(self.modeButtonEscort)
        layout.addWidget(self.modeButtonHybrid)
        layout.addWidget(self.modeButtonKoth)
        layout.addWidget(self.modeButtonPush)

        self.modeGroupBox.setLayout(layout)

    def modeEscort_clicked(self):
        self.modeGroupBox.setVisible(False)
        self.escortMapsBox.setVisible(True)

    def modeHybrid_clicked(self):
        self.modeGroupBox.setVisible(False)
        self.hybridMapsBox.setVisible(True)

    def modeKoth_clicked(self):
        self.modeGroupBox.setVisible(False)
        self.teamGroupBox.setVisible(False)
        self.kothMapsBox.setVisible(True)
        self.resultDraw.setVisible(False)
        self.game.teamChosen(Team.NoTeam)

    def modePush_clicked(self):
        self.modeGroupBox.setVisible(False)
        self.teamGroupBox.setVisible(False)
        self.game.teamChosen(Team.NoTeam)
        self.pushMapsBox.setVisible(True)
        self.resultDraw.setVisible(True)

    def createTeamGroupBox(self):
        teamButtonAttack = QRadioButton('Attack')
        teamButtonAttack.clicked.connect(lambda: self.game.teamChosen(Team.Attack))
        teamButtonDefense = QRadioButton('Defense')
        teamButtonDefense.clicked.connect(lambda: self.game.teamChosen(Team.Defense))

        self.radioGroupTeam.addButton(teamButtonAttack)
        self.radioGroupTeam.addButton(teamButtonDefense)

        layout = QVBoxLayout()
        layout.addWidget(teamButtonAttack)
        layout.addWidget(teamButtonDefense)

        self.teamGroupBox.setLayout(layout)

    def comp_clicked(self, state):
        # comp is enabled
        self.game.teamChosen(Team.Comp)
        if state == QtCore.Qt.Checked:
            self.teamGroupBox.setEnabled(False)
            self.teamGroupBox.setHidden(True)
            if not self.kothMapsBox.isVisible():
                self.resultDraw.setVisible(True)
            return
        # comp is disabled
        self.game.teamIsChosen = False
        self.teamGroupBox.setEnabled(True)
        if not self.kothMapsBox.isVisible():
            self.teamGroupBox.setHidden(False)
        self.resultDraw.setVisible(False)

    def createEscortMapsBox(self):
        mapSelectionBack = QPushButton('Back to Mode select')
        mapSelectionBack.clicked.connect(self.mapSelect_back)
        mapButtonDorado = QRadioButton('Dorado')
        mapButtonDorado.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Dorado))
        mapButtonHavana = QRadioButton('Havana')
        mapButtonHavana.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Havana))
        mapButtonJunkertown = QRadioButton('Junkertown')
        mapButtonJunkertown.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Junkertown))
        mapButtonRialto = QRadioButton('Rialto')
        mapButtonRialto.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Rialto))
        mapButtonRoute66 = QRadioButton('Route 66')
        mapButtonRoute66.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Route))
        mapButtonShambali = QRadioButton('Shambali')
        mapButtonShambali.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Shambali))
        mapButtonWatchpointGibraltar = QRadioButton('Watchpoint: Gibraltar')
        mapButtonWatchpointGibraltar.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Gibraltar))

        self.radioEscortGroup.addButton(mapButtonDorado)
        self.radioEscortGroup.addButton(mapButtonHavana)
        self.radioEscortGroup.addButton(mapButtonJunkertown)
        self.radioEscortGroup.addButton(mapButtonRialto)
        self.radioEscortGroup.addButton(mapButtonRoute66)
        self.radioEscortGroup.addButton(mapButtonShambali)
        self.radioEscortGroup.addButton(mapButtonWatchpointGibraltar)

        escortLayout = QVBoxLayout()
        escortLayout.addWidget(mapSelectionBack)
        escortLayout.addWidget(mapButtonDorado)
        escortLayout.addWidget(mapButtonHavana)
        escortLayout.addWidget(mapButtonJunkertown)
        escortLayout.addWidget(mapButtonRialto)
        escortLayout.addWidget(mapButtonRoute66)
        escortLayout.addWidget(mapButtonShambali)
        escortLayout.addWidget(mapButtonWatchpointGibraltar)

        self.escortMapsBox.setLayout(escortLayout)

    def createHybridMapsBox(self):
        mapSelectionBack = QPushButton('Back to Mode select')
        mapSelectionBack.clicked.connect(self.mapSelect_back)

        mapButtonBlizzardWorld = QRadioButton('Blizzard World')
        mapButtonBlizzardWorld.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.BlizzardWorld))
        mapButtonEichenwalde = QRadioButton('Eichenwalde')
        mapButtonEichenwalde.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.Eichenwalde))
        mapButtonHollywood = QRadioButton('Hollywood')
        mapButtonHollywood.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.Hollywood))
        mapButtonKingsRow = QRadioButton('King\'s Row')
        mapButtonKingsRow.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.KingsRow))
        mapButtonNewYork = QRadioButton('New York City')
        mapButtonNewYork.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.Midtown))
        mapButtonNumbani = QRadioButton('Numbani')
        mapButtonNumbani.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.Numbani))
        mapButtonParaiso = QRadioButton('Paraiso')
        mapButtonParaiso.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.Paraiso))
        mapButtonRiodeJaneiro = QRadioButton('Rio de Janeiro')
        mapButtonRiodeJaneiro.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.RioDeJaneiro))

        self.radioHybridGroup.addButton(mapButtonBlizzardWorld)
        self.radioHybridGroup.addButton(mapButtonEichenwalde)
        self.radioHybridGroup.addButton(mapButtonHollywood)
        self.radioHybridGroup.addButton(mapButtonKingsRow)
        self.radioHybridGroup.addButton(mapButtonNewYork)
        self.radioHybridGroup.addButton(mapButtonNumbani)
        self.radioHybridGroup.addButton(mapButtonParaiso)
        self.radioHybridGroup.addButton(mapButtonRiodeJaneiro)

        hybridLayout = QVBoxLayout()
        hybridLayout.addWidget(mapSelectionBack)
        hybridLayout.addWidget(mapButtonBlizzardWorld)
        hybridLayout.addWidget(mapButtonEichenwalde)
        hybridLayout.addWidget(mapButtonHollywood)
        hybridLayout.addWidget(mapButtonKingsRow)
        hybridLayout.addWidget(mapButtonNumbani)
        hybridLayout.addWidget(mapButtonNewYork)
        hybridLayout.addWidget(mapButtonParaiso)
        hybridLayout.addWidget(mapButtonRiodeJaneiro)

        self.hybridMapsBox.setLayout(hybridLayout)

    def createKothMapsBox(self):
        mapSelectionBack = QPushButton('Back to Mode select')
        mapSelectionBack.clicked.connect(self.mapSelect_back)

        mapButtonBusan = QRadioButton('Busan')
        mapButtonBusan.clicked.connect(lambda: self.game.mapChosen(Map.KothMap.value.Busan))
        mapButtonIlios = QRadioButton('Ilios')
        mapButtonIlios.clicked.connect(lambda: self.game.mapChosen(Map.KothMap.value.Ilios))
        mapButtonLijiang = QRadioButton('Lijiang Tower')
        mapButtonLijiang.clicked.connect(lambda: self.game.mapChosen(Map.KothMap.value.Lijiang))
        mapButtonNepal = QRadioButton('Nepal')
        mapButtonNepal.clicked.connect(lambda: self.game.mapChosen(Map.KothMap.value.Nepal))
        mapButtonOasis = QRadioButton('Oasis')
        mapButtonOasis.clicked.connect(lambda: self.game.mapChosen(Map.KothMap.value.Oasis))

        self.radioKothGroup.addButton(mapButtonBusan)
        self.radioKothGroup.addButton(mapButtonIlios)
        self.radioKothGroup.addButton(mapButtonLijiang)
        self.radioKothGroup.addButton(mapButtonNepal)
        self.radioKothGroup.addButton(mapButtonOasis)

        kothLayout = QVBoxLayout()
        kothLayout.addWidget(mapSelectionBack)
        kothLayout.addWidget(mapButtonBusan)
        kothLayout.addWidget(mapButtonIlios)
        kothLayout.addWidget(mapButtonLijiang)
        kothLayout.addWidget(mapButtonNepal)
        kothLayout.addWidget(mapButtonOasis)

        self.kothMapsBox.setLayout(kothLayout)

    def createPushMapsBox(self):
        mapSelectionBack = QPushButton('Back to Mode select')
        mapSelectionBack.clicked.connect(self.mapSelect_back)

        mapButtonEsperanca = QRadioButton('Esperanca')
        mapButtonEsperanca.clicked.connect(lambda: self.game.mapChosen(Map.PushMap.value.Esperanca))
        mapButtonRome = QRadioButton('Rome')
        mapButtonRome.clicked.connect(lambda: self.game.mapChosen(Map.PushMap.value.Colosseo))
        mapButtonToronto = QRadioButton('Toronto')
        mapButtonToronto.clicked.connect(lambda: self.game.mapChosen(Map.PushMap.value.NewQueenStreet))

        self.radioPushGroup.addButton(mapButtonEsperanca)
        self.radioPushGroup.addButton(mapButtonRome)
        self.radioPushGroup.addButton(mapButtonToronto)

        pushLayout = QVBoxLayout()
        pushLayout.addWidget(mapSelectionBack)
        pushLayout.addWidget(mapButtonToronto)
        pushLayout.addWidget(mapButtonEsperanca)
        pushLayout.addWidget(mapButtonRome)

        self.pushMapsBox.setLayout(pushLayout)

    def mapSelect_back(self):
        # Button reset
        self.radioEscortGroup.setExclusive(False)
        self.radioHybridGroup.setExclusive(False)
        self.radioKothGroup.setExclusive(False)
        self.radioPushGroup.setExclusive(False)
        if self.radioEscortGroup.checkedButton() is not None:
            self.radioEscortGroup.checkedButton().setChecked(False)
        if self.radioHybridGroup.checkedButton() is not None:
            self.radioHybridGroup.checkedButton().setChecked(False)
        if self.radioKothGroup.checkedButton() is not None:
            self.radioKothGroup.checkedButton().setChecked(False)
        if self.radioPushGroup.checkedButton() is not None:
            self.radioPushGroup.checkedButton().setChecked(False)
        self.radioEscortGroup.setExclusive(True)
        self.radioHybridGroup.setExclusive(True)
        self.radioKothGroup.setExclusive(True)
        self.radioPushGroup.setExclusive(True)

        # Ui reset
        self.modeGroupBox.setVisible(True)
        self.escortMapsBox.setVisible(False)
        self.hybridMapsBox.setVisible(False)
        self.kothMapsBox.setVisible(False)
        self.pushMapsBox.setVisible(False)
        self.game.mapIsSelected = False
        if not self.compPlaying.isChecked():
            self.teamGroupBox.setVisible(True)
            self.game.teamIsChosen = False
        else:
            self.resultDraw.setVisible(True)

    def createSocialGroupBox(self):
        voiceComboStr = QLabel('# in vc')
        voiceComboStr.setToolTip('How many people are in the team voicechat (including you and your group)?')
        self.voiceCombo.addItems(map(str, range(0, 6)))
        self.voiceCombo.currentIndexChanged.connect(lambda: self.game.voiceChanged(self.voiceCombo.currentText()))

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(voiceComboStr)
        layout.addWidget(self.voiceCombo)
        layout.addStretch()
        layout.addWidget(QLabel('Comment:'))
        layout.addWidget(self.comment)
        layout.addStretch()

        self.socialGroupBox.setLayout(layout)

    def createResultBox(self):
        self.resultVictory = QPushButton()
        self.resultVictory.clicked.connect(lambda: self.game.resultChanged(Result.Victory))
        self.resultVictory.setIcon(QtGui.QIcon('pictures/victory_transparent.png'))
        self.resultVictory.setIconSize(QtCore.QSize(100, 40))
        self.resultDefeat = QPushButton()
        self.resultDefeat.clicked.connect(lambda: self.game.resultChanged(Result.Defeat))
        self.resultDefeat.setIcon(QtGui.QIcon('pictures/defeat_transparent.png'))
        self.resultDefeat.setIconSize(QtCore.QSize(100, 40))
        self.resultDraw.clicked.connect(lambda: self.game.resultChanged(Result.Draw))
        self.resultDraw.setIcon(QtGui.QIcon('pictures/draw_transparent.png'))
        self.resultDraw.setIconSize(QtCore.QSize(100, 40))
        self.resultDraw.setVisible(False)

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.resultVictory)
        layout.addStretch()
        layout.addWidget(self.resultDraw)
        layout.addStretch()
        layout.addWidget(self.resultDefeat)
        layout.addStretch()
        self.resultBox.setLayout(layout)

    def createSubmitBox(self):
        submit = QPushButton('Submit')
        submit.clicked.connect(self.submitClicked)
        openLastGame = QPushButton('Open last game')
        openLastGame.clicked.connect(lambda: self.openLastClicked(False))

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(openLastGame)
        layout.addStretch()
        layout.addWidget(submit)
        layout.addStretch()

        self.submitBox.setLayout(layout)

    def createMainScreen(self):
        finish = QPushButton('Track Stats')
        finish.clicked.connect(self.startTracking)
        if self.player.text != '':
            self.player.setToolTip(self.player.text())

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Player Name:'))
        layout.addWidget(self.player)
        self.player.adjustSize()
        layout.addWidget(finish)
        self.mainScreen.setLayout(layout)
        self.mainScreen.adjustSize()

    def startTracking(self):
        playerName = str.strip(self.player.text())
        if re.search(r'\S', playerName):
            self.game.player = Player(playerName)
            self.currentPlayer = self.game.player
            self.setToStatsScreen()
        else:
            self.errorUsername = InvalidUserName()
            self.errorUsername.show()

    def chooseRole(self, role: str):
        if role == 'Tank':
            self.tankRoleImage.setVisible(True)
            self.dpsRoleImage.setVisible(False)
            self.supportRoleImage.setVisible(False)
        elif role == 'Dps':
            self.tankRoleImage.setVisible(False)
            self.dpsRoleImage.setVisible(True)
            self.supportRoleImage.setVisible(False)
        elif role == 'Support':
            self.tankRoleImage.setVisible(False)
            self.dpsRoleImage.setVisible(False)
            self.supportRoleImage.setVisible(True)

    def submitClicked(self):
        if self.game.gameValid() is False:
            self.errorWindow()
        else:
            self.game.comment = self.comment.text()
            self.doc.addGame(self.game)
            self.setToStatsScreen()
            self.initialize()

    def errorWindow(self):
        self.error = ErrorWindow()
        self.error.show()

    def groupSizeChanged(self, groupSize: int):
        self.ownVoicechat.clear()
        self.ownVoicechat.addItems(map(str, range(0, groupSize + 1)))
        self.ownVoicechat.setCurrentIndex(groupSize)
        self.voiceCombo.clear()
        self.voiceCombo.addItems(map(str, range(groupSize, 6)))
        self.voiceCombo.setCurrentIndex(0)

    def openLastClicked(self, confirmed: bool):
        if not confirmed:
            self.openLastConfirm = AreYouSure(self)
            self.openLastConfirm.show()
        else:
            self.initialize()
            game = self.doc.openLastGame()
            self.game.player = Player(game.player.username)
            self.game.player.socketName = game.player.socketName
            self.dateEdit.setDate(QDate.fromString(game.date, 'yyyy-MM-dd'))
            self.peoplePlaying.setCurrentIndex(int(game.groupSize) - 1)
            self.ownVoicechat.setCurrentIndex(int(game.ownVoice))

            if game.role == 'Tank':
                self.radioGroupRole.buttons()[0].click()
            elif game.role == 'Dps':
                self.radioGroupRole.buttons()[1].click()
            elif game.role == 'Support':
                self.radioGroupRole.buttons()[2].click()

            # Gamemode and Map
            if game.gameMode == 'Escort':
                self.modeButtonEscort.click()
                for escortMap in self.radioEscortGroup.buttons():
                    if escortMap.text() == game.mapPlayed:
                        escortMap.click()
                        break
            elif game.gameMode == 'Hybrid':
                self.modeButtonHybrid.click()
                for hybridMap in self.radioHybridGroup.buttons():
                    if hybridMap.text() == game.mapPlayed:
                        hybridMap.click()
                        break
            elif game.gameMode == 'Koth':
                self.modeButtonKoth.click()
                for kothMap in self.radioKothGroup.buttons():
                    if kothMap.text() == game.mapPlayed:
                        kothMap.click()
                        break
            elif game.gameMode == 'Push':
                self.modeButtonPush.click()
                for pushMap in self.radioPushGroup.buttons():
                    if pushMap.text() == game.mapPlayed:
                        pushMap.click()
                        break

            # Team
            if game.team == 'Comp':
                self.compPlaying.click()
            elif game.team == 'Attack':
                self.radioGroupTeam.buttons()[0].click()
            elif game.team == 'Defense':
                self.radioGroupTeam.buttons()[1].click()

            # Voicechat
            self.voiceCombo.setCurrentIndex(int(game.voice))

            # Result
            if game.result == 'Victory':
                self.resultVictory.click()
            elif game.result == 'Draw':
                self.resultDraw.click()
            elif game.result == 'Defeat':
                self.resultDefeat.click()


class ErrorWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel('Error, not all parameters were inputed')
        self.redoButton = QPushButton('Input missing things')
        self.redoButton.clicked.connect(self.closeThis)
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addWidget(self.redoButton)
        layout.addStretch()
        self.setLayout(layout)

    def closeThis(self):
        self.close()


class InvalidUserName(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel('Error, invalid username')
        self.redoButton = QPushButton('Input username')
        self.redoButton.clicked.connect(self.closeThis)
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addWidget(self.redoButton)
        layout.addStretch()
        self.setLayout(layout)

    def closeThis(self):
        self.close()


class AreYouSure(QWidget):
    def __init__(self, widgetGallery: WidgetGallery):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel('Are you sure? Current inputs are being deleted')
        self.openLast = QPushButton('Yes, open last game')
        self.undo = QPushButton('No, go back')
        self.openLast.clicked.connect(self.closeThis)
        self.openLast.clicked.connect(lambda: WidgetGallery.openLastClicked(self=widgetGallery, confirmed=True))
        self.undo.clicked.connect(self.closeThis)

        labelLayout = QHBoxLayout()
        labelLayout.addStretch()
        labelLayout.addWidget(self.label)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.openLast)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.undo)
        buttonLayout.addStretch()

        layout.addLayout(labelLayout)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

    def closeThis(self):
        self.close()
