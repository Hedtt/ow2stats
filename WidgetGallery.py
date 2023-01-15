from PyQt5.QtCore import QObject, QDateTime, QDate
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QAbstractButton, QDateEdit, QButtonGroup, QMainWindow, QMenuBar,
                             QDockWidget)
import re
from sheets import *
from player import *
from game import *


class WidgetGallery(QMainWindow):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.openLastConfirm = AreYouSure(self)
        self.errorUsername = InvalidUserName()
        self.resultDefeat = QPushButton()
        self.resultVictory = QPushButton()
        self.modeButtonPush = QPushButton('Push')
        self.modeButtonKoth = QPushButton('Koth')
        self.modeButtonHybrid = QPushButton('Hybrid')
        self.modeButtonEscort = QPushButton('Escort')
        self.peoplePlaying = QComboBox()
        self.dateEdit = QDateEdit()
        self.game = None
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


        widget = QWidget(self)
        main_layout = QGridLayout(widget)
        main_layout.addWidget(self.mainScreen, 0, 0)
        main_layout.addWidget(self.generalBox, 0, 0)
        main_layout.addWidget(self.roleGroupBox, 1, 0)
        main_layout.addWidget(self.modeGroupBox, 2, 0)
        main_layout.addWidget(self.escortMapsBox, 2, 0)
        main_layout.addWidget(self.hybridMapsBox, 2, 0)
        main_layout.addWidget(self.kothMapsBox, 2, 0)
        main_layout.addWidget(self.pushMapsBox, 2, 0)
        main_layout.addWidget(self.teamGroupBox, 3, 0)
        main_layout.addWidget(self.socialGroupBox, 4, 0)
        main_layout.addWidget(self.resultBox, 5, 0)
        main_layout.addWidget(self.submitBox, 6, 0)
        self.setCentralWidget(widget)
        # self.setLayout(main_layout)


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
        self.dateEdit.setDate(QDate.currentDate())
        self.dateEdit.dateChanged.connect(lambda: self.game.dateChanged(self.dateEdit.date()))
        people_playing_str = QLabel('# Group')
        people_playing_str.setToolTip('How many people are in the group you\'re playing in?')
        self.peoplePlaying.addItems(map(str, range(1, 6)))
        self.peoplePlaying.currentIndexChanged.connect(
            lambda: self.game.groupSizeChanged(self.peoplePlaying.currentText()))
        self.peoplePlaying.currentIndexChanged.connect(
            lambda: self.groupSizeChanged(self.peoplePlaying.currentIndex() + 1))
        own_voicechat_str = QLabel('# Voicechat')
        own_voicechat_str.setToolTip('How many people of your group are in team voicechat?')
        self.ownVoicechat.addItems(map(str, range(0, 6)))
        self.ownVoicechat.currentIndexChanged.connect(
            lambda: self.game.ownVoiceChanged(self.ownVoicechat.currentText()))
        self.ownVoicechat.currentIndexChanged.connect(
            lambda: self.ownVoiceChanged(self.ownVoicechat.currentText()))
        self.compPlaying.stateChanged.connect(self.comp_clicked)

        layout = QHBoxLayout()
        layout.addWidget(QLabel('Date:'))
        layout.addWidget(self.dateEdit)
        layout.addStretch()
        layout.addWidget(people_playing_str)
        layout.addWidget(self.peoplePlaying)
        layout.addStretch()
        layout.addWidget(own_voicechat_str)
        layout.addWidget(self.ownVoicechat)
        layout.addStretch()
        layout.addWidget(QLabel('Playing Comp:'))
        layout.addWidget(self.compPlaying)
        self.generalBox.setLayout(layout)

    def createRoleGroupBox(self):

        radio_button_tank = QRadioButton('Tank')
        radio_button_tank.clicked.connect(lambda: self.chooseRole(radio_button_tank.text()))
        radio_button_tank.clicked.connect(lambda: self.game.roleChosen(Role.Tank))
        radio_button_dps = QRadioButton('Dps')
        radio_button_dps.clicked.connect(lambda: self.game.roleChosen(Role.Dps))
        radio_button_dps.clicked.connect(lambda: self.chooseRole(radio_button_dps.text()))
        radio_button_support = QRadioButton('Support')
        radio_button_support.clicked.connect(lambda: self.game.roleChosen(Role.Support))
        radio_button_support.clicked.connect(lambda: self.chooseRole(radio_button_support.text()))

        self.radioGroupRole.addButton(radio_button_tank)
        self.radioGroupRole.addButton(radio_button_dps)
        self.radioGroupRole.addButton(radio_button_support)

        check_button_queued_tank = QCheckBox('Tank')
        check_button_queued_tank.stateChanged.connect(lambda: self.game.roleQueuedChanged(Role.Tank))
        # check_button_queued_tank.stateChanged.connect(lambda: self.roleQueuedChanged(Role.Tank))
        check_button_queued_dps = QCheckBox('Dps')
        check_button_queued_dps.stateChanged.connect(lambda: self.game.roleQueuedChanged(Role.Dps))
        # check_button_queued_dps.stateChanged.connect(lambda: self.roleQueuedChanged(Role.Dps))
        check_button_queued_support = QCheckBox('Support')
        check_button_queued_support.stateChanged.connect(lambda: self.game.roleQueuedChanged(Role.Support))
        # check_button_queued_support.stateChanged.connect(lambda: self.roleQueuedChanged(Role.Support))

        self.checkGroupRoleQueue.addButton(check_button_queued_tank)
        self.checkGroupRoleQueue.addButton(check_button_queued_dps)
        self.checkGroupRoleQueue.addButton(check_button_queued_support)

        tank_role_pixmap = QtGui.QPixmap('pictures/Tank_icon.svg')
        dps_role_pixmap = QtGui.QPixmap('pictures/Damage_icon.svg')
        support_role_pixmap = QtGui.QPixmap('pictures/Support_icon.svg')
        self.tankRoleImage.resize(80, 80)
        self.dpsRoleImage.resize(80, 80)
        self.supportRoleImage.resize(80, 80)
        self.tankRoleImage.setPixmap(tank_role_pixmap.scaled(self.tankRoleImage.size(), QtCore.Qt.KeepAspectRatio))
        self.dpsRoleImage.setPixmap(dps_role_pixmap.scaled(self.dpsRoleImage.size(), QtCore.Qt.KeepAspectRatio))
        self.supportRoleImage.setPixmap(
            support_role_pixmap.scaled(self.supportRoleImage.size(), QtCore.Qt.KeepAspectRatio))

        tank_role_image_layout = QGridLayout()
        tank_role_image_layout.addWidget(self.tankRoleImage)
        self.tankRoleImage.setVisible(False)

        dps_role_image_layout = QGridLayout()
        dps_role_image_layout.addWidget(self.dpsRoleImage)
        self.dpsRoleImage.setVisible(False)

        support_role_image_layout = QGridLayout()
        support_role_image_layout.addWidget(self.supportRoleImage)
        self.supportRoleImage.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(radio_button_tank)
        layout.addWidget(radio_button_dps)
        layout.addWidget(radio_button_support)
        layout_queue = QVBoxLayout()
        layout_queue.addWidget(QLabel('Queued for:'))
        layout_queue.addWidget(check_button_queued_tank)
        layout_queue.addWidget(check_button_queued_dps)
        layout_queue.addWidget(check_button_queued_support)
        main_layout = QHBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(tank_role_image_layout)
        main_layout.addLayout(dps_role_image_layout)
        main_layout.addLayout(support_role_image_layout)
        main_layout.addLayout(layout_queue)
        self.roleGroupBox.setLayout(main_layout)

    def createMapGroupBox(self):
        map_button_gothenburg = QRadioButton('Gothenburg')
        map_button_india = QRadioButton('India')
        map_button_monte_carlo = QRadioButton('Monte Carlo')

        # TODO: add new maps to mode

    def createModeGroupBox(self):
        self.modeButtonEscort.clicked.connect(self.modeEscort_clicked)
        self.modeButtonEscort.clicked.connect(lambda: self.game.gameModeChosen(GameMode.Escort))
        self.modeButtonHybrid.clicked.connect(self.modeHybrid_clicked)
        self.modeButtonHybrid.clicked.connect(lambda: self.game.gameModeChosen(GameMode.Hybrid))
        self.modeButtonKoth.clicked.connect(self.modeKoth_clicked)
        self.modeButtonKoth.clicked.connect(lambda: self.game.gameModeChosen(GameMode.Koth))
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
        team_button_attack = QRadioButton('Attack')
        team_button_attack.clicked.connect(lambda: self.game.teamChosen(Team.Attack))
        team_button_defense = QRadioButton('Defense')
        team_button_defense.clicked.connect(lambda: self.game.teamChosen(Team.Defense))

        self.radioGroupTeam.addButton(team_button_attack)
        self.radioGroupTeam.addButton(team_button_defense)

        layout = QVBoxLayout()
        layout.addWidget(team_button_attack)
        layout.addWidget(team_button_defense)

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
        self.game.teamIsChosen.val = False
        self.teamGroupBox.setEnabled(True)
        if not self.kothMapsBox.isVisible():
            self.teamGroupBox.setHidden(False)
        self.resultDraw.setVisible(False)

    def createEscortMapsBox(self):
        map_selection_back = QPushButton('Back to Mode select')
        map_selection_back.clicked.connect(self.mapSelect_back)
        map_button_dorado = QRadioButton('Dorado')
        map_button_dorado.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Dorado))
        map_button_havana = QRadioButton('Havana')
        map_button_havana.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Havana))
        map_button_junkertown = QRadioButton('Junkertown')
        map_button_junkertown.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Junkertown))
        map_button_rialto = QRadioButton('Rialto')
        map_button_rialto.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Rialto))
        map_button_route66 = QRadioButton('Route 66')
        map_button_route66.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Route))
        map_button_shambali = QRadioButton('Shambali')
        map_button_shambali.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Shambali))
        map_button_watchpoint_gibraltar = QRadioButton('Watchpoint: Gibraltar')
        map_button_watchpoint_gibraltar.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Gibraltar))

        self.radioEscortGroup.addButton(map_button_dorado)
        self.radioEscortGroup.addButton(map_button_havana)
        self.radioEscortGroup.addButton(map_button_junkertown)
        self.radioEscortGroup.addButton(map_button_rialto)
        self.radioEscortGroup.addButton(map_button_route66)
        self.radioEscortGroup.addButton(map_button_shambali)
        self.radioEscortGroup.addButton(map_button_watchpoint_gibraltar)

        escort_layout = QVBoxLayout()
        escort_layout.addWidget(map_selection_back)
        escort_layout.addWidget(map_button_dorado)
        escort_layout.addWidget(map_button_havana)
        escort_layout.addWidget(map_button_junkertown)
        escort_layout.addWidget(map_button_rialto)
        escort_layout.addWidget(map_button_route66)
        escort_layout.addWidget(map_button_shambali)
        escort_layout.addWidget(map_button_watchpoint_gibraltar)

        self.escortMapsBox.setLayout(escort_layout)

    def createHybridMapsBox(self):
        map_selection_back = QPushButton('Back to Mode select')
        map_selection_back.clicked.connect(self.mapSelect_back)

        map_button_blizzard_world = QRadioButton('Blizzard World')
        map_button_blizzard_world.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.BlizzardWorld))
        map_button_eichenwalde = QRadioButton('Eichenwalde')
        map_button_eichenwalde.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.Eichenwalde))
        map_button_hollywood = QRadioButton('Hollywood')
        map_button_hollywood.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.Hollywood))
        map_button_kings_row = QRadioButton('King\'s Row')
        map_button_kings_row.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.KingsRow))
        map_button_new_york = QRadioButton('Midtown')
        map_button_new_york.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.Midtown))
        map_button_numbani = QRadioButton('Numbani')
        map_button_numbani.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.Numbani))
        map_button_paraiso = QRadioButton('Paraiso')
        map_button_paraiso.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.Paraiso))
        map_button_rio_de_janeiro = QRadioButton('Rio de Janeiro')
        map_button_rio_de_janeiro.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.RioDeJaneiro))

        self.radioHybridGroup.addButton(map_button_blizzard_world)
        self.radioHybridGroup.addButton(map_button_eichenwalde)
        self.radioHybridGroup.addButton(map_button_hollywood)
        self.radioHybridGroup.addButton(map_button_kings_row)
        self.radioHybridGroup.addButton(map_button_new_york)
        self.radioHybridGroup.addButton(map_button_numbani)
        self.radioHybridGroup.addButton(map_button_paraiso)
        self.radioHybridGroup.addButton(map_button_rio_de_janeiro)

        hybrid_layout = QVBoxLayout()
        hybrid_layout.addWidget(map_selection_back)
        hybrid_layout.addWidget(map_button_blizzard_world)
        hybrid_layout.addWidget(map_button_eichenwalde)
        hybrid_layout.addWidget(map_button_hollywood)
        hybrid_layout.addWidget(map_button_kings_row)
        hybrid_layout.addWidget(map_button_numbani)
        hybrid_layout.addWidget(map_button_new_york)
        hybrid_layout.addWidget(map_button_paraiso)
        hybrid_layout.addWidget(map_button_rio_de_janeiro)

        self.hybridMapsBox.setLayout(hybrid_layout)

    def createKothMapsBox(self):
        map_selection_back = QPushButton('Back to Mode select')
        map_selection_back.clicked.connect(self.mapSelect_back)

        map_button_busan = QRadioButton('Busan')
        map_button_busan.clicked.connect(lambda: self.game.mapChosen(Map.KothMap.value.Busan))
        map_button_ilios = QRadioButton('Ilios')
        map_button_ilios.clicked.connect(lambda: self.game.mapChosen(Map.KothMap.value.Ilios))
        map_button_lijiang = QRadioButton('Lijiang Tower')
        map_button_lijiang.clicked.connect(lambda: self.game.mapChosen(Map.KothMap.value.Lijiang))
        map_button_nepal = QRadioButton('Nepal')
        map_button_nepal.clicked.connect(lambda: self.game.mapChosen(Map.KothMap.value.Nepal))
        map_button_oasis = QRadioButton('Oasis')
        map_button_oasis.clicked.connect(lambda: self.game.mapChosen(Map.KothMap.value.Oasis))

        self.radioKothGroup.addButton(map_button_busan)
        self.radioKothGroup.addButton(map_button_ilios)
        self.radioKothGroup.addButton(map_button_lijiang)
        self.radioKothGroup.addButton(map_button_nepal)
        self.radioKothGroup.addButton(map_button_oasis)

        koth_layout = QVBoxLayout()
        koth_layout.addWidget(map_selection_back)
        koth_layout.addWidget(map_button_busan)
        koth_layout.addWidget(map_button_ilios)
        koth_layout.addWidget(map_button_lijiang)
        koth_layout.addWidget(map_button_nepal)
        koth_layout.addWidget(map_button_oasis)

        self.kothMapsBox.setLayout(koth_layout)

    def createPushMapsBox(self):
        map_selection_back = QPushButton('Back to Mode select')
        map_selection_back.clicked.connect(self.mapSelect_back)

        map_button_esperanca = QRadioButton('Esperanca')
        map_button_esperanca.clicked.connect(lambda: self.game.mapChosen(Map.PushMap.value.Esperanca))
        map_button_rome = QRadioButton('Rome')
        map_button_rome.clicked.connect(lambda: self.game.mapChosen(Map.PushMap.value.Colosseo))
        map_button_toronto = QRadioButton('Toronto')
        map_button_toronto.clicked.connect(lambda: self.game.mapChosen(Map.PushMap.value.NewQueenStreet))

        self.radioPushGroup.addButton(map_button_esperanca)
        self.radioPushGroup.addButton(map_button_rome)
        self.radioPushGroup.addButton(map_button_toronto)

        push_layout = QVBoxLayout()
        push_layout.addWidget(map_selection_back)
        push_layout.addWidget(map_button_toronto)
        push_layout.addWidget(map_button_esperanca)
        push_layout.addWidget(map_button_rome)

        self.pushMapsBox.setLayout(push_layout)

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
        self.game.mapIsSelected.val = False
        if not self.compPlaying.isChecked():
            self.teamGroupBox.setVisible(True)
            self.game.teamIsChosen.val = False
        else:
            self.resultDraw.setVisible(True)

    def createSocialGroupBox(self):
        voice_combo_str = QLabel('# in vc')
        voice_combo_str.setToolTip('How many people are in the team voicechat (including you and your group)?')
        self.voiceCombo.addItems(map(str, range(0, 6)))
        self.voiceCombo.currentIndexChanged.connect(lambda: self.game.voiceChanged(self.voiceCombo.currentText()))

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(voice_combo_str)
        layout.addWidget(self.voiceCombo)
        layout.addStretch()
        layout.addWidget(QLabel('Comment:'))
        layout.addWidget(self.comment)
        layout.addStretch()

        self.socialGroupBox.setLayout(layout)

    def createResultBox(self):
        self.resultVictory.clicked.connect(lambda: self.game.resultChanged(Result.Victory))
        self.resultVictory.setIcon(QtGui.QIcon('pictures/victory_transparent.png'))
        self.resultVictory.setIconSize(QtCore.QSize(100, 40))
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
        open_last_game = QPushButton('Open last game')
        open_last_game.clicked.connect(lambda: self.openLastClicked(False))

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(open_last_game)
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
        player_name = str.strip(self.player.text())
        if re.search(r'\S', player_name):
            self.game.player = Player(player_name)
            self.currentPlayer = self.game.player
            self.setToStatsScreen()
        else:
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
        [valid, errors] = self.game.gameValid()
        if valid is False:
            str_of_errors = ""
            for error in errors:
                str_of_errors += error + "\n"
            self.errorWindow(str_of_errors)
        else:
            self.game.comment = self.comment.text()
            self.doc.addGame(self.game)
            self.setToStatsScreen()
            self.initialize()

    def errorWindow(self, error_text: str):
        self.error = ErrorWindow(error_text)
        self.error.show()

    def groupSizeChanged(self, group_size: int):
        self.ownVoicechat.clear()
        self.ownVoicechat.addItems(map(str, range(0, group_size + 1)))
        self.ownVoicechat.setCurrentIndex(group_size)
        self.voiceCombo.clear()
        self.voiceCombo.addItems(map(str, range(group_size, 6)))
        self.voiceCombo.setCurrentIndex(0)

    def ownVoiceChanged(self, own_voice: str):
        self.voiceCombo.clear()
        if own_voice != "":
            self.voiceCombo.addItems(map(str,range(int(own_voice), 6)))

    def openLastClicked(self, confirmed: bool):
        if not confirmed:
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

            # Game mode and Map
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
    def __init__(self, error_text: str):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel(error_text)
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
