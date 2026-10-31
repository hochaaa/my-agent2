import streamlit as st
from dotenv import load_dotenv

from exchange import (
    CURRENCIES,
    get_exchange_rate,
    convert_currency
)


# 환경변수 불러오기
load_dotenv()


# Streamlit 페이지 설정
st.set_page_config(
    page_title="Currency Mate",
    page_icon="😊",
    layout="centered"
)


# -------------------------------
# 메인 화면
# -------------------------------

st.title("😊 내 친구 챗봇")


# 안내 문구와 환율 계산기 버튼을 가로로 배치
caption_col, button_col = st.columns(
    [4, 1.5],
    gap="small",
    vertical_alignment="center"
)


with caption_col:

    st.caption(
        "Frankfurter API와 AI를 활용한 환율 조회 챗봇"
    )


# -------------------------------
# 환율 계산기 (팝업)
# -------------------------------

with button_col:

    with st.popover("환율 계산기", use_container_width=False):

        # 통화 선택
        col1, col2 = st.columns(2)

        with col1:

            base_currency = st.selectbox(
                "기준 통화",
                options=list(CURRENCIES.keys()),
                index=0,
                format_func=lambda x: f"{x} - {CURRENCIES[x]}"
            )

        with col2:

            target_currency = st.selectbox(
                "대상 통화",
                options=list(CURRENCIES.keys()),
                index=1,
                format_func=lambda x: f"{x} - {CURRENCIES[x]}"
            )


        # 금액 입력
        amount = st.number_input(
            "환산할 금액",
            min_value=0.0,
            value=100.0,
            step=10.0
        )


        # 환율 조회
        if st.button(
            "환율 조회",
            use_container_width=True
        ):

            try:

                result = get_exchange_rate(
                    base_currency,
                    target_currency
                )

                rate = result["rate"]
                date = result["date"]

                converted = convert_currency(
                    amount,
                    rate
                )

                st.metric(
                    label=f"{target_currency} 환산 금액",
                    value=f"{converted:,.2f} {target_currency}"
                )

                st.success(
                    f"1 {base_currency} = {rate:,.4f} {target_currency}"
                )

                st.caption(
                    f"환율 기준일: {date}"
                )

            except Exception as e:

                st.error(
                    f"환율 조회 중 오류가 발생했습니다: {e}"
                )


st.write("")


# -------------------------------
# AI 환율 챗봇 (메인 기능)
# -------------------------------

# 대화 기록 초기화
if "messages" not in st.session_state:

    st.session_state.messages = []


# 메시지 개수 확인
message_count = len(st.session_state.messages)


# -------------------------------
# 채팅 영역 높이 자동 조절
# -------------------------------

# 메시지가 없으면 채팅 영역을 생성하지 않음
# 메시지가 늘어나면 높이 증가
# 최대 450px까지만 증가

if message_count == 0:

    chat_height = 0

else:

    chat_height = min(
        120 * message_count,
        450
    )


# 챗봇 전체를 하나의 박스로 감싸기
with st.container(border=True):

    st.subheader("AI 환율 챗봇")

    st.caption(
        "채팅을 통해 질문해 보세요."
    )


    # -------------------------------
    # 채팅 메시지 영역
    # -------------------------------

    if message_count > 0:

        chat_container = st.container(
            height=chat_height,
            border=False
        )

        with chat_container:

            # 기존 대화 출력
            for message in st.session_state.messages:

                with st.chat_message(message["role"]):

                    st.write(message["content"])


    # -------------------------------
    # 채팅 입력창 (맨 아래)
    # -------------------------------

    prompt = st.chat_input(
        "환율에 대해 질문해 보세요.",
        key="currency_chat_input"
    )


    if prompt:

        # 사용자 메시지 저장
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        # AI 응답 생성
        try:

            from chatbot import agent

            with st.spinner("환율을 조회하고 있습니다..."):

                response = agent.invoke({
                    "messages": st.session_state.messages
                })

                answer = response["messages"][-1].content

                # AI 메시지 저장
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

        except Exception as e:

            st.session_state.messages.append({
                "role": "assistant",
                "content": f"챗봇 오류: {e}"
            })

        # 새 메시지를 채팅 영역에 표시
        st.rerun()


# -------------------------------
# 하단 안내
# -------------------------------

st.divider()

st.caption(
    "환율 데이터 제공: Frankfurter API | "
    "최신 일별 기준 환율이며 실시간 거래 환율이 아닙니다."
)