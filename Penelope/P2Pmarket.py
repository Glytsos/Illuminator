

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import pymarket as pm

r = np.random.RandomState(1234)
mar = pm.Market()

mar.accept_bid(1, 6.7, 0, True, 0)
mar.accept_bid(1, 6.6, 1, True, 0)
mar.accept_bid(1, 6.5, 2, True, 0)
mar.accept_bid(1, 6.4, 3, True, 0)
mar.accept_bid(1, 6.3, 4, True, 0)
mar.accept_bid(1, 6, 5, True, 0)

mar.accept_bid(1, 1, 6, False, 0)
mar.accept_bid(1, 2, 7, False, 0)
mar.accept_bid(2, 3, 8, False, 0)
mar.accept_bid(2, 4, 9, False, 0)
mar.accept_bid(1, 6.1, 10, False, 0)

bids = mar.bm.get_df()
transactions, extras = mar.run('p2p', r=r)
stats = mar.statistics()