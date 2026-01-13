from collections import defaultdict
import pandas as pd
import numpy as np


NORMALIZE_INDUSTRIES = {
 # Communication / Electronics
 "Communication Equipment, Computers & Other Electronics": "Communication Equipment, Computers and Other Electronics",
 "Manufacture of Communication Equipment, Computers and Other Electronic Equipment": "Communication Equipment, Computers and Other Electronics",
 
 # Electrical machinery
 "Electrical Machinery and Equipment": "Electrical Machinery and Equipment",
 "Manufacture of Electrical Machinery and Equipment": "Electrical Machinery and Equipment",
 
 # Raw chemicals
 "Raw Chemical Materials and Chemical Products": "Chemical Materials and Products",
 "Manufacture of Raw Chemical Materials and Chemical Products": "Chemical Materials and Products",
 
 # Rubber / plastic
 "Rubber Products": "Rubber and Plastic Products",
 "Plastic Products": "Rubber and Plastic Products",
 "Rubber and Plastic Products": "Rubber and Plastic Products",
 
 # Transport
 "Transport Equipment": "Transport Equipment",
 "Manufacture of Transport Equipment": "Transport Equipment",
 "Railway/Ship/Aeronautics & Other Transport Equipment": "Transport Equipment",
 
 # Furniture / timber
 "Timber Processing, Bamboo/Cane/Palm/Straw Products": "Timber Processing, Bamboo and Straw Products",
 "Timber Processing, Bamboo, Cane, Palm Fiber and Straw Products": "Timber Processing, Bamboo and Straw Products",
 
 # Instruments
 "Instruments and Office Machinery": "Instruments, Meters and Office Machinery",
 "Instruments and Meters": "Instruments, Meters and Office Machinery",
 "Manufacture of Instruments, Meters and Machinery for Cultural and Office Use": "Instruments, Meters and Office Machinery",
 
 # Cultural goods
 "Cultural/Educational/Sports/Entertainment Articles": "Cultural, Educational and Sports Goods",
 "Manufacture of Cultural, Educational and Sports Articles": "Cultural, Educational and Sports Goods",
 "Manufacture of Cultural, Educational and Sports Goods": "Cultural, Educational and Sports Goods",
 
 # Machinery
 "General-purpose Machinery": "General-purpose Machinery",
 "Manufacture of General-purpose Machinery": "General-purpose Machinery",
 "Special-purpose Machinery": "Special-purpose Machinery",
 "Manufacture of Special-purpose Machinery": "Special-purpose Machinery",
 
 # Leather
 "Leather, Fur, Feather & Related Products and Footwear": "Leather, Fur, Feather and Related Products",
 "Leather, Fur, Feather, Down and Related Products": "Leather, Fur, Feather and Related Products",
 "Feather, Furs, Down and Related Products": "Leather, Fur, Feather and Related Products",
 
 # Petroleum
 "Petroleum Refining, Coking and Nuclear Fuel Processing": "Petroleum, Coal and other Fuel Processing",
 "Petroleum, Coal and other Fuel Processing": "Petroleum, Coal and other Fuel Processing",
 
 # Energy and utilities
 "Electric Power & Heat Production/Supply": "Electric Power and Heat Production/Supply",
 "Production and Supply of Electric Power and Heat Power": "Electric Power and Heat Production/Supply",
 "Gas Production and Supply": "Production and Supply of Gas",
 "Production and Supply of Gas": "Production and Supply of Gas",
 "Water Production and Supply": "Production and Supply of Water",
 "Production and Supply of Water": "Production and Supply of Water",
 
 # Mining
 "Mining Specialized and Auxiliary Operations": "Auxiliary Mining Operations",
 "Auxiliary Mining Operations": "Auxiliary Mining Operations",
 "Mining and Washing of Coal": "Coal Mining and Dressing",
 "Coal Mining and Dressing": "Coal Mining and Dressing",
 "Mining and Dressing of Other Ores": "Mining and Dressing of Nonmetal Ores",
 
 # Recycling
 "Comprehensive Utilization of Waste": "Recycling and Disposal of Waste",
 
 # Default — остальные останутся как есть
 }

SECTOR_MAPPING_2013_TO_2023 = {
    "Processing of Farm and Sideline Food": "Processing of Food from Agricultural Products",
    "Manufacture of Food": "Manufacturing of Foods",
    "Textile Industry": "Textile Industry",
    "Manufacture of Textile Garments, Footwear and Headgear": "Manufacture of Textile Wearing Apparel, Clothing",
    "Manufacture of Cultural, Educational, Sports and Entertainment Articles": "Manufacture of Culture and Education, Arts and Crafts, Sports and Entertainment Supplies",
    "Petroleum, Coal and other Fuel Processing": "Processing of Petroleum, Coking, Processing of Nuclear",
    "Manufacture of Raw Chemical Materials and Chemical Products": "Manufacturing of Raw Chemical Material and Chemical Products",
    "Manufacture of Medicines": "Manufacturing of Medical and Pharmaceutical Products",
    "Rubber and Plastic Products": "Manufacture of Rubber and Plastic",
    "Nonmetal Mineral Products": "Manufacturing of Non-metallic Mineral Products",
    "Smelting and Pressing of Ferrous Metals": "Smelting and Pressing of Ferrous Metals",
    "Smelting and Pressing of Nonferrous Metals": "Smelting and Pressing of Non-ferrous Metals",
    "Metal Products": "Manufacturing of Metal Products",
    "Manufacture of General-purpose Machinery": "Manufacturing of General Purpose Equipment",
    "Manufacture of Special-purpose Machinery": "Manufacturing of Special Purpose Equipment",
    "Manufacture of Automobile": "Manufacture of Automobile",
    "Manufacture of Electrical Machinery and Equipment": "Manufacturing of Electric Machinery and Equipment",
    "Manufacture of Communication Equipment, Computers and Other Electronic Equipment": "Manufacture of Computers, Communications and Other Electronic Equipment",
    "Production and Supply of Electric Power and Heat Power": "Production and Supply of Electric Power and Heat Power",
    "Production and Supply of Gas": "Production and Supply of Gas",
}


def prepare_economic_indicators(df):
    df = df.copy()

    # --- нормализация отраслей ---
    df["Industry_norm"] = (
        df["Отрасль"]
        .map(NORMALIZE_INDUSTRIES)
        .fillna(df["Отрасль"])
    )

    # --- пересчёты ---
    df["Workers_real"] = df["Workers"] * 10_000
    df["Profit_per_worker"] = (df["Профит"] * 100_000_000) / df["Workers_real"]
    df["Workers_per_enterprise"] = df["Workers_real"] / df["Number"]

    # --- фильтры ---
    df = df[df["год"] != 2023]
    df = df[~(
        (df["Industry_norm"] == "Transport Equipment") &
        (df["год"] >= 2012)
    )]

    # --- агрегация ---
    result = (
        df.groupby(["Industry_norm", "год"], as_index=False)
          .agg({
              "Profit_per_worker": "mean",
              "Профит": "sum",
              "Workers_real": "sum",
              "TotalOutput": "sum",
              "Number": "sum",
              "Workers_per_enterprise": "mean"
          })
          .sort_values(["Industry_norm", "год"])
    )

    return result

def prepare_gdp_composition(df):
    df["Final Consumption %"] = df["Final Consumption"] / df["GDP"] * 100
    df["Gross Capital Formation %"] = df["Gross Capital Formation"] / df["GDP"] * 100
    df["Net Exports %"] = df["Net Exports"] / df["GDP"] * 100

    return df

def prepare_industries(
    rows,
    min_subindustry_count=3
):
    industry_data = defaultdict(list)

    for industry, subindustry, count in rows:
        industry_data[industry].append((subindustry, count))

    final_data = {}

    for industry, subentries in industry_data.items():
        sub_dict = {}
        other_count = 0

        for subindustry, count in subentries:
            if (
                count < min_subindustry_count
                or subindustry is None
            ):
                other_count += count
            else:
                sub_dict[subindustry] = count

        if other_count > 0:
            sub_dict["Other"] = other_count

        final_data[industry] = sorted(
            sub_dict.items(),
            key=lambda x: x[1],
            reverse=True
        )

    # 🔑 сортировка индустрий по сумме стачек
    return sorted(
        final_data.items(),
        key=lambda x: sum(v for _, v in x[1]),
        reverse=True
    )

def prepare_strikes_by_year_and_city(df, state="Guangdong"):
    gd = df[df["State"] == state].copy()

    gd["Year"] = gd["Start_Date"].dt.year

    pivot = (
        gd
        .pivot_table(
            index="Year",
            columns="City",
            values="id",
            aggfunc="count",
            fill_value=0
        )
        .reset_index()
        .sort_values("Year")
    )

    return pivot

def prepare_strikes_by_year_and_category(df, category_col):
    tmp = df.copy()
    tmp["year"] = tmp["Start_Date"].dt.year

    result = (
        tmp
        .dropna(subset=[category_col])
        .pivot_table(
            index="year",
            columns=category_col,
            values="id",
            aggfunc="count",
            fill_value=0
        )
        .reset_index()
        .sort_values("year")
    )

    return result

def prepare_strikes_by_state_and_response(df):
    action_data = defaultdict(int)

    for _, row in df.iterrows():
        state = row.get("State")
        action_str = row.get("Action_Response")

        if not state or not action_str:
            continue

        parts = [p.strip() for p in action_str.split("/")]

        for part in parts:
            action_data[(state, part)] += 1

    data = [
        (state, response, cnt)
        for (state, response), cnt in action_data.items()
    ]

    return pd.DataFrame(
        data,
        columns=["State", "Response", "Number_of_Strikes"]
    )

def prepare_strikes_by_state_and_industry(df, min_count=5):
    grouped = (
        df
        .groupby(["State", "Industry"])
        .size()
        .reset_index(name="Number_of_Strikes")
    )

    return grouped[grouped["Number_of_Strikes"] >= min_count]

def prepare_strikes_by_state_and_demand(
    df,
    min_state_strikes=20
):
    # 1. отбираем активные регионы
    active_states = (
        df
        .groupby("State")
        .size()
        .reset_index(name="total")
        .query("total > @min_state_strikes")["State"]
        .tolist()
    )
    df = df[df["State"].isin(active_states)]

    # 2. разбиваем Worker_Demands
    demand_data = defaultdict(int)

    for _, row in df.iterrows():
        state = row.get("State")
        demands = row.get("Worker_Demands")

        if not state or not demands:
            continue

        parts = [p.strip() for p in demands.split("/")]

        for part in parts:
            demand_data[(state, part)] += 1

    data = [
        (state, demand, cnt)
        for (state, demand), cnt in demand_data.items()
    ]

    return pd.DataFrame(
        data,
        columns=["State", "Demand", "Number_of_Strikes"]
    )

def prepare_action_by_state_and_type(
    df,
    min_count=5
):
    # сначала считаем общее число инцидентов
    grouped = (
        df
        .groupby(["State", "Strike_or_Protest"])
        .size()
        .reset_index(name="count")
    )

    # HAVING COUNT(*) > 4
    grouped = grouped[grouped["count"] >= min_count]

    action_data = defaultdict(int)

    for _, row in grouped.iterrows():
        state = row["State"]
        action_str = row["Strike_or_Protest"]
        count = row["count"]

        if not action_str:
            continue

        parts = [p.strip() for p in action_str.split("/")]

        for part in parts:
            action_data[(state, part)] += count

    data = [
        (state, action, cnt)
        for (state, action), cnt in action_data.items()
    ]

    return pd.DataFrame(
        data,
        columns=["State", "Action", "Number_of_Strikes"]
    )

def prepare_strikes_by_size(df, state=None):
    if state:
        df = df[df["State"] == state]

    grouped = (
        df
        .groupby("Range_Number_of_Employees")
        .size()
        .reset_index(name="Number_of_Strikes")
    )

    def sort_key(label):
        try:
            return int(label.split("-")[0])
        except Exception:
            return float("inf")

    grouped = grouped.sort_values(
        by="Range_Number_of_Employees",
        key=lambda s: s.map(sort_key)
    )

    return grouped

def prepare_demands(df):
    df = df.copy()

    df["Worker_Demands"] = df["Worker_Demands"].fillna("Other")
    df["Worker_Demands"] = df["Worker_Demands"].str.split("/")

    df = df.explode("Worker_Demands")
    df["Worker_Demands"] = df["Worker_Demands"].str.strip()

    return (
        df.groupby("Worker_Demands")
          .size()
          .reset_index(name="total_strikes")
          .sort_values("total_strikes", ascending=False)
    )

def robust_zscore(series, base_value=None):
    median = series.median() if base_value is None else base_value
    mad = (series - median).abs().median()
    if mad == 0 or np.isnan(mad):
        return pd.Series(0, index=series.index)
    return (series - median) / (1.4826 * mad)


def build_strike_table(
    df_start,
    df_end,
    year_start,
    year_end,
    median_profit_base=None
):
    df_start = df_start.copy()
    df_end = df_end.copy()

    sector_mapping = None

    if year_start == 2013 and year_end == 2023:
            sector_mapping = SECTOR_MAPPING_2013_TO_2023
            
    if sector_mapping is not None:
        df_end["Sector_mapped"] = df_end["Sector"].map(sector_mapping)
        merged = df_end.merge(
            df_start,
            left_on="Sector_mapped",
            right_on="Sector",
            suffixes=(f"_{year_end}", f"_{year_start}")
        ).rename(columns={"Sector_mapped": "Sector"})
    else:
        merged = df_end.merge(
            df_start,
            on="Sector",
            suffixes=(f"_{year_end}", f"_{year_start}")
        )

    # --- базовые показатели ---
    merged["profit_per_worker"] = (
        merged[f"Total Profits_{year_end}"] /
        merged[f"Employed Persons_{year_end}"]
    )

    merged["profit_per_worker_start"] = (
        merged[f"Total Profits_{year_start}"] /
        merged[f"Employed Persons_{year_start}"]
    )

    merged["Profit per Worker growth (%)"] = (
        np.arcsinh(merged["profit_per_worker"]) -
        np.arcsinh(merged["profit_per_worker_start"])
    ) * 100

    for col in [
        "Enterprises",
        "Output Value",
        "Business Revenue",
        "Total Profits",
        "Employed Persons"
    ]:
        merged[f"{col}_pct_growth"] = (
            merged[f"{col}_{year_end}"] /
            merged[f"{col}_{year_start}"] - 1
        ) * 100

    merged["Weight"] = (
        merged[f"Total Profits_{year_end}"] /
        merged[f"Total Profits_{year_end}"].sum()
    ) * 100

    # --- композитные компоненты ---
    base_emp_growth = 64.61 if year_end == 2013 else 7.48
    base_avg_workers = 400

    merged["avg_workers_per_enterprise"] = (
        merged[f"Employed Persons_{year_end}"] * 10000 /
        merged[f"Enterprises_{year_end}"]
    )

    merged["comp_avg_workers"] = 0.20 * robust_zscore(
        merged["avg_workers_per_enterprise"],
        base_avg_workers
    )

    comp_emp = robust_zscore(
        merged["Employed Persons_pct_growth"],
        base_emp_growth
    ).clip(upper=0)

    merged["comp_emp_growth"] = 0.20 * comp_emp

    if median_profit_base is None:
        median_profit_base = merged["profit_per_worker"].median()

    merged["comp_profit_worker"] = 0.40 * robust_zscore(
        merged["profit_per_worker"],
        median_profit_base
    )

    merged["comp_profit_per_worker_growth"] = 0.20 * robust_zscore(
        merged["Profit per Worker growth (%)"],
        0.0
    )

    def penalize(x, alpha=2):
        return np.where(x >= 0, 1 + x, 1 / (1 + np.abs(x) * alpha))

    merged["strike_leverage"] = (
        penalize(merged["comp_avg_workers"]) *
        penalize(merged["comp_emp_growth"]) *
        penalize(merged["comp_profit_worker"]) *
        penalize(merged["comp_profit_per_worker_growth"])
        - 1
    )

    return merged