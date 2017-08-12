#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: path_info
# @Date: 11/8/2017
# @Author: Mark Wang
# @Email: wangyouan@gamil.com


import os


class PathInfo(object):
    ROOT_PATH = '/home/zigan/Documents/WangYouan/research/banking'

    DATA_PATH = os.path.join(ROOT_PATH, 'data')
    CUSIP_STOCK_PRICE_PATH = os.path.join(DATA_PATH, 'price_cusip')
    TICKER_STOCK_PRICE_PATH = os.path.join(DATA_PATH, 'price_ticker')

    CUSIP_STOCK_RETURN_PATH = os.path.join(DATA_PATH, 'return_cusip')
    TICKER_STOCK_RETURN_PATH = os.path.join(DATA_PATH, 'return_ticker')

    CUSIP_MARKET_VALUE_PATH = os.path.join(DATA_PATH, 'market_value_cusip')
    TICKER_MARKET_VALUE_PATH = os.path.join(DATA_PATH, 'market_value_ticker')

    TEMP_PATH = os.path.join(ROOT_PATH, 'temp')
    RESULT_PATH = os.path.join(ROOT_PATH, 'result')
