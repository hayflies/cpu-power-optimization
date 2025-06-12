import psutil
import os
import joblib
import numpy as np
import time
import platform

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/xgb_model.pkl')

def load_model():
    return joblib.load(MODEL_PATH)

def get_current_features():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_times = psutil.cpu_times_percent()
    iowait = 0.0 if platform.system() == 'Windows' else getattr(cpu_times, 'iowait', 0.0)
    num_procs = len(psutil.pids())
    return np.array([[cpu_percent, iowait, num_procs]])

def predict_loop(n_iterations=10):
    print("[INFO] 실시간 예측 시작")
    prev_power = None
    for _ in range(n_iterations):
        features = get_current_features()
        model = load_model()
        predicted_freq = model.predict(features)[0]
        estimated_power = 5 + (predicted_freq / 1000) * (features[0][0] / 100) * 0.5
        if prev_power is not None:
            delta = round(estimated_power - prev_power, 2)
            print(f"예측 주파수: {predicted_freq:.2f} MHz | 추정 전력: {estimated_power:.2f} W | 전력 변화량: {delta:+.2f} W")
        else:
            print(f"예측 주파수: {predicted_freq:.2f} MHz | 추정 전력: {estimated_power:.2f} W")
        prev_power = estimated_power
        time.sleep(1)

if __name__ == '__main__':
    predict_loop()