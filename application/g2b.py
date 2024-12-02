from selenium import webdriver
from selenium.webdriver.common.by import By
from dataclasses import asdict
from urllib.parse import urlencode, quote
from datetime import datetime
import json
import time
from libraries.items_init import Bid_list_data

class realize():
     
    def __init__(self, typeof,start_dt,end_dt,section):
        super().__init__()  # 부모 클래스의 초기화 메서드 호출
        self._typeof      = typeof
        self._start_dt    = start_dt
        self._end_dt      = end_dt
        self._limit       = "30"
        self._section     = section 

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

        for page in range(1,5) :
            print(f"크롤링 중: {page} 페이지")
            list_url = encoded_url+f"&currentPageNo={page}"
            print(list_url)
            driver.get(list_url)
        
            # 페이지 로드 대기
            time.sleep(3)

           # 게시글 테이블의 두 번째 <td> 요소 선택
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
                                    site_code = "01"
                                  ))
                    #items.append(Post(title = bid_title,link = link ,author = typeof , date = date))
                    
                except Exception as e:
                    # <td>가 없는 행 (예: 헤더)일 경우 패스
                    pass
            # 크롤링 종료
            json_data = json.dumps([asdict(item) for item in bid_items], ensure_ascii=False, indent=4)
            print(json_data)
        #driver.quit() 
        return bid_items

    def detail_run(self):
        # detail_run 메서드의 데이터 설정
        self.site = "g2b"
        self.bid_title = "상세 데이터 타이틀"
        self.bid_dt = "2024-11-01"
        self.reg_dt = "2024-11-25"
        self.detail_url = "http://www.bidscore.co.kr/detail"
        return self