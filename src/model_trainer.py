import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
import numpy as np

# 데이터 파일 경로
DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/cpu_power_data.csv')
MODEL_DIR = os.path.join(os.path.dirname(__file__), '../models')
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, 'xgb_model.pkl')

def train_model():
    # 데이터 로드
    df = pd.read_csv(DATA_FILE)

    # 특성과 라벨 정의
    X = df[['cpu_percent', 'iowait', 'num_running_processes']]
    y = df['cpu_freq']

    # 학습/테스트 데이터 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 모델 학습
    model = XGBRegressor()
    model.fit(X_train, y_train)

    # 예측 및 평가
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    print(f"[RESULT] RMSE: {rmse:.2f}")

    # 모델 저장
    joblib.dump(model, MODEL_PATH)
    print(f"[INFO] 모델이 저장되었습니다: {MODEL_PATH}")

if __name__ == '__main__':
    train_model()