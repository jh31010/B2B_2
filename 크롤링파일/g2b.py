
'''
아래 내용은 공통 적용 기능입니다.
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from dataclasses import asdict
from urllib.parse import urlencode, quote
from datetime import datetime
from dataclasses import dataclass
import json
import time
import sys
import argparse
import requests
import mysql.connector

# ArgumentParser 객체 생성
parser = argparse.ArgumentParser(description="Process some input arguments.")

# 인자값 추가
parser.add_argument('--site_code', type=str, help='Name of the person')
parser.add_argument('--typeof', type=str, help='Age of the person')
parser.add_argument('--start_dt', type=str, help='Age of the person')
parser.add_argument('--end_dt', type=str, help='Age of the person')
parser.add_argument('--section', type=str, help='Age of the person')

args = parser.parse_args()

site_code = args.site_code
typeof    = args.typeof     # list , detail 등의 형태   
start_dt  = args.start_dt   # 시작일    
end_dt    = args.end_dt     # 종료일
section   = args.section    # B01, B02, B03 시설 용역 물품,

# 필수값 처리 exe --site_code 01 --typeof list --section B01
site_code = "01"
typeof    = "detail"
section   = "B01"

'''
# DB Connect 정보 불러오기 - 특정 url에서 불러옴
connect_url = "https://w1.bidscore.co.kr/develop/b2b/connect"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Content-Type": "application/json"
}

try:
    # GET 요청
    response = requests.get(connect_url, headers=headers)
    response.raise_for_status()  # HTTP 오류 발생 시 예외 처리
    
    # JSON 데이터 디코드
    config = response.json()  # response.text 대신 response.json() 사용
    
    conn_master  = mysql.connector.connect(
        host = config['bs_master']['hostname'],
        user = config['bs_master']['username'],
        password = config['bs_master']['password'],
        database = config['bs_master']['database']
    )
    
    conn_slave  = mysql.connector.connect(
        host = config['bs_slave']['hostname'],
        user = config['bs_slave']['username'],
        password = config['bs_slave']['password'],
        database = config['bs_slave']['database']
    )

except requests.exceptions.RequestException as e:
    print(f"Network or HTTP error occurred: {e}") 
    exit
except KeyError:
    print("'bs_master' key not found in the response")
    exit
except json.JSONDecodeError:
    print("Failed to decode JSON response")
    exit
'''
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
if opt_config[site_code][typeof][section]['start_dt'] != "" :
    start_dt = opt_config[site_code][typeof][section]['start_dt']
if opt_config[site_code][typeof][section]['end_dt'] != "" :
    end_dt = opt_config[site_code][typeof][section]['end_dt']    

if opt_config[site_code][typeof][section]['active'] == "off" :    
    print("opt setup -> active Off")
    sys.exit(1)
#sys.exit(1)

'''추가사항은 아래에 작성해주세요.'''


@dataclass
class Bid_list_data:
    bid_num: str
    bid_title: str
    bid_url: str
    reg_dt : str
    typeof : str
    section : str
    site_code : str
    

class realize():
     
    def __init__(self, site_code,typeof,start_dt,end_dt,section):
        super().__init__()  # 부모 클래스의 초기화 메서드 호출
        self._typeof      = typeof
        self._start_dt    = start_dt
        self._end_dt      = end_dt
        self._limit       = "30"
        self._section     = section 
        self._site_code   = site_code

    def run(self):
        if self._typeof == "list":
            return self.list_run()
        elif self._typeof == "detail" :
            return self.detail_run()
         
    def list_run(self):
 
        if self._section == "B01" :
            section = "3"
        elif self._section == "B02" :
            section = "5"
        elif self._section == "B03" :
            section = "3"
            
        base_url = "https://www.g2b.go.kr:8101/ep/tbid/tbidList.do?bidSearchType=1&radOrgan=1&searchDtType=1&searchType=1&"
        
        params   = {
            "fromBidDt" : datetime.strptime(self._start_dt, "%Y-%m-%d").strftime("%Y/%m/%d"),
            "toBidDt"   : datetime.strptime(self._end_dt, "%Y-%m-%d").strftime("%Y/%m/%d"),
            "taskClCds" : section, #1 물품 , 3 시설 , 5 용역 ,
            "recordCountPerPage" : self._limit
        }

        encoded_url = base_url + urlencode(params, quote_via=quote)
        print(encoded_url)
    
        bid_items = []
    
        driver = webdriver.Chrome()        

        for page in range(1,2) :
            print(f"크롤링 중: {page} 페이지")
            list_url = encoded_url+f"&currentPageNo={page}"
            print(list_url)
            driver.get(list_url)
        
            # 페이지 로드 대기
            time.sleep(3)

            # page 크콜링 - 시작 [ 게시글 테이블의 두 번째 <td> 요소 선택 ]
            rows = driver.find_elements(By.CSS_SELECTOR, ".table_list_tbidTbl tr")  # 테이블의 모든 행 가져오기
            for row in rows:
                try:
                    bid_num   = row.find_element(By.CSS_SELECTOR, "td:nth-of-type(2)").text  # 두 번째 <td> 가져오기
                    typeof    = row.find_element(By.CSS_SELECTOR, "td:nth-of-type(3)").text
                    bid_title = row.find_element(By.CSS_SELECTOR, "td:nth-of-type(4)").text
                    link      = row.find_element(By.CSS_SELECTOR, "td:nth-of-type(2)").find_element(By.CSS_SELECTOR,"a").get_attribute("href")
                    date      = row.find_element(By.CSS_SELECTOR, "td:nth-of-type(8)").text 
                    
                    bid_items.append(Bid_list_data(
                                    bid_num   = bid_num,
                                    bid_title = bid_title,
                                    bid_url   = link,
                                    reg_dt    = date,
                                    typeof    = typeof,
                                    site_code = self._site_code,
                                    section   = self._section
                                  ))
                   
                except Exception as e:
                    # <td>가 없는 행 (예: 헤더)일 경우 패스
                    pass
            # page 크롤링 - 종료
            
            # 데이터 저장 - 시작 
            
            #cursor = conn_master.cursor()
            for items in bid_items :
                '''check_sql = "SELECT * FROM b2b_bid_info WHERE bid_num='%s' AND site_code='%s'",(items.bid_num,items.site_code)
                cursor.execute(check_sql)
                row = cursor.fetchone()
                if row['b2b_u_key'] == "" :
                    print("insert")
                elif row['b2b_u_key'] != "" :
                    if row['state'] == "ing" :
                        print("pass")
                    else : 
                        print("update")'''
                print(items.bid_url)
            # 데이터 저장 - 종료
             
        #driver.quit() 
        return bid_items

    def detail_run(self):
    
        driver = webdriver.Chrome()   
        driver.get("https://www.g2b.go.kr:8081/ep/invitation/publish/bidInfoDtl.do?bidno=20241208100&bidseq=00&releaseYn=Y&taskClCd=3")
        x_path = {
            "bid_num"        : "입찰공고번호 - 차수",
            "bid_title"      : "공고명",
            "supply_name"    : "공고기관",
            "org_name"       : "수요기관",
            "bid_status"     : "입찰방법",
            "nbid_status"    : "낙찰방법",
            "bid_place"      : "공사현장",
            "reg_dt"         : "공고일시",
            "manager"        : "공고담당자",
            "phone"          : "공고담당자",
            "bid_reg_dt"     : "입찰개시일시",
            "bid_end_dt"     : "입찰마감일시",
            "bid_dt"         : "개찰(입찰)일시",
            "place_dt"       : "입찰참가자격등록마감일시",
            "virtual_cost"   : "",
            "virtual_cost_2" : "",
            "cir_cost"       : "",
            "area"           : "",
            "license"        : "",
            "basic_cost"     : "",
            "file_list"       : ""
        }
        
        try:
            # 테이블의 모든 행 가져오기
            rows = driver.find_elements(By.CSS_SELECTOR, "table.table_info tbody tr")
            
            # 데이터 저장용 딕셔너리
            extracted_data = {}

            # 각 행의 데이터 추출
            for row in rows:
                # <th>와 <td> 요소 추출
                try:
                    th = row.find_element(By.CSS_SELECTOR, "th").text.strip()
                    td = row.find_element(By.CSS_SELECTOR, "td").text.strip()
                    extracted_data[th] = td
                except Exception as e:
                    # 두 번째 <td>가 있는 경우 처리
                    try:
                        th_2 = row.find_element(By.XPATH, ".//th[2]").text.strip()
                        td_2 = row.find_element(By.XPATH, ".//td[2]").text.strip()
                        extracted_data[th_2] = td_2
                    except:
                        continue

            # 결과 출력
            for key, value in extracted_data.items():
                print(f"키값 : {key} => 결과값 : [ {value} ] ")
        finally:
            # WebDriver 종료
            driver.quit()
            
        '''
        # 딕셔너리를 순회하며 XPATH의 텍스트 출력
        try:
            for item, x in x_path.items():  # 딕셔너리의 키와 값을 반복
                if x:  # XPATH 값이 비어있지 않을 때만 처리
                    try:
                        x = f"//th[p='{x}']/following-sibling::td/div/strong"
                        element = driver.find_element(By.XPATH, x)
                        print(f"{item}: {element.text}")
                    except Exception as e:
                        print(f"{item}: Error - {e}")
                else:
                    print(f"{item}: No XPATH provided")
        finally:
            # WebDriver 종료
            time.sleep(10)
            driver.quit()
        '''
        
        time.sleep(10)
        '''
        cursor = conn_master.cursor()
        sql = "SELECT * FROM b2b_bid_data WHERE site_code ='%s' AND state='new'",(self._site_code)
        cursor.execute(sql)
        for row in cursor.fetchall():
            chr = driver.get(row['detail_url'])
            data1 = chr.find_element()
            ... 
            ..
            insert_sql = "insert into b2b_bid_data (name,name,name)"
            value = ('a','b','c')
            cursor.execute(insert_sql,values)
            conn_master.commit()
        cursor.close()
        conn_master.close()
        '''
        
        # detail_run 메서드의 데이터 설정
        self.site = "g2b"
        self.bid_title = "상세 데이터 타이틀"
        self.bid_dt = "2024-11-01"
        self.reg_dt = "2024-11-25"
        self.detail_url = "http://www.bidscore.co.kr/detail"
        return self

proc = realize(site_code,typeof,start_dt,end_dt,section)
proc.run()
sys.exit()
