import pandas as pd
import matplotlib.pyplot as plt

# ตั้งค่าฟอนต์ไทย (Windows)
plt.rcParams['font.family'] = ['Tahoma', 'Angsana New', 'TH Sarabun New']

def analyze_and_plot(results_list, total_times_dict, total_orders):
    df = pd.DataFrame(results_list)
    summary = df.groupby('scenario')['finish_time'].agg(['mean', 'max']).rename(
        columns={'mean': 'เวลาเฉลี่ยต่อจาน', 'max': 'เวลารวมทั้งหมด (จากจานสุดท้าย)'}
    )

    plot_data = summary['เวลาเฉลี่ยต่อจาน']

    plt.figure(figsize=(10, 6))
    bars = plot_data.plot(kind='bar', color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    plt.title(f'เวลาเฉลี่ยต่อออเดอร์ (จาก {total_orders} ออเดอร์)', fontsize=14)
    plt.ylabel('นาทีต่อออเดอร์', fontsize=12)
    plt.xlabel('สถานการณ์', fontsize=12)
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars.patches:
        plt.annotate(f'{bar.get_height():.1f} นาที',
                     (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                     ha='center', va='center', size=10, xytext=(0, 8),
                     textcoords='offset points')

    plt.tight_layout()
    plt.show()
