import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/cpu_power_data.csv')
SAVE_DIR = os.path.join(os.path.dirname(__file__), '.')
os.makedirs(SAVE_DIR, exist_ok=True)

def plot_cpu_data():
    df = pd.read_csv(DATA_FILE)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    def estimate_power(cpu_percent, freq_mhz):
        base_power = 5
        dynamic_power = (freq_mhz / 1000) * (cpu_percent / 100) * 0.5
        return round(base_power + dynamic_power, 2)

    df['estimated_power'] = df.apply(lambda row: estimate_power(row['cpu_percent'], row['cpu_freq']), axis=1)
    df['power_change'] = df['estimated_power'].diff().fillna(0)

    plt.figure(figsize=(14, 12))

    plt.subplot(5, 1, 1)
    plt.plot(df['timestamp'], df['cpu_percent'], label='CPU Usage (%)', color='tab:blue')
    plt.ylabel('CPU (%)')
    plt.title('CPU Usage Over Time')
    plt.grid(True)

    plt.subplot(5, 1, 2)
    plt.plot(df['timestamp'], df['cpu_freq'], label='CPU Frequency (MHz)', color='tab:green')
    plt.ylabel('Freq (MHz)')
    plt.title('CPU Frequency Over Time')
    plt.grid(True)

    plt.subplot(5, 1, 3)
    plt.plot(df['timestamp'], df['num_running_processes'], label='Running Processes', color='tab:red')
    plt.ylabel('Processes')
    plt.title('Number of Running Processes Over Time')
    plt.grid(True)

    plt.subplot(5, 1, 4)
    plt.plot(df['timestamp'], df['estimated_power'], label='Estimated Power (W)', color='tab:purple')
    plt.ylabel('Power (W)')
    plt.title('Estimated Power Consumption Over Time')
    plt.grid(True)

    plt.subplot(5, 1, 5)
    plt.plot(df['timestamp'], df['power_change'], label='Power Change (W)', color='tab:orange')
    plt.ylabel('Power Change (W)')
    plt.title('Power Change Over Time')
    plt.grid(True)

    plt.tight_layout()
    output_path = os.path.join(SAVE_DIR, 'cpu_data_plot.png')
    plt.savefig(output_path)
    print(f"[INFO] Graph saved to: {output_path}")
    plt.show()

if __name__ == '__main__':
    plot_cpu_data()