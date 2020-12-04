import sys
sys.path.append('..')

from flask import Flask, jsonify, request
import pandas as pd

from fin_app.utils.config import DataLocationConfig


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False 

df_stocklist = pd.read_csv(
    DataLocationConfig.STOCKLIST_FILE
)
df_company_data = pd.read_csv(
    DataLocationConfig.COMPANY_DATA
)
print(df_company_data.columns)
df_company_data['証券コード'] = df_company_data['証券コード'].astype(int)
BASIC_DATA_COLS = [
    '提出日', '会計期間終了日', '証券コード', '会社名', '業種', '従業員数', '平均臨時雇用人員', '平均年齢', '平均勤続年数', '平均年間給与'
]
df_company_basic_data = df_company_data[BASIC_DATA_COLS]
FINANCIAL_DATA_COLS = [
    '提出日', '会計期間終了日', '証券コード', '会社名', '所有株式数',
    '発行済株式（自己株式を除く。）の総数に対する所有株式数の割合', '発行済株式総数', '連結子会社の数', '１株当たり純資産',
    '自己資本比率', '現金及び現金同等物の残高', '資産', '流動資産', '固定資産', '有形固定資産', '無形固定資産',
    '投資その他の資産', '負債', '流動負債', '短期借入金', '1年内償還予定の社債', '1年内返済予定の長期借入金',
    '固定負債', '社債', '転換社債型新株予約権付社債', 'コマーシャル・ペーパー', '長期借入金', '純資産', '株主資本',
    '資本金', '資本剰余金', '利益剰余金', '自己株式', '評価・換算差額等', '売上高', '売上原価', '売上総利益',
    '販売費及び一般管理費', '給料及び手当', '減価償却費、販売費及び一般管理費', '研究開発費', '営業利益', '営業外収益',
    '営業外費用', '支払利息', '経常利益', '特別利益', '特別損失', '税引前純利益', '法人税等', '純利益',
    '親会社株主に帰属する純利益', '包括利益', '１株当たり純利益', '調整1株当たり純利益', '１株当たり配当額', '株価収益率',
    '自己資本利益率', '営業活動によるキャッシュ・フロー', '減価償却費、営業活動によるキャッシュ・フロー',
    '投資活動によるキャッシュ・フロー', '財務活動によるキャッシュ・フロー', '現金及び現金同等物の増減', '前期資産', '前期売上高',
    '前期純利益', '粗利益', '売上高総利益率', '売上高営業利益率',
    '売上高経常利益率', '売上高販管費率', '総資本回転率', '流動比率', '売上高変化率', '純利益変化率', '期首期末平均資産',
    '総資産経常利益率', '総資産純利益率', '総資産親会社株主に帰属する純利益率', '自己資本', '有利子負債', 
]
df_company_financial_data = df_company_data[FINANCIAL_DATA_COLS]


@app.route('/company_list', methods=['GET'])
def company_list():

    sector = request.args.get('sector', None)

    if sector is not None:
        df = df_stocklist[df_stocklist['業種分類']==sector]
    else:
        df = df_stocklist.copy()

    if len(df) > 0:
        company_list = df.apply(lambda x: {
            'company_name': x['銘柄名'].replace('(株)', ''),
            'ticker': x['銘柄コード'],
            'sector': x['業種分類']
        }, axis=1).to_list()
    else:
        company_list = []

    return jsonify({'company_list': company_list})


@app.route('/company_basic_data', methods=['GET'])
@app.route('/company_basic_data/<int:ticker>', methods=['GET'])
def company_basic_data(ticker: int=None):

    if ticker is not None:
        df = df_company_basic_data[df_company_basic_data['証券コード']==ticker]
    else:
        df = df_company_basic_data

    if len(df) > 0:
        company_basic_data = df.apply(
            lambda x: {col_name: x[col_name] for col_name in BASIC_DATA_COLS},
            axis=1
        ).to_list()
    else:
        company_basic_data = []

    return jsonify({'company_basic_data': company_basic_data})


@app.route('/company_financial_data', methods=['GET'])
@app.route('/company_financial_data/<int:ticker>', methods=['GET'])
def company_financial_data(ticker: int=None):

    if ticker is not None:
        df = df_company_financial_data[df_company_financial_data['証券コード']==ticker]
    else:
        df = df_company_financial_data

    if len(df) > 0:
        company_financial_data = df.apply(
            lambda x: {col_name: x[col_name] for col_name in FINANCIAL_DATA_COLS},
            axis=1
        ).to_list()
    else:
        company_financial_data = []

    return jsonify({'company_financial_data': company_financial_data})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
