import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import subprocess
import requests
import schedule
import time
import threading
import itertools
import sys
import os


# 1. proc setup 

# 실행
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "options_state.txt")
site_str = parse_txt_to_site_str(file_path)
print(site_str)
# 데이터 예시


#sys_init
sys_opt_url = "https://w1.bidscore.co.kr/develop/b2b/opt"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Content-Type": "application/json"
}
response = requests.get(sys_opt_url, headers=headers)
response.raise_for_status()  # HTTP 오류 발생 시 예외 처리
# 각 로봇별 option 설정값 
opt_config = response.json()  # response.text 대신 response.json() 사용



# 실행할 작업 함수
def task(site_data, meter, initial_value):
    
    typeof = "리스트" if site_data[2] == "list" else "상세"

    if site_data[3] == "B01":
        section = "시설"
    elif site_data[3] == "B02":
        section = "용역"
    elif site_data[3] == "B03":
        section = "물품"

    interval_value = opt_config[site_data[1]][site_data[2]][site_data[3]]['term'] 
    site_name      = "[ " + section + " ] " + site_data[4] +" " + typeof
    print(interval)
    print("[ " + section + " ] " + site_data[4] +" " + typeof)
    # Meter 초기화
    '''subprocess.run(
        [
            site_data[0],
            "--site_code",site_data[1],
            "--typeof",site_data[2],
            "--section",site_data[3],
        ],
        capture_output=True,
        text=True,
        check=True,
    )'''
    meter.configure(text="수집대기",bootstyle="primary")
    print(f"[{site_name}] Meter 초기화 완료: {initial_value}")
    

# 색상 변경을 위한 색상 리스트
colors = itertools.cycle(["red", "blue", "green", "yellow", "orange"])

# 라벨 텍스트 반짝이 효과 함수
blinking = True  # 반짝임 활성화 여부

# 라벨 텍스트 반짝이 효과 함수
def blink_text():
    if blinking:  # 반짝임 활성화 시에만 실행
        current_color = next(colors)  # 다음 색상 가져오기
        left_label.configure(foreground=current_color)  # 라벨 색상 변경
        my_w.after(1000, blink_text)  # 500ms 후 다시 실행

# 반짝임 종료 함수
def stop_blinking():
    global blinking
    blinking = False  # 반짝임 중지
    left_label.configure(foreground="white")  # 라벨 색상 변경

# 반짝임 시작 함수
def start_blinking():
    global blinking
    blinking = True  # 반짝임 활성화
    blink_text()  # 다시 반짝임 시작
    

# 스케줄링된 작업을 스레드에서 실행
def run_task(func, *args):
    thread = threading.Thread(target=func, args=args)
    thread.start()

# Meter를 업데이트하는 데이터 저장용 리스트
meters = []
scheduler_running = True

# 스케줄러를 실행하는 함수 (별도 스레드에서 실행)
def run_scheduler():
    global scheduler_running
    for meter_data in meters:
       meter_data["meter"].configure(text="수집대기",bootstyle="primary")
    while scheduler_running:
        schedule.run_pending()  # 스케줄 실행
        print('run_scheduler...')
        time.sleep(1)

# 스케줄러 시작 함수
def start_scheduler():
    global scheduler_running 
    scheduler_running = True
    left_label.configure(text="스케줄 상태: 구동 중..")
    start_blinking()
    threading.Thread(target=run_scheduler, daemon=True).start()

def stop_scheduler():
    global scheduler_running
    scheduler_running = False
    left_label.configure(text="스케줄 상태: 대기 중")
    stop_blinking()
    for meter_data in meters:
        meter_data["meter"].configure(text="종료",bootstyle="primary")

# 텍스트 파일 읽고 데이터 변환
def parse_txt_to_site_str(file_path):
    site_str = []
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # 첫 번째 줄은 헤더로 제외하고 데이터 처리
    for line in lines[1:]:
        columns = line.strip().split("|")
        if len(columns) == 4:  # 데이터가 올바른 형식인지 확인
            file_name, module, section, title = columns
            site_str.append((file_name, '01', module, section, title))  # '01' 추가
    return site_str

# 실행
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "options_state.txt")
site_str = parse_txt_to_site_str(file_path)
print(site_str)
# 데이터 예시


#sys_init
sys_opt_url = "https://w1.bidscore.co.kr/develop/b2b/opt"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Content-Type": "application/json"
}
response = requests.get(sys_opt_url, headers=headers)
response.raise_for_status()  # HTTP 오류 발생 시 예외 처리
# 각 로봇별 option 설정값 
opt_config = response.json()  # response.text 대신 response.json() 사용

if len(site_str) == 1 : 
    width  = "240"
    height = "300" 
elif len(site_str) == 2 :
    width = "500"
    height = "300"
elif len(site_str) == 3 :
    width = "700"
    height = "300"
else : 
    width = "700"
    if len(site_str) > 3 and len(site_str) < 7 :
        height = "500" 
    elif len(site_str) > 6 and len(site_str) < 10 :
        height = "700"
    else :
        height = "300"

# Tkinter 창 생성
my_w = ttk.Window()
my_w.geometry(f"{width}x{height}")
my_w.style.theme_use("darkly")

# 시작 위치 초기화
r, c = 0, 0

for idx, site in enumerate(site_str):
    typeof = "리스트" if site[2] == "list" else "상세"

    if site[3] == "B01":
        section = "시설"
    elif site[3] == "B02":
        section = "용역"
    elif site[3] == "B03":
        section = "물품"

    start_dt = opt_config[site[1]][site[2]][site[3]]['start_dt']
    end_dt   = opt_config[site[1]][site[2]][site[3]]['end_dt']
    interval = opt_config[site[1]][site[2]][site[3]]['term'] 
    # 라벨 생성 및 배치
    label1 = ttk.Label(my_w, text="[ " + section + " ] " + site[4] +" " + typeof+" " +interval+"초", font=("Helvetica", 14))
    label1.grid(row=r, column=c, padx=30, pady=15, sticky="w")

    # 날짜 프레임 생성 및 배치
    date_frame = ttk.Frame(my_w, padding=6, relief="solid", borderwidth=1)
    date_frame.grid(row=r + 1, column=c, padx=30, pady=10, sticky="nsew")

    # 시작 날짜 라벨 및 입력 필드
    start_label = ttk.Label(date_frame, text=f"시작 날짜 : {start_dt}", font=("Helvetica", 14))
    start_label.grid(row=0, column=0, columnspan=2, pady=5)
    
    # 종료 날짜 라벨 및 입력 필드
    end_label = ttk.Label(date_frame, text=f"종료 날짜 : {end_dt}", font=("Helvetica", 14))
    end_label.grid(row=1, column=0, columnspan=2, pady=5)
    
    #m1 = ttk.Label(date_frame, text=site[6], font=("Helvetica", 45,"bold"))
    #m1.grid(row=2, column=0, columnspan=2, pady=10)
    m1 = ttk.Label(date_frame, text="대기중", font=("Helvetica", 35,"bold"))
    m1.grid(row=2, column=0, columnspan=2, pady=10)
    
    # Meter 데이터 저장 (Meter와 초기값 저장)
    meters.append({"meter": m1, "min_value": 0, "initial_value": int(interval)})

    # 위치 업데이트
    c += 1  # 다음 열로 이동
    if c > 2:  # 열이 2개를 초과하면
        r += 2  # 다음 행으로 이동 (2행 차지)
        c = 0  # 첫 번째 열로 초기화

# 각 데이터 항목에 대해 동적 스케줄 설정
for site_data, meter_data in zip(site_str, meters):
    interval = int(opt_config[site_data[1]][site_data[2]][site_data[3]]['term'])            
    schedule.every(interval).seconds.do(
        lambda data=site_data, m=meter_data["meter"], init_val=meter_data["initial_value"]: run_task(task, data, m, init_val)
    )
# 하단 버튼 프레임 생성
button_frame = ttk.Frame(my_w)
button_frame.grid(row=r + 3, column=0, columnspan=3, padx=10, pady=20, sticky="ew")  # 양쪽 끝에 확장 가능 설정

# 왼쪽 라벨 추가
left_label = ttk.Label(button_frame, text="스케줄 상태: 대기 중", font=("Helvetica", 18))
left_label.pack(side="left", padx=5)  # 프레임 왼쪽에 라벨 배치

# 스케줄러 종료 버튼 추가
stop_button = ttk.Button(button_frame, text="스케줄러 종료", bootstyle="danger outline", command=stop_scheduler)
stop_button.pack(side="right", padx=5)  # 종료 버튼이 시작 버튼 왼쪽에 위치

# 스케줄러 시작 버튼 추가
start_button = ttk.Button(button_frame, text="스케줄러 시작", bootstyle="success outline", command=start_scheduler)
start_button.pack(side="right", padx=5)  # 프레임 오른쪽에 버튼 배치


my_w.mainloop()
