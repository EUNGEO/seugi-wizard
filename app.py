import streamlit as st

# 페이지 환경 설정
st.set_page_config(page_title="선생님 전용 생기부 마법사", layout="wide", initial_sidebar_state="expanded")

# --- 스타일링 (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #10b981; color: white; height: 3em; }
    .stTextArea>div>div>textarea { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ 스마트 생기부 마법사 v1.1 (Web)")
st.info("이 사이트는 선생님 전용입니다. 입력하신 정보는 브라우저를 닫으면 저장되지 않으니 안심하세요.")

# --- 데이터베이스 ---
DATA = {
    "한국지리": ["학습역량 활동", "지리도서 성찰일지", "지역 공공정책서 작성"],
    "통합사회": ["학습역량 활동", "환경오염 뉴스분석", "다문화 지역분석", "세계문화 카드놀이"],
    "창체": ["인문사회 토론", "아침맞이", "1인1역", "국어 글쓰기", "1학기 프로젝트", "학급 진로발표", "학급 독서발표"]
}

# --- 로직 함수 ---
def calc_bytes(text):
    return len(text.encode('utf-8-sig')) # 나이스와 가장 유사한 바이트 계산식

# --- 사이드바 영역 ---
with st.sidebar:
    st.header("👤 학생 정보")
    name = st.text_input("학생 성함", value="홍길동")
    st.divider()
    category = st.selectbox("기록 영역 선택", ["교과 세특", "창체(자율/진로)"])

# --- 메인 영역 ---
if category == "교과 세특":
    subj = st.radio("과목 선택", ["한국지리", "통합사회"], horizontal=True)
    st.subheader(f"📖 {subj} 세특 작성")
    
    selected = st.multiselect("수행한 활동을 골라주세요 (최대 2~3개)", DATA[subj])
    memo = st.text_area("학생별 특이사항 (메모)", placeholder="예: 구체적인 통계 수치를 활용함, 질문이 날카로움 등")
    
    if st.button("문장 생성하기"):
        # 여기에 나중에 선생님이 주실 '세부 조건' 로직이 들어갑니다.
        base = " ".join([f"{act}에 참여하여 탁월한 성과를 보임." for act in selected])
        final = f"{name} 학생은 {base} {memo}"
        st.success("완성된 문구")
        st.code(final, language=None)
        st.caption(f"현재 바이트: {calc_bytes(final)} / 1500 (교과세특 한도)")

else:
    st.subheader("🍀 학급 창체 활동 배치")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("🔹 **자율활동**")
        auto_sel = st.multiselect("자율활동으로 넣을 항목", DATA["창체"], key="auto")
    with col2:
        st.write("🔸 **진로활동**")
        career_sel = st.multiselect("진로활동으로 넣을 항목", DATA["창체"], key="career")
        
    if st.button("창체 기록 합치기"):
        res_auto = f"{name} 학생은 " + " ".join([f"{a} 활동을 통해 리더십을 발휘함." for a in auto_sel])
        res_career = f"{name} 학생은 " + " ".join([f"{c} 활동으로 진로 역량을 탐색함." for c in career_sel])
        
        st.divider()
        st.success("최종 결과")
        st.text_area("자율활동 칸 복사용", res_auto, height=100)
        st.text_area("진로활동 칸 복사용", res_career, height=100)

st.caption("v1.1 - 선생님의 지시에 따라 한국지리/통합사회/창체 7종 모듈이 통합되었습니다.")

선생님, 이제 이 코드를 GitHub에 올리고 Streamlit Cloud에 연결만 하시면 됩니다! 주소가 생성되면 저에게 알려주세요. 그다음, **문장을 더 예쁘게 만드는 '세부 조건'**을 프로그램에 심는 작업을 도와드릴게요!

혹시 GitHub 가입이나 업로드 과정에서 막히는 부분이 있다면 바로 말씀해 주세요!
