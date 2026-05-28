import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 웹앱 페이지 설정
st.set_page_config(page_title="전국 야구장 위치 지도", page_icon="⚾", layout="wide")

st.title("⚾ 전국 야구장 위치 검색 웹앱")
st.write("원하는 구단이나 지역의 야구장을 검색하고 위치를 확인해보세요!")

# 2. 전국 주요 야구장 데이터 세팅 (위도, 경도)
@st.cache_data
def load_data():
    data = {
        "야구장명": [
            "잠실야구장", "고척스카이돔", "인천SSG랜더스필드", 
            "수원KT위즈파크", "대전한화생명이글스파크", "대구삼성라이온즈파크", 
            "광주기아챔피언스필드", "창원NC파크", "부산사직야구장"
        ],
        "연고구단": [
            "LG 트윈스 / 두산 베어스", "키움 히어로즈", "SSG 랜더스", 
            "KT 위즈", "한화 이글스", "삼성 라이온즈", 
            "KIA 타이거즈", "NC 다이노스", "롯데 자이언츠"
        ],
        "주소": [
            "서울특별시 송파구 올림픽로 25", "서울특별시 구로구 경인로 430", "인천광역시 미추홀구 매소홀로 618",
            "경기도 수원시 장안구 경수대로 893", "대전광역시 중구 대종로 373", "대구광역시 수성구 야구전설로 1",
            "광주광역시 북구 서림로 10", "경상남도 창원시 마산회원구 삼호로 63", "부산광역시 동래구 사직로 45"
        ],
        "latitude": [37.5122, 37.4982, 37.4371, 37.2997, 36.3172, 35.8412, 35.1682, 35.2232, 35.1941],
        "longitude": [127.0719, 126.8671, 126.6933, 127.0101, 127.4292, 128.6815, 126.8891, 128.5826, 129.0615]
    }
    return pd.DataFrame(data)

df = load_data()

# 3. 사이드바 - 검색 및 필터링 기능
st.sidebar.header("🔍 야구장 검색")

# 텍스트 검색 (구단명 또는 야구장명)
search_query = st.sidebar.text_input("구단명 또는 야구장 이름을 입력하세요:", "")

# 데이터 필터링
if search_query:
    filtered_df = df[
        df["야구장명"].str.contains(search_query, case=False) | 
        df["연고구단"].str.contains(search_query, case=False)
    ]
else:
    filtered_df = df

# 4. 메인 화면 레이아웃 분할
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📋 야구장 목록")
    if filtered_df.empty:
        st.warning("검색 결과가 없습니다.")
    else:
        st.dataframe(
            filtered_df[["야구장명", "연고구단", "주소"]], 
            hide_index=True, 
            use_container_width=True
        )

with col2:
    st.subheader("🗺️ 지도 확인")
    
    # 대한민국 중심부를 기본 위치로 설정
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)
    
    # 필터링된 야구장 마커 추가
    for _, row in filtered_df.iterrows():
        popup_text = f"<b>{row['야구장명']}</b><br>구단: {row['연고구단']}<br>주소: {row['주소']}"
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=row["야구장명"],
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)
    
    # 스트림릿에 지도 렌더링
    st_folium(m, width="100%", height=500, returned_objects=[])