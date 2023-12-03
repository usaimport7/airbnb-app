import streamlit as st
from datetime import datetime
import os
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# Secretsから認証情報を取得
google_credentials = json.loads(st.secrets["google_credentials"]["key"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(google_credentials, scope)
# 環境変数からGoogle認証情報を取得
google_credentials_path = os.getenv('GOOGLE_CREDENTIALS_JSON_PATH')

# Googleスプレッドシートの設定
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(google_credentials_path, scope)
client = gspread.authorize(creds)
sheet = client.open('checkin-airbnb').sheet1

# アプリのタイトル
st.title('Airbnb Checkin Form / Airbnb チェックインフォーム')

# 国籍の選択肢
nationalities = [
    '', 'Japan 日本', 'USA 米国', 'China 中国', 'France フランス',
    'Germany ドイツ', 'Australia オーストラリア', 'Korea 韓国',
    'United Kingdom イギリス', 'Canada カナダ', 'Brazil ブラジル', 'Other その他'
]

# 職業の選択肢
occupations = [
    '', 'Office Worker 会社員', 'Freelance フリーランス', 'Public Servant 公務員',
    'Business Owner 会社経営', 'Housewife 主婦', 'Part-time Job アルバイト',
    'Unemployed 無職', 'Student 学生', 'Other その他'
]

# フォームの作成
with st.form(key='checkin_form'):
    room_number = st.text_input('Room Number / 部屋番号', '')
    name = st.text_input('Name / 名前', '')
    gender = st.selectbox('Gender / 性別', ['', 'Male / 男性', 'Female / 女性', 'Other / その他'])
    age = st.selectbox('Age / 年齢', list(range(101)))
    nationality = st.selectbox('Nationality / 国籍', nationalities)
    if nationality == 'Other その他':
        nationality_other = st.text_input('Nationality (Other) / 国籍（その他）', '')
    else:
        nationality_other = ''

    # パスポート番号の入力欄（日本人以外の場合は必須）
    if nationality != 'Japan 日本':
        passport_number = st.text_input('Passport Number (Required for non-Japanese) / パスポート番号（日本人以外の場合は必須）', '')
    else:
        passport_number = st.text_input('Passport Number / パスポート番号', '', disabled=True)

    address = st.text_input('Home Address / 住所', '')
    occupation = st.selectbox('Occupation / 職業', occupations)
    if occupation == 'Other その他':
        occupation_other = st.text_input('Occupation (Other) / 職業（その他）', '')
    else:
        occupation_other = ''

    checkin_date = st.date_input('Check-in Date / チェックイン日', min_value=datetime.today())
    checkout_date = st.date_input('Check-out Date / チェックアウト日', min_value=datetime.today())
    previous_location = st.text_input('Previous Location / 前泊地', '')
    next_destination = st.text_input('Next Destination / 次の宿泊地', '')
    submit_button = st.form_submit_button(label='Send / 送信')

    if submit_button:
        final_nationality = nationality_other if nationality == 'Other その他' else nationality
        final_occupation = occupation_other if occupation == 'Other その他' else occupation

        # スプレッドシートに送信するデータをコンソールに出力（デバッグ用）
        data_to_send = [
            room_number, 
            name, 
            final_nationality, 
            passport_number, 
            gender, 
            age, 
            address, 
            final_occupation, 
            checkin_date.strftime('%Y-%m-%d'), 
            checkout_date.strftime('%Y-%m-%d'), 
            previous_location, 
            next_destination
        ]
        print("Sending data:", data_to_send)

        # スプレッドシートにデータを送信
        sheet.append_row(data_to_send)

        st.success('Data submitted successfully. / データを送信しました。')
