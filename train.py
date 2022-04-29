"""
Script for updating model
"""

import os
import map_classification as mc


if __name__ == "__main__":
    try:
        os.remove("mapsim_3_top50_600f_weights.h5")
    except FileNotFoundError as e:
        pass

    try:
        os.remove("mapsim_4_top50_600f_weights.h5")
    except FileNotFoundError as e:
        pass

    # soldier
    mc.create_model(3)
    mc.train_model(3)

    # demoman
    mc.create_model(4)
    mc.train_model(4)
