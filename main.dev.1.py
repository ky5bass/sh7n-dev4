# supabaseの代わりにjsonを使用

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import json # from supabase import create_client
import shutil
from os.path import relpath
# from os import environ
from datetime import timedelta
from datetime import datetime as _datetime

obj_distDirPath = Path(__file__).parent / 'public'  # 注 このディレクトリの中身は空であるものとして以下進める
obj_srcDirPath  = Path(__file__).parent / 'static'
obj_tplDirPath  = Path(__file__).parent / 'templates'

# 曜日リスト
lst_days = [ { "symbol": "sun", "name_ja": "日曜日", },
             { "symbol": "mon", "name_ja": "月曜日", },
             { "symbol": "tue", "name_ja": "火曜日", },
             { "symbol": "wed", "name_ja": "水曜日", },
             { "symbol": "thu", "name_ja": "木曜日", },
             { "symbol": "fri", "name_ja": "金曜日", },
             { "symbol": "sat", "name_ja": "土曜日", }, ]

def relative_path(
    absolute: str,
    cwd: str,
) -> str:
    """cwdに対するabsoluteの相対パスを取得"""

    # 引数のバリデーションチェック
    if '/' != absolute[0]: raise ValueError(f"argument 'absolute' must start with '/': {absolute}")
    if '/' != cwd[0]:      raise ValueError(f"argument 'cwd' must start with '/': {cwd}")
    
    # 相対パスを取得
    str_retPath = relpath(absolute, cwd)

    return str_retPath

def main():
    # ソースディレクトリを丸ごとコピー
    shutil.copytree(obj_srcDirPath, obj_distDirPath / obj_srcDirPath.name)

    # 出力先ディレクトリ内にbunchディレクトリを作成
    obj_targetDirPath = obj_distDirPath / 'bunch'
    obj_targetDirPath.mkdir()
    for dct_day in lst_days:
        str_targetDaySymbol = dct_day["symbol"]
        obj_targetDirPath = obj_distDirPath / f'bunch/{str_targetDaySymbol}'
        obj_targetDirPath.mkdir()

    # すべての束の情報を取得
    obj_jsonPath = Path(__file__).parent / f'test/supabase-test-data/bunches.json'
    with obj_jsonPath.open('rt') as f:
        lst_bunches: list = json.load(f)

    # レンダリングの準備
    obj_env = Environment(loader=FileSystemLoader(obj_tplDirPath), trim_blocks=False)
    obj_env.globals['relative_path'] = relative_path    # テンプレにrelative_path関数を埋め込み
    # 参考 関数埋め込みの方法→ https://gist.github.com/snaka/2575718

    # 本日のdayIdを取得
    obj_now = _datetime.now() + timedelta(hours=+9)
    # 注 9時間後にすることで日本時間に変換
    int_todayId = obj_now.weekday()     # 月曜=>0, ..., 日曜=>6

    # トップページをレンダリング
    obj_template = obj_env.get_template('index.tpl')
    str_output = obj_template.render(int_TodayId=int_todayId,
                                     lst_Days=lst_days,
                                     str_Cwd='/',)
    obj_outputPath = obj_distDirPath / 'index.html'
    with obj_outputPath.open('wt') as f:
        f.write(str_output)
    # 参考 extendsの方法→ https://www.python.ambitious-engineer.com/archives/809

    for int_dayId, dct_day in enumerate(lst_days):
        # 曜日に対応する束のカードを取得
        obj_jsonPath = Path(__file__).parent / f'test/supabase-test-data/bunch{int_dayId}.json'
        with obj_jsonPath.open('rt') as f:
            lst_cards: list = json.load(f)

        # 更新日付を取得
        dct_bunch = lst_bunches[int_dayId]
        str_dateRaw = dct_bunch['updated_at']
        obj_tmpDtm = _datetime.strptime(str_dateRaw, r'%Y-%m-%d')
        str_date = obj_tmpDtm.strftime(r'%Y年%-m月%-d日')
        # 注 %-m %-d で月日を1桁で表現できる。ただしUnix環境に依存しており、Windowsなら %#m %#d らしい。
        #    参考 https://stackoverflow.com/questions/904928/python-strftime-date-without-leading-0#answer-2073189

        # bunchページをレンダリング
        obj_template = obj_env.get_template('bunch.tpl')
        str_output = obj_template.render(lst_Cards=lst_cards,
                                         str_CreatedDate=str_date,
                                         int_TargetDayId=int_dayId,
                                         lst_Days=lst_days,
                                         str_Cwd='/bunch', )
        str_targetDaySymbol = dct_day['symbol']
        obj_outputPath = obj_distDirPath / f'bunch/{str_targetDaySymbol}/index.html'
        with obj_outputPath.open('wt') as f:
            f.write(str_output)

if __name__ == '__main__':
    main()