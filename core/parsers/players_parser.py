from bs4 import BeautifulSoup

from core.models import Player, Matchday, Season, Country, PlayerUserOwnership
from core.parsers.base_parser import BaseParser


class PlayersParser(BaseParser):
    def __init__(self, html_source, user):
        self.html_source = html_source
        self.user = user

    def parse(self):
        soup = BeautifulSoup(self.html_source, "html.parser")
        return self.parse_players_html(soup)

    def parse_players_html(self, soup):
        """
        :param soup: BeautifulSoup of player page
        :return: parsed players
        :rtype: list
        """
        players_table = soup.find(id="playerTable").tbody
        player_list = players_table.find_all('tr')  # 1 row per player
        return [self.parse_player_row(player_row) for player_row in player_list]

    def parse_player_row(self, player_row):
        matchday = Matchday.objects.all()[0]
        player_values = self._filter_invalid_cells(player_row.find_all('td'))
        ofm_id = player_row.find_all('input', class_='playerid')[0]['value']
        name = player_values[6].a.get_text().replace('\n', '').replace('\t', '').strip(' ')
        position = player_values[5].find_all('span')[1].get_text()
        age = int(player_values[7].get_text())
        birth_season, success = Season.objects.get_or_create(number=matchday.season.number - age)

        displayed_country = player_values[8].get_text().replace('\n', '').replace('\t', '').strip(' ')
        country_name = ''.join([i for i in displayed_country if not i.isdigit()])
        country_choices = dict(Country._meta.get_field('country').choices)
        country_no = list(country_choices.keys())[list(country_choices.values()).index(country_name)]
        nationality, success = Country.objects.get_or_create(country=country_no)

        player, success = Player.objects.get_or_create(
            id=ofm_id,
            name=name,
            position=position,
            birth_season=birth_season,
            nationality=nationality
        )

        self._create_player_user_ownership(player, matchday)

        return player

    def _create_player_user_ownership(self, player, matchday):
        existing_contracts = PlayerUserOwnership.objects.filter(player=player, user=self.user, sold_on_matchday=None)
        
        if existing_contracts.count() > 0:
            contract = existing_contracts[0]
        else:
            contract, success = PlayerUserOwnership.objects.get_or_create(player=player, user=self.user, bought_on_matchday=matchday)

        return contract
