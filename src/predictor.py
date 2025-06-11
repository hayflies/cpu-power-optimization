

import psutil
import os
import joblib
import numpy as np
import time

# 모델 파일 경로
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/xgb_model.pkl')

# 모델 로드
model = joblib.load(MODEL_PATH)

def get_current_features():
    cpu_percent = psutil.cpu_percent(interval=1)
    iowait = psutil.cpu_times_percent().iowait
    num_procs = len(psutil.pids())
    return np.array([[cpu_percent, iowait, num_procs]])

def predict_loop(n_iterations=10):
    print("[INFO] 실시간 예측 시작")
    for _ in range(n_iterations):
        features = get_current_features()
        predicted_freq = model.predict(features)[0]
        print(f"예측 주파수: {predicted_freq:.2f} MHz")
        time.sleep(1)

if __name__ == '__main__':
    predict_loop()