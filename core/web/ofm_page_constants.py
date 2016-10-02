class Constants:
    BASE = 'http://www.onlinefussballmanager.de'
    HEAD = 'http://www.onlinefussballmanager.de/head-int.php'
    AWP_BOUNDARIES = 'http://www.ofm-forum.de/showthread.php?91605-aktuelle-Aufwertungsgrenzen/page9999'

    class Office:
        pass
    OFFICE = Office()
    OFFICE.OFFICE = 'http://www.onlinefussballmanager.de/office/buero.php'
    OFFICE.TEAM_INFO = 'http://www.onlinefussballmanager.de/league/teaminfo.php'
    OFFICE.INGAME_EMAIL = 'http://www.onlinefussballmanager.de/user/ingamemail/index.php'
    OFFICE.NOTES = 'http://www.onlinefussballmanager.de/user/ingamemail/index.php?page=notizen'
    OFFICE.BETTING = 'http://www.onlinefussballmanager.de/office/wetten.php'
    OFFICE.HISTORY = 'http://www.onlinefussballmanager.de/office/history.php'
    OFFICE.OFM_HISTORY = 'http://www.onlinefussballmanager.de/office/ofm_history.php'
    OFFICE.PROFILE = 'http://www.onlinefussballmanager.de/user/profil.php'

    class Team:
        pass
    TEAM = Team()
    TEAM.PLAYERS = 'http://www.onlinefussballmanager.de/team/players.php'
    TEAM.LINEUP = 'http://www.onlinefussballmanager.de/team/aufstellung2d.php?game=liga'
    TEAM.FRIENDLY_LINEUP = 'http://www.onlinefussballmanager.de/team/aufstellung2d.php?game=friendly'
    TEAM.CUP_LINEUP = 'http://www.onlinefussballmanager.de/team/aufstellung2d.php?game=pokal'
    TEAM.FUNCUP_LINEUP = 'http://www.onlinefussballmanager.de/team/aufstellung2d.php?game=funcup'
    TEAM.WORLD_CUP_LINEUP = 'http://www.onlinefussballmanager.de/team/aufstellung2d.php?game=world_cup'
    TEAM.TRAINING = 'http://www.onlinefussballmanager.de/team/training_2011.php'
    TEAM.PLAYER_STATISTICS = 'http://www.onlinefussballmanager.de/team/players-statistics.php'
    TEAM.YOUTH = 'http://www.onlinefussballmanager.de/team/youth.php'

    class Transfer:
        pass
    TRANSFER = Transfer()
    TRANSFER.OFFERS = 'http://www.onlinefussballmanager.de/transfer/angebote.php'
    TRANSFER.AMATEURS = 'http://www.onlinefussballmanager.de/transfer/amas.php'
    TRANSFER.TRANSFER_MARKET = 'http://www.onlinefussballmanager.de/transfer/transfermarkt.php'
    TRANSFER.PLAYERSWITCH = 'http://www.onlinefussballmanager.de/transfer/spielerwechsel.php'
    TRANSFER.BIDDING = 'http://www.onlinefussballmanager.de/transfer/transfer_gebote.php'
    TRANSFER.AWP_CALCULATOR = 'http://www.onlinefussballmanager.de/010_transfer/awp_rechner_noplus.php'
    TRANSFER.MARKET_VALUES = 'http://www.onlinefussballmanager.de/transfer/marketvalues.php'

    class Stadium:
        pass
    STADIUM = Stadium()
    STADIUM.OVERVIEW = 'http://www.onlinefussballmanager.de/stadium/stadium.php'
    STADIUM.SPECTATORS = 'http://www.onlinefussballmanager.de/stadium/zuschauer.php'
    STADIUM.ENVIRONMENT = 'http://www.onlinefussballmanager.de/stadium/stadium-environment.php'

    class Finances:
        pass
    FINANCES = Finances()
    FINANCES.OVERVIEW = 'http://www.onlinefussballmanager.de/finances/finanzen.php'
    FINANCES.BANK = 'http://www.onlinefussballmanager.de/finances/bank.php'
    FINANCES.SPONSOR = 'http://www.onlinefussballmanager.de/finances/spon_waehlen.php'

    class League:
        pass
    LEAGUE = League()
    LEAGUE.MATCHDAY_TABLE = 'http://www.onlinefussballmanager.de/league/spieltag_tabelle_2.php'
    LEAGUE.LINEUP = 'http://www.onlinefussballmanager.de/team/aufstellung2d.php?game=liga'
    LEAGUE.TOPSTARS = 'http://www.onlinefussballmanager.de/league/bestespieler.php'
    LEAGUE.GOAL_SCORERS = 'http://www.onlinefussballmanager.de/league/torschuetzen.php'
    LEAGUE.TACKLINGS = 'http://www.onlinefussballmanager.de/league/bestezwk.php'
    LEAGUE.BAN_OR_INJURY = 'http://www.onlinefussballmanager.de/league/sperrenstatistik.php'
    LEAGUE.FAIRPLAY = 'http://www.onlinefussballmanager.de/league/fairplay.php'
    LEAGUE.STADIUMS = 'http://www.onlinefussballmanager.de/league/ligastadien.php'
    LEAGUE.TEAMS = 'http://www.onlinefussballmanager.de/league/teamstatistik3.php'
    LEAGUE.MATCH_SCHEDULE = 'http://www.onlinefussballmanager.de/league/teaminfo.php'
    LEAGUE.SEASON_PATHWAY = 'http://www.onlinefussballmanager.de/league/saisonverlauf.php'

    class OfmCup:
        pass
    OFM_CUP = OfmCup()
    OFM_CUP.MATCH_SCHEDULE = 'http://www.onlinefussballmanager.de/ofm_cup/pokal2.php'
    OFM_CUP.LINEUP = 'http://www.onlinefussballmanager.de/team/aufstellung2d.php?game=pokal'
    OFM_CUP.SCORERS = 'http://www.onlinefussballmanager.de/ofm_cup/poktorschuetzen.php'
    OFM_CUP.SUSPENDED_PLAYERS = 'http://www.onlinefussballmanager.de/ofm_cup/poksperren.php'
    OFM_CUP.HISTORY = 'http://www.onlinefussballmanager.de/ofm_cup/pokhistory.php'
    OFM_CUP.RULES = 'http://www.onlinefussballmanager.de/ofm_cup/pokregeln2.php'

    class WorldCup:
        pass
    WORLD_CUP = WorldCup()
    WORLD_CUP.MATCH_SCHEDULE = 'http://www.onlinefussballmanager.de/world_cup/worldcup.php'
    WORLD_CUP.LINEUP = 'http://www.onlinefussballmanager.de/team/aufstellung2d.php?game=world_cup'
    WORLD_CUP.SCORERS = 'http://www.onlinefussballmanager.de/world_cup/worldcup-torschuetzen.php'
    WORLD_CUP.SUSPENDED_PLAYERS = 'http://www.onlinefussballmanager.de/world_cup/worldcup-sperren.php'
    WORLD_CUP.HISTORY = 'http://www.onlinefussballmanager.de/world_cup/worldcup-history.php'
    WORLD_CUP.RULES = 'http://www.onlinefussballmanager.de/world_cup/worldcup-regeln.php'

    class FunCup:
        pass
    FUN_CUP = FunCup()
    FUN_CUP.MY_FUN_CUPS = 'http://www.onlinefussballmanager.de/funcups/funcup_meine.php'
    FUN_CUP.SEARCH = 'http://www.onlinefussballmanager.de/funcups/funcup_uebersicht.php'
    FUN_CUP.ORGANIZE = 'http://www.onlinefussballmanager.de/funcups/orga/funcup_organisieren.php?neu=true'
    FUN_CUP.LINEUP = 'http://www.onlinefussballmanager.de/team/aufstellung2d.php?game=funcup'
    FUN_CUP.INSTRUCTIONS = 'http://www.onlinefussballmanager.de/funcups/funcup_anleitung.php'

    class Friendly:
        pass
    FRIENDLY = Friendly()
    FRIENDLY.ORGANIZED = 'http://www.onlinefussballmanager.de/friendlies/organisierte_fr_2.php'
    FRIENDLY.OFFER = 'http://www.onlinefussballmanager.de/friendlies/anbieten_fr.php'
    FRIENDLY.ACCEPT = 'http://www.onlinefussballmanager.de/friendlies/annehmen_fr.php'
    FRIENDLY.LINEUP = 'http://www.onlinefussballmanager.de/team/aufstellung2d.php?game=friendly'

    class Statistics:
        pass
    STATISTICS = Statistics()
    STATISTICS.CLUBS = 'http://www.onlinefussballmanager.de/statistics/vereinsstatistiken.php'
    STATISTICS.TEAM_STRENGTHS = 'http://www.onlinefussballmanager.de/statistics/alleteams.php'
    STATISTICS.TEAM_SALARIES = 'http://www.onlinefussballmanager.de/statistics/teamgehaelter.php'
    STATISTICS.STADIUMS = 'http://www.onlinefussballmanager.de/statistics/allestadien.php'
    STATISTICS.TEAM_EQUITIES = 'http://www.onlinefussballmanager.de/statistics/teams_markwert.php'
    STATISTICS.ETERNAL_CHART = 'http://www.onlinefussballmanager.de/statistics/ewigetabelle.php'
    STATISTICS.SEARCH_ALL = 'http://www.onlinefussballmanager.de/statistics/search_all.php'
    STATISTICS.SEARCH_TEAM = 'http://www.onlinefussballmanager.de/statistics/search_team.php'
    STATISTICS.SEARCH_PLAYER = 'http://www.onlinefussballmanager.de/statistics/search_spieler.php'
