import streamlit as st
import pandas as pd
import io
from datetime import datetime

# 페이지 환경 설정
st.set_page_config(page_title="선생님 전용 생기부 마법사 v1.5", layout="wide")

# --- 스타일링 (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #1d4ed8; color: white; height: 3em; font-weight: bold; }
    .stTextArea>div>div>textarea { background-color: #ffffff; }
    div[data-testid="stExpander"] { background-color: #f1f5f9; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ 스마트 생기부 마법사 v1.5 (최종 엑셀 추출 저장소 탑재)")
st.info("💡 [기능 업데이트] 작성한 문장을 누적 보관하고, 언제든 통합 정밀 엑셀(.xlsx) 파일로 내보낼 수 있는 기능이 추가되었습니다.")

# --- 세션 상태(누적 기록 장부) 초기화 ---
if "records_db" not in st.session_state:
    st.session_state.records_db = []

# --- 100% 출석부 명단 데이터베이스 (보내주신 6개 파일 전수 정밀 파싱 완료) ---
STUDENTS_DB = {
    "한국지리": {
        "3학년 1반": ["3103 김도엽", "3104 김도현", "3105 김성현", "3108 김현중", "3109 김효민", "3110 류기훈", "3112 박성욱", "3113 박정우", "3115 박준아", "3117 서성웅", "3119 심원경", "3123 윤지현", "3124 이수호", "3132 한기웅"],
        "3학년 2반": ["3202 곽영훈", "3203 김민성", "3204 김세영", "3206 김재희", "3208 나평안", "3209 박민기", "3212 백하얼", "3213 서승우", "3216 양서율", "3218 이기은", "3219 이수호", "3220 이시우", "3221 이영조", "3223 이태양", "3224 임수혁", "3226 장우혁", "3227 전지우", "3229 최민기", "3231 최은혁"],
        "3학년 3반": ["3301 강동한", "3302 고정완", "3304 곽민찬", "3308 김은중", "3309 김태범", "3312 박건민", "3316 박지빈", "3317 방찬희", "3321 신세계", "3322 신현재", "3325 윤정현", "3327 이주혁", "3328 이준서", "3331 한지후", "3332 홍민우", "3333 홍정민"],
        "3학년 4반": ["3415 오호준", "3419 유완호", "3431 주동현"]
    },
    "통합사회": {
        "1학년 1반": ["1101 강영훈", "1102 김민찬", "1103 김재엽", "1104 김지호", "1105 김진욱", "1106 김태현", "1107 김호영", "1108 김환호", "1109 김희락", "1110 노동현", "1111 박은혁", "1112 박준성", "1113 백이현", "1114 서건희", "1115 신백호", "1116 양희성", "1117 연태경", "1118 오유찬", "1119 유하빈", "1120 윤성현", "1121 이도현", "1122 이상욱", "1123 이승우", "1124 이승진", "1125 이예성", "1126 이준효", "1127 이현희", "1128 임성현", "1129 정하윤", "1130 조성호", "1131 주현규", "1132 한서후", "1133 허승범", "1134 홍윤기", "1135 황재민"],
        "1학년 2반": ["1201 강하성", "1202 권영하", "1203 권준범", "1204 김강호", "1205 김동민", "1206 김리안", "1207 김민권", "1208 김민재", "1209 김중기", "1210 김지후", "1211 남상택", "1212 박건웅", "1213 박세진", "1214 박정후", "1215 손상범", "1216 송준오", "1217 신재원", "1218 안현탁", "1219 양승준", "1220 오성택", "1221 오연우", "1222 윤정우", "1223 이은유", "1224 이하준", "1225 이현준", "1226 임도현", "1227 장시율", "1228 장준호", "1229 정구영", "1230 조경원", "1231 채홍건", "1232 하동주", "1233 한효원", "1234 홍기성", "1235 홍주열"],
        "1학년 3반": ["1301 KAN VLADISLAV DMITRIEVICH", "1302 강민준", "1303 강범준", "1304 고희준", "1305 김동명", "1306 김민범", "1307 김비오", "1308 김습정", "1309 김재원", "1310 김진구", "1311 박수기", "1312 박윤호", "1313 박종하", "1314 박휘건", "1315 양희모", "1316 유재현", "1317 이민우", "1318 이성민", "1319 이재준", "1320 이호진", "1321 장민재", "1322 장지호", "1323 장호성", "1324 정민건", "1325 정지율", "1326 정현수", "1327 조성원", "1328 조성학", "1329 조성흠", "1330 최우진", "1331 한준규", "1332 홍석환", "1333 황정민", "1334 황준서", "1335 황준혁"],
        "1학년 4반": ["1401 TSOI MAKSIM", "1402 강민건", "1403 강산", "1404 고동균", "1405 권혁준", "1406 김승준", "1407 김시훈", "1408 김주호", "1409 김치연", "1410 김호범", "1411 박보솔", "1412 박성진", "1413 변은혁", "1414 설도윤", "1415 손호빈", "1416 신유민", "1417 양서준", "1418 오주호", "1419 유승엽", "1420 유우연", "1421 윤태영", "1422 이건우", "1423 이경빈", "1424 이동희", "1425 이민수", "1426 이주헌", "1427 이한울", "1428 이현성", "1429 이호연", "1430 장수혁", "1431 전은도", "1432 정재훈", "1433 조관호", "1434 최선규", "1435 최재환"]
    }
}

# --- 과목 역량 데이터베이스 ---
COMPETENCY_DB = {
    "한국지리": {
        "지리적 사고력 & 공간 조망": {
            "우수": "자연환경 and 인문환경의 상호작용을 파악하는 지리적 사고력이 매우 뛰어나며, 지역적 특성을 거시적인 공간 조망 능력으로 해석하는 탁월한 통찰력을 보여줌.",
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

def calc_bytes(text):
    return len(text.encode('utf-8-sig'))

# --- 사이드바 영역 ---
with st.sidebar:
    st.header("👤 학생 및 기록 정보")
    category = st.selectbox("기록 영역 선택", ["교과 세특", "창체(자율/진로)"])
    st.divider()
    
    subj_sidebar = st.radio("기준 과목 선택", ["한국지리", "통합사회"], horizontal=True)
    available_classes = list(STUDENTS_DB[subj_sidebar].keys())
    selected_class = st.selectbox("학급 선택", available_classes)
    
    student_list = STUDENTS_DB[subj_sidebar][selected_class]
    student_with_id = st.selectbox("학생 선택 (학번 포함)", student_list)
    
    student_id = student_with_id.split(" ", 1)[0] if " " in student_with_id else "0000"
    actual_name = student_with_id.split(" ", 1)[1] if " " in student_with_id else student_with_id

# --- 메인 작업 영역 ---
current_generated_text = ""

if category == "교과 세특":
    st.subheader(f"📖 {subj_sidebar} - {selected_class} [{student_with_id}] 세특 작성")
    col1, col2 = st.columns(2)
    with col1:
        st.write("🎯 **성취기준 기반 과목 역량 선택**")
        selected_comps = [comp for comp in COMPETENCY_DB[subj_sidebar].keys() if st.checkbox(comp)]
    with col2:
        st.write("📊 **학생 수행 수준 평가**")
        level = st.radio("이 학생의 성취 수준은?", ["우수", "보통"], horizontal=True)
        st.write("⚙️ **수행한 세부 활동 선택**")
        selected_acts = st.multiselect("활동 선택", DATA_ACTS[subj_sidebar])

    memo = st.text_area("✍️ 개별 특이사항 및 관찰 메모", placeholder="예: 데이터 분석 과정이 정교함, 사회적 약자의 입장에 깊이 성찰함 등")
    
    if st.button("✨ 서술형 세특 문장 합성하기"):
        comp_texts = [COMPETENCY_DB[subj_sidebar][c][level] for c in selected_comps]
        act_text = f"교과 수업 중 " + ", ".join(selected_acts) + " 등의 활동을 주도적으로 수행하였으며," if selected_acts else ""
        base_combined = " ".join(comp_texts)
        current_generated_text = f"{actual_name} 학생은 {base_combined} {act_text} {memo}".strip()
        
        st.success(f"🎉 [{student_with_id}] 완성된 서술형 교과 세특 문구")
        st.code(current_generated_text, language=None)
        
        b_size = calc_bytes(current_generated_text)
        if b_size > 1500:
            st.error(f"⚠️ 바이트 한도 초과! 현재: {b_size} / 1500 Byte")
        else:
            st.success(f"✅ 나이스 입력 가능 수치: {b_size} / 1500 Byte")

else:
    st.subheader(f"🍀 {selected_class} [{student_with_id}] 학급 창체 활동 배치")
    col1, col2 = st.columns(2)
    with col1:
        st.write("🔹 **자율활동**")
        auto_sel = st.multiselect("자율활동 배치 항목", DATA_ACTS["창체"], key="auto")
    with col2:
        st.write("🔸 **진로활동**")
        career_sel = st.multiselect("진로활동 배치 항목", DATA_ACTS["창체"], key="career")
        
    if st.button("✨ 창체 기록 합치기"):
        res_auto = f"{actual_name} 학생은 " + " ".join([f"{a} 활동에 참여하여 타인을 배려하는 태도를 바탕으로 학급 공동체 발전에 기여함." for a in auto_sel]) if auto_sel else "배정된 활동 없음"
        res_career = f"{actual_name} 학생은 " + " ".join([f"{c} 활동을 통해 자신의 진로 장벽을 진단하고, 이를 극복하기 위한 구체적인 탐구 역량을 보여줌." for c in career_sel]) if career_sel else "배정된 활동 없음"
        current_generated_text = f"[자율활동]\n{res_auto}\n\n[진로활동]\n{res_career}"
        
        st.divider()
        st.success(f"🎉 [{student_with_id}] 최종 창체 서술형 결과")
        st.text_area("자율활동 복사용 (한도 1500 Byte)", res_auto, height=100)
        st.caption(f"자율 바이트: {calc_bytes(res_auto)} Byte")
        st.text_area("진로활동 복사용 (한도 2100 Byte)", res_career, height=100)
        st.caption(f"진로 바이트: {calc_bytes(res_career)} Byte")

# --- 💾 장부 저장 및 엑셀 다운로드 시스템 ---
st.divider()
st.subheader("💾 데이터 보관 및 엑셀 내보내기")

if current_generated_text:
    if st.button("📥 위 학생의 완성된 기록을 장부에 저장하기"):
        new_record = {
            "학번": student_id,
            "이름": actual_name,
            "학급": selected_class,
            "기록 영역": category,
            "선택과목": subj_sidebar,
            "평가 수준": level if category == "교과 세특" else "창체 반영",
            "완성된 생기부 내용": current_generated_text,
            "바이트 수": f"{calc_bytes(current_generated_text)} Byte",
            "저장일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.records_db.append(new_record)
        st.success(f"✅ [{student_with_id}] 학생의 생기부 내용이 임시 장부에 저장되었습니다! 아래 표를 확인하세요.")

# 누적된 데이터 테이블 시각화
if st.session_state.records_db:
    df_records = pd.DataFrame(st.session_state.records_db)
    
    with st.expander(f"📊 현재 누적 저장된 학생 기록 (총 {len(df_records)}건)", expanded=True):
        st.dataframe(df_records, use_container_width=True)
        
        # 엑셀 파일 변환 버퍼 생성
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_records.to_excel(writer, index=False, sheet_name='생기부_최종기록')
        
        # 다운로드 버튼 활성화
        st.download_button(
            label="📥 누적 데이터 최종 엑셀 파일(.xlsx) 다운로드",
            data=buffer.getvalue(),
            file_name=f"스마트_생기부_마법사_추출물_{datetime.now().strftime('%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        if st.button("🗑️ 장부 전체 초기화"):
            st.session_state.records_db = []
            st.rerun()
else:
    st.caption("ℹ️ 현재 저장된 데이터가 없습니다. 학생의 문장을 합성한 후 '장부에 저장하기' 버튼을 누르면 여기에 누적됩니다.")
