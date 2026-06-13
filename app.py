# --- 사이드바 영역 수정 ---
with st.sidebar:
    st.header("⚙️ 스마트 생기부 마법사 설정")
    
    # 1단계: 세특 영역 선택
    category = st.radio("1단계: 기록 영역 선택", ["교과 세특", "창체(자율/진로)"])
    st.divider()
    
    # 2단계: 대상 학생 선택 (교과 세특일 때만 과목 선택 노출)
    st.write("2단계: 대상 학생 선택")
    
    subj_sidebar = None
    if category == "교과 세특":
        subj_sidebar = st.radio("기준 과목 선택", ["한국지리", "통합사회"], horizontal=True)
        available_classes = list(STUDENTS_DB[subj_sidebar].keys())
        selected_class = st.selectbox("학급 선택", available_classes)
        student_list = STUDENTS_DB[subj_sidebar][selected_class]
    else:
        # 창체일 경우 과목 구분 없이 학급 선택 (예시 데이터 구조에 맞춰 조정 가능)
        selected_class = st.selectbox("학급 선택", ["1학년 1반", "1학년 2반", "1학년 3반", "1학년 4반", "3학년 1반", "3학년 2반", "3학년 3반", "3학년 4반"])
        # 창체 시에는 모든 학생을 하나로 합치거나 특정 로직 필요
        student_list = []
        for subj in STUDENTS_DB:
            if selected_class in STUDENTS_DB[subj]:
                student_list.extend(STUDENTS_DB[subj][selected_class])
        student_list = sorted(list(set(student_list)))

    student_with_id = st.selectbox("학생 선택", student_list)
    
    student_id = student_with_id.split(" ", 1)[0] if " " in student_with_id else "0000"
    actual_name = student_with_id.split(" ", 1)[1] if " " in student_with_id else student_with_id

# --- 메인 작업 영역 (상단 타이틀 조정) ---
st.title("🛡️ 스마트 생기부 마법사 v2.0")
st.info(f"현재 선택된 모드: **{category}** | 대상: **{selected_class} {actual_name}**")
