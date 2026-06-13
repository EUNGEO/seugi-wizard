import streamlit as st

# 페이지 환경 설정
st.set_page_config(page_title="선생님 전용 생기부 마법사 v1.2", layout="wide")

# --- 스타일링 (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #1d4ed8; color: white; height: 3em; font-weight: bold; }
    .stTextArea>div>div>textarea { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ 스마트 생기부 마법사 v1.2 (서술형 & 과목역량 내장형)")
st.info("💡 [업데이트 완료] 교과 역량 데이터베이스 내장 및 수준별 차등 기재 기능이 적용되었습니다.")

# --- 데이터베이스 (과목 역량 및 성취기준 맥락 내장) ---
COMPETENCY_DB = {
    "한국지리": {
        "지리적 사고력 & 공간 조망": {
            "우수": "자연환경과 인문환경의 상호작용을 파악하는 지리적 사고력이 매우 뛰어나며, 지역적 특성을 거시적인 공간 조망 능력으로 해석하는 탁월한 통찰력을 보여줌.",
            "보통": "지리적 현상에 대한 기본적인 개념을 잘 이해하고 있으며, 우리 국토의 공간적 변화 과정을 성실하게 탐구하는 태도를 나타냄."
        },
        "GIS 데이터 분석 역량": {
            "우수": "통계 자료와 GIS(지리정보시스템) 데이터를 교차 분석하여 공간적 패턴을 도출해내는 데이터 메타 인지 능력이 대단히 독창적임.",
            "보통": "수업 중 제시된 지리 통계 지표와 지도 자료를 해석하여 지역의 당면 과제를 파악하는 분석력을 보여줌."
        },
        "국토 애호 및 지속가능발전": {
            "우수": "지역 사회의 지리적 이슈에 깊은 관심을 두고 국토의 균형 발전과 지속 가능한 성장을 연계하여 대안을 모색하는 공동체적 책임감이 돋보임.",
            "보통": "우리 국토의 소중함을 인식하고 환경 보존과 지역 개발 사이의 균형이 필요함을 이해하고 있음."
        }
    },
    "통합사회": {
        "비판적 사고 및 문제해결": {
            "우수": "현대 사회의 복잡한 사회 문제를 다각적인 관점에서 분석하고, 이면에 숨겨진 구조적 원인을 날카롭게 짚어내는 비판적 사고력이 매우 탁월함.",
            "보통": "사회 현상의 특징을 객관적인 자료를 토대로 이해하려 노력하며, 탐구 과제를 논리적으로 해결하기 위해 주도적으로 참여함."
        },
        "문화 상대주의 & 다문화 수용성": {
            "우수": "다양한 문화권의 고유한 가치를 존중하는 문화 상대주의적 태도가 체화되어 있으며, 다문화 사회의 갈등을 해결하기 위한 포용적 연대 의식을 발휘함.",
            "보통": "세계 문화의 다양성을 편견 없이 수용하려는 태도를 지니고 있으며, 다문화 프로젝트에 적극적으로 동참함."
        },
        "인권 감수성 & 시민 의식": {
            "우수": "사회적 약자의 권리 보장 문제에 깊이 공감하는 높은 인권 감수성을 지니고 있으며, 민주 시민으로서의 권리와 의무를 깊이 성찰하는 리더십을 보여줌.",
            "보통": "기본권의 중요성과 인권 신장의 역사를 잘 이해하고 있으며, 학급 내 평등한 문화 조성에 기여함."
        }
    }
}

DATA_ACTS = {
    "한국지리": ["지리도서 성찰일지 작성", "지역 공공정책 제안서 프로젝트"],
    "통합사회": ["환경오염 뉴스분석 토론", "세계문화 카드놀이 기반 멘토링 활동"],
    "창체": ["인문사회 토론", "아침맞이", "1인1역", "국어 글쓰기", "1학기 프로젝트", "학급 진로발표", "학급 독서발표"]
}

# --- 바이트 계산기 ---
def calc_bytes(text):
    return len(text.encode('utf-8-sig'))

# --- 사이드바 ---
with st.sidebar:
    st.header("👤 학생 정보 입력")
    name = st.text_input("학생 성함", value="홍길동")
    st.divider()
    category = st.selectbox("기록 영역 선택", ["교과 세특", "창체(자율/진로)"])

# --- 메인 영역 ---
if category == "교과 세특":
    subj = st.radio("과목 선택", ["한국지리", "통합사회"], horizontal=True)
    st.subheader(f"📖 {subj} 세특 핵심 역량 연동 작성")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("🎯 **성취기준 기반 과목 역량 선택**")
        selected_comps = []
        for comp_name in COMPETENCY_DB[subj].keys():
            if st.checkbox(comp_name):
                selected_comps.append(comp_name)
                
    with col2:
        st.write("📊 **학생 수행 수준 평가**")
        level = st.radio("이 학생의 성취 수준은?", ["우수", "보통"], horizontal=True)
        st.write("⚙️ **수행한 세부 활동 선택**")
        selected_acts = st.multiselect("활동 선택", DATA_ACTS[subj])

    memo = st.text_area("✍️ 개별 특이사항 및 관찰 메모", placeholder="예: 구체적인 통계 자료를 인용함, 모둠 활동 시 갈등을 중재함 등")
    
    if st.button("✨ 서술형 세특 문장 합성하기"):
        comp_texts = [COMPETENCY_DB[subj][c][level] for c in selected_comps]
        act_text = f"교과 수업 중 " + ", ".join(selected_acts) + " 등의 활동을 주도적으로 수행하였으며," if selected_acts else ""
        
        base_combined = " ".join(comp_texts)
        final_text = f"{name} 학생은 {base_combined} {act_text} {memo}".strip()
        
        st.success("🎉 완성된 서술형 교과 세특 문구")
        st.code(final_text, language=None)
        
        b_size = calc_bytes(final_text)
        if b_size > 1500:
            st.error(f"⚠️ 바이트 한도 초과! 현재: {b_size} / 1500 Byte")
        else:
            st.success(f"✅ 나이스 입력 가능 수치: {b_size} / 1500 Byte")

else:
    st.subheader("🍀 학급 창체 활동 배치 (서술형 반영)")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("🔹 **자율활동**")
        auto_sel = st.multiselect("자율활동 배치 항목", DATA_ACTS["창체"], key="auto")
    with col2:
        st.write("🔸 **진로활동**")
        career_sel = st.multiselect("진로활동 배치 항목", DATA_ACTS["창체"], key="career")
        
    if st.button("✨ 창체 기록 합치기"):
        res_auto = f"{name} 학생은 " + " ".join([f"{a} 활동에 참여하여 타인을 배려하는 태도를 바탕으로 학급 공동체 발전에 기여함." for a in auto_sel]) if auto_sel else "배정된 활동 없음"
        res_career = f"{name} 학생은 " + " ".join([f"{c} 활동을 통해 자신의 진로 장벽을 진단하고, 이를 극복하기 위한 구체적인 탐구 역량을 보여줌." for c in career_sel]) if career_sel else "배정된 활동 없음"
        
        st.divider()
        st.success("🎉 최종 창체 서술형 결과")
        st.text_area("자율활동 복사용 (한도 1500 Byte)", res_auto, height=120)
        st.caption(f"자율 바이트: {calc_bytes(res_auto)} Byte")
        st.text_area("진로활동 복사용 (한도 2100 Byte)", res_career, height=120)
        st.caption(f"진로 바이트: {calc_bytes(res_career)} Byte")
