# simulation_model.py
# ----------------------------------------------------
# (เวอร์ชันแก้ไข 25 ต.ค. 2025 - ใช้วิธี 'env' ที่ถูกต้อง)
# ----------------------------------------------------
import salabim as sim
from config import T_PREP, T_COOK, T_FINISH

class Order(sim.Component):
    
    # --- *** ไม่ต้องมี setup() หรือ __init__() *** ---

    # process() จะดึงข้อมูลทุกอย่างจาก 'self.env'
    def process(self):
        
        # --- 1. ดึงข้อมูลที่ 'main.py' แปะไว้ใน 'env' ---
        env = self.env
        resources = env.current_resources     # ดึง resources จาก env
        results_list = env.all_results      # ดึง list ผลลัพธ์จาก env
        scenario_name = env.current_scenario  # ดึงชื่อ scenario จาก env

        # --- 2. ดึงทรัพยากรที่ต้องใช้ ---
        person = resources['person']
        pan = resources['pan']
        
        # --- 3. เริ่มกระบวนการ ---
        order_id = self.name()
        
        # --- ขั้นตอนที่ 1: เตรียมของ (ใช้ 'คน') ---
        print(f"เวลา {env.now():.0f}: {order_id} - รอ 'คน' เตรียมของ")
        yield self.request(person)
        print(f"เวลา {env.now():.0f}: {order_id} - 'คน' เริ่มเตรียมของ")
        yield self.hold(T_PREP)
        self.release(person)
        print(f"เวลา {env.now():.0f}: {order_id} - 'คน' เตรียมของเสร็จ")

        # --- ขั้นตอนที่ 2: ปรุง (ใช้ 'กระทะ') ---
        print(f"เวลา {env.now():.0f}: {order_id} - รอ 'กระทะ'")
        yield self.request(pan)
        print(f"เวลา {env.now():.0f}: {order_id} - 'กระทะ' เริ่มปรุง (ตอนนี้ 'คน' ว่าง)")
        yield self.hold(T_COOK)
        self.release(pan)
        print(f"เวลา {env.now():.0f}: {order_id} - 'กระทะ' ปรุงเสร็จ")

        # --- ขั้นตอนที่ 3: จัดจาน (ใช้ 'คน' อีกครั้ง) ---
        print(f"เวลา {env.now():.0f}: {order_id} - รอ 'คน' จัดจาน")
        yield self.request(person)
        print(f"เวลา {env.now():.0f}: {order_id} - 'คน' เริ่มจัดจาน")
        yield self.hold(T_FINISH)
        self.release(person)
        print(f"เวลา {env.now():.0f}: {order_id} - *** ทำเสร็จ ***")
        
        # เก็บผลลัพธ์ (ใช้ list ที่ดึงมาจาก env)
        results_list.append({
            'scenario': scenario_name,
            'order_id': int(order_id.split(' ')[1]),
            'finish_time': env.now()
        })