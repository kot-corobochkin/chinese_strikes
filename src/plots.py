import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot_strikes_over_time(df, title=None):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Strike_Count"],
        mode="lines+markers",
        line=dict(width=3),
        marker=dict(size=8),
        name="Strikes"
    ))

    fig.update_layout(
        title=title or "Strikes in China by Year",
        xaxis_title="Year",
        yaxis_title="Number of strikes",
        template="plotly_white",
        hovermode="x unified"
    )
    fig.show()


def plot_action_types_pie(df, title=None):
    fig = px.pie(
        df,
        values="Count",
        names="Action",
        title=title or "Types of Protest Actions"
    )

    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(template="plotly_white")

    fig.show()


import plotly.graph_objects as go
import pandas as pd

def plot_indicator(df, y, title, yaxis_title, visible_industries):
    fig = go.Figure()

    df = df.copy()
    df[y] = pd.to_numeric(df[y], errors="coerce")

    year_totals = df.groupby("год")[y].sum()

    for industry, group in df.groupby("Industry_norm"):
        group = group.sort_values("год").copy()

        group["share_pct"] = (
            group[y] / group["год"].map(year_totals) * 100
        )

        fig.add_trace(go.Scatter(
            x=group["год"],
            y=group[y].astype(float),   # 🔑 ВОТ ЭТО КЛЮЧ
            mode="lines+markers",
            name=industry,
            visible=True if industry in visible_industries else "legendonly",
            customdata=group["share_pct"].astype(float),
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "Year: %{x}<br>"
                + yaxis_title + ": %{y:,.0f}<br>"
                "Share of total: %{customdata:.1f}%"
                "<extra></extra>"
            )
        ))

    fig.update_layout(
        title=title,
        xaxis_title="Год",
        yaxis_title=yaxis_title,
        template="plotly_white",
        hovermode="x unified"
    )

    fig.show()

def plot_gdp(df): 
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Final Consumption"],
        customdata=df[["Final Consumption %"]],
        mode='lines',
        name='Final Consumption',
        stackgroup='one',
        hovertemplate='Year: %{x}<br>Final Consumption: %{y}B<br>Share: %{customdata[0]:.2f}%<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Gross Capital Formation"],
        customdata=df[["Gross Capital Formation %"]],
        mode='lines',
        name='Gross Capital Formation',
        stackgroup='one',
        hovertemplate='Year: %{x}<br>Gross Capital: %{y}B<br>Share: %{customdata[0]:.2f}%<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Net Exports"],
        customdata=df[["Net Exports %"]],
        mode='lines',
        name='Net Exports',
        stackgroup='one',
        hovertemplate='Year: %{x}<br>Net Exports: %{y}B<br>Share: %{customdata[0]:.2f}%<extra></extra>'
    ))

    fig.update_layout(
        title='Guangdong GDP by Expenditure Approach (Area Chart)',
        xaxis_title='Year',
        yaxis_title='100 million yuan',
        legend_title='Components',
        hovermode='x unified'
    )

    fig.show()

def plot_sunburst(sorted_industries, title):
    rows = []


    INDUSTRY_COLORS = {
        "Manufacturing": "#EF553B",
        "Transport, storage, logistics and postal": "#636EFA",
        "Construction": "#00CC96",
        "Education": "#FFA15A",
        "Services": "#AB63FA",
        "Mining": "#FFD700",
        "Government and public sector": "#19D3F3"
}

    for industry, subcats in sorted_industries:
        for sub, count in subcats:
            rows.append({
                "label": sub,
                "parent": industry,
                "value": count,
                "color": INDUSTRY_COLORS.get(industry, "#CCCCCC")
            })

        rows.append({
            "label": industry,
            "parent": "",
            "value": sum(c for _, c in subcats),
            "color": INDUSTRY_COLORS.get(industry, "#CCCCCC")
        })

    df = pd.DataFrame(rows)
    color_map = dict(zip(df["label"], df["color"]))

    fig = px.sunburst(
        df,
        names="label",
        parents="parent",
        values="value",
        color="label",
        color_discrete_map=color_map,
        title=title
    )

    fig.update_layout(margin=dict(t=40, l=0, r=0, b=0))
    fig.show()

def plot_wages(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["Year"],
        y=df["Growth Rate (%)"],
        name="Темп роста (%)",
        marker_color="teal"
    ))
    fig.update_layout(
        title="📈 Темп роста средней зарплаты (1978–2023)",
        xaxis_title="Год",
        yaxis_title="Годовой прирост, %",
        template="plotly_white",
        hovermode="x unified"
    )
    fig.show()
    

def plot_strikes_by_city(df):
    fig = px.line(
        df,
        x="year",
        y=df.columns[1:],  # все города
        title="Забастовки в Гуандуне по городам"
    )

    fig.update_layout(
        xaxis_title="Год",
        yaxis_title="Число забастовок",
        hovermode="x unified"
    )

    fig.show()


def plot_strikes_by_industry(industry_year_df):
    fig_industry = px.line(
    industry_year_df,
    x="year",
    y=industry_year_df.columns[1:],
    title="Забастовки по индустриям"
    )

    fig_industry.update_layout(
        xaxis_title="Год",
        yaxis_title="Число стачек",
        hovermode="x unified"
    )

    fig_industry.show()

def plot_strikes_by_subindustry(industry_year_df):
    fig_subindustry = px.line(
    industry_year_df,
    x="year",
    y=industry_year_df.columns[1:],
    title="Забастовки по подотраслям"
    )

    fig_subindustry.update_layout(
        xaxis_title="Год",
        yaxis_title="Число стачек",
        hovermode="x unified"
    )
    fig_subindustry.show()

def plot_strikes_by_response_and_state(df):
        fig = px.bar(
            df,
            x="State",
            y="Number_of_Strikes",
            color="Response",
            title="Количество стачек по типам реакции в регионах"
        )

        fig.update_layout(
            xaxis_title="Регион",
            yaxis_title="Число стачек",
            hovermode="x unified"
        )

        fig.show()

def plot_strikes_by_state_and_industry(df):
    fig = px.bar(
        df,
        x="State",
        y="Number_of_Strikes",
        color="Industry",
        title="Количество стачек по отраслям в регионах"
    )

    fig.update_layout(
        xaxis_title="Регион",
        yaxis_title="Количество стачек",
        hovermode="x unified"
    )

    fig.show()

def plot_strikes_by_state_and_demand(df):
    fig = px.bar(
        df,
        x="State",
        y="Number_of_Strikes",
        color="Demand",
        title="Количество стачек по типам требований в регионах"
    )

    fig.update_layout(
        xaxis_title="Регион",
        yaxis_title="Количество стачек",
        hovermode="x unified"
    )

    fig.show()

def plot_action_by_state_and_type(df):
    fig = px.bar(
        df,
        x="State",
        y="Number_of_Strikes",
        color="Action",
        title="Количество инцидентов по типам в регионах"
    )

    fig.update_layout(
        xaxis_title="Регион",
        yaxis_title="Количество инцидентов",
        hovermode="x unified"
    )

    fig.show()

def plot_strikes_by_size(
    all_df,
    gd_df,
    title
):
    groups = all_df["Range_Number_of_Employees"]

    all_counts = all_df["Number_of_Strikes"]
    gd_counts = gd_df.set_index("Range_Number_of_Employees") \
                     .reindex(groups, fill_value=0)["Number_of_Strikes"]

    total_all = all_counts.sum()
    total_gd = gd_counts.sum()

    all_pct = (all_counts / total_all * 100) if total_all else 0
    gd_pct = (gd_counts / total_gd * 100) if total_gd else 0

    fig = go.Figure()

    fig.add_bar(
        x=groups,
        y=all_counts,
        name="Все регионы",
        hovertemplate=[
            f"{g}<br>Стачек: {c}<br>Доля: {p:.2f}%"
            for g, c, p in zip(groups, all_counts, all_pct)
        ]
    )

    fig.add_bar(
        x=groups,
        y=gd_counts,
        name="Гуандун",
        hovertemplate=[
            f"{g}<br>Стачек: {c}<br>Доля: {p:.2f}%"
            for g, c, p in zip(groups, gd_counts, gd_pct)
        ]
    )

    fig.update_layout(
        title=title,
        xaxis_title="Диапазон численности работников",
        yaxis_title="Количество стачек",
        barmode="group",
        hovermode="x unified"
    )

    fig.show()

def plot_demands(total_by_demand):
    fig = px.bar(
        total_by_demand,
        x="Worker_Demands",
        y="total_strikes",
        color="Worker_Demands",
        title="Стачки по требованиям (суммарно за 2021–2024)",
        labels={
            "total_strikes": "Число стачек",
            "Worker_Demands": "Требование"
        }
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False
    )

    fig.show()

def plot_industry_vulnerability(df, title):
    fig = px.scatter(
        df,
        x="Employed Persons_pct_growth",
        y="Profit per Worker growth (%)",
        color="strike_leverage",
        size="Weight",
        hover_name="Sector",
        labels={
            "Employed Persons_pct_growth": "Рост занятости (%)",
            "Profit per Worker growth (%)": "Рост прибыли на 1 рабочего (%)",
            "Weight": "Доля отрасли в прибыли (%)",
            "strike_leverage": "Структурная сила"
        },
        title=title,
        size_max=80,
        color_continuous_scale="Plasma"
    )

    fig.update_layout(
        coloraxis=dict(cmin=-1.5, cmax=1.5)
    )

    fig.show()