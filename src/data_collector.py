import psutil
import csv
import os
import platform
from datetime import datetime

# 저장할 CSV 파일 경로
DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
os.makedirs(DATA_DIR, exist_ok=True)
CSV_FILE = os.path.join(DATA_DIR, 'cpu_power_data.csv')

def collect_cpu_data(duration_seconds=60, interval_seconds=1):
    print(f"[INFO] CPU 데이터 수집 시작: {duration_seconds}초 동안 {interval_seconds}초 간격으로 수집")

    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'cpu_percent', 'cpu_freq', 'iowait', 'num_running_processes', 'estimated_power'])

    for _ in range(int(duration_seconds / interval_seconds)):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cpu_percent = psutil.cpu_percent(interval=interval_seconds)
        cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0
        cpu_times = psutil.cpu_times_percent()
        iowait = 0.0 if platform.system() == 'Windows' else getattr(cpu_times, 'iowait', 0.0)
        num_procs = len(psutil.pids())
        estimated_power = 5 + (cpu_freq / 1000) * (cpu_percent / 100) * 0.5

        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, cpu_percent, cpu_freq, iowait, num_procs, round(estimated_power, 2)])

        print(f"{timestamp} | CPU: {cpu_percent}% | Freq: {cpu_freq:.2f} MHz | IOwait: {iowait:.2f}% | Procs: {num_procs} | Power: {estimated_power:.2f} W")

    print(f"[INFO] 데이터 수집 완료. CSV 저장 위치: {CSV_FILE}")

if __name__ == '__main__':
    collect_cpu_data(duration_seconds=60, interval_seconds=1)