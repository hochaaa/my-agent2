import requests


# Frankfurter API 주소
BASE_URL = "https://api.frankfurter.dev/v1/latest"


# 지원 통화 목록
CURRENCIES = {
    "USD": "미국 달러",
    "KRW": "대한민국 원",
    "JPY": "일본 엔",
    "EUR": "유로",
    "GBP": "영국 파운드",
    "CNY": "중국 위안",
    "CHF": "스위스 프랑",
    "CAD": "캐나다 달러",
    "AUD": "호주 달러",
}


# 환율 조회 함수
def get_exchange_rate(base_currency, target_currency):

    # 같은 통화인 경우
    if base_currency == target_currency:
        return {
            "rate": 1.0,
            "date": "동일 통화"
        }

    # API 요청 파라미터
    params = {
        "base": base_currency,
        "symbols": target_currency
    }

    # API 요청
    response = requests.get(
        BASE_URL,
        params=params,
        timeout=10
    )

    # HTTP 오류 확인
    response.raise_for_status()

    # JSON 데이터 변환
    data = response.json()

    # 환율 정보 추출
    rate = data["rates"][target_currency]

    return {
        "rate": rate,
        "date": data["date"]
    }


# 환율 계산 함수
def convert_currency(amount, rate):

    converted_amount = amount * rate

    return converted_amount