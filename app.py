import streamlit as st
import pandas as pd
import io
from datetime import datetime

# 페이지 환경 설정
st.set_page_config(page_title="선생님 전용 생기부 마법사 v2.1", layout="wide")

# --- 스타일링 (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #1d4ed8; color: white; height: 3em; font-weight: bold; }
    .stTextArea>div>div>textarea { background-color: #ffffff; }
    div[data-testid="stExpander"] { background-color: #f1f5f9; border-radius: 10px; }
    .activity-box { background-color: #eff6ff; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; margin-bottom: 15px; }
    .tab-header { font-size: 1.2em; font-weight: bold; color: #1e40af; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ 스마트 생기부 마법사 v2.1 (우리 반 3-2 전용)")
st.info("💡 [v2.1 업데이트] 우리 반 명단이 연동되었으며, 창체 영역이 자율/진로 탭 구조로 개편되었습니다.")

# --- 세션 상태(누적 기록 장부) 초기화 ---
if "records_db" not in st.session_state:
    st.session_state.records_db = []

# --- 3학년 2반 전용 명단 데이터베이스 ---
STUDENTS_LIST = [
    "3201 김대현", "3202 곽영훈", "3203 김민성", "3204 김세영", "3205 김시환",
    "3206 김재희", "3207 김지환", "3208 나평안", "3209 박민기", "3210 박정진",
    "3211 박희준", "3212 백하얼", "3213 서승우", "3214 서한울", "3215 심준식",
    "3216 양서율", "3217 오기택", "3218 이기은", "3219 이수호", "3220 이시우",
    "3221 이영조", "3222 이진오", "3223 이태양", "3224 임수혁", "3225 임종원",
    "3226 장우혁", "3227 전지우", "3228 진서준", "3229 최민기", "3230 최성훈",
    "3231 최은혁", "3232 홍예준"
]

# --- 교과 마스터 DB (기존 데이터 유지) ---
ACTIVITY_MASTER_DB = {
    "한국지리": {
        "지리도서 성찰일지 작성": {
            "역량명": "지리적 사고력 & 공간 조망 역량",
            "우수": "독서 성찰 활동 중 자연환경과 인문환경의 상호작용을 파악하는 지리적 사고력이 매우 뛰어나며, 도서 속 핵심 이슈를 거시적인 공간 조망 능력으로 재해석하는 탁월한 통찰력을 보여줌.",
            "보통": "지리 관련 도서를 읽고 주요 지리적 개념과 현상을 올바르게 이해하려 노력하였으며, 성찰일지를 기한 내에 성실하게 작성하는 태도를 나타냄."
        },
        "지역 공공정책 제안서 프로젝트": {
            "역량명": "GIS 데이터 분석 및 국토발전 역량",
            "우수": "지역의 실질적 통계 자료와 GIS 데이터를 교차 분석하여 공간적 불균형 패턴을 도출해내는 데이터 메타 인지 능력이 독창적이며, 국토의 지속 가능한 성장을
