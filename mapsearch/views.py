from django.http import JsonResponse
import requests
from config.settings import env

# REST API 키 불러오기
# 이 키는 카카오 개발자 센터에서 발급받은 키를 사용
# 발급받은 키는 config/settings.py 파일에 저장하여 보안 유지
REST_API_KEY = env('REST_API_KEY')


# 카카오 지도 검색 API를 호출하는 함수
# 클라이언트에서 전달받은 검색 키워드를 이용하여 카카오 지도 검색 API를 호출
# 호출한 결과를 클라이언트에게 반환
# 반환하는 데이터는 JSON 형식
def keyword(request):
    # 카카오 지도 검색 API 중, 키워드로 장소 검색하는 API 호출
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    
    # API 호출에 필요한 헤더 정보 
    # REST API 키를 헤더에 포함
    # 헤더에 포함하지 않으면 API 호출이 불가능
    headers = {
        "Authorization": f"KakaoAK {REST_API_KEY}",
    }

    # 현재 클라이언트가 보고 있는 지도 중심 좌표 x, y
    # 기본값은 "청년취업사관학교 강동캠퍼스" 위치
    # 클라이언트에서 x, y 좌표를 전달받으면 그 좌표를 사용
    # 전달받지 못하면 기본값을 사용
    # 클라이언트에서 전달받은 x, y 좌표는 문자열이므로 숫자로 변환
    # 클라이언트에서 전달받지 못하면 기본값을 사용
    x = request.GET.get("locate_x",127.173488088873)
    y = request.GET.get("locate_y",37.5574814787209)

    # API 호출에 필요한 쿼리 스트링
    query = request.GET.get("query")

    # 검색 키워드와 중심 좌표를 전달
    # 검색 키워드는 필수이고, 중심 좌표는 필수가 아님
    # 중심 좌표를 전달하지 않으면 기본값을 사용
    params = {
        "radius": 20000,
        "query": query,
    }
    # API 호출
    # API 호출에 필요한 URL, 헤더, 쿼리 스트링을 전달
    response = requests.get(url, headers=headers, params=params)

    # 응답 확인
    # 응답이 정상적으로 오면 status_code가 200이 됨
    if response.status_code == 200:
        
        # JSON 형식의 응답 데이터를 파이썬 객체로 변환
        data=response.json()
        
        # 현재 클라이언트가 보고 있는 지도 중심 좌표와 검색 결과 중 가장 가까운 장소의 좌표를 비교
        # 가장 가까운 장소의 좌표가 현재 클라이언트가 보고 있는 지도 중심 좌표와 가까우면
        # 검색 결과 중 가장 가까운 장소를 클라이언트에게 보여줌
        locate = float(x)+float(y)

        # 검색 결과가 없는 경우 오류 메시지 반환
        if len(data["documents"]) == 0:
            return JsonResponse({"error": "검색 결과가 없습니다."})
        
        # 검색 결과가 있는 경우, 검색 결과 중 가장 가까운 장소를 찾음
        closest = 0

        # 검색 결과 중 가장 가까운 장소의 좌표와 현재 클라이언트가 보고 있는 지도 중심 좌표와의 차이가 가장 작은 장소를 찾음
        for e in data["documents"]:
            if abs(locate - (float(e["x"])+float(e["y"]))) < abs(locate - (float(data["documents"][closest]["x"])+float(data["documents"][closest]["y"]))):
                closest = data["documents"].index(e)

        # 응답 데이터에 가장 가까운 장소의 정보를 추가
        data.update({"closest": data["documents"][closest]})
    else:
        # 오류가 발생한 경우 오류 내용 출력
        print(f"Error: {response.status_code}")

    # 응답 데이터 반환
    return JsonResponse(data)