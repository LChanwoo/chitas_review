from django.http import JsonResponse
import requests
import json

REST_API_KEY = "a382c419760c032a0a3b78e1e7daffbb"

def keyword(request):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {
        "Authorization": f"KakaoAK {REST_API_KEY}",
    }
    # 현재 클라이언트가 보고 있는 지도 중심 좌표 x, y
    # "기본값은 청년취업사관학교 강동캠퍼스" 위치
    x = request.GET.get("locate_x",127.173488088873)
    y = request.GET.get("locate_y",37.5574814787209)
    query = request.GET.get("query")
    params = {
        "radius": 20000,
        "query": query,
    }
    response = requests.get(url, headers=headers, params=params)

    # 응답 확인
    if response.status_code == 200:
        # JSON 형식의 응답 데이터를 파이썬 객체로 변환
        data=response.json()
        print(data)
        locate = float(x)+float(y)
        if len(data["documents"]) == 0:
            return JsonResponse({"error": "검색 결과가 없습니다."})
        closest = 0
        for e in data["documents"]:
            if abs(locate - (float(e["x"])+float(e["y"]))) < abs(locate - (float(data["documents"][closest]["x"])+float(data["documents"][closest]["y"]))):
                closest = data["documents"].index(e)
        print(data["documents"][closest])
        data.update({"closest": data["documents"][closest]})

    else:
        print(f"Error: {response.status_code}")
    return JsonResponse(data)