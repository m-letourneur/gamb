
class Ranking(object):

    def __init__(self):
        """
        Table template:
            {
                "Bastia" : 14
            }
        """
        self.season = None
        self.league = None
        self.date_dt = None
        self.table = None

    def __call__(self, season, league, date_dt):

        self.season = season
        self.league = league
        self.date_dt = date_dt
        self.table = self._get_table()

    def _get_table(self):
        # Get empty table for season and league
        empty_table = self._get_empty_table()
        # Compute the full table
        table = self._complete_table(empty_table)
        return table

    def _get_empty_table(self):
        return {}

    def _complete_table(self, empty_table):
        table = empty_table
        return table
