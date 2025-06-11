import os
import subprocess
import platform
from src.data_collector import collect_cpu_data
from src.model_trainer import train_model
from src.predictor import get_current_features, model
from visualizations.plot import plot_cpu_data

def set_cpu_frequency(freq_mhz):
    """
    CPU 주파수를 설정합니다.
    - Linux: cpufreq-set 사용
    - macOS, Windows: 실제 주파수 설정은 건너뜁니다 (시뮬레이션 출력만 수행)
    """
    system_platform = platform.system()
    if system_platform == 'Darwin':
        print("[SKIP] macOS에서는 CPU 주파수 설정이 지원되지 않습니다.")
        return
    elif system_platform == 'Windows':
        print("[SKIP] Windows에서는 일반적으로 사용자 수준에서 CPU 주파수를 조절할 수 없습니다.")
        return

    freq_khz = int(freq_mhz * 1000)
    try:
        for cpu in range(os.cpu_count()):
            subprocess.run(['sudo', 'cpufreq-set', '-c', str(cpu), '-f', f'{freq_khz}'], check=True)
        print(f"[ACTION] CPU 주파수 {freq_khz} kHz로 설정 완료")
    except Exception as e:
        print(f"[ERROR] 주파수 설정 실패: {e}")

def estimate_power(cpu_percent, freq_mhz):
    """
    추정 전력 소비량 계산 (단위: W)
    비례 모델: base_power + dynamic component
    """
    base_power = 5  # idle 상태 기준 전력 (W)
    dynamic_power = (freq_mhz / 1000) * (cpu_percent / 100) * 0.5  # 단순 비례 모델
    return round(base_power + dynamic_power, 2)

def main():
    # 1. 데이터 수집
    collect_cpu_data(duration_seconds=60, interval_seconds=1)

    # 2. 모델 학습
    train_model()

    # 3. 실시간 예측 및 주파수 설정
    print("\n[INFO] 실시간 예측 및 주파수 조정 시작")
    for _ in range(10):
        features = get_current_features()
        predicted_freq = model.predict(features)[0]
        estimated_power = estimate_power(features[0][0], predicted_freq)
        print(f"[PREDICT] {predicted_freq:.2f} MHz | CPU: {features[0][0]:.1f}% → 추정 전력: {estimated_power} W")
        set_cpu_frequency(predicted_freq)

    # 4. 시각화
    print("\n[INFO] 수집된 데이터를 시각화합니다...")
    plot_cpu_data()

if __name__ == '__main__':
    main()