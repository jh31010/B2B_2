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

# 0. init 
meters = []
scheduler_running = True
blinking = True  # 반짝임 활성화 여부
colors = itertools.cycle(["red", "blue", "green", "yellow", "orange"]) # 색상 변경을 위한 색상 리스트 

# 1. proc setup 
#    - setup.ini 에서 구동할 exe 파일 리스트 불러오기
#    - 파일명 , 모듈형태 (list,detail,etc) , 공고분류(시설,용역,물품), 표시할 제목
# 텍스트 파일 읽고 데이터 변환
def parse_txt_strip(file_path):
    setup_ini = [] 
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # 첫 번째 줄은 헤더로 제외하고 데이터 처리
    for line in lines[1:]:
        columns = line.strip().split("|")
        if len(columns) == 4:  # 데이터가 올바른 형식인지 확인
            file_name, module, section, title = columns
            setup_ini.append((file_name, '01', module, section, title))  # '01' 추가
    return setup_ini

current_dir      = os.path.dirname(os.path.abspath(__file__))
file_path         = os.path.join(current_dir, "setup.ini")
active_setup_arr = parse_txt_strip(file_path)

# 2. proc_setup - 2 
#    - 실시간으로 상태값을 변경해줘야 하는 부분은 웹상에서 불러올 수 있도록 처리함
#    - 실행주기 (term) , 수행시작날짜 ( start_dt ) , 수행종료날짜 ( end_dt ) , 수행상태 : on OR off
sys_opt_url = "https://w1.bidscore.co.kr/develop/b2b/opt"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Content-Type": "application/json"
}
response = requests.get(sys_opt_url, headers=headers)
response.raise_for_status()  # HTTP 오류 발생 시 예외 처리
opt_config = response.json()  # response.text 대신 response.json() 사용

# 4. ttkBootstrap UI 영역

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
    

# 라벨 텍스트 반짝이 효과 함수
def blink_text():
    if blinking:  # 반짝임 활성화 시에만 실행
        current_color = next(colors)  # 다음 색상 가져오기
        left_label.configure(foreground=current_color)  # 라벨 색상 변경
        tk_wrap.after(1000, blink_text)  # 500ms 후 다시 실행

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

# 각 데이터 항목에 대해 동적 스케줄 설정
for site_data, meter_data in zip(active_setup_arr, meters):
    interval = int(opt_config[site_data[1]][site_data[2]][site_data[3]]['term'])            
    schedule.every(interval).seconds.do(
        lambda data=site_data, m=meter_data["meter"], init_val=meter_data["initial_value"]: run_task(task, data, m, init_val)
    )


# 3. ttkBootstrap UI 영역

#tkniter size 정의
basic_width_size  = "250" # 기본 width size
basic_height_size = "300" # 기본 height size
add_width_size    = "260" # 가중치 width size
add_height_size   = "200" # 가중치 Height size

if(len(active_setup_arr) > 3) :
    basic_width_size = basic_width_size+(basic_width_size*2)
    if len(active_setup_arr) > 3 and len(active_setup_arr) < 7 : 
        basic_height_size = basic_height_size+add_height_size
    elif len(active_setup_arr) > 6 and len(active_setup_arr) < 10 : 
        basic_height_size = basic_height_size+(add_height_size*2)
else :
    basic_width_size = int(basic_width_size)+(int(basic_width_size)*(len(active_setup_arr)-1))

tk_wrap = ttk.Window()
tk_wrap.geometry(f"{basic_width_size}x{basic_height_size}")
tk_wrap.style.theme_use("darkly") #테마적용

# 시작 위치 초기화
r, c = 0, 0

#setup.ini에서 가져온 리스트 만큼 PAINT
for idx,list_item in enumerate(active_setup_arr):
    
    start_dt = opt_config[list_item[1]][list_item[2]][list_item[3]]['start_dt']
    end_dt   = opt_config[list_item[1]][list_item[2]][list_item[3]]['end_dt']
    interval = opt_config[list_item[1]][list_item[2]][list_item[3]]['term'] 
    title    = list_item[4]+" "+interval+"초"
    
    title_label = ttk.Label(tk_wrap,text="", font=("Helvetica", 14))
    title_label.grid(row=r, column=c, padx=30, pady=15, sticky="w")
   
    #frame 
    box_frame = ttk.Frame(tk_wrap, padding=6, relief="solid", borderwidth=1)
    box_frame.grid(row=r + 1, column=c, padx=30, pady=10, sticky="nsew")
    
    # 시작 날짜 라벨 및 입력 필드
    start_label = ttk.Label(box_frame, text=f"시작 날짜 : {start_dt}", font=("Helvetica", 14))
    start_label.grid(row=0, column=0, columnspan=2, pady=5)
    
    # 종료 날짜 라벨 및 입력 필드
    end_label = ttk.Label(box_frame, text=f"종료 날짜 : {end_dt}", font=("Helvetica", 14))
    end_label.grid(row=1, column=0, columnspan=2, pady=5)
    
    state_lable = ttk.Label(box_frame, text="대기중", font=("Helvetica", 35,"bold"))
    state_lable.grid(row=2, column=0, columnspan=2, pady=10)
    
    # Meter 데이터 저장 (Meter와 초기값 저장)
    meters.append({"meter": state_lable, "min_value": 0, "initial_value": int(interval)})

    # 위치 업데이트
    c += 1  # 다음 열로 이동
    if c > 2:  # 열이 2개를 초과하면
        r += 2  # 다음 행으로 이동 (2행 차지)
        c = 0  # 첫 번째 열로 초기화

# 하단 버튼 프레임 생성
button_frame = ttk.Frame(tk_wrap)
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

tk_wrap.mainloop()
