import pandas as pd
import numpy as np
import sys
from scipy import signal
import seaborn
import matplotlib.pyplot as plt
from pykalman import KalmanFilter
seaborn.set()

def butterSmooth(data):
    b, a = signal.butter(2, 0.15, btype='lowpass', analog=False)
    filtered_atotal = signal.filtfilt(b, a, data["atotal"])
    results = data.copy()
    results["atotal"] = filtered_atotal
    return results

def kalmanSmooth(kalman_data):
    initial_state = kalman_data.iloc[0]
    observation_covariance = np.diag([0.00005, 0.00005, 0, 0]) ** 2 
    transition_covariance = np.diag([0.00005, 0.00005, 0, 0]) ** 2 
    transition = [
        [1, 0, 6*(10**-7), 29*(10**-7)], 
        [0, 1, -43*(10**-7), 12*(10**-7)], 
        [0, 0, 1, 0], 
        [0, 0, 0, 1]]
    kf = KalmanFilter(
        initial_state_mean=initial_state,
        initial_state_covariance=observation_covariance,
        observation_covariance=observation_covariance,
        transition_covariance=transition_covariance,
        transition_matrices=transition
      )
    kalman_smoothed, _ = kf.smooth(kalman_data)
    results = kalman_data.copy()
    results['lat'] = kalman_smoothed[:,0]
    results['lon'] = kalman_smoothed[:,1]
    return results

def main(input_file, output_file):
    data = pd.read_csv(input_file)
    data["time"] = pd.to_datetime(data["time"], utc=True)

    # butterworth smooth the acceleration data points
    data["atotal"] = butterSmooth(data)["atotal"]

    # use kalman filter to smooth latitude and longitude data
    smoothed_data = kalmanSmooth(data.set_index("time")[["latitude", "longitude", "wx", "wy"]]).reset_index()
    data["lon"] = smoothed_data["lon"]
    data["lat"] = smoothed_data["lat"]
    data.drop(columns=["longitude", "latitude"], inplace=True)
    data.to_csv(output_file, index=False)
    return 0

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)