import streamlit as st
import pandas as pd
import pymysql
import os
from dotenv import load_dotenv
import plotly.express as px

load_dotenv()

# ------------------------- DB & LOADERS -------------------------
def get_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database='autoreg_kr',
        charset='utf8mb4'
    )

@st.cache_data(ttl=300)
def load_car_data():
    query = "SELECT year, gender, age_group, car_count FROM gender_age_car"
    with get_connection() as conn:
        return pd.read_sql(query, conn)

@st.cache_data(ttl=300)
def load_faq():
    query = "SELECT question, answer FROM faq"
    with get_connection() as conn:
        return pd.read_sql(query, conn)

@st.cache_data(ttl=300)
def load_fuel_data():
    query = "SELECT ym, car_type, fuel_type, car_count FROM fuel_car"
    with get_connection() as conn:
        df = pd.read_sql(query, conn)
    df["ym"] = df["ym"].astype(str)
    try:
        df["ym_dt"] = pd.to_datetime(df["ym"], format="%Y%m")
    except Exception:
        df["ym_dt"] = pd.to_datetime(df["ym"], errors="coerce")
    df["year"] = df["ym_dt"].dt.year
    df["ym_str"] = df["ym_dt"].dt.strftime("%Y-%m")
    return df

# ✅ 지역/차종 테이블 로더 추가
@st.cache_data(ttl=300)
def load_region_data():
    # car_reg_region: ym='YYYY-MM' 문자열 가정
    query = """
        SELECT ym, region, passenger_total, bus_total, truck_total, special_total, total_count
        FROM car_reg_region
    """
    with get_connection() as conn:
        df = pd.read_sql(query, conn)
    df["ym"] = pd.to_datetime(df["ym"], format="%Y-%m", errors="coerce")
    df["year"] = df["ym"].dt.year
    df["month"] = df["ym"].dt.month
    return df

# ------------------------- PAGE CONFIG -------------------------
st.set_page_config(
    page_title="자동차 등록 현황 대시보드",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------- SIDEBAR NAV -------------------------
st.sidebar.title("☰ 메뉴")
page = st.sidebar.radio(
    "이동",
    ["⚤ 성별/연령별 현황", "⚡︎ 연료별 현황", "🏕 지역/차종 현황", "？ FAQ"],
    index=0,
    label_visibility="collapsed"
)

# 공통 데이터
df = load_car_data()
age_order = ["10대이하","20대","30대","40대","50대","60대","70대","80대","90대이상"]
df["age_group"] = pd.Categorical(df["age_group"], categories=age_order, ordered=True)
year_list = sorted(df["year"].unique())

# ------------------------- 성별/연령 페이지 -------------------------
if page == "⚤ 성별/연령별 현황":
    st.title("👫🏻 성별/연령별 자동차 등록 현황")

    st.sidebar.divider()
    show_filters = st.sidebar.toggle("필터 표시", value=False)
    if show_filters:
        st.sidebar.subheader("필터")
        years_sel = st.sidebar.multiselect("연도 범위(추이용)", year_list, default=year_list)
        genders_sel = st.sidebar.multiselect("성별 선택(추이용)", ["여성","남성"], default=["여성","남성"])
    else:
        years_sel = year_list
        genders_sel = ["여성", "남성"]

    filtered_df = df[df["year"].isin(years_sel) & df["gender"].isin(genders_sel)]

    tab1, tab2 = st.tabs(["📈 연도별 증감률","📎 선택 연도 성별·연령 비율"])

    # 탭1
    with tab1:
        yearly_total = df.groupby("year")["car_count"].sum().reset_index().sort_values("year")
        display_df = yearly_total.copy()
        display_df["증감"] = display_df["car_count"].diff().fillna(0).astype(int)
        display_df["증감률(%)"] = display_df["car_count"].pct_change().fillna(0) * 100

        fig_growth = px.line(
            display_df, x="year", y="증감률(%)",
            markers=True, template="plotly_white",
            labels={"year": "연도", "증감률(%)": "증감률 (%)"},
            title="연도별 등록수 증감률"
        )
        fig_growth.update_yaxes(tickformat=",.2f", ticksuffix="%")
        fig_growth.update_traces(hovertemplate="연도=%{x}<br>증감률=%{y:,.2f}%")

        table_df = display_df.copy()
        table_df["등록 수"] = table_df["car_count"].apply(lambda x: f"{x:,.0f}명")
        table_df["전년 대비 증감"] = table_df["증감"].apply(lambda x: f"{x:+,}명")
        table_df["전년 대비 증감률"] = table_df["증감률(%)"].apply(lambda x: f"{x:+.2f}%")
        table_df = table_df[["year", "등록 수", "전년 대비 증감", "전년 대비 증감률"]]
        table_df.columns = ["연도", "등록 수", "전년 대비 증감", "전년 대비 증감률"]

        g1, g2 = st.columns([2, 1])
        g1.plotly_chart(fig_growth, use_container_width=True)
        g2.dataframe(table_df, use_container_width=True, hide_index=True)


    # 탭2
    with tab2:
        selected_year_tab2 = st.selectbox("연도 선택", year_list, index=len(year_list)-1, key="year_for_pies")
        age_colors = {
            "10대이하": "#FFD9D9", "20대": "#FFE0B2", "30대": "#FFF59D",
            "40대": "#B2FF59", "50대": "#80DEEA", "60대": "#B39DDB",
            "70대": "#FFCCBC", "80대": "#F8BBD0", "90대이상": "#CFD8DC"
        }
        year_df = df[df["year"] == selected_year_tab2]

        def pie_by_gender(g):
            gdf = (
                year_df[year_df["gender"] == g]
                .groupby("age_group")["car_count"].sum()
                .reindex(age_order).fillna(0).reset_index()
            )
            total = gdf["car_count"].sum()
            gdf["pct"] = (gdf["car_count"] / total * 100) if total > 0 else 0
            fig = px.pie(
                gdf, names="age_group", values="car_count",
                color="age_group", color_discrete_map=age_colors,
                hole=0.35, template="plotly_white",
                title=f"{selected_year_tab2}년 {g} 연령대 비율"
            )
            fig.update_traces(textposition="inside", textinfo="percent+label")
            return fig

        c1, c2 = st.columns(2)
        c1.plotly_chart(pie_by_gender("남성"), use_container_width=True)
        c2.plotly_chart(pie_by_gender("여성"), use_container_width=True)

# ------------------------- 연료 페이지 -------------------------
elif page == "⚡︎ 연료별 현황":
    st.title("🔋 연료별 자동차 등록 현황")

    df_fuel = load_fuel_data()

    st.sidebar.divider()
    show_filters_f = st.sidebar.toggle("필터 표시", value=False)
    years_f = sorted(df_fuel["year"].dropna().unique().tolist())
    fuels_f = sorted(df_fuel["fuel_type"].dropna().unique().tolist())
    cartypes_f = sorted(df_fuel["car_type"].dropna().unique().tolist())

    if show_filters_f:
        st.sidebar.subheader("필터(연료)")
        years_sel_f = st.sidebar.multiselect("연도 범위", years_f, default=years_f)
        fuels_sel_f = st.sidebar.multiselect("연료 선택", fuels_f, default=fuels_f)
        cartypes_sel_f = st.sidebar.multiselect("차종 선택", cartypes_f, default=cartypes_f)
    else:
        years_sel_f = years_f
        fuels_sel_f = fuels_f
        cartypes_sel_f = cartypes_f

    fdf = df_fuel[
        df_fuel["year"].isin(years_sel_f)
        & df_fuel["fuel_type"].isin(fuels_sel_f)
        & df_fuel["car_type"].isin(cartypes_sel_f)
    ].copy()

    tab_f1, tab_f2 = st.tabs(["📈 연료별 비율", "📊 연료별 차종 비율"])

    # 탭1: 연도별 연료 비율 (파이)
    with tab_f1:
        fuel_filtered = fdf.copy()
        years_fuel = sorted(fuel_filtered["year"].dropna().unique().tolist())
        selected_year_fuel = st.selectbox(
            "연도 선택 (연료별 비율 보기)",
            options=years_fuel,
            index=len(years_fuel) - 1,
            key="fuel_year_select"
        )
        pie_df = (
            fuel_filtered[fuel_filtered["year"] == selected_year_fuel]
            .groupby("fuel_type")["car_count"]
            .sum()
            .reset_index()
        )
        pie_df = pie_df[pie_df["fuel_type"].notna()]
        pie_df = pie_df[pie_df["fuel_type"] != "소계"]

        pastel_colors = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF",
                         "#EAD1DC", "#CFE2F3", "#FFF2CC"]
        fig_fuel_pie = px.pie(
            pie_df, names="fuel_type", values="car_count",
            hole=0.3, color_discrete_sequence=pastel_colors,
            template="plotly_white", title=f"{selected_year_fuel}년 연료별 자동차 등록 비율"
        )
        fig_fuel_pie.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_fuel_pie, use_container_width=True)

    # 탭2: 연료별 차종 비율 (차종 라인)
    with tab_f2:
        available_fuels = sorted(
            fdf.loc[fdf["fuel_type"].notna() & (fdf["fuel_type"] != "소계"), "fuel_type"].unique().tolist()
        )
        selected_fuel_type = st.selectbox(
            "연료 선택 (차종별 현황 보기)",
            options=available_fuels,
            index=0,
            key="fuel_type_for_car_type_line"
        )
        car_type_df = (
            fdf[fdf["fuel_type"] == selected_fuel_type]
            .groupby("car_type", as_index=False)["car_count"]
            .sum()
            .sort_values("car_count", ascending=False)
        )
        fig_line = px.line(
            car_type_df, x="car_type", y="car_count",
            markers=True, template="plotly_white",
            labels={"car_type": "차종", "car_count": "등록 수 (대)"},
            title=f"{selected_fuel_type} 차종별 자동차 등록 현황 (꺾은선)"
        )
        fig_line.update_xaxes(categoryorder="array", categoryarray=car_type_df["car_type"].tolist())
        fig_line.update_yaxes(tickformat=",.0f", ticksuffix="대")
        fig_line.update_traces(
            line=dict(color="#FF4500", width=3),
            marker=dict(color="#FF4500", size=8),
            hovertemplate="차종=%{x}<br>등록 수=%{y:,.0f}대"
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # # 탭3: 연-연료 히트맵
    # with tab_f3:
    #     heat_df = fdf.groupby(["fuel_type", "ym_dt"])["car_count"].sum().reset_index()
    #     pivot = heat_df.pivot(index="fuel_type", columns="ym_dt", values="car_count").fillna(0)
    #     pivot.columns = [c.strftime("%Y-%m") if hasattr(c, "strftime") else str(c) for c in pivot.columns]
    #     pivot = pivot.reindex(sorted(pivot.columns), axis=1)
    #     fig_heat = px.imshow(
    #         pivot, aspect="auto", color_continuous_scale="Blues",
    #         labels=dict(x="연월", y="연료", color="등록 수 (대)"),
    #         title="연-연료별 등록 수 히트맵"
    #     )
    #     st.plotly_chart(fig_heat, use_container_width=True)

# ------------------------- 지역/차종 페이지 (신규) -------------------------
elif page == "🏕 지역/차종 현황":
    st.title("🌍 지역/차종 자동차 등록 현황")
    st.markdown("2015-01 ~ 2024-12 기간의 지역별·차종별 등록 현황")

    df_region = load_region_data()

    # 상단 필터
    col1, col2 = st.columns(2)
    with col1:
        years_r = sorted(df_region["year"].dropna().unique().tolist())
        selected_year_r = st.selectbox("연도 선택", years_r, index=len(years_r)-1)
    with col2:
        regions_r = sorted(df_region["region"].dropna().unique().tolist())
        selected_region_r = st.selectbox("지역 선택", regions_r)

    # 필터 적용
    rdf = df_region[(df_region["year"] == selected_year_r) & (df_region["region"] == selected_region_r)]

    st.subheader(f"📍 {selected_region_r} 지역 {selected_year_r}년 차량 등록 현황")

    # 원형 차트 (차종 비율)
    vehicle_cols = {
        "승용차": "passenger_total",
        "버스": "bus_total",
        "화물차": "truck_total",
        "특수차": "special_total",
    }
    df_pie = pd.DataFrame({
        "차종": list(vehicle_cols.keys()),
        "등록수": [rdf[col].sum() for col in vehicle_cols.values()]
    })
    fig_pie = px.pie(
        df_pie, names="차종", values="등록수",
        hole=0.3, template="plotly_white", title="차종별 비율"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Top 5 (해당 연도/지역 내 월별 total_count 상위)
    st.subheader(f"🏆 {selected_region_r} 지역 {selected_year_r}년 등록수 Top 5")
    top5 = rdf.sort_values(by="total_count", ascending=False).head(5)
    top5_display = top5[['ym', 'passenger_total', 'bus_total', 'truck_total', 'special_total', 'total_count']].copy()
    top5_display['ym'] = top5_display['ym'].dt.strftime('%Y-%m')
    st.dataframe(top5_display.style.hide(axis="index"))

# ------------------------- FAQ -------------------------
else:
    st.title("📢 FAQ")
    faq_df = load_faq()
    for _, row in faq_df.iterrows():
        with st.expander(row["question"]):
            st.write(row["answer"])

# ------------------------- STYLES -------------------------
# st.markdown("""
# <style>
# :root{
#   --sidebar-bg: #f9fafb;
#   --sidebar-fg: #111827;
#   --accent:     #3b82f6;
#   --accent-soft:#dbeafe;
#   --accent-hover:#e0f2fe;
# }
# [data-testid="stSidebar"]{ background: var(--sidebar-bg); color: var(--sidebar-fg); }
# .stMultiSelect [data-baseweb="tag"]{
#   background: var(--accent-soft) !important; color: #1e3a8a !important;
#   border-radius: 8px !important; padding: 2px 6px !important; font-size: 0.9rem !important;
# }
# .stMultiSelect [role="listbox"] [role="option"]:hover{ background: var(--accent-hover) !important; color: #0c4a6e !important; }
# .stMultiSelect [role="listbox"] [aria-selected="true"]{ background: var(--accent-soft) !important; color: #075985 !important; }
# </style>
# """, unsafe_allow_html=True)
