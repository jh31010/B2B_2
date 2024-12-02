from dataclasses import dataclass

@dataclass
class Bid_list_data:
    bid_num: str
    bid_title: str
    bid_url: str
    reg_dt : str
    typeof : str
    site_code : str
    
@dataclass
class Bid_detail_data:
    bid_num: str
    bid_title: str
    bid_url: str
    reg_dt : str
    typeof : str
    site_code : str

@dataclass
class Nbid_list_data:
    bid_num: str
    bid_title: str
    bid_url: str
    reg_dt : str
    typeof : str
    site_code : str
    
@dataclass
class Nbid_detail_data:
    bid_num: str
    bid_title: str
    bid_url: str
    reg_dt : str
    typeof : str
    site_code : str
    
@dataclass
class Nbid_Company_data:
    bid_num: str
    bid_title: str
    bid_url: str
    reg_dt : str
    typeof : str
    site_code : str