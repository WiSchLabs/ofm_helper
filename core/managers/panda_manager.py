import os

import numpy as np
import pandas as pd
from matplotlib import style

from ofm_helper.common_settings import TRANSFERS_DIR

style.use('ggplot')


class PandaManager:

    def __init__(self):
        self.data_frame = self._load_data()

    def get_data(self):
        if self.data_frame is None or self.data_frame.empty:
            self.data_frame = self._load_data()
        return self.data_frame

    def filter_transfers(self, positions=None, ages=None, strengths=None, seasons=None, matchdays=None):
        filtered_df = self.get_data().copy()
        if positions:
            filtered_df = filtered_df[filtered_df.Position.isin(positions)]
        if ages:
            filtered_df = filtered_df[filtered_df.Age.isin(ages)]
        if strengths:
            filtered_df = filtered_df[filtered_df.Strength.isin(strengths)]
        if seasons:
            filtered_df = filtered_df[filtered_df.Season.isin(seasons)]
        if matchdays:
            filtered_df = filtered_df[filtered_df.Matchday.isin(matchdays)]
        return filtered_df

    def get_prices_grouped_by_strength(self, position='MS', age=33):
        df = self.filter_transfers(positions=[position], ages=[age])

        return df.groupby('Strength').Price

    def get_prices_grouped_by_age(self, position='MS', strength=16):
        df = self.filter_transfers(positions=[position], strengths=[strength])

        return df.groupby('Age').Price

    def _load_data(self):
        self.data_frame = pd.DataFrame()
        for file in os.listdir(TRANSFERS_DIR):
            if file.endswith('csv'):
                df = pd.read_csv('{}/{}'.format(TRANSFERS_DIR, file),
                                 index_col=0,
                                 dtype={7: np.int32, 8: np.int32, 9: np.int32},
                                 skip_blank_lines=True,
                                 )
                df.drop(df.columns[[2, 3, 4]], axis=1, inplace=True)

                df = df.rename(columns={df.columns[0]: "Matchday",
                                        df.columns[1]: "Season",
                                        df.columns[2]: "Position",
                                        df.columns[3]: "Age",
                                        df.columns[4]: "Strength",
                                        df.columns[5]: "Price",
                                        })

                if self.data_frame.empty:
                    self.data_frame = df
                else:
                    self.data_frame = self.data_frame.append(df)

        return self.data_frame
