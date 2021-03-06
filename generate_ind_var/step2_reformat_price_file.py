#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step2_reformat_price_file
# @Date: 12/8/2017
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os

import pandas as pd
import pathos

from constants import Constants as const


def reformat_file(file_path):
    df = pd.read_pickle(file_path)
    if hasattr(df, 'set_index'):
        df = df.set_index(const.CRSP_DATE)[const.CRSP_PRICE]

    # there may be some negative value in crsp data. Details can be found in
    # http://faq.library.princeton.edu/econ/faq/11159
    df = df.dropna().apply(abs)

    if not df.empty:
        df.sort_index().to_pickle(file_path)
    else:
        os.remove(file_path)
    return 1


if __name__ == '__main__':
    cusip_list = os.listdir(const.CUSIP_STOCK_PRICE_PATH)
    ticker_file_list = os.listdir(const.TICKER_STOCK_PRICE_PATH)

    pool = pathos.multiprocessing.Pool(processes=pathos.multiprocessing.cpu_count() - 2)
    pool.map(reformat_file, map(lambda x: os.path.join(const.TICKER_STOCK_PRICE_PATH, x), ticker_file_list))
    pool.map(reformat_file, map(lambda x: os.path.join(const.CUSIP_STOCK_PRICE_PATH, x), cusip_list))
