import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.set_page_config(page_title="선생님 전용 생기부 마법사 v2.1", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #1d4ed8; color: white; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ 스마트 생기부 마법사 v2.1 (3-2 전용)")

if "records_db" not in st.session_state:
    st.session_state.records_db = []

# 3-2 명단
STUDENTS_LIST = [
    "3201 김대현", "3202 곽영훈", "3203 김민성", "3204 김세영", "3205 김시환", "3206 김재희", "3207 김지환", 
    "3208 나평안", "3209 박민기", "3210 박정진", "3211 박희준", "3212 백하얼", "3213 서승우", "3214 서한울", 
    "3215 심준식", "3216 양서율", "3217 오기택", "3218 이기은", "3219 이수호", "3220 이시우", "3221 이영조", 
    "3222 이진오", "3223 이태양", "3224 임수혁", "3225 임종원", "3226 장우혁", "3227 전지우", "3228 진서준", 
    "3229 최민기", "3230 최성훈", "3231 최은혁", "3232 홍예준"
]

# 사이드바
with st.sidebar:
    category = st.radio("기록 영역 선택", ["교과 세특", "창체(자율/진로)"])
    student_with_id = st.selectbox("학생 선택", STUDENTS_LIST)
    student_id, actual_name = student_with_id.split(" ", 1)

# 메인 로직
if category == "교과 세특":
    st.subheader(f"📖 [{student_with_id}] 교과 세특 입력")
    # (기존 교과 로직 유지...)
    act_title = st.text_input("활동 주제")
    if st.button("저장"):
        st.success("저장 완료")

else:
    st.subheader(f"🍀 [{student_with_id}] 창체 활동 입력")
    tab1, tab2 = st.tabs(["자율활동", "진로활동"])
    
    with tab1:
        auto_text = st.text_area("자율활동 내용을 입력하세요", key="auto")
        if st.button("자율활동 저장"):
            # 저장 로직
            st.success("자율활동 기록됨")
            
    with tab2:
        career_text = st.text_area("진로활동 내용을 입력하세요", key="career")
        if st.button("진로활동 저장"):
            # 저장 로직
            st.success("진로활동 기록됨")

# 데이터 관리
if st.session_state.records_db:
    st.divider()
    st.dataframe(pd.DataFrame(st.session_state.records_db))
