from libraries.items_init import list_field_items

class list_realize(list_field_items):
    
    def __init__(self, state):
        super().__init__()  # 부모 클래스의 초기화 메서드 호출
        self._state = state

    def run(self):
        if self._state == "list":
            return self.list_run()
        elif self._state == "detail" :
            return self.detail_run()
            
    def list_run(self):
        # list_run 메서드의 데이터 설정
        self.site = "kepco"
        self.bid_title = "013데이터 타이틀"
        self.bid_dt = "2024-10-31"
        self.reg_dt = "2024-11-22"
        self.detail_url = "http://www.bidscore.co.kr"
        return self

    def detail_run(self):
        # detail_run 메서드의 데이터 설정
        self.site = "kepco"
        self.bid_title = "상세 데이터 타이틀"
        self.bid_dt = "2024-11-01"
        self.reg_dt = "2024-11-25"
        self.detail_url = "http://www.bidscore.co.kr/detail"
        return self