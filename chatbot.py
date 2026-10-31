from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool

from exchange import get_exchange_rate, convert_currency


# 환율 조회 도구
@tool
def exchange_rate_tool(
    amount: float,
    base_currency: str,
    target_currency: str
) -> str:
    """
    특정 금액을 다른 통화로 환산합니다.

    Args:
        amount: 환산할 금액
        base_currency: 기준 통화 코드 (USD, KRW 등)
        target_currency: 대상 통화 코드 (KRW, USD 등)
    """

    base_currency = base_currency.upper()
    target_currency = target_currency.upper()

    try:

        # 환율 조회
        result = get_exchange_rate(
            base_currency,
            target_currency
        )

        rate = result["rate"]
        date = result["date"]

        # 환율 계산
        converted = convert_currency(amount, rate)

        return f"""
        기준 통화: {base_currency}
        대상 통화: {target_currency}

        환율: 1 {base_currency} = {rate:,.4f} {target_currency}

        환산 금액:
        {amount:,.2f} {base_currency}
        = {converted:,.2f} {target_currency}

        환율 기준일: {date}
        """

    except Exception as e:

        return f"환율 조회 중 오류가 발생했습니다: {str(e)}"


# OpenAI 모델 초기화
model = init_chat_model(
    "gpt-5.4-mini",
    temperature=0
)


# AI Agent 생성
agent = create_agent(
    model=model,
    tools=[exchange_rate_tool],
    system_prompt="""
    당신은 환율 조회 전문 AI 챗봇입니다.

    다음 규칙을 반드시 지키세요.

    1. 사용자가 환율을 질문하면 exchange_rate_tool을 사용하세요.

    2. 환율이나 환산 금액을 추측하지 마세요.

    3. 반드시 API에서 조회한 환율을 기준으로 답변하세요.

    4. 환율 기준일을 표시하세요.

    5. 답변은 한국어로 작성하세요.

    6. 금액은 천 단위 구분기호를 사용하세요.

    7. Frankfurter API는 실시간 금융시장 체결가가 아니라 최신 일별 기준 환율을 제공합니다.

    8. API 조회에 실패하면 임의의 환율을 생성하지 마세요.

    9. 사용자가 통화를 명시하지 않았다면 필요한 정보를 질문하세요.

    10. 답변은 간결하고 이해하기 쉽게 작성하세요.

    11. 사용자가 한국어로 "달러 환율", "엔화 환율", "유로 환율"이라고 질문하고 대상 통화를 명시하지 않았다면 KRW를 기본 대상 통화로 해석하세요.

    12. 사용자가 "달러 환율이 얼마야?"라고 질문하면 1 USD를 KRW로 환산한 환율을 조회하세요.
    """
)