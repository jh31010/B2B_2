from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import sys

# 웹 드라이버 생성
driver = webdriver.Chrome()
# 네이버 홈페이지 열기
driver.get("https://www.naver.com")

rand_str = ['조달청 공동도급','확보예가','낙찰잘되는 방법','비드스코어','투데이낙찰리포트','공동도급업체 빨리 찾기','입찰','공고정보','적격심사 별지','적격심사','낙찰자선정밥법','1순위문자','공동도급']

numbers = list(range(1,5))
random.shuffle(numbers)

#1 text - search
def search_str_chrome(str = "") :
    search_box  = driver.find_element(By.NAME, "query")  # 네이버 검색창의 name 속성은 'query'
    
    if search_box.get_attribute("value") != "" :
        for _ in range(len(search_box.get_attribute("value"))):
            search_box.send_keys(Keys.BACKSPACE)
            time.sleep(0.1)  # 0.1초 대기
    if str == "" :
        search_text = rand_str[random.randint(0,len(rand_str)-1)]     
    else :
        search_text = str
        
    #search_text = "비드스코어"
    for char in search_text:
        search_box.send_keys(char)  # 한 글자씩 입력
        time.sleep(0.2)  # 각 글자 사이에 0.3초 대기 (조정 가능)
        
    search_box.send_keys(Keys.RETURN)  # 또는 Keys.ENTER

#2 browser - scroll - up
def browser_scroll_down() :
    rand_position     = random.randint(2,4)
    print(f"scroll_position : {rand_position}")
    
    #현재 스크롤 위치 초기화
    current_scroll_position = 0 
    # 페이지 전체 높이 가져오기
    page_height = driver.execute_script("return document.body.scrollHeight")

    break_point = random.randint(4,10)
    idx         = 1
    # 천천히 스크롤 내리기
    while current_scroll_position < page_height/rand_position:
        rand_scroll_inc   = random.randint(100,230) 
        print(f"scroll_inc : {rand_scroll_inc}")
        current_scroll_position += rand_scroll_inc
        driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")
        rand_scroll_speed = random.randint(2,5)
        rand = rand_scroll_speed*0.1
        print(f"scroll_speed : {rand}")
        print(f"break_point : {break_point}")
        print(f"idx : {idx}")
        if break_point == idx :
            time.sleep(random.randint(2,8))
            idx = 1 
            break_point = random.randint(4,10)
        time.sleep(rand)  # 0.1초 대기 (조정 가능)
        idx = idx+1

#3 browser - scroll - down
def browser_scroll_up() :
    current_scroll_position = driver.execute_script("return window.pageYOffset;")
    # 천천히 스크롤 위로 올리기
    while current_scroll_position > 0:
        rand_scroll_inc   = random.randint(150,280) 
        print(f"scroll_inc : {rand_scroll_inc}")
        current_scroll_position -= rand_scroll_inc
        driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")
        time.sleep(0.1)  # 0.1초 대기

def search_str_link_click(str,enum) :
    # 모든 링크의 href 속성 출력
    print("search_str_link_click")
    links = driver.find_elements(By.TAG_NAME, "a")
    rand  = random.randint(1,4)
    print(rand)
    rc    = 1
    for link in links:
        href = link.get_attribute("href")  # href 속성 가져오기
        text = link.text  # 링크 텍스트 가져오기
        if href:  # href가 존재하는 경우에만 출력
            print(f"텍스트: {text}, 링크: {href}")
            if str in text :
                if enum in href :
                    site_move(href)
                    return True
                    #if rand == rc :
                       
                    rc = rc+1
            

def site_move(str) :
    driver.get(str)


#명령어 실행
search_str_chrome()
browser_scroll_down()
driver.back()
time.sleep(random.randint(3,5))  # 0.1초 대기
search_str_chrome()
time.sleep(random.randint(3,10))  # 0.1초 대기
search_str_chrome("비드스코어")
time.sleep(random.randint(3,10))  # 0.1초 대기
browser_scroll_down()
search_str_link_click("예가","blog")
# 화면에 보이는 모든 <a> 태그 가져오기



#browser_scorll_up()
#browser_scroll_down()
#search_str_chrome()
#site_move()
time.sleep(10)
sys.exit(1)
choice = random.randint(1,6)


#time.sleep(random.randint(5, 12))  # 5초 대기

choice = random.randint(1,5)
choice = 1
if choice == 1 :
    search_box = driver.find_element(By.NAME, "query")  # 네이버 검색창의 name 속성은 'query'
    search_term = "조달청 공동도급"

    for char in search_term:
        search_box.send_keys(char)  # 한 글자씩 입력
        time.sleep(0.2)  # 각 글자 사이에 0.3초 대기 (조정 가능)
    
    
         # 화면에 보이는 블로그 링크 수집
    blog_links = driver.find_elements(By.CSS_SELECTOR, "a")  # 링크 태그 (필요시 CSS 선택자 수정)
    print(blog_links)
    # 필터링: 특정 링크만 선택 (네이버 블로그 링크만 클릭하는 조건 설정)
    #blog_links = [link for link in blog_links if "blog.naver.com" in link.get_attribute("href")]
    
    '''
    # 랜덤하게 링크 선택 후 클릭
    if blog_links:  # 링크가 존재하는 경우에만 클릭
        random_link = random.choice(blog_links)
        print("랜덤 선택된 링크:", random_link.get_attribute("href"))
        #random_link.click()
    else:
        print("블로그 링크를 찾을 수 없습니다.")
    '''
    # 검색 버튼 클릭
    search_button = driver.find_element(By.CLASS_NAME, "btn_search")  # 검색 버튼의 class 이름
    search_button.click()
    print('active 1')    
    
    # 현재 스크롤 위치 초기화
    current_scroll_position = 0 
    scroll_increment = 100  # 한 번에 스크롤할 픽셀 크기

    # 페이지 전체 높이 가져오기
    page_height = driver.execute_script("return document.body.scrollHeight")

    # 천천히 스크롤 내리기
    while current_scroll_position < page_height/3:
        scroll_increment = random.randint(100,230)
        current_scroll_position += scroll_increment
        driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")
        rand = random.randint(2,21)
        rand = rand*0.1
        print(rand)
        time.sleep(rand)  # 0.1초 대기 (조정 가능)
    
    scroll_step = 100
    # 천천히 스크롤 위로 올리기
    while current_scroll_position > 0:
        current_scroll_position -= scroll_step
        driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")
        time.sleep(0.1)  # 0.1초 대기

    time.sleep(random.randint(3, 6))  # 5초 대기
 
   
    
    time.sleep(random.randint(15, 67))  # 5초 대기
 
    search_box = driver.find_element(By.NAME, "query")  # 네이버 검색창의 name 속성은 'query'
    for _ in range(len(search_term)):
        search_box.send_keys(Keys.BACKSPACE)
        time.sleep(0.1)  # 0.1초 대기
 
    search_box = driver.find_element(By.NAME, "query")  # 네이버 검색창의 name 속성은 'query'
    search_term = "확보예가"
    for char in search_term:
        search_box.send_keys(char)  # 한 글자씩 입력
        time.sleep(0.2)  # 각 글자 사이에 0.3초 대기 (조정 가능)
    
    time.sleep(random.randint(2, 3))  # 5초 대기
    
    # 검색 버튼 클릭
    search_button = driver.find_element(By.CLASS_NAME, "bt_search")  # 검색 버튼의 class 이름
    search_button.click()
    print('active 1')    

    time.sleep(random.randint(15, 67))  # 5초 대기
    
if choice == 2 :
    print('active 1')    
if choice == 3 :
    print('active 1')    
if choice == 4 :
    print('active 1')    
if choice == 5 :
    print('active 1')    
        
# 검색창에 단어 입력







'''

'''
# 페이지 유지 시간


# 브라우저 닫기
#driver.quit()


