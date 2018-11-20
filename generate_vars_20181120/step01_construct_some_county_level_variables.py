#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step01_construct_some_county_level_variables
# @Date: 20/11/2018
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python3 -m generate_vars_20181120.step01_construct_some_county_level_variables
"""

import os

import pandas as pd
from pandas import DataFrame

from constants import Constants as const

SOD_DATA_PATH = os.path.join(const.DATA_PATH, '20180908_revision', 'SOD_1976-1985_Fed_micro_data.dta')
SOD_DATA2_PATH = os.path.join(const.DATA_PATH, '20180908_revision', 'SOD_1986-2006_Fed_micro_data.dta')
FDIC_DATA_PATH = os.path.join(const.DATA_PATH, 'FDIC_data', 'Branch Office Deposits')


def calculate_soc_fips(row):
    county_code = int(row['sumd9150'])
    state_code = int(row['sumd9210'])
    return state_code * 1000 + county_code


RSSD9001 = 'rssd9001'
TOTAL_DEPOSIT = 'sumd2200'
YEAR = 'year'

if __name__ == '__main__':

    # Sort a branch list
    sod_df: DataFrame = pd.read_stata(SOD_DATA_PATH)
    sod_df.loc[:, const.FIPS] = sod_df.apply(calculate_soc_fips, axis=1)
    sod_df = sod_df[sod_df['sumd9310'] != 9]
    sod_df_drop_duplicates = sod_df[[RSSD9001, YEAR, const.FIPS, TOTAL_DEPOSIT]].copy()

    sod_df2: DataFrame = pd.read_stata(SOD_DATA2_PATH).dropna(subset=['sumd9150', 'sumd9210'], how='any')
    sod_df2.loc[:, const.FIPS] = sod_df2.apply(calculate_soc_fips, axis=1)
    sod_df2 = sod_df2[sod_df2['sumd9310'] != 9]
    sod_df2_drop_duplicates = sod_df2[[RSSD9001, YEAR, const.FIPS, TOTAL_DEPOSIT]].copy()

    fdic_dfs = [sod_df_drop_duplicates, sod_df2_drop_duplicates[sod_df2_drop_duplicates[YEAR] < 1994]]
    for year in range(1994, 2017):
        tmp_path = os.path.join(FDIC_DATA_PATH, 'ALL_{}.csv'.format(year))

        fdic_df = pd.read_csv(tmp_path, encoding='latin-1').rename(index=str, columns={
            'STCNTYBR': const.FIPS, 'YEAR': YEAR, 'RSSDHCR': RSSD9001, 'DEPSUM': TOTAL_DEPOSIT})

        fdic_dfs.append(fdic_df[[const.FIPS, YEAR, RSSD9001, TOTAL_DEPOSIT, ]].copy())

    bank_branch_df = pd.concat(fdic_dfs, ignore_index=True, sort=False).dropna(subset=[RSSD9001])
    bank_branch_df.to_pickle(os.path.join(const.TEMP_PATH, '20181120_branch_location_total_deposit_info.pkl'))
