import numpy as np
import pandas as pd
import sys

def main(ankle_path, hand_path, pocket_path, output_file):
    ankle_gps = pd.read_csv(ankle_path + "/gps.csv")
    ankle_gps["time"] = pd.to_datetime(ankle_gps["time"], utc=True)
    ankle_gps = ankle_gps.groupby(ankle_gps['time'].dt.round('1S')).agg('mean').reset_index()
    ankle_gps = ankle_gps.drop([0, 1])

    ankle_start_time = ankle_gps["time"].min()

    ankle_accl = pd.read_csv(ankle_path + "/accl.csv")
    ankle_accl["time"] = pd.to_datetime(ankle_start_time + pd.to_timedelta(ankle_accl["time"], unit='sec'), utc=True)
    ankle_accl = ankle_accl.groupby(ankle_accl['time'].dt.round('1S')).agg('mean').reset_index()

    ankle_gyro = pd.read_csv(ankle_path + "/gyro.csv")
    ankle_gyro["time"] = pd.to_datetime(ankle_start_time + pd.to_timedelta(ankle_gyro["time"], unit='sec'), utc=True)
    ankle_gyro = ankle_gyro.groupby(ankle_accl['time'].dt.round('1S')).agg('mean').reset_index()

    ankle = ankle_gps.merge(ankle_accl, on=["time"], how="inner")
    ankle = ankle.merge(ankle_gyro, on=["time"], how="inner")


    hand_gps = pd.read_csv(hand_path + "/gps.csv")
    hand_gps["time"] = pd.to_datetime(hand_gps["time"], utc=True)
    hand_gps = hand_gps.groupby(hand_gps['time'].dt.round('1S')).agg('mean').reset_index()
    hand_gps = hand_gps.drop([0, 1])

    hand_start_time = hand_gps["time"].min()

    hand_accl = pd.read_csv(hand_path + "/accl.csv")
    hand_accl["time"] = pd.to_datetime(hand_start_time + pd.to_timedelta(hand_accl['time'], unit='sec'), utc=True)
    hand_accl = hand_accl.groupby(hand_accl['time'].dt.round('1S')).agg('mean').reset_index()

    hand_gyro = pd.read_csv(hand_path + "/gyro.csv")
    hand_gyro["time"] = pd.to_datetime(hand_start_time + pd.to_timedelta(hand_gyro['time'], unit='sec'), utc=True)
    hand_gyro = hand_gyro.groupby(hand_accl['time'].dt.round('1S')).agg('mean').reset_index()

    hand = hand_gps.merge(hand_accl, on=["time"], how="inner")
    hand = hand.merge(hand_gyro, on=["time"], how="inner")

    pocket_gps = pd.read_csv(pocket_path + "/gps.csv")
    pocket_gps["time"] = pd.to_datetime(pocket_gps["time"], utc=True)
    pocket_gps = pocket_gps.groupby(pocket_gps['time'].dt.round('1S')).agg('mean').reset_index()
    pocket_gps = pocket_gps.drop([0, 1])

    pocket_start_time = pocket_gps["time"].min()

    pocket_accl = pd.read_csv(ankle_path + "/accl.csv")
    pocket_accl["time"] = pd.to_datetime(pocket_start_time + pd.to_timedelta(pocket_accl["time"], unit='sec'), utc=True)
    pocket_accl = pocket_accl.groupby(pocket_accl['time'].dt.round('1S')).agg('mean').reset_index()

    pocket_gyro = pd.read_csv(ankle_path + "/gyro.csv")
    pocket_gyro["time"] = pd.to_datetime(pocket_start_time + pd.to_timedelta(pocket_gyro["time"], unit='sec'), utc=True)
    pocket_gyro = pocket_gyro.groupby(pocket_accl['time'].dt.round('1S')).agg('mean').reset_index()

    pocket = pocket_gps.merge(pocket_accl, on=["time"], how="inner")
    pocket = pocket.merge(pocket_gyro, on=["time"], how="inner")

    ankle["type"] = "ankle"
    hand["type"] = "hand"
    pocket["type"] = "pocket"
    data = pd.concat([ankle, hand, pocket], ignore_index=True)
    data["type"] = data["type"].astype("string")
    data.to_csv(output_file, index=False)
    return 0

if __name__ == "__main__":
    ankle_path = sys.argv[1]
    hand_path = sys.argv[2]
    pocket_path = sys.argv[3]
    output_file = sys.argv[4]
    main(ankle_path, hand_path, pocket_path, output_file)
