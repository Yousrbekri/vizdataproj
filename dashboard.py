import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')


st.set_page_config(
    page_title="Dashboard Environnemental",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    /* Fond blanc pour toute l'application */
    .stApp {
        background-color: #bcdef5;
    }
    
    /* Style pour le header */
    .main-header {
        background: #ebf5fc; 
        border-radius: 2rem;
        box-shadow: 0 4px 24px rgba(0,30,60,0.10);
        padding: 2.5rem 2rem 2rem 2rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }

    .main-header h1 {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-weight: 800;
        letter-spacing: 1px;
        line-height: 1.12;
        text-shadow: 1px 2px 8px rgba(0,30,60,0.07);
    }

    .main-header .main-title {
        color: #094670;
        font-size: 4rem;
        margin-bottom: 0.2rem;
        margin-top: 0;
    }

    .main-header .subtitle {
        color: #095170; 
        font-size: 3rem;
        margin-top: 0.4rem;
        margin-bottom: 0;
        font-weight: 800;
    }

    /* Conteneur KPI */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        margin-top: 1rem;
    }

    /* Cartes KPI avec bordures */
    .kpi-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
        flex: 1;
        margin: 0 0rem;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .kpi-card h3 {
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        height: 2em;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .kpi-card h2 {
        font-size: 1.5rem;
        margin: 0.5rem 0;
    }
    .kpi-card p {
        font-size: 0.8rem;
        margin: 0;
    }

    /* Conteneur filtres */
    .filters-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        background: #c9e0f0;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }

    /* Style des onglets */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        width: 100%;
    }

    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        background-color: #4e6580;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-left: 10px;
        padding-right: 10px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #8ab4d1;
        border-bottom: 3px solid #1f77b4;
    }
    .stTabs [aria-selected="true"] [data-testid="stMarkdownContainer"] p {
        color: white;
        font-weight: bold;
    }

    /* Style des sélecteurs */
    .stSelectbox, .stSlider, .stDateInput {
        color: #f9f9f9;
    }
    .stSelectbox div, .stSlider div, .stDateInput div {
        color: white !important; 
        font-size: 1rem;
        font-weight: bold;
    }

    /* Conteneurs de graphiques */
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }

    
    .stTabs [aria-selected="true"] [data-testid="stMarkdownContainer"] p {
        color: white;
        font-weight: bold;
    }
    h3 {
        color: #094670;font-family: 'Segoe UI', Arial, sans-serif;font-weight: 700;font-size: 2.1rem;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

#st.title("Tableau de bord des ressources en eau \net gestion hydrique")
st.markdown(
    """
    <div class='main-header'>
        <div style='text-align: center;'>
            <h1 class='main-title'>🌍 Afrique – Tableau de bord</h1>
            <h1 class='subtitle'>Ressources en Eau et Gestion Hydrique</h1>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)



df = pd.read_csv("dataset5.csv")

aliases_fr = {
    "area":"Pays",
    "year":"Année",
    "ag_withdrawal_pct_trwr_pct":"% prélèvements agricoles sur ressources renouvelables",
    "ag_withdrawal_pc_m3phab_yr":"Prélèvements agricoles (m³/hab/an)",
    "dam_cap_pc_m3phab":"Capacité barrage par habitant (m³/hab)",
    "gw_internal_recharge_km3_yr":"Recharge renouvelable des nappes (km³/an)",
    "ind_withdrawal_pc_m3phab_yr":"Prélèvements industriels (m³/hab/an)",
    "mun_withdrawal_pc_m3phab_yr":"Prélèvements municipaux (m³/hab/an)",
    "sdg642_ag_contrib_ws_pct":"Contribution agriculture au stress (%)",
    "sdg642_ind_contrib_ws_pct":"Contribution industrie au stress (%)",
    "sdg642_mun_contrib_ws_pct":"Contribution municipal au stress (%)",
    "sdg642_water_stress_pct":"Stress hydrique SDG 6.4.2 (%)",
    "dam_cap_total_km3":"Capacité totale des barrages (km³)",
    "tfww_km3_yr":"Prélèvements d’eau totaux (km³/an)",
    "trgw_km3_yr":"Ressources renouvelables souterraines (km³/an)",
    "trwr_km3_yr":"Ressources renouvelables totales (km³/an)",
    "tww_pc_m3phab_yr":"Consommation totale par habitant (m³/hab/an)",
    "tfww_trwr_pct":"Ratio prélèvements totaux / ressources renouvelables (%)",
    "stockage_sur_trwr_pct":"Part du stockage barrage sur ressources renouvelables (%)",
    "part_ag_pct":"Part agricole (%)",
    "part_ind_pct":"Part industrielle (%)",
    "part_mun_pct":"Part municipale (%)",
    "stress_cat":"Catégorie de stress",
    "pressure_cat":"Catégorie de pressure",
    'contribution_pct': 'Contribution au stress (%)',
    'secteur': 'Secteur'

  }


# Section KPI horizontaux avec fond blanc
st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
st.markdown("### Synthèse des indicateurs hydriques principaux")
selected_year = st.selectbox(
    "Année :",
    options=sorted(df['year'].unique()),
    key="year_kpi"
)
# Création des 5 KPI
col1, col2, col3, col4, col5 = st.columns(5)

df_selected_year = df[df['year'] == selected_year]
kpi_stress_mean = df_selected_year['sdg642_water_stress_pct'].mean()
kpi_trwr_sum = df_selected_year['trwr_km3_yr'].sum()
kpi_conso_mean = df_selected_year['tww_pc_m3phab_yr'].mean()
kpi_damcap_mean = df_selected_year['dam_cap_pc_m3phab'].mean()
kpi_part_gw = 100 * (df_selected_year['trgw_km3_yr'].sum() / df_selected_year['trwr_km3_yr'].sum())

with col1:
    st.markdown(
        f"""
        <div class='kpi-card'>
            <h3 style='color: #1f77b4;'> Stress Hydrique</h3>
            <h2 style='color: #2e86ab;'>{kpi_stress_mean:.1f}%</h2>
            <p style='color: #666;'>Moyenne {selected_year}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class='kpi-card'>
            <h3 style='color: #1f77b4;'> Ressources Eau</h3>
            <h2 style='color: #a23b72;'>{kpi_trwr_sum:.0f} km³</h2>
            <p style='color: #666;'>Total {selected_year}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class='kpi-card'>
            <h3 style='color: #1f77b4;'> Consommation</h3>
            <h2 style='color: #f18f01;'>{kpi_conso_mean:.0f} m³/hab</h2>
            <p style='color: #666;'>Moyenne {selected_year}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class='kpi-card'>
            <h3 style='color: #1f77b4;font-size: 1rem'> Capacité-Barrages</h3>
            <h2 style='color: #c73e1d;'>{kpi_damcap_mean:.1f} m³/hab</h2>
            <p style='color: #666;'>Moyenne {selected_year}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        f"""
        <div class='kpi-card'>
            <h3 style='color: #1f77b4;'> Eaux Souterraines</h3>
            <h2 style='color: #3d348b;'>{kpi_part_gw:.1f}%</h2>
            <p style='color: #666;'>Part {selected_year}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)

# Séparateur léger
st.markdown("<hr style='border: 1px solid #e0e0e0; margin: 2rem 0;'>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "Ressource et Stockage",
    "Pression et Stress Hydrique",
    "Contribution Sectorielle au Stress",
    "Consomation d'eau"
])

with tab1:
    st.markdown("<h2 style='color:#094670;font-weight:700;'>Ressources Renouvelables & Ressources Souterraines</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Ressources en eau renouvelables par pays</h3>",unsafe_allow_html=True)
        fig1 = px.choropleth(
            df,
            locations='area',
            locationmode='country names',
            color='trwr_km3_yr',
            color_continuous_scale='Blues',
            hover_name='area',
            hover_data={
                'trwr_km3_yr': ':.1f',
                'tfww_km3_yr': ':.1f',
                'sdg642_water_stress_pct': ':.1f'
            },
            title=aliases_fr['trwr_km3_yr'],
            labels={
                'trwr_km3_yr': aliases_fr['trwr_km3_yr'],
                'tfww_km3_yr': aliases_fr['tfww_km3_yr'],
                'sdg642_water_stress_pct': aliases_fr['sdg642_water_stress_pct']
            }
        )

        fig1.update_layout(
            coloraxis_colorbar_title='km³/an',
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='natural earth',
                scope='africa'
            ),
            margin=dict(l=0, r=0, t=40, b=0),
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown(
            "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Top des pays par ressources en eau</h3>",
            unsafe_allow_html=True)

        df_rank = df[df['year'] == 2022].nlargest(10, 'trwr_km3_yr')
        fig4 = px.bar(
            df_rank,
            x='trwr_km3_yr',
            y='area',
            orientation='h',
            title=f"Top {10} — Ressources en eau renouvelables en {2022}",
            labels={
                'trwr_km3_yr': 'Ressources en eau renouvelables (km³/an)',
                'area': 'Pays'
            },
            color='trwr_km3_yr',
            color_continuous_scale='Blues'
        )
        fig4.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title='Ressources en eau renouvelables (km³/an)',
            yaxis_title='Pays',
            coloraxis_showscale=False
        )
        fig4.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title='Ressources en eau renouvelables (km³/an)',
            yaxis_title='Pays',
        )
        #fig4.update_traces(marker_line_width=0)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown(
        "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Répartition géographique des ressources</h3>",
        unsafe_allow_html=True)
    df_sc3 = df[df['year'] == 2022]
    fig3 = px.scatter(
        df_sc3,
        x='trwr_km3_yr',
        y='tww_pc_m3phab_yr',
        color='area',
        hover_name='area',
        title=f"{aliases_fr['trwr_km3_yr']} vs {aliases_fr['tww_pc_m3phab_yr']} ",
        labels={
            'trwr_km3_yr': aliases_fr['trwr_km3_yr'],
            'tww_pc_m3phab_yr': aliases_fr['tww_pc_m3phab_yr']
        }
    )
    fig3.update_layout(
        xaxis_title=aliases_fr['trwr_km3_yr'],
        yaxis_title=aliases_fr['tww_pc_m3phab_yr']
    )
    st.plotly_chart(fig3, use_container_width=True)



    st.markdown(
        "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Relation entre ressources en eau et capacité des barrages</h3>",
        unsafe_allow_html=True)
    df_sc2 = df[df['year'] == 2022]
    fig = px.scatter(
        df_sc2, x='trwr_km3_yr', y='dam_cap_total_km3',
        size='dam_cap_pc_m3phab', hover_name='area',
        title=f"Ressources en eau vs Capacité des barrages",
        labels={
            'trwr_km3_yr': 'Ressources en eau renouvelables (km³/an)',
            'dam_cap_total_km3': 'Capacité totale des barrages (km³)',
            'dam_cap_pc_m3phab': 'Capacité des barrages par habitant (m³/hab)',
        }
    )
    fig.update_xaxes(range=[-20, 400])
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Top des pays par ressources en eau</h3>",
        unsafe_allow_html=True)
    df_y = df[df['year'] == 2022]
    top_n = 15

    for var, title in [('trgw_km3_yr', 'Ressources souterraines')]:
        d = df_y.sort_values(var, ascending=False)
        fig_top = px.bar(d.head(top_n), x=var, y='area', orientation='h',
                         title=f'Top {top_n} — {title} (km³/an) — ')
        fig_top.update_layout(yaxis={'categoryorder': 'total ascending'})
        fig_top.update_traces(marker_color='#64b5f6')

        fig_bot = px.bar(d.tail(top_n), x=var, y='area', orientation='h',
                         title=f'Bas {top_n} — {title} (km³/an) — ')
        fig_bot.update_layout(yaxis={'categoryorder': 'total ascending'})
        fig_bot.update_traces(marker_color='#64b5f6')


    coll1,coll2 = st.columns(2)

    with coll1:
        st.plotly_chart(fig_top, use_container_width=True)

    with coll2:
        st.plotly_chart(fig_bot, use_container_width=True)








    st.markdown("---")
    st.markdown("<h2 style='color:#094670;font-weight:700;'>Capacité des Barrages</h2>",
                unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown(
            "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Capacité totale des barrage</h3>",
            unsafe_allow_html=True)
        fig6 = px.choropleth(
            df, locations='area', locationmode='country names',
            color='dam_cap_total_km3',
            color_continuous_scale='YlOrBr',
            hover_name='area',
            hover_data={'dam_cap_total_km3': ':.2f', 'dam_cap_pc_m3phab': ':.1f'},
            title='Capacité totale des barrages (km³)',
            labels = {
                 'dam_cap_pc_m3phab': aliases_fr['dam_cap_pc_m3phab'],
                 'dam_cap_total_km3': aliases_fr['dam_cap_total_km3']
            }
        )
        fig6.update_layout(coloraxis_colorbar_title='km³')
        fig6.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth', scope='africa'),
            margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig6, use_container_width=True)

    with col4:
        st.markdown(
            "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Capacité des barrage par habitant</h3>",
            unsafe_allow_html=True)
        fig5 = px.choropleth(
            df, locations='area', locationmode='country names',
            color='dam_cap_pc_m3phab',
            color_continuous_scale='Oranges',
            hover_name='area',
            hover_data={'dam_cap_pc_m3phab': ':.1f', 'dam_cap_total_km3': ':.2f'},
            title='Capacité de barrage par habitant (m³/hab)',
            labels={
                'dam_cap_pc_m3phab': aliases_fr['dam_cap_pc_m3phab'],
                'dam_cap_total_km3': aliases_fr['dam_cap_total_km3']
            }
        )
        fig5.update_layout(coloraxis_colorbar_title='m³/hab')
        fig5.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth', scope='africa'),
            margin=dict(l=0, r=0, t=40, b=0))

        st.plotly_chart(fig5, use_container_width=True)

    col5, col6 = st.columns(2)
    with col5:
        st.markdown(
            "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Pays à plus forte/faible capacité de stockage des barrages (km³)</h3>",
            unsafe_allow_html=True)
        df_y = df[df['year'] == 2022].sort_values('dam_cap_total_km3', ascending=False)
        top_n = 15
        fig_top = px.bar(df_y.head(top_n), x='dam_cap_total_km3', y='area', orientation='h',
                         title=f'Top {top_n} — Capacité totale (km³) — ')
        fig_top.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_top, use_container_width=True)

        fig_bot = px.bar(df_y.tail(top_n), x='dam_cap_total_km3', y='area', orientation='h',
                         title=f'Bas {top_n} — Capacité totale (km³) —')
        fig_bot.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_bot, use_container_width=True)

    with col6:
        st.markdown(
            "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Pays à plus forte/faible capacité de stockage par habitant (m³/hab)</h3>",
            unsafe_allow_html=True)
        df_y = df[df['year'] == 2022].sort_values('dam_cap_pc_m3phab', ascending=False)
        fig_top_pc = px.bar(df_y.head(top_n), x='dam_cap_pc_m3phab', y='area', orientation='h',
                            title=f'Top {top_n} — Capacité par habitant (m³/hab) —')
        fig_top_pc.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_top_pc, use_container_width=True)

        fig_bot_pc = px.bar(df_y.tail(top_n), x='dam_cap_pc_m3phab', y='area', orientation='h',
                            title=f'Bas {top_n} — Capacité par habitant (m³/hab) —')
        fig_bot_pc.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_bot_pc, use_container_width=True)

    st.markdown("---")





num_cols = [
    'sdg642_water_stress_pct','tww_pc_m3phab_yr','dam_cap_pc_m3phab',
    'trwr_km3_yr','tfww_km3_yr',
    'sdg642_ag_contrib_ws_pct','sdg642_ind_contrib_ws_pct','sdg642_mun_contrib_ws_pct'
]
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce')


selected_year = int(df['year'].dropna().max())

bins = [0,25,50,75,100,np.inf]
labels = ['Faible','Moyen','Élevé','Critique','Extrême']
df['stress_cat'] = pd.cut(df['sdg642_water_stress_pct'], bins=bins, labels=labels, include_lowest=True)


with tab2:
    st.markdown("<h2 style='color:#094670;font-weight:700;'>Stress Hydrique et Prélèvement des Ressources</h2>",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Stress Hydrique</h3>",
            unsafe_allow_html=True)
        fig21 = px.choropleth(
            df, locations='area', locationmode='country names',
            color='sdg642_water_stress_pct',
            hover_name='area',
            hover_data={'sdg642_water_stress_pct':':.1f','tww_pc_m3phab_yr':':.1f','dam_cap_pc_m3phab':':.1f'},
            color_continuous_scale='Reds',
            title=aliases_fr['sdg642_water_stress_pct'],
            labels={
                'tww_pc_m3phab_yr': aliases_fr['tww_pc_m3phab_yr'],
                'dam_cap_pc_m3phab': aliases_fr['dam_cap_pc_m3phab'],
                'sdg642_water_stress_pct': aliases_fr['sdg642_water_stress_pct']
            }
        )
        fig21.update_layout(coloraxis_colorbar_title=aliases_fr['sdg642_water_stress_pct'],
                  geo=dict(showframe=False, showcoastlines=True,projection_type='natural earth',scope='africa'),margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig21, use_container_width=True)


    num_cols = ['tfww_trwr_pct', 'sdg642_water_stress_pct', 'tww_pc_m3phab_yr',
                'dam_cap_pc_m3phab', 'trwr_km3_yr', 'tfww_km3_yr']
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    year = int(df['year'].dropna().max())
    # Catégories de pression (exemples proches du SDG)
    bins = [0, 25, 50, 75, 100, np.inf]
    labels = ['Faible', 'Moyen', 'Élevé', 'Critique', 'Extrême']
    df['pressure_cat'] = pd.cut(df['tfww_trwr_pct'], bins=bins, labels=labels, include_lowest=True)

    col3, col4 = st.columns(2)
    # st.markdown("**Ressources en eau renouvelables par pays**")
    df_counts = (df.groupby(['year', 'stress_cat'])['area']
                 .count().reset_index(name='nb_pays'))
    df_counts_year = df_counts[df_counts['year'] == 2022]

    df_counts2 = (df.groupby(['year', 'pressure_cat'])['area']
                  .count().reset_index(name='nb_pays'))
    df_counts_year2 = df_counts2[df_counts['year'] == 2022]


    with col2:
        st.markdown(
            "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Répartition</h3>",
            unsafe_allow_html=True)
        color_map_red = {'Faible': '#fde0dc',  'Moyen': '#f8bbd0', 'Élevé': '#f06262', 'Critique': '#e53935', 'Extrême': '#b71c1c'}
        fig22 = px.bar(
            df_counts_year,
            x='stress_cat',
            y='nb_pays',
            color='stress_cat',
            category_orders={'stress_cat': ['Faible', 'Moyen', 'Élevé', 'Critique', 'Extrême']},
            color_discrete_map=color_map_red,
            title=f"Répartition des pays par catégorie de stress hydrique — {year}",
            labels={
                'stress_cat': aliases_fr['stress_cat'],
                'nb_pays': "Nombre de pays"
            }
        )

        fig22.update_layout(
            xaxis_title=aliases_fr['stress_cat'],
            yaxis_title="Nombre de pays",
            legend_title=aliases_fr['stress_cat']
        )
        st.plotly_chart(fig22, use_container_width=True)
    with col3:
        st.markdown(
            "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Prelevement par Ressource</h3>",
            unsafe_allow_html=True)
        color_map = {'Faible': '#43a047',  'Moyen': '#fbc02d','Élevé': '#fb8c00',  'Critique': '#e53935','Extrême': '#b71c1c' }
        fig24 = px.choropleth(
            df, locations='area', locationmode='country names',
            color='pressure_cat',
            category_orders={'pressure_cat': ['Faible', 'Moyen', 'Élevé', 'Critique', 'Extrême']},
            color_discrete_map=color_map,
            title='Catégories de pression sur la ressource en eau'
        )
        fig24.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth', scope='africa'),
            margin=dict(l=0, r=0, t=40, b=0))

        st.plotly_chart(fig24, use_container_width=True)



    with col4:
        st.markdown(
            "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Répartition</h3>",
            unsafe_allow_html=True)
        fig25 = px.bar(
            df_counts_year2,
            x='pressure_cat',
            y='nb_pays',
            color='pressure_cat',
            category_orders={'pressure_cat': ['Faible', 'Moyen', 'Élevé', 'Critique', 'Extrême']},
            color_discrete_map=color_map,
            title=f"Répartition des pays par catégories de pression —",
            labels={
                'pressure_cat': aliases_fr['pressure_cat'],
                'nb_pays': "Nombre de pays"
            }
        )
        fig25.update_layout(
            xaxis_title=aliases_fr['pressure_cat'],
            yaxis_title="Nombre de pays",
            legend_title=aliases_fr['pressure_cat']
        )
        st.plotly_chart(fig25, use_container_width=True)

    st.markdown(
        "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Corrélations entre stress hydrique et indicateurs associés</h3>",
        unsafe_allow_html=True)
    cols = ['sdg642_water_stress_pct', 'tww_pc_m3phab_yr', 'dam_cap_pc_m3phab', 'tfww_km3_yr', 'trwr_km3_yr']
    corr = df[cols].corr()
    corr.index = [aliases_fr.get(c, c) for c in corr.index]
    corr.columns = [aliases_fr.get(c, c) for c in corr.columns]

    fig23 = px.imshow(
        corr,
        text_auto=True,
        aspect='auto',
        color_continuous_scale='Reds',
        title="Matrice de corrélation (stress et variables associées)"
    )

    fig23.update_layout(
        xaxis_title="Variables",
        yaxis_title="Variables"
    )
    st.plotly_chart(fig23, use_container_width=True)



with tab4:
    st.markdown("<h2 style='color:#094670;font-weight:700;'>Consomation par habitant & Consomation sectorisée de l'eau</h2>",
                unsafe_allow_html=True)
    num_cols = [
        'ag_withdrawal_pc_m3phab_yr', 'ind_withdrawal_pc_m3phab_yr', 'mun_withdrawal_pc_m3phab_yr',
        'tww_pc_m3phab_yr', 'sdg642_water_stress_pct'
    ]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')

    year = int(df['year'].dropna().max())

    sect_map = {
        'ag_withdrawal_pc_m3phab_yr': 'Agriculture (m³/hab/an)',
        'ind_withdrawal_pc_m3phab_yr': 'Industrie (m³/hab/an)',
        'mun_withdrawal_pc_m3phab_yr': 'Municipal (m³/hab/an)'
    }
    color_map = {
        'Agriculture (m³/hab/an)': '#248f4d',
        'Industrie (m³/hab/an)': '#8c5606',
        'Municipal (m³/hab/an)': '#fbc02d'
    }
    df_long = df.melt(id_vars=['area', 'year'], value_vars=list(sect_map.keys()),
                      var_name='variable', value_name='pc_m3phab_yr')
    df_long['secteur'] = df_long['variable'].map(sect_map)
    def top_bottom(df_year, var, k=10, color='#25b35c'):
        d = df_year.sort_values(var, ascending=False)
        fig_top = px.bar(d.head(k), x=var, y='area', orientation='h',
                         title=f'Top {k} — {sect_map[var]} (m³/hab/an) — {year}')
        fig_top.update_traces(marker_color=color)
        fig_top.update_layout(yaxis={'categoryorder': 'total ascending'})
        fig_bot = px.bar(d.tail(k), x=var, y='area', orientation='h',
                         title=f'Bas {k} — {sect_map[var]} (m³/hab/an) — {year}')
        fig_bot.update_traces(marker_color=color)
        fig_bot.update_layout(yaxis={'categoryorder': 'total ascending'})

        return fig_top, fig_bot


    st.markdown(
        "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Classement des pays par consommation sectorielle d’eau par habitant</h3>",
        unsafe_allow_html=True)


    d1 = df_long[df_long['year'] == 2022]
    top_areas = (d1.groupby('area')['pc_m3phab_yr'].sum().sort_values(ascending=False).head(15).index.tolist())
    d1_top = d1[d1['area'].isin(top_areas)]
    order_area_top = (d1_top.groupby('area')['pc_m3phab_yr'].sum().sort_values(ascending=False).index.tolist())
    fig41 = px.bar(
        d1_top,x='area',y='pc_m3phab_yr',color='secteur',
        category_orders={'area': order_area_top, 'secteur': list(sect_map.values())},
        color_discrete_map=color_map,
        title=f'Top 15 pays — Consommation sectorisée par habitant ({year})'
    )
    fig41.update_layout(xaxis_title='Pays', yaxis_title='m³/hab/an', barmode='stack')
    st.plotly_chart(fig41, use_container_width=True)

    st.markdown(
        "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Consommation sectorielle d’eau par habitant</h3>",
        unsafe_allow_html=True)
    df_y = df[df['year'] == year]
    for var, v in zip(sect_map, sect_map.values()):
        c = color_map[v]
        f1, f2 = top_bottom(df_y, var, k=10, color=c)
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(f1, use_container_width=True)
        with col2:
            st.plotly_chart(f2, use_container_width=True)

    st.markdown(
        "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Analyse sectorielle de la consommation d’eau par habitant</h3>",
        unsafe_allow_html=True)


    col_1, col_2 = st.columns(2)
    with col_1:
        year_radar = st.selectbox(
            "Sélectionnez l'année :",
            options=sorted(df['year'].unique()),
            index=len(df['year'].unique()) - 1,
            key="radar_year"
        )

    with col_2:
        selected_countries_radar = st.multiselect(
            "Sélectionnez les pays :",
            options=df['area'].unique(),
            default=['Algeria', 'Morocco', 'Tunisia'],
            key="radar_countries"
        )

    if selected_countries_radar:
        d3 = df[(df['year'] == year_radar) & (df['area'].isin(selected_countries_radar))]
        axes = ['ag_withdrawal_pc_m3phab_yr', 'ind_withdrawal_pc_m3phab_yr', 'mun_withdrawal_pc_m3phab_yr']
        labels = ['Agriculture', 'Industrie', 'Municipal']

        fig_radar = go.Figure()

        for _, r in d3.iterrows():
            vals = [r[a] for a in axes]
            vals = vals + vals[:1]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals,
                theta=labels + labels[:1],
                fill='toself',
                name=r['area']
            ))

        # Personnaliser le layout
        fig_radar.update_layout(
            title=f'Répartition sectorielle de la consommation (m³/hab/an) — {year_radar}',
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    showticklabels=True,
                    gridcolor='lightgray'
                ),
                angularaxis=dict(
                    gridcolor='lightgray',
                    linecolor='black'
                ),
                bgcolor='white'
            ),
            showlegend=True,
        )


        df_line = df[df['area'].isin(selected_countries_radar)].sort_values(['area', 'year'])
        fig_y = px.line(
            df_line, x='year', y='tww_pc_m3phab_yr', color='area',
            markers=True, title='Évolution de la consommation par habitant (m³/hab/an)',
            labels={
                'tww_pc_m3phab_yr': aliases_fr['tww_pc_m3phab_yr']
            }
        )
        fig_y.update_layout(xaxis_title=aliases_fr['year'], yaxis_title=aliases_fr['tww_pc_m3phab_yr'])





        col_3, col_4 = st.columns(2)
        with col_3:
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_4:
            st.plotly_chart(fig_y, use_container_width=True)

        st.markdown(
            "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Relations entre la consommation totale d’eau (m³/hab/an) et le niveau de stress hydrique SDG par pays</h3>",
            unsafe_allow_html=True)

        df_sc = df[df['year'] == year]
        fig_sc = px.scatter(
            df_sc, x='tww_pc_m3phab_yr', y='sdg642_water_stress_pct',
            size='dam_cap_pc_m3phab', color='area', hover_name='area',
            title="Conso par habitant vs Stress SDG",
            labels={'tww_pc_m3phab_yr': aliases_fr['tww_pc_m3phab_yr'],
                    'sdg642_water_stress_pct': aliases_fr['sdg642_water_stress_pct']}
        )
        st.plotly_chart(fig_sc, use_container_width=True)

with tab3:
    st.markdown("<h2 style='color:#094670;font-weight:700;'>Contribution au stress par secteur</h2>",
                unsafe_allow_html=True)
    num_cols = [
        'sdg642_ag_contrib_ws_pct', 'sdg642_ind_contrib_ws_pct', 'sdg642_mun_contrib_ws_pct',
        'sdg642_water_stress_pct', 'tww_pc_m3phab_yr', 'dam_cap_pc_m3phab'
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    contrib_map = {
        'sdg642_ag_contrib_ws_pct': 'Agriculture',
        'sdg642_ind_contrib_ws_pct': 'Industrie',
        'sdg642_mun_contrib_ws_pct': 'Municipal'
    }
    color_map2 = {
        'Agriculture': '#25b35c',
        'Industrie': '#8c5606',
        'Municipal': '#fbc02d'
    }
    df_long = df.melt(
        id_vars=['area', 'year', 'sdg642_water_stress_pct'],
        value_vars=list(contrib_map.keys()),
        var_name='variable', value_name='contribution_pct'
    )
    df_long['secteur'] = df_long['variable'].map(contrib_map)
    selected_year = int(df['year'].dropna().max())
    selected_country = df['area'].dropna().iloc[0]






    col__1, col__2 = st.columns(2)
    with col__1:
        year_s = st.selectbox(
            "Sélectionnez l'année :",
            options=sorted(df['year'].unique()),
            index=len(df['year'].unique()) - 1,
            key="cont_year"
        )
    with col__2:
        selected_countries = st.selectbox(
            "Sélectionnez les pays :",
            options=sorted(df['area'].unique()),
            index=len(df['year'].unique()) - 1,
            key="cont_countries"
        )

    st.markdown(
        "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Part des secteurs dans la pression sur l’eau</h3>",
        unsafe_allow_html=True)

    if selected_countries:
        d0 = df_long[(df_long['area'] == selected_countries) & (df_long['year'] == year_s)]
        for _, r in d3.iterrows():
            vals = [r[a] for a in axes]
            vals = vals + vals[:1]
            fig_donut = px.pie(
                d0, names='secteur', values='contribution_pct', hole=0.55,color='secteur',
                color_discrete_map=color_map2,
                title=f'Contributions au stress SDG — {selected_countries} ({year_s})'
            )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_donut, use_container_width=True)

    year = year_s
    d1 = df_long[df_long['year'] == year].copy()
    order_area = (df[df['year'] == year]
                  .sort_values('sdg642_water_stress_pct', ascending=False)['area'].tolist())

    st.markdown(
        "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Part des secteurs dans la contribution aux niveaux de stress hydrique</h3>",
        unsafe_allow_html=True)
    fig_stack_countries = px.bar(
        d1, x='area', y='contribution_pct', color='secteur',
        category_orders={'area': order_area, 'secteur': list(sect_map.values())},
        title=f'Composition sectorielle du stress — {year}',
        color_discrete_map=color_map2,
        labels={'area': aliases_fr['area'], 'contribution_pct': aliases_fr['contribution_pct']}
    )
    fig_stack_countries.update_layout(barmode='stack')
    st.plotly_chart(fig_stack_countries, use_container_width=True)

    d6 = df_long[df_long['area'] == selected_countries].copy()
    fig_combo = px.bar(
        d6, x='year', y='contribution_pct', color='secteur',
        category_orders={'secteur': list(sect_map.values())},
        color_discrete_map=color_map2,
        title=f'Contributions et stress total — {selected_countries}'
    )
    d_stress = (df[df['area'] == selected_countries][['year', 'sdg642_water_stress_pct']]
                .sort_values('year'))
    fig_combo.add_trace(go.Scatter(
        x=d_stress['year'], y=d_stress['sdg642_water_stress_pct'],
        mode='lines+markers', name='Stress total (%)', yaxis='y2'
    ))
    fig_combo.update_layout(
        yaxis=dict(title='Contribution (%)'),
        yaxis2=dict(title='Stress (%)', overlaying='y', side='right')
    )
    st.markdown(
        "<h3 style='color:#094670;font-size: 1.3rem;font-weight:700;'>Variation des contributions sectorielles au stress hydrique et niveau global</h3>",
        unsafe_allow_html=True)
    st.plotly_chart(fig_combo, use_container_width=True)



st.markdown("""
    <div style="text-align:center; color:#094670;">
      <hr>
      <b>Sources des données :</b>
      <a href='https://data.apps.fao.org/aquastat/?lang=en&share=f-9345f601-3c88-413b-8cb9-0572547bf9e' target='_blank'>Dataset Ressources Eau,Barrages & Stress Hydrique</a> |
      <br><br>
      <span style="font-size:0.9rem;">App & visualisations © 2025</span>
    </div>
""", unsafe_allow_html=True)

