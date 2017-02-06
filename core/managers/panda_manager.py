import os

import numpy as np
import pandas as pd
from attrdict import AttrDict

from ofm_helper.common_settings import TRANSFERS_DIR


class TransferFilter(AttrDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'positions'):
            self.positions = None
        if not hasattr(self, 'ages'):
            self.ages = None
        if not hasattr(self, 'strengths'):
            self.strengths = None
        if not hasattr(self, 'seasons'):
            self.seasons = None
        if not hasattr(self, 'matchdays'):
            self.matchdays = None
        if not hasattr(self, 'min_price'):
            self.min_price = None
        if not hasattr(self, 'max_price'):
            self.max_price = None


class PandaManager:
    def __init__(self):
        self.data_frame = self._load_data()

    def get_data(self):
        if self.data_frame is None or self.data_frame.empty:
            self.data_frame = self._load_data()
        return self.data_frame

    def filter_transfers(self, transfer_filter=None):
        filtered_df = self.get_data().copy()

        if transfer_filter:
            if transfer_filter.positions:
                filtered_df = filtered_df[filtered_df.Position.isin(transfer_filter.positions)]
            if transfer_filter.ages:
                filtered_df = filtered_df[filtered_df.Age.isin(transfer_filter.ages)]
            if transfer_filter.strengths:
                filtered_df = filtered_df[filtered_df.Strength.isin(transfer_filter.strengths)]
            if transfer_filter.seasons:
                filtered_df = filtered_df[filtered_df.Season.isin(transfer_filter.seasons)]
            if transfer_filter.matchdays:
                filtered_df = filtered_df[filtered_df.Matchday.isin(transfer_filter.matchdays)]
            if transfer_filter.min_price:
                filtered_df = filtered_df[filtered_df.Price >= transfer_filter.min_price]
            if transfer_filter.max_price:
                filtered_df = filtered_df[filtered_df.Price <= transfer_filter.max_price]
            return filtered_df
        else:
            return self.data_frame

    def get_grouped_prices(self, group_by='Strength', **kwargs):
        df = self.filter_transfers(TransferFilter(**kwargs))
        return df.groupby(group_by).Price

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
