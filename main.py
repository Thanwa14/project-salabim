# main.py
# ----------------------------------------------------
# (เวอร์ชันแก้ไข 26 ต.ค. 2025 - Final stable)
# ----------------------------------------------------
import salabim as sim
sim.yieldless(False)  # ✅ เปิดโหมด process-based (ใช้ yield ได้)

from config import SCENARIOS, TOTAL_ORDERS
from simulation_model import Order
from analysis import analyze_and_plot


def run():
    print("--- 0. เริ่มต้นโปรแกรมจำลอง ---")

    all_results = []
    total_times = {}

    print("\n--- 4. เริ่มรัน Simulation ทั้ง 3 สถานการณ์ ---")

    for name, config in SCENARIOS.items():
        print(f"\n---== {name} ==---")

        # ✅ สร้าง Environment
        env = sim.Environment(trace=False)

        # ✅ ผูกข้อมูลส่วนกลางเข้ากับ env
        env.all_results = all_results
        env.current_scenario = name

        # ✅ สร้าง Resource (ไม่ต้องส่ง env)
        env.current_resources = {
            "person": sim.Resource(name="Person", capacity=config['person_cap']),
            "pan": sim.Resource(name="Pan", capacity=config['pan_cap'])
        }

        # ✅ สร้างออเดอร์ใน environment นี้ (ไม่ใช้ with)
        for i in range(TOTAL_ORDERS):
            Order(f"ออเดอร์ {i+1}", env=env)

        # ✅ รัน simulation
        env.run()

        total_times[name] = env.now()
        print(f"---== จบ {name} | เวลารวม: {env.now():.0f} นาที ==---")

    # ✅ วิเคราะห์ผลลัพธ์ทั้งหมด
    analyze_and_plot(all_results, total_times, TOTAL_ORDERS)

    print("\n--- 0. จบโปรแกรม ---")


if __name__ == "__main__":
    run()
