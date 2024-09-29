## 사용된 기술 스택

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **API**: Kakao 지도 API, Kakao 로그인 API
- **Containerization**: Docker, Docker Compose

## 주요 기능

- **위치 기반 음식점 및 카페 탐색**: Kakao 지도 API를 사용하여 지정한 위치 근처의 음식점과 카페를 검색하는 기능
- **음식점-카페 쌍 평가**: 특정 음식점과 그 근처의 카페를 하나의 쌍으로 묶어 코스로 별점 평가 및 리뷰 작성 기능
- **리뷰 작성**: 본인이 선택한 음식점과 카페에 대한 리뷰 작성, 수정 기능
- **리뷰 조회**: Kakao 지도 API를 사용하여 지정한 위치 근처의 리뷰가 있는 음식점-카페, 음식점, 카페를 확인할 수 있음
- **로그인/로그아웃**: OAuth 2.0을 기반으로 한 Kakao 로그인 기능

