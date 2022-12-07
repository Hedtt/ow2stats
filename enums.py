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
        Dorado = 1
        Havana = 2
        Junkertown = 3
        Rialto = 4
        Route = 5
        Shambali = 6
        Gibraltar = 7

    class HybridMap(Enum):
        BlizzardWorld = 1
        Eichenwalde = 2
        Hollywood = 3
        KingsRow = 4
        NYC = 5
        Numbani = 6
        RioDeJaneiro = 7
        Paraiso = 8

    class KothMap(Enum):
        Busan = 1
        Ilios = 2
        Lijiang = 3
        Nepal = 4
        Oasis = 5

    class PushMap(Enum):
        Esperanca = 1
        Rome = 2
        Toronto = 3
