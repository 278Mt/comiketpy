from .data_set import InitComiketpyKey
from .data_set import AnalyzeTwitter
from .data_set import AnalyzeCircleMs
from .help import help

def init_keys(Ck="", Cs="", At="", As="", Un="", Pw=""):
    ICK = InitComiketpyKey()
    ICK.init_keys(Ck, Cs, At, As, Un, Pw)

def data_init():
    AC = AnalyzeCircleMs()
    AC.make_csv_all_id()
    AC.make_csv_all_circle_info()

    AT = AnalyzeTwitter()
    AT.get_all_followers_count()





"""
ckp.make_map()
ckp.search()
"""
