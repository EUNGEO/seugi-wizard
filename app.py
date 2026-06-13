import streamlit as st
import pandas as pd
import io
from datetime import datetime

# 페이지 환경 설정
st.set_page_config(page_title="선생님 전용 생기부 마법사 v3.5", layout="wide")

st.markdown("""
    <style>
    .standard-box { background-color: #fef3c7; padding: 15px; border-radius: 10px; border-left: 5px solid #d97706; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ 스마트 생기부 마법사 v3.5 (데이터 복구 완료)")

# --- 🌟 성취기준 데이터베이스 복구 ---
ACTIVITY_MASTER_DB = {
    "한국지리": {
        "지역공공정책서": {
            "성취기준": [
                "[12한지04-01] 우리나라 촌락의 최근 변화상을 파악하고, 도시의 발달 과정 및 도시체계의 특성을 탐구한다.",
                "[12한지04-02] 도시의 지역 분화 과정 및 내부 구조의 변화를 이해하고, 대도시권의 형성 및 확대가 주민 생활에 미친 영향을 설명한다.",
                "[12한지04-03] 주요 대도시를 사례로 도시 계획과 재개발 과정이 도시 경관과 주민 생활에 미친 영향에 대해 분석한다.",
                "[12한지04-04] 지역 개발의 영향으로 나타나는 공간 및 환경 불평등과 지역 갈등 문제를 파악하고, 국토 개발 과정이 우리 국토에 미친 영향에 대해 평가한다."
            ]
        }
    },
    "통합사회": {
        "다문화 공존 데이터 프로젝트": {
            "성취기준": [
                "[10통사1-04-03] 문화적 차이에 대한 상대주의적 태도의 필요성을 이해하고, 보편 윤리의 차원에서 자문화와 타문화를 평가한다.",
                "[10통사1-04-04] 다문화 사회의 현황을 조사하고, 문화적 다양성을 존중하는 태도를 바탕으로 갈등 해결 방안을 모색한다."
            ]
        },
        "환경문제 신문기사 분석하기": {
            "성취기준": [
                "[10통사1-03-01] 자연환경이 인간의 생활에 미치는 영향에 관한 과거와 현재의 사례를 조사하여 분석하고, 안전하고 쾌적한 환경에서 살아가는 것이 시민의 권리임을 주장한다.",
                "[10통사1-03-02] 자연에 대한 인간의 다양한 관점을 사례를 통해 비교하고, 인간과 자연의 바람직한 관계를 제안한다.",
                "[10통사1-03-03] 환경 문제 해결을 위한 정부, 시민사회, 기업 등의 다양한 노력을 조사하고, 생태시민으로서 실천 방안을 모색한다."
            ]
        }
    }
}

# --- 메인 작업 로직 ---
category = st.selectbox("기록 영역 선택", ["교과 세특", "창체(자율/진로)"])
subj_sidebar = st.radio("기준 과목 선택", ["한국지리", "통합사회"], horizontal=True)

if category == "교과 세특":
    selected_act = st.selectbox("활동 선택", list(ACTIVITY_MASTER_DB[subj_sidebar].keys()))
    act_meta = ACTIVITY_MASTER_DB[subj_sidebar][selected_act]
    
    st.write("💡 **[참고] 이 활동의 교육과정 국가 성취기준**")
    for std in act_meta["성취기준"]:
        st.markdown(f'<div class="standard-box">{std}</div>', unsafe_allow_html=True)
    
    st.text_input("활동 주제", key="act_title")
    st.text_area("활동 세부 내용", key="act_detail")
    
    if st.button("문장 만들기"):
        st.success(f"{st.session_state.act_title}을(를) 주제로 {st.session_state.act_detail}")
