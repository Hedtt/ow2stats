from enum import Enum


class Role(Enum):
    Tank = 1
    Dps = 2
    Support = 3


class GameMode(Enum):
    Escort = 1
    Hybrid = 2
    Koth = 3
    Push = 4
    Flashpoint = 5


class Team(Enum):
    NoTeam = 0
    Attack = 1
    Defense = 2
    Comp = 3


class Result(Enum):
    Victory = 1
    Draw = 2
    Defeat = 3


class Map(Enum):
    class EscortMap(Enum):
        CircuitRoyal = 1
        Dorado = 2
        Havana = 3
        Junkertown = 4
        Rialto = 5
        Route = 6
        Shambali = 7
        Gibraltar = 8

    class HybridMap(Enum):
        BlizzardWorld = 1
        Eichenwalde = 2
        Hollywood = 3
        KingsRow = 4
        Midtown = 5
        Numbani = 6
        Paraiso = 7
        RioDeJaneiro = 8

    class KothMap(Enum):
        Busan = 1
        Ilios = 2
        Lijiang = 3
        Nepal = 4
        Oasis = 5
        Peninsula = 6
        Samoa = 7

    class PushMap(Enum):
        Colosseo = 1
        Esperanca = 2
        NewQueenStreet = 3

    class FlashpointMap(Enum):
        NewJunkCity = 1
        Suravasa = 2
