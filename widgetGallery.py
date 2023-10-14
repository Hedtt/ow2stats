from PyQt5.QtCore import QObject, QDateTime, QDate
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QAbstractButton, QDateEdit, QButtonGroup, QMainWindow, QMenuBar,
                             QDockWidget, QMenu, QAction, QMessageBox, QFrame)
import re
from sheets import *
from player import *
from game import *
from areYouSure import showConfirm


# noinspection PyUnresolvedReferences
class WidgetGallery(QMainWindow):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.check_button_save_queue = None
        self.missing_params = QLabel()
        self.resultDefeat = QPushButton()
        self.resultVictory = QPushButton()
        self.modeButtonPush = QPushButton('Push')
        self.modeButtonKoth = QPushButton('Koth')
        self.modeButtonHybrid = QPushButton('Hybrid')
        self.modeButtonEscort = QPushButton('Escort')
        self.modeButtonFlashpoint = QPushButton('Flashpoint')
        self.peoplePlaying = QComboBox()
        self.dateEdit = QDateEdit()
        self.game = None
        self.comment = QLineEdit()
        self.doc = GDoc()
        self.currentPlayer = None
        self.currentVersion = open('setup/version').read()
        self.setWindowTitle(f'Ow2Stats Version {self.currentVersion}')
        self.saveQueue = False

        self.voiceCombo = QComboBox()
        self.ownVoicechat = QComboBox()
        self.radioPushGroup = QButtonGroup()
        self.radioKothGroup = QButtonGroup()
        self.radioEscortGroup = QButtonGroup()
        self.radioHybridGroup = QButtonGroup()
        self.radioFlashpointGroup = QButtonGroup()
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
        self.flashpointMapsBox = QGroupBox('Flashpoint')
        self.flashpointMapsBox.setVisible(False)

        self.teamGroupBox = QGroupBox('Team')
        self.modeGroupBox = QGroupBox('Mode')
        self.mapGroupBox = QGroupBox('Map')
        self.roleGroupBox = QGroupBox('Role')

        self.createRoleGroupBox()
        self.createTeamGroupBox()
        self.createGeneralBox()
        self.createModeGroupBox()
        self.createEscortMapsBox()
        self.createHybridMapsBox()
        self.createKothMapsBox()
        self.createPushMapsBox()
        self.createFlashpointMapsBox()
        self.createSocialGroupBox()
        self.createResultBox()
        self.createSubmitBox()
        self.createMainScreen()

        self._createActions()
        self._createMenuBar()

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
        main_layout.addWidget(self.flashpointMapsBox, 2,0)
        main_layout.addWidget(self.teamGroupBox, 3, 0)
        main_layout.addWidget(self.socialGroupBox, 4, 0)
        main_layout.addWidget(self.resultBox, 5, 0)
        main_layout.addWidget(self.submitBox, 6, 0)
        self.setCentralWidget(widget)
        # self.setLayout(main_layout)

        self.initialize()

        self.setToStartScreen()

    def _createActions(self):
        """
        create actions for the toolbar
        """
        self.patchNotesAction = QAction("Patch Notes", self)
        self.patchNotesAction.triggered.connect(self.openPatchNotes)
        self.helpAction = QAction("Help", self)

        self.delAction = QAction("Delete current game data", self)
        self.delAction.triggered.connect(self.initialize)

        self.openLastAction = QAction("Open last game", self)
        self.openLastAction.triggered.connect(lambda: self.openLastClicked(False))

    def _createMenuBar(self):
        """
        create the menu bar and add the actions to the corresponding submenus
        """
        menu_bar = self.menuBar()

        game_menu = menu_bar.addMenu("Game")
        game_menu.addAction(self.delAction)
        game_menu.addAction(self.openLastAction)

        about_menu = menu_bar.addMenu("About")
        about_menu.addAction(self.patchNotesAction)
        about_menu.addAction(self.helpAction)

    def initialize(self):
        """
        set up a new game
        """
        # save old queue
        if self.saveQueue:
            tmp = self.game.roleQueue
        else:
            tmp = None

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

        # Save Queue if clicked
        if tmp is not None:
            for role in tmp:
                if role == Role.Tank:
                    self.check_button_queued_tank.setChecked(True)
                elif role == Role.Dps:
                    self.check_button_queued_dps.setChecked(True)
                else:
                    self.check_button_queued_support.setChecked(True)


        # Map reset
        self.mapSelect_back()

        # Social reset
        self.peoplePlaying.setCurrentIndex(self.peoplePlaying.currentIndex())
        self.game.groupSizeChanged(self.peoplePlaying.currentIndex()+1)
        self.ownVoicechat.setCurrentIndex(self.ownVoicechat.currentIndex())
        self.game.ownVoiceChanged(self.ownVoicechat.currentIndex())
        self.voiceCombo.setCurrentIndex(self.ownVoicechat.currentIndex())
        self.comment.setText('')

        # Unset color from result screen
        self.resultVictory.setStyleSheet("background-color: none")
        self.resultDefeat.setStyleSheet("background-color: none")
        self.resultDraw.setStyleSheet("background-color: none")

        # Set submit uncheckable
        self.submit.setDisabled(True)
        self.someParamChanged()

    def setToStartScreen(self):
        """
        start screen that only pops up when launching the application where the user puts in their name
        """
        self.mainScreen.setVisible(True)
        self.generalBox.setVisible(False)
        self.roleGroupBox.setVisible(False)
        self.modeGroupBox.setVisible(False)
        self.escortMapsBox.setVisible(False)
        self.hybridMapsBox.setVisible(False)
        self.kothMapsBox.setVisible(False)
        self.pushMapsBox.setVisible(False)
        self.flashpointMapsBox.setVisible(False)
        self.teamGroupBox.setVisible(False)
        self.socialGroupBox.setVisible(False)
        self.resultBox.setVisible(False)
        self.submitBox.setVisible(False)
        self.mainScreen.adjustSize()

        self.menuBar().setVisible(False)

    def setToStatsScreen(self):
        """
        main window of the application
        """
        self.mainScreen.setVisible(False)
        self.generalBox.setVisible(True)
        self.roleGroupBox.setVisible(True)
        self.modeGroupBox.setVisible(True)
        self.teamGroupBox.setVisible(True)
        self.socialGroupBox.setVisible(True)
        self.resultBox.setVisible(True)
        self.submitBox.setVisible(True)

        self.menuBar().setVisible(True)

    def createGeneralBox(self):
        """
        creates the top most box with date, group size, voice in group, comp
        """
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
        # noinspection PyUnresolvedReferences
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
        """
        what role is played -> display that role, what role is queued?
        """
        radio_button_tank = QRadioButton('Tank')
        radio_button_tank.clicked.connect(lambda: self.chooseRole(radio_button_tank.text()))
        radio_button_tank.clicked.connect(lambda: self.game.roleChosen(Role.Tank))
        radio_button_tank.clicked.connect(self.someParamChanged)
        radio_button_dps = QRadioButton('Dps')
        radio_button_dps.clicked.connect(lambda: self.game.roleChosen(Role.Dps))
        radio_button_dps.clicked.connect(lambda: self.chooseRole(radio_button_dps.text()))
        radio_button_dps.clicked.connect(self.someParamChanged)
        radio_button_support = QRadioButton('Support')
        radio_button_support.clicked.connect(lambda: self.game.roleChosen(Role.Support))
        radio_button_support.clicked.connect(lambda: self.chooseRole(radio_button_support.text()))
        radio_button_support.clicked.connect(self.someParamChanged)


        self.radioGroupRole.addButton(radio_button_tank)
        self.radioGroupRole.addButton(radio_button_dps)
        self.radioGroupRole.addButton(radio_button_support)

        # what role is queued?
        self.check_button_queued_tank = QCheckBox('Tank')
        self.check_button_queued_tank.stateChanged.connect(lambda: self.game.roleQueuedChanged(Role.Tank))
        self.check_button_queued_tank.stateChanged.connect(self.someParamChanged)
        self.check_button_queued_dps = QCheckBox('Dps')
        self.check_button_queued_dps.stateChanged.connect(lambda: self.game.roleQueuedChanged(Role.Dps))
        self.check_button_queued_dps.stateChanged.connect(self.someParamChanged)
        self.check_button_queued_support = QCheckBox('Support')
        self.check_button_queued_support.stateChanged.connect(lambda: self.game.roleQueuedChanged(Role.Support))
        self.check_button_queued_support.stateChanged.connect(self.someParamChanged)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        # separator.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
        separator.setLineWidth(1)
        separator.setFrameShadow(QFrame.Sunken)
        self.check_button_save_queue = QCheckBox('Save Queue')
        self.check_button_save_queue.stateChanged.connect(self.saveQueueChanged)


        self.checkGroupRoleQueue.addButton(self.check_button_queued_tank)
        self.checkGroupRoleQueue.addButton(self.check_button_queued_dps)
        self.checkGroupRoleQueue.addButton(self.check_button_queued_support)

        # set up pictures for role played
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
        layout_queue.addWidget(self.check_button_queued_tank)
        layout_queue.addWidget(self.check_button_queued_dps)
        layout_queue.addWidget(self.check_button_queued_support)
        layout_queue.addWidget(separator)
        layout_queue.addWidget(self.check_button_save_queue)
        main_layout = QHBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(tank_role_image_layout)
        main_layout.addLayout(dps_role_image_layout)
        main_layout.addLayout(support_role_image_layout)
        main_layout.addLayout(layout_queue)
        self.roleGroupBox.setLayout(main_layout)

    def createModeGroupBox(self):
        self.modeButtonEscort.clicked.connect(self.modeEscort_clicked)
        self.modeButtonEscort.clicked.connect(lambda: self.game.gameModeChosen(GameMode.Escort))
        self.modeButtonHybrid.clicked.connect(self.modeHybrid_clicked)
        self.modeButtonHybrid.clicked.connect(lambda: self.game.gameModeChosen(GameMode.Hybrid))
        self.modeButtonKoth.clicked.connect(self.modeKoth_clicked)
        self.modeButtonKoth.clicked.connect(lambda: self.game.gameModeChosen(GameMode.Koth))
        self.modeButtonPush.clicked.connect(self.modePush_clicked)
        self.modeButtonPush.clicked.connect(lambda: self.game.gameModeChosen(GameMode.Push))
        self.modeButtonFlashpoint.clicked.connect(self.modeFlashpoint_clicked)
        self.modeButtonFlashpoint.clicked.connect(lambda: self.game.gameModeChosen(GameMode.Flashpoint))
        layout = QHBoxLayout()
        layout.addWidget(self.modeButtonEscort)
        layout.addWidget(self.modeButtonHybrid)
        layout.addWidget(self.modeButtonKoth)
        layout.addWidget(self.modeButtonPush)
        layout.addWidget(self.modeButtonFlashpoint)

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

    def modeFlashpoint_clicked(self):
        self.modeGroupBox.setVisible(False)
        self.teamGroupBox.setVisible(False)
        self.game.teamChosen(Team.NoTeam)
        self.flashpointMapsBox.setVisible(True)
        self.resultDraw.setVisible(False)

    def createTeamGroupBox(self):
        team_button_attack = QRadioButton('Attack')
        team_button_attack.clicked.connect(lambda: self.game.teamChosen(Team.Attack))
        team_button_attack.clicked.connect(self.someParamChanged)

        team_button_defense = QRadioButton('Defense')
        team_button_defense.clicked.connect(lambda: self.game.teamChosen(Team.Defense))
        team_button_defense.clicked.connect(self.someParamChanged)

        self.radioGroupTeam.addButton(team_button_attack)
        self.radioGroupTeam.addButton(team_button_defense)

        layout = QVBoxLayout()
        layout.addWidget(team_button_attack)
        layout.addWidget(team_button_defense)

        self.teamGroupBox.setLayout(layout)

    def comp_clicked(self, state):
        self.someParamChanged()
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

        map_button_circuit = QRadioButton('Circuit Royal')
        map_button_circuit.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.CircuitRoyal))
        map_button_circuit.clicked.connect(self.someParamChanged)

        map_button_dorado = QRadioButton('Dorado')
        map_button_dorado.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Dorado))
        map_button_dorado.clicked.connect(self.someParamChanged)

        map_button_havana = QRadioButton('Havana')
        map_button_havana.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Havana))
        map_button_havana.clicked.connect(self.someParamChanged)

        map_button_junkertown = QRadioButton('Junkertown')
        map_button_junkertown.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Junkertown))
        map_button_junkertown.clicked.connect(self.someParamChanged)

        map_button_rialto = QRadioButton('Rialto')
        map_button_rialto.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Rialto))
        map_button_rialto.clicked.connect(self.someParamChanged)

        map_button_route66 = QRadioButton('Route 66')
        map_button_route66.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Route))
        map_button_route66.clicked.connect(self.someParamChanged)

        map_button_shambali = QRadioButton('Shambali')
        map_button_shambali.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Shambali))
        map_button_shambali.clicked.connect(self.someParamChanged)

        map_button_watchpoint_gibraltar = QRadioButton('Watchpoint: Gibraltar')
        map_button_watchpoint_gibraltar.clicked.connect(lambda: self.game.mapChosen(Map.EscortMap.value.Gibraltar))
        map_button_watchpoint_gibraltar.clicked.connect(self.someParamChanged)

        self.radioEscortGroup.addButton(map_button_circuit)
        self.radioEscortGroup.addButton(map_button_dorado)
        self.radioEscortGroup.addButton(map_button_havana)
        self.radioEscortGroup.addButton(map_button_junkertown)
        self.radioEscortGroup.addButton(map_button_rialto)
        self.radioEscortGroup.addButton(map_button_route66)
        self.radioEscortGroup.addButton(map_button_shambali)
        self.radioEscortGroup.addButton(map_button_watchpoint_gibraltar)

        escort_layout = QVBoxLayout()
        escort_layout.addWidget(map_selection_back)
        escort_layout.addWidget(map_button_circuit)
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
        map_button_blizzard_world.clicked.connect(self.someParamChanged)

        map_button_eichenwalde = QRadioButton('Eichenwalde')
        map_button_eichenwalde.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.Eichenwalde))
        map_button_eichenwalde.clicked.connect(self.someParamChanged)

        map_button_hollywood = QRadioButton('Hollywood')
        map_button_hollywood.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.Hollywood))
        map_button_hollywood.clicked.connect(self.someParamChanged)

        map_button_kings_row = QRadioButton('King\'s Row')
        map_button_kings_row.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.KingsRow))
        map_button_kings_row.clicked.connect(self.someParamChanged)

        map_button_new_york = QRadioButton('Midtown')
        map_button_new_york.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.Midtown))
        map_button_new_york.clicked.connect(self.someParamChanged)

        map_button_numbani = QRadioButton('Numbani')
        map_button_numbani.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.Numbani))
        map_button_numbani.clicked.connect(self.someParamChanged)

        map_button_paraiso = QRadioButton('Paraiso')
        map_button_paraiso.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.Paraiso))
        map_button_paraiso.clicked.connect(self.someParamChanged)

        map_button_rio_de_janeiro = QRadioButton('Rio de Janeiro')
        map_button_rio_de_janeiro.clicked.connect(lambda: self.game.mapChosen(Map.HybridMap.value.RioDeJaneiro))
        map_button_rio_de_janeiro.clicked.connect(self.someParamChanged)

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

        map_button_peninsula = QRadioButton('Antarctic Peninsula')
        map_button_peninsula.clicked.connect(lambda: self.game.mapChosen(Map.KothMap.value.Peninsula))
        map_button_peninsula.clicked.connect(self.someParamChanged)
        map_button_busan = QRadioButton('Busan')
        map_button_busan.clicked.connect(lambda: self.game.mapChosen(Map.KothMap.value.Busan))
        map_button_busan.clicked.connect(self.someParamChanged)

        map_button_ilios = QRadioButton('Ilios')
        map_button_ilios.clicked.connect(lambda: self.game.mapChosen(Map.KothMap.value.Ilios))
        map_button_ilios.clicked.connect(self.someParamChanged)

        map_button_lijiang = QRadioButton('Lijiang Tower')
        map_button_lijiang.clicked.connect(lambda: self.game.mapChosen(Map.KothMap.value.Lijiang))
        map_button_lijiang.clicked.connect(self.someParamChanged)

        map_button_nepal = QRadioButton('Nepal')
        map_button_nepal.clicked.connect(lambda: self.game.mapChosen(Map.KothMap.value.Nepal))
        map_button_nepal.clicked.connect(self.someParamChanged)

        map_button_oasis = QRadioButton('Oasis')
        map_button_oasis.clicked.connect(lambda: self.game.mapChosen(Map.KothMap.value.Oasis))
        map_button_oasis.clicked.connect(self.someParamChanged)

        map_button_samoa = QRadioButton('Samoa')
        map_button_samoa.clicked.connect(lambda: self.game.mapChosen(Map.KothMap.value.Samoa))
        map_button_samoa.clicked.connect(self.someParamChanged)


        self.radioKothGroup.addButton(map_button_peninsula)
        self.radioKothGroup.addButton(map_button_busan)
        self.radioKothGroup.addButton(map_button_ilios)
        self.radioKothGroup.addButton(map_button_lijiang)
        self.radioKothGroup.addButton(map_button_nepal)
        self.radioKothGroup.addButton(map_button_oasis)
        self.radioKothGroup.addButton(map_button_samoa)

        koth_layout = QVBoxLayout()
        koth_layout.addWidget(map_selection_back)
        koth_layout.addWidget(map_button_peninsula)
        koth_layout.addWidget(map_button_busan)
        koth_layout.addWidget(map_button_ilios)
        koth_layout.addWidget(map_button_lijiang)
        koth_layout.addWidget(map_button_nepal)
        koth_layout.addWidget(map_button_oasis)
        koth_layout.addWidget(map_button_samoa)

        self.kothMapsBox.setLayout(koth_layout)

    def createPushMapsBox(self):
        map_selection_back = QPushButton('Back to Mode select')
        map_selection_back.clicked.connect(self.mapSelect_back)

        map_button_esperanca = QRadioButton('Esperanca')
        map_button_esperanca.clicked.connect(lambda: self.game.mapChosen(Map.PushMap.value.Esperanca))
        map_button_esperanca.clicked.connect(self.someParamChanged)

        map_button_rome = QRadioButton('Rome')
        map_button_rome.clicked.connect(lambda: self.game.mapChosen(Map.PushMap.value.Colosseo))
        map_button_rome.clicked.connect(self.someParamChanged)

        map_button_toronto = QRadioButton('Toronto')
        map_button_toronto.clicked.connect(lambda: self.game.mapChosen(Map.PushMap.value.NewQueenStreet))
        map_button_toronto.clicked.connect(self.someParamChanged)

        self.radioPushGroup.addButton(map_button_esperanca)
        self.radioPushGroup.addButton(map_button_rome)
        self.radioPushGroup.addButton(map_button_toronto)

        push_layout = QVBoxLayout()
        push_layout.addWidget(map_selection_back)
        push_layout.addWidget(map_button_toronto)
        push_layout.addWidget(map_button_esperanca)
        push_layout.addWidget(map_button_rome)

        self.pushMapsBox.setLayout(push_layout)

    def createFlashpointMapsBox(self):
        map_selection_back = QPushButton('Back to Mode select')
        map_selection_back.clicked.connect(self.mapSelect_back)

        map_button_newjunkcity = QRadioButton('New Junk City')
        map_button_newjunkcity.clicked.connect(lambda: self.game.mapChosen(Map.FlashpointMap.value.NewJunkCity))
        map_button_newjunkcity.clicked.connect(self.someParamChanged)

        map_button_suravasa = QRadioButton('Suravasa')
        map_button_suravasa.clicked.connect(lambda: self.game.mapChosen(Map.FlashpointMap.value.Suravasa))
        map_button_suravasa.clicked.connect(self.someParamChanged)

        self.radioFlashpointGroup.addButton(map_button_newjunkcity)
        self.radioFlashpointGroup.addButton(map_button_suravasa)

        flashpoint_layout = QVBoxLayout()
        flashpoint_layout.addWidget(map_selection_back)
        flashpoint_layout.addWidget(map_button_newjunkcity)
        flashpoint_layout.addWidget(map_button_suravasa)

        self.flashpointMapsBox.setLayout(flashpoint_layout)

    def mapSelect_back(self):
        # Button reset
        self.radioEscortGroup.setExclusive(False)
        self.radioHybridGroup.setExclusive(False)
        self.radioKothGroup.setExclusive(False)
        self.radioPushGroup.setExclusive(False)
        self.radioFlashpointGroup.setExclusive(False)
        if self.radioEscortGroup.checkedButton() is not None:
            self.radioEscortGroup.checkedButton().setChecked(False)
        if self.radioHybridGroup.checkedButton() is not None:
            self.radioHybridGroup.checkedButton().setChecked(False)
        if self.radioKothGroup.checkedButton() is not None:
            self.radioKothGroup.checkedButton().setChecked(False)
        if self.radioPushGroup.checkedButton() is not None:
            self.radioPushGroup.checkedButton().setChecked(False)
        if self.radioFlashpointGroup.checkedButton() is not None:
            self.radioFlashpointGroup.checkedButton().setChecked(False)
        self.radioEscortGroup.setExclusive(True)
        self.radioHybridGroup.setExclusive(True)
        self.radioKothGroup.setExclusive(True)
        self.radioPushGroup.setExclusive(True)
        self.radioFlashpointGroup.setExclusive(True)

        # Ui reset
        self.modeGroupBox.setVisible(True)
        self.escortMapsBox.setVisible(False)
        self.hybridMapsBox.setVisible(False)
        self.kothMapsBox.setVisible(False)
        self.pushMapsBox.setVisible(False)
        self.flashpointMapsBox.setVisible(False)
        self.game.mapIsSelected.val = False
        if not self.compPlaying.isChecked():
            self.teamGroupBox.setVisible(True)
            self.game.teamIsChosen.val = False
        else:
            self.resultDraw.setVisible(True)

        self.someParamChanged()

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
        def toggle_selected(result: Result):
            if result == Result.Victory:
                self.resultVictory.setStyleSheet("background-color: black")
                self.resultDefeat.setStyleSheet("background-color: none")
                self.resultDraw.setStyleSheet("background-color: none")
            elif result == Result.Defeat:
                self.resultVictory.setStyleSheet("background-color: none")
                self.resultDefeat.setStyleSheet("background-color: black")
                self.resultDraw.setStyleSheet("background-color: none")
            elif result == Result.Draw:
                self.resultVictory.setStyleSheet("background-color: none")
                self.resultDefeat.setStyleSheet("background-color: none")
                self.resultDraw.setStyleSheet("background-color: black")

        self.resultVictory.clicked.connect(lambda: self.game.resultChanged(Result.Victory))
        self.resultVictory.clicked.connect(self.someParamChanged)
        self.resultVictory.setIcon(QtGui.QIcon('pictures/victory_transparent.png'))
        self.resultVictory.setIconSize(QtCore.QSize(100, 40))
        self.resultVictory.clicked.connect(lambda: toggle_selected(Result.Victory))

        self.resultDefeat.clicked.connect(lambda: self.game.resultChanged(Result.Defeat))
        self.resultDefeat.clicked.connect(self.someParamChanged)
        self.resultDefeat.setIcon(QtGui.QIcon('pictures/defeat_transparent.png'))
        self.resultDefeat.setIconSize(QtCore.QSize(100, 40))
        self.resultDefeat.clicked.connect(lambda: toggle_selected(Result.Defeat))

        self.resultDraw.clicked.connect(lambda: self.game.resultChanged(Result.Draw))
        self.resultDraw.clicked.connect(self.someParamChanged)
        self.resultDraw.setIcon(QtGui.QIcon('pictures/draw_transparent.png'))
        self.resultDraw.setIconSize(QtCore.QSize(100, 40))
        self.resultDraw.setVisible(False)
        self.resultDraw.clicked.connect(lambda: toggle_selected(Result.Draw))




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
        self.submit = QPushButton('Submit')
        self.submit.clicked.connect(self.submitClicked)

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.missing_params)
        layout.addStretch()
        layout.addWidget(self.submit)
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
            name_error = QMessageBox()
            name_error.setText("Invalid username!")
            name_error.setWindowTitle("Error!")
            # nameError.setStandardButtons(QMessageBox.Ok)
            retval = name_error.exec_()

    def chooseRole(self, role: str):
        self.someParamChanged()
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
            errors = QMessageBox()
            errors.setText("One or more things are missing!")
            errors.setDetailedText(str_of_errors)
            errors.setWindowTitle("Error!")
            errors.exec_()
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
            self.voiceCombo.addItems(map(str, range(int(own_voice), 6)))

    def openLastClicked(self, confirmed: bool):
        if not confirmed:
            retval = showConfirm()
            if retval == 1024:
                self.openLastClicked(True)
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
            elif game.gameMode == 'Flashpoint':
                self.modeButtonFlashpoint.click()
                for flashopintMap in self.radioFlashpointGroup.buttons():
                    if flashopintMap.text() == game.mapPlayed:
                        flashopintMap.click()
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

    def someParamChanged(self):
        [valid, errors] = self.game.gameValid()
        if valid is False:
            str_of_errors = ""
            for error in errors:
                str_of_errors += error + "\n"
            self.missing_params.setText(str_of_errors)
        else:
            self.missing_params.setText('All inputs are valid')
            self.submit.setDisabled(False)

    def saveQueueChanged(self):
        if self.check_button_save_queue.isChecked() and self.game.roleQueue is not None:
            self.saveQueue = True
        else:
            self.saveQueue = False


    @staticmethod
    def openPatchNotes():
        patch_notes = QMessageBox()
        patch_notes.setIcon(QMessageBox.Information)

        with open('patchNotes', 'r') as file:
            all_patches = file.read()
        patches_list = re.split("(\d+.\d+.\d+:)", all_patches)
        patch_notes.setText(patches_list[1]+patches_list[2])
        patch_notes.setDetailedText(all_patches)
        patch_notes.setWindowTitle("Patch Notes")
        patch_notes.setStandardButtons(QMessageBox.Close)

        patch_notes.exec_()
