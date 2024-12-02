"""_summary_
   1. .py args 
    site_code : 사이트 코드값 DB와 동일 ex : [ 01 , 02 ]
    typeof    : list or detail ex : 'list' , 'detail'
    start_dt  : list 시작날짜 설정 : '2024-11-20'
    end_dt    : list 종료날짜 설정 : '2024-11-30'
    section   : B01 공사 , B02 용역, B03 물품 , B99 통합  'B01
    실행       : .list.py --site_code g2b --typeof list --start_dt 2024-11-20 --end_dt 2024-11-30 --section B01
"""

import argparse

# ArgumentParser 객체 생성
parser = argparse.ArgumentParser(description="Process some input arguments.")

# 인자값 추가
parser.add_argument('--site_code', type=str, help='Name of the person')
parser.add_argument('--typeof', type=str, help='Age of the person')
parser.add_argument('--start_dt', type=str, help='Age of the person')
parser.add_argument('--end_dt', type=str, help='Age of the person')
parser.add_argument('--section', type=str, help='Age of the person')

# 인자값 파싱
args = parser.parse_args()

site_code = args.site_code
typeof    = args.typeof
start_dt  = args.start_dt
end_dt    = args.end_dt
section   = args.section

# 테스트 값
site_code = "01"
typeof    = "list"
start_dt  = "2024-11-20"
end_dt    = "2024-11-30"
section   = "B01"

if site_code == "01" : 
    import application.g2b as g2b
    proc = g2b.realize(typeof,start_dt,end_dt,section)
    proc.run()
elif site_code == "03":
    import application.kepco as kepco
    ca = kepco.realize(typeof)
    ca.run()
