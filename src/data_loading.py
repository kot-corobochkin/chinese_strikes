import json
import pandas as pd
from pathlib import Path
import sys
from collections import defaultdict

def load_strikes_from_json(
    path,
    start_year=2011,
    end_year=2024,
    strike_pattern="Strike",
    debug=False
):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")

    # 🔑 КЛЮЧЕВОЙ МОМЕНТ
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 🔑 ВЫТАСКИВАЕМ СПИСОК
    df = pd.DataFrame(data["chinese_strikes"])


    # дальше всё корректно
    df["Start_Date"] = pd.to_datetime(df["Start_Date"], errors="coerce")

    filtered = df[
        (df["Start_Date"].dt.year >= start_year) &
        (df["Start_Date"].dt.year < end_year) &
        (df["Strike_or_Protest"].str.contains(strike_pattern, na=False))
    ]

    return (
        filtered
        .groupby(filtered["Start_Date"].dt.year)
        .size()
        .reset_index(name="Strike_Count")
        .rename(columns={"Start_Date": "Year"})
        .sort_values("Year")
    )

def load_action_types_from_json(
    path,
    start_year=2021,
    end_year=2024,
    state="Guangdong",
    industry="Electronics"
):

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data["chinese_strikes"])
    df["Start_Date"] = pd.to_datetime(df["Start_Date"], errors="coerce")

    filtered = df[
        (df["Start_Date"].dt.year >= start_year) &
        (df["Start_Date"].dt.year < end_year) &
        (df["State"] == state) &
        (df["subIndustry_name"] == industry)
    ]

    action_data = defaultdict(int)

    for action_str in filtered["Strike_or_Protest"].dropna():
        parts = [p.strip() for p in action_str.split("/")]
        for part in parts:
            action_data[part] += 1

    return pd.DataFrame({
        "Action": action_data.keys(),
        "Count": action_data.values()
    }).sort_values("Count", ascending=False)

def load_economic_data():
        # 规模以上工业企业主要经济指标 
    #  (единицы: профит и output — в 100 млн юаней, занятые — в 10 000 человек)

    data2002 = [
    {"Отрасль":"Coal Mining and Dressing","Профит":-0.04,"TotalOutput":3.20,"Number":18,"Workers":0.99,"год":2002},
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":65.88,"TotalOutput":252.73,"Number":2,"Workers":0.04,"год":2002},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":0.56,"TotalOutput":7.71,"Number":22,"Workers":0.51,"год":2002},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":0.84,"TotalOutput":17.07,"Number":31,"Workers":1.03,"год":2002},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":2.49,"TotalOutput":54.63,"Number":196,"Workers":3.18,"год":2002},
    {"Отрасль":"Processing of Farm and Sideline Food","Профит":10.26,"TotalOutput":503.65,"Number":611,"Workers":10.41,"год":2002},
    {"Отрасль":"Manufacture of Food","Профит":22.43,"TotalOutput":297.51,"Number":492,"Workers":10.25,"год":2002},
    {"Отрасль":"Manufacture of Beverage","Профит":19.09,"TotalOutput":240.88,"Number":210,"Workers":4.29,"год":2002},
    {"Отрасль":"Tobacco Products","Профит":17.92,"TotalOutput":119.80,"Number":19,"Workers":0.84,"год":2002},
    {"Отрасль":"Textile Industry","Профит":13.38,"TotalOutput":784.52,"Number":1444,"Workers":38.64,"год":2002},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":9.23,"TotalOutput":765.07,"Number":2069,"Workers":70.88,"год":2002},
    {"Отрасль":"Leather, Fur, Feather, Down and Related Products","Профит":8.11,"TotalOutput":508.89,"Number":1017,"Workers":54.48,"год":2002},
    {"Отрасль":"Timber Processing, Bamboo, Cane, Palm Fiber and Straw Products","Профит":3.42,"TotalOutput":134.04,"Number":293,"Workers":5.63,"год":2002},
    {"Отрасль":"Manufacture of Furniture","Профит":4.75,"TotalOutput":220.06,"Number":500,"Workers":14.94,"год":2002},
    {"Отрасль":"Papermaking and Paper Products","Профит":14.63,"TotalOutput":404.40,"Number":826,"Workers":13.29,"год":2002},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":12.60,"TotalOutput":270.00,"Number":678,"Workers":13.83,"год":2002},
    {"Отрасль":"Manufacture of Cultural, Educational and Sports Articles","Профит":10.10,"TotalOutput":333.28,"Number":622,"Workers":41.03,"год":2002},
    {"Отрасль":"Petroleum Refining, Coking and Nuclear Fuel Processing","Профит":8.73,"TotalOutput":553.03,"Number":52,"Workers":1.82,"год":2002},
    {"Отрасль":"Manufacture of Raw Chemical Materials and Chemical Products","Профит":108.55,"TotalOutput":1140.98,"Number":1310,"Workers":18.06,"год":2002},
    {"Отрасль":"Manufacture of Medicines","Профит":21.71,"TotalOutput":246.56,"Number":280,"Workers":7.39,"год":2002},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":2.31,"TotalOutput":44.26,"Number":74,"Workers":1.29,"год":2002},
    {"Отрасль":"Rubber Products","Профит":3.70,"TotalOutput":97.93,"Number":204,"Workers":5.59,"год":2002},
    {"Отрасль":"Plastic Products","Профит":23.46,"TotalOutput":802.17,"Number":1735,"Workers":39.27,"год":2002},
    {"Отрасль":"Nonmetal Mineral Products","Профит":18.79,"TotalOutput":685.14,"Number":1665,"Workers":36.20,"год":2002},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":20.80,"TotalOutput":332.26,"Number":253,"Workers":4.72,"год":2002},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":6.63,"TotalOutput":285.71,"Number":306,"Workers":5.45,"год":2002},
    {"Отрасль":"Metal Products","Профит":29.72,"TotalOutput":866.75,"Number":1870,"Workers":38.26,"год":2002},
    {"Отрасль":"Manufacture of General-purpose Machinery","Профит":12.85,"TotalOutput":312.47,"Number":708,"Workers":12.91,"год":2002},
    {"Отрасль":"Manufacture of Special-purpose Machinery","Профит":12.95,"TotalOutput":218.30,"Number":483,"Workers":10.00,"год":2002},
    {"Отрасль":"Manufacture of Transport Equipment","Профит":95.26,"TotalOutput":918.60,"Number":613,"Workers":18.47,"год":2002},
    {"Отрасль":"Manufacture of Electrical Machinery and Equipment","Профит":79.49,"TotalOutput":2160.43,"Number":2190,"Workers":78.93,"год":2002},
    {"Отрасль":"Manufacture of Communication Equipment, Computers and Other Electronic Equipment","Профит":246.51,"TotalOutput":5932.21,"Number":1768,"Workers":113.62,"год":2002},
    {"Отрасль":"Manufacture of Instruments, Meters and Machinery for Cultural and Office Use","Профит":24.28,"TotalOutput":654.31,"Number":445,"Workers":22.17,"год":2002},
    {"Отрасль":"Handicraft and Other Manufactures","Профит":8.02,"TotalOutput":295.38,"Number":722,"Workers":23.91,"год":2002},
    {"Отрасль":"Recycling and Disposal of Waste","Профит":0.19,"TotalOutput":16.69,"Number":14,"Workers":0.40,"год":2002},
    {"Отрасль":"Production and Supply of Electric Power and Heat Power","Профит":131.10,"TotalOutput":880.31,"Number":487,"Workers":13.73,"год":2002},
    {"Отрасль":"Production and Supply of Gas","Профит":-1.14,"TotalOutput":58.78,"Number":37,"Workers":0.58,"год":2002},
    {"Отрасль":"Production and Supply of Water","Профит":5.87,"TotalOutput":93.75,"Number":228,"Workers":4.14,"год":2002}
    ]

    data2004 = [
    {"Отрасль":"Coal Mining and Dressing","Профит":0.15,"TotalOutput":5.35,"Number":15,"Workers":0.95,"год":2004},
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":123.23,"TotalOutput":352.69,"Number":3,"Workers":0.15,"год":2004},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":4.75,"TotalOutput":14.26,"Number":20,"Workers":0.55,"год":2004},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":1.98,"TotalOutput":21.36,"Number":30,"Workers":0.95,"год":2004},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":2.17,"TotalOutput":61.04,"Number":184,"Workers":3.06,"год":2004},
    {"Отрасль":"Processing of Farm and Sideline Food","Профит":4.21,"TotalOutput":640.20,"Number":656,"Workers":11.15,"год":2004},
    {"Отрасль":"Manufacture of Food","Профит":27.33,"TotalOutput":343.63,"Number":506,"Workers":10.47,"год":2004},
    {"Отрасль":"Manufacture of Beverage","Профит":17.23,"TotalOutput":263.95,"Number":204,"Workers":4.28,"год":2004},
    {"Отрасль":"Tobacco Products","Профит":21.78,"TotalOutput":155.05,"Number":16,"Workers":0.84,"год":2004},
    {"Отрасль":"Textile Industry","Профит":10.61,"TotalOutput":915.78,"Number":1559,"Workers":42.04,"год":2004},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":8.32,"TotalOutput":851.85,"Number":2110,"Workers":73.63,"год":2004},
    {"Отрасль":"Leather, Fur, Feather, Down and Related Products","Профит":5.87,"TotalOutput":572.06,"Number":1049,"Workers":58.66,"год":2004},
    {"Отрасль":"Timber Processing, Bamboo, Cane, Palm Fiber and Straw Products","Профит":5.16,"TotalOutput":164.42,"Number":321,"Workers":6.21,"год":2004},
    {"Отрасль":"Manufacture of Furniture","Профит":5.78,"TotalOutput":276.59,"Number":518,"Workers":17.60,"год":2004},
    {"Отрасль":"Papermaking and Paper Products","Профит":17.73,"TotalOutput":470.98,"Number":868,"Workers":14.18,"год":2004},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":13.42,"TotalOutput":317.12,"Number":757,"Workers":15.18,"год":2004},
    {"Отрасль":"Manufacture of Cultural, Educational and Sports Articles","Профит":8.76,"TotalOutput":391.17,"Number":657,"Workers":43.62,"год":2004},
    {"Отрасль":"Petroleum Refining, Coking and Nuclear Fuel Processing","Профит":38.12,"TotalOutput":792.94,"Number":65,"Workers":2.17,"год":2004},
    {"Отрасль":"Manufacture of Raw Chemical Materials and Chemical Products","Профит":138.59,"TotalOutput":1394.43,"Number":1408,"Workers":18.43,"год":2004},
    {"Отрасль":"Manufacture of Medicines","Профит":19.69,"TotalOutput":239.10,"Number":280,"Workers":6.72,"год":2004},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":1.46,"TotalOutput":48.47,"Number":80,"Workers":1.30,"год":2004},
    {"Отрасль":"Rubber Products","Профит":3.47,"TotalOutput":113.45,"Number":219,"Workers":5.98,"год":2004},
    {"Отрасль":"Plastic Products","Профит":20.38,"TotalOutput":945.44,"Number":1853,"Workers":41.94,"год":2004},
    {"Отрасль":"Nonmetal Mineral Products","Профит":28.31,"TotalOutput":873.74,"Number":1804,"Workers":39.04,"год":2004},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":20.55,"TotalOutput":485.20,"Number":247,"Workers":4.48,"год":2004},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":8.65,"TotalOutput":402.77,"Number":336,"Workers":6.37,"год":2004},
    {"Отрасль":"Metal Products","Профит":44.09,"TotalOutput":1138.03,"Number":2024,"Workers":41.88,"год":2004},
    {"Отрасль":"Manufacture of General-purpose Machinery","Профит":22.10,"TotalOutput":447.63,"Number":783,"Workers":15.14,"год":2004},
    {"Отрасль":"Manufacture of Special-purpose Machinery","Профит":16.80,"TotalOutput":287.79,"Number":545,"Workers":11.94,"год":2004},
    {"Отрасль":"Manufacture of Transport Equipment","Профит":118.76,"TotalOutput":1189.84,"Number":642,"Workers":20.05,"год":2004},
    {"Отрасль":"Manufacture of Electrical Machinery and Equipment","Профит":77.70,"TotalOutput":2687.18,"Number":2343,"Workers":90.93,"год":2004},
    {"Отрасль":"Manufacture of Communication Equipment, Computers and Other Electronic Equipment","Профит":254.25,"TotalOutput":7465.91,"Number":1860,"Workers":136.32,"год":2004},
    {"Отрасль":"Manufacture of Instruments, Meters and Machinery for Cultural and Office Use","Профит":25.04,"TotalOutput":800.86,"Number":455,"Workers":24.78,"год":2004},
    {"Отрасль":"Handicraft and Other Manufactures","Профит":6.72,"TotalOutput":352.72,"Number":767,"Workers":24.63,"год":2004},
    {"Отрасль":"Recycling and Disposal of Waste","Профит":0.05,"TotalOutput":20.37,"Number":19,"Workers":0.40,"год":2004},
    {"Отрасль":"Production and Supply of Electric Power and Heat Power","Профит":144.01,"TotalOutput":1028.58,"Number":484,"Workers":13.39,"год":2004},
    {"Отрасль":"Production and Supply of Gas","Профит":-0.58,"TotalOutput":82.75,"Number":40,"Workers":0.56,"год":2004},
    {"Отрасль":"Production and Supply of Water","Профит":7.66,"TotalOutput":106.18,"Number":229,"Workers":4.24,"год":2004}
    ]

    data2005 = [
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":177.57,"TotalOutput":480.26,"Number":5,"Workers":0.15,"год":2005},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":6.85,"TotalOutput":27.19,"Number":35,"Workers":0.66,"год":2005},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":4.66,"TotalOutput":28.99,"Number":35,"Workers":1.02,"год":2005},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":2.12,"TotalOutput":41.26,"Number":177,"Workers":2.33,"год":2005},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":23.58,"TotalOutput":742.74,"Number":720,"Workers":11.64,"год":2005},
    {"Отрасль":"Manufacture of Food","Профит":33.94,"TotalOutput":403.10,"Number":595,"Workers":11.73,"год":2005},
    {"Отрасль":"Manufacture of Beverage","Профит":22.14,"TotalOutput":318.53,"Number":187,"Workers":4.87,"год":2005},
    {"Отрасль":"Tobacco Products","Профит":27.34,"TotalOutput":171.37,"Number":10,"Workers":0.71,"год":2005},

    {"Отрасль":"Textile Industry","Профит":22.46,"TotalOutput":1111.04,"Number":2104,"Workers":59.30,"год":2005},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":19.47,"TotalOutput":959.53,"Number":2474,"Workers":84.69,"год":2005},
    {"Отрасль":"Feather, Furs, Down and Related Products","Профит":11.67,"TotalOutput":692.22,"Number":1344,"Workers":77.81,"год":2005},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":8.13,"TotalOutput":173.12,"Number":381,"Workers":6.83,"год":2005},
    {"Отрасль":"Manufacture of Furniture","Профит":7.89,"TotalOutput":406.05,"Number":788,"Workers":25.25,"год":2005},
    {"Отрасль":"Papermaking and Paper Products","Профит":26.54,"TotalOutput":666.74,"Number":1280,"Workers":21.27,"год":2005},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":19.56,"TotalOutput":381.11,"Number":978,"Workers":18.34,"год":2005},
    {"Отрасль":"Manufacture of Cultural, Educational and Sports Goods","Профит":12.18,"TotalOutput":488.42,"Number":878,"Workers":54.08,"год":2005},

    {"Отрасль":"Petroleum Refining, Coking and Nuclear Fuel Processing","Профит":19.12,"TotalOutput":958.41,"Number":89,"Workers":2.39,"год":2005},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":159.50,"TotalOutput":1652.88,"Number":1862,"Workers":22.17,"год":2005},
    {"Отрасль":"Manufacture of Medicines","Профит":19.79,"TotalOutput":286.75,"Number":312,"Workers":7.08,"год":2005},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":2.19,"TotalOutput":79.83,"Number":94,"Workers":1.76,"год":2005},
    {"Отрасль":"Rubber Products","Профит":7.72,"TotalOutput":183.39,"Number":397,"Workers":11.32,"год":2005},
    {"Отрасль":"Plastic Products","Профит":38.61,"TotalOutput":1243.77,"Number":2660,"Workers":57.87,"год":2005},
    {"Отрасль":"Nonmetal Mineral Products","Профит":39.74,"TotalOutput":1053.53,"Number":2017,"Workers":44.23,"год":2005},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":12.72,"TotalOutput":727.11,"Number":280,"Workers":6.66,"год":2005},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":20.84,"TotalOutput":660.21,"Number":526,"Workers":9.97,"год":2005},
    {"Отрасль":"Metal Products","Профит":65.21,"TotalOutput":1467.53,"Number":2929,"Workers":60.88,"год":2005},

    {"Отрасль":"General-purpose Machinery","Профит":34.11,"TotalOutput":657.38,"Number":1203,"Workers":22.94,"год":2005},
    {"Отрасль":"Special-purpose Machinery","Профит":35.73,"TotalOutput":538.51,"Number":1060,"Workers":23.03,"год":2005},
    {"Отрасль":"Transport Equipment","Профит":128.36,"TotalOutput":1592.42,"Number":831,"Workers":24.06,"год":2005},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":111.07,"TotalOutput":3787.67,"Number":3519,"Workers":131.87,"год":2005},
    {"Отрасль":"Communication Equipment, Computers and Other Electronics","Профит":318.07,"TotalOutput":9831.34,"Number":2980,"Workers":199.23,"год":2005},
    {"Отрасль":"Instruments and Office Machinery","Профит":31.83,"TotalOutput":930.57,"Number":631,"Workers":28.65,"год":2005},
    {"Отрасль":"Handicraft and Other Manufactures","Профит":14.52,"TotalOutput":482.03,"Number":918,"Workers":30.41,"год":2005},
    {"Отрасль":"Recycling and Disposal of Waste","Профит":1.52,"TotalOutput":71.78,"Number":76,"Workers":1.02,"год":2005},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":197.30,"TotalOutput":2381.41,"Number":447,"Workers":13.53,"год":2005},
    {"Отрасль":"Gas Production and Supply","Профит":2.27,"TotalOutput":137.77,"Number":47,"Workers":0.68,"год":2005},
    {"Отрасль":"Water Production and Supply","Профит":7.59,"TotalOutput":123.60,"Number":272,"Workers":4.52,"год":2005}
    ]


    data2006 = [
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":187.65,"TotalOutput":550.45,"Number":7,"Workers":0.18,"год":2006},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":5.38,"TotalOutput":35.72,"Number":51,"Workers":0.76,"год":2006},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":8.33,"TotalOutput":42.43,"Number":43,"Workers":1.16,"год":2006},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":3.76,"TotalOutput":54.82,"Number":190,"Workers":2.15,"год":2006},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":35.51,"TotalOutput":841.71,"Number":761,"Workers":12.98,"год":2006},
    {"Отрасль":"Manufacture of Food","Профит":44.04,"TotalOutput":474.72,"Number":627,"Workers":12.46,"год":2006},
    {"Отрасль":"Manufacture of Beverage","Профит":23.38,"TotalOutput":359.32,"Number":203,"Workers":5.09,"год":2006},
    {"Отрасль":"Tobacco Products","Профит":35.38,"TotalOutput":193.38,"Number":10,"Workers":0.64,"год":2006},

    {"Отрасль":"Textile Industry","Профит":33.90,"TotalOutput":1273.16,"Number":2293,"Workers":63.45,"год":2006},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":28.88,"TotalOutput":1121.20,"Number":2593,"Workers":92.33,"год":2006},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":17.61,"TotalOutput":811.19,"Number":1368,"Workers":83.78,"год":2006},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":11.97,"TotalOutput":221.23,"Number":412,"Workers":7.34,"год":2006},
    {"Отрасль":"Manufacture of Furniture","Профит":13.19,"TotalOutput":509.44,"Number":924,"Workers":30.32,"год":2006},
    {"Отрасль":"Papermaking and Paper Products","Профит":38.74,"TotalOutput":800.19,"Number":1317,"Workers":24.20,"год":2006},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":21.36,"TotalOutput":427.55,"Number":1006,"Workers":19.25,"год":2006},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":10.72,"TotalOutput":596.29,"Number":925,"Workers":56.18,"год":2006},

    {"Отрасль":"Petroleum Refining, Coking and Nuclear Fuel Processing","Профит":-6.04,"TotalOutput":1327.61,"Number":92,"Workers":2.46,"год":2006},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":167.50,"TotalOutput":2024.07,"Number":1927,"Workers":23.63,"год":2006},
    {"Отрасль":"Manufacture of Medicines","Профит":25.82,"TotalOutput":372.09,"Number":324,"Workers":7.98,"год":2006},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":3.38,"TotalOutput":140.59,"Number":100,"Workers":2.36,"год":2006},
    {"Отрасль":"Rubber Products","Профит":7.31,"TotalOutput":225.81,"Number":429,"Workers":12.55,"год":2006},
    {"Отрасль":"Plastic Products","Профит":60.34,"TotalOutput":1565.43,"Number":2913,"Workers":63.59,"год":2006},
    {"Отрасль":"Nonmetal Mineral Products","Профит":48.16,"TotalOutput":1377.40,"Number":2144,"Workers":48.79,"год":2006},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":21.01,"TotalOutput":912.20,"Number":284,"Workers":6.92,"год":2006},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":36.81,"TotalOutput":1060.61,"Number":586,"Workers":11.53,"год":2006},
    {"Отрасль":"Metal Products","Профит":66.91,"TotalOutput":1953.85,"Number":3311,"Workers":69.53,"год":2006},

    {"Отрасль":"General-purpose Machinery","Профит":35.46,"TotalOutput":830.23,"Number":1289,"Workers":25.80,"год":2006},
    {"Отрасль":"Special-purpose Machinery","Профит":44.78,"TotalOutput":681.09,"Number":1129,"Workers":26.57,"год":2006},
    {"Отрасль":"Transport Equipment","Профит":173.12,"TotalOutput":2134.03,"Number":904,"Workers":28.30,"год":2006},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":155.47,"TotalOutput":4835.56,"Number":3785,"Workers":149.65,"год":2006},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":388.58,"TotalOutput":11891.08,"Number":3099,"Workers":225.23,"год":2006},
    {"Отрасль":"Instruments and Office Machinery","Профит":32.43,"TotalOutput":1101.19,"Number":630,"Workers":31.57,"год":2006},
    {"Отрасль":"Handicraft and Other Manufactures","Профит":22.36,"TotalOutput":593.47,"Number":985,"Workers":32.05,"год":2006},
    {"Отрасль":"Recycling and Disposal of Waste","Профит":3.41,"TotalOutput":88.07,"Number":85,"Workers":1.41,"год":2006},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":388.12,"TotalOutput":2896.27,"Number":449,"Workers":15.89,"год":2006},
    {"Отрасль":"Gas Production and Supply","Профит":-0.70,"TotalOutput":166.52,"Number":50,"Workers":0.74,"год":2006},
    {"Отрасль":"Water Production and Supply","Профит":23.68,"TotalOutput":184.79,"Number":278,"Workers":4.78,"год":2006}
    ]



    data2007 = [
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":174.28,"TotalOutput":574.70,"Number":9,"Workers":0.24,"год":2007},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":11.86,"TotalOutput":59.89,"Number":70,"Workers":1.06,"год":2007},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":18.03,"TotalOutput":75.29,"Number":50,"Workers":1.35,"год":2007},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":6.37,"TotalOutput":78.32,"Number":231,"Workers":2.53,"год":2007},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":53.86,"TotalOutput":1121.65,"Number":799,"Workers":14.02,"год":2007},
    {"Отрасль":"Manufacture of Food","Профит":55.85,"TotalOutput":592.30,"Number":656,"Workers":13.31,"год":2007},
    {"Отрасль":"Manufacture of Beverage","Профит":30.58,"TotalOutput":431.10,"Number":214,"Workers":6.03,"год":2007},
    {"Отрасль":"Tobacco Products","Профит":41.02,"TotalOutput":229.97,"Number":11,"Workers":0.64,"год":2007},

    {"Отрасль":"Textile Industry","Профит":49.30,"TotalOutput":1485.23,"Number":2494,"Workers":62.66,"год":2007},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":43.86,"TotalOutput":1390.70,"Number":2897,"Workers":100.23,"год":2007},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":27.43,"TotalOutput":978.59,"Number":1494,"Workers":84.53,"год":2007},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":19.30,"TotalOutput":311.99,"Number":503,"Workers":8.75,"год":2007},
    {"Отрасль":"Manufacture of Furniture","Профит":22.77,"TotalOutput":670.98,"Number":1090,"Workers":31.89,"год":2007},
    {"Отрасль":"Papermaking and Paper Products","Профит":42.81,"TotalOutput":998.60,"Number":1468,"Workers":24.96,"год":2007},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":26.66,"TotalOutput":519.20,"Number":1099,"Workers":21.51,"год":2007},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":22.91,"TotalOutput":736.64,"Number":1037,"Workers":56.96,"год":2007},

    {"Отрасль":"Petroleum Refining, Coking and Nuclear Fuel Processing","Профит":45.16,"TotalOutput":1621.33,"Number":95,"Workers":2.57,"год":2007},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":257.60,"TotalOutput":2578.28,"Number":2119,"Workers":27.16,"год":2007},
    {"Отрасль":"Manufacture of Medicines","Профит":37.79,"TotalOutput":432.12,"Number":334,"Workers":8.25,"год":2007},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":9.57,"TotalOutput":167.95,"Number":96,"Workers":2.12,"год":2007},
    {"Отрасль":"Rubber Products","Профит":6.93,"TotalOutput":275.38,"Number":469,"Workers":13.92,"год":2007},
    {"Отрасль":"Plastic Products","Профит":92.55,"TotalOutput":2023.69,"Number":3408,"Workers":73.32,"год":2007},
    {"Отрасль":"Nonmetal Mineral Products","Профит":101.46,"TotalOutput":1789.58,"Number":2325,"Workers":52.45,"год":2007},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":45.18,"TotalOutput":1247.01,"Number":327,"Workers":7.64,"год":2007},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":55.84,"TotalOutput":1519.55,"Number":675,"Workers":13.23,"год":2007},
    {"Отрасль":"Metal Products","Профит":102.39,"TotalOutput":2620.80,"Number":3879,"Workers":78.72,"год":2007},

    {"Отрасль":"General-purpose Machinery","Профит":54.70,"TotalOutput":1100.96,"Number":1485,"Workers":29.43,"год":2007},
    {"Отрасль":"Special-purpose Machinery","Профит":69.64,"TotalOutput":923.24,"Number":1373,"Workers":31.18,"год":2007},
    {"Отрасль":"Transport Equipment","Профит":279.65,"TotalOutput":2943.41,"Number":954,"Workers":33.09,"год":2007},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":240.84,"TotalOutput":6243.44,"Number":4344,"Workers":160.94,"год":2007},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":484.21,"TotalOutput":13377.33,"Number":3649,"Workers":253.30,"год":2007},
    {"Отрасль":"Instruments and Office Machinery","Профит":50.13,"TotalOutput":1335.60,"Number":687,"Workers":34.34,"год":2007},
    {"Отрасль":"Handicraft and Other Manufactures","Профит":26.74,"TotalOutput":841.94,"Number":1124,"Workers":32.86,"год":2007},
    {"Отрасль":"Recycling and Disposal of Waste","Профит":4.41,"TotalOutput":167.39,"Number":98,"Workers":1.66,"год":2007},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":438.04,"TotalOutput":3351.63,"Number":387,"Workers":14.92,"год":2007},
    {"Отрасль":"Gas Production and Supply","Профит":9.30,"TotalOutput":237.11,"Number":62,"Workers":0.79,"год":2007},
    {"Отрасль":"Water Production and Supply","Профит":26.63,"TotalOutput":199.88,"Number":276,"Workers":4.84,"год":2007}
    ]


    data2008 = [
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":423.31,"TotalOutput":774.29,"Number":9,"Workers":0.36,"год":2008},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":21.11,"TotalOutput":99.61,"Number":83,"Workers":1.09,"год":2008},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":17.55,"TotalOutput":92.50,"Number":59,"Workers":1.39,"год":2008},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":15.10,"TotalOutput":150.33,"Number":287,"Workers":3.20,"год":2008},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":63.18,"TotalOutput":1494.31,"Number":911,"Workers":15.94,"год":2008},
    {"Отрасль":"Manufacture of Food","Профит":73.45,"TotalOutput":746.21,"Number":788,"Workers":15.91,"год":2008},
    {"Отрасль":"Manufacture of Beverage","Профит":30.73,"TotalOutput":489.08,"Number":244,"Workers":6.89,"год":2008},
    {"Отрасль":"Tobacco Products","Профит":42.80,"TotalOutput":256.12,"Number":14,"Workers":0.69,"год":2008},

    {"Отрасль":"Textile Industry","Профит":58.04,"TotalOutput":1746.77,"Number":2965,"Workers":71.73,"год":2008},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":60.74,"TotalOutput":1725.28,"Number":3563,"Workers":111.12,"год":2008},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":39.43,"TotalOutput":1174.44,"Number":1845,"Workers":97.14,"год":2008},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":27.71,"TotalOutput":381.54,"Number":625,"Workers":10.29,"год":2008},
    {"Отрасль":"Manufacture of Furniture","Профит":29.72,"TotalOutput":831.17,"Number":1417,"Workers":36.39,"год":2008},
    {"Отрасль":"Papermaking and Paper Products","Профит":39.24,"TotalOutput":1324.35,"Number":1858,"Workers":30.09,"год":2008},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":36.86,"TotalOutput":652.62,"Number":1447,"Workers":25.17,"год":2008},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":15.33,"TotalOutput":873.38,"Number":1266,"Workers":67.25,"год":2008},

    {"Отрасль":"Petroleum Refining, Coking and Nuclear Fuel Processing","Профит":-57.82,"TotalOutput":1898.00,"Number":110,"Workers":2.66,"год":2008},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":243.02,"TotalOutput":3123.91,"Number":2669,"Workers":31.55,"год":2008},
    {"Отрасль":"Manufacture of Medicines","Профит":48.98,"TotalOutput":498.65,"Number":377,"Workers":8.87,"год":2008},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":0.66,"TotalOutput":154.36,"Number":92,"Workers":2.00,"год":2008},
    {"Отрасль":"Rubber Products","Профит":7.93,"TotalOutput":323.63,"Number":605,"Workers":15.37,"год":2008},
    {"Отрасль":"Plastic Products","Профит":101.35,"TotalOutput":2423.13,"Number":4244,"Workers":89.37,"год":2008},
    {"Отрасль":"Nonmetal Mineral Products","Профит":130.89,"TotalOutput":2220.60,"Number":2692,"Workers":56.04,"год":2008},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":1.56,"TotalOutput":1493.45,"Number":404,"Workers":8.62,"год":2008},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":66.50,"TotalOutput":1817.14,"Number":761,"Workers":15.56,"год":2008},
    {"Отрасль":"Metal Products","Профит":133.91,"TotalOutput":3095.34,"Number":4764,"Workers":87.86,"год":2008},

    {"Отрасль":"General-purpose Machinery","Профит":80.87,"TotalOutput":1530.32,"Number":1952,"Workers":34.75,"год":2008},
    {"Отрасль":"Special-purpose Machinery","Профит":78.75,"TotalOutput":1151.11,"Number":1888,"Workers":39.73,"год":2008},
    {"Отрасль":"Transport Equipment","Профит":310.42,"TotalOutput":3453.17,"Number":1285,"Workers":40.79,"год":2008},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":313.38,"TotalOutput":7145.19,"Number":5469,"Workers":178.99,"год":2008},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":435.59,"TotalOutput":15373.81,"Number":4819,"Workers":286.72,"год":2008},
    {"Отрасль":"Instruments and Office Machinery","Профит":51.28,"TotalOutput":1351.58,"Number":770,"Workers":35.41,"год":2008},
    {"Отрасль":"Handicraft and Other Manufactures","Профит":49.98,"TotalOutput":1066.65,"Number":1332,"Workers":37.57,"год":2008},
    {"Отрасль":"Recycling and Disposal of Waste","Профит":8.02,"TotalOutput":333.71,"Number":172,"Workers":2.78,"год":2008},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":232.12,"TotalOutput":3653.41,"Number":434,"Workers":17.99,"год":2008},
    {"Отрасль":"Gas Production and Supply","Профит":14.40,"TotalOutput":292.42,"Number":79,"Workers":0.96,"год":2008},
    {"Отрасль":"Water Production and Supply","Профит":26.51,"TotalOutput":213.04,"Number":304,"Workers":5.14,"год":2008}
    ]


    data2009 = [
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":231.23,"TotalOutput":512.14,"Number":10,"Workers":0.41,"год":2009},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":9.90,"TotalOutput":104.51,"Number":80,"Workers":1.04,"год":2009},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":17.93,"TotalOutput":95.82,"Number":52,"Workers":1.32,"год":2009},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":15.73,"TotalOutput":197.47,"Number":306,"Workers":3.48,"год":2009},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":78.03,"TotalOutput":1517.37,"Number":959,"Workers":15.51,"год":2009},
    {"Отрасль":"Manufacture of Food","Профит":106.46,"TotalOutput":895.74,"Number":851,"Workers":16.29,"год":2009},
    {"Отрасль":"Manufacture of Beverage","Профит":38.24,"TotalOutput":603.86,"Number":277,"Workers":7.29,"год":2009},
    {"Отрасль":"Tobacco Products","Профит":48.52,"TotalOutput":289.57,"Number":15,"Workers":0.80,"год":2009},

    {"Отрасль":"Textile Industry","Профит":83.29,"TotalOutput":1929.22,"Number":2889,"Workers":67.20,"год":2009},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":77.86,"TotalOutput":1937.25,"Number":3530,"Workers":109.29,"год":2009},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":54.76,"TotalOutput":1227.27,"Number":1769,"Workers":86.51,"год":2009},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":26.07,"TotalOutput":391.44,"Number":634,"Workers":9.55,"год":2009},
    {"Отрасль":"Manufacture of Furniture","Профит":40.04,"TotalOutput":872.26,"Number":1409,"Workers":32.46,"год":2009},
    {"Отрасль":"Papermaking and Paper Products","Профит":54.39,"TotalOutput":1249.49,"Number":1770,"Workers":27.27,"год":2009},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":45.12,"TotalOutput":726.03,"Number":1457,"Workers":23.69,"год":2009},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":26.29,"TotalOutput":894.47,"Number":1236,"Workers":60.60,"год":2009},

    {"Отрасль":"Petroleum Refining, Coking and Nuclear Fuel Processing","Профит":118.76,"TotalOutput":1899.53,"Number":107,"Workers":2.38,"год":2009},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":314.68,"TotalOutput":3209.18,"Number":2658,"Workers":31.66,"год":2009},
    {"Отрасль":"Manufacture of Medicines","Профит":72.23,"TotalOutput":618.00,"Number":396,"Workers":9.94,"год":2009},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":4.95,"TotalOutput":136.46,"Number":83,"Workers":1.80,"год":2009},
    {"Отрасль":"Rubber Products","Профит":15.81,"TotalOutput":362.46,"Number":601,"Workers":14.59,"год":2009},
    {"Отрасль":"Plastic Products","Профит":124.61,"TotalOutput":2640.21,"Number":4359,"Workers":88.63,"год":2009},
    {"Отрасль":"Nonmetal Mineral Products","Профит":146.38,"TotalOutput":2334.60,"Number":2666,"Workers":53.32,"год":2009},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":44.79,"TotalOutput":1419.46,"Number":436,"Workers":8.02,"год":2009},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":92.54,"TotalOutput":1827.56,"Number":687,"Workers":14.11,"год":2009},
    {"Отрасль":"Metal Products","Профит":158.59,"TotalOutput":3256.46,"Number":4781,"Workers":82.75,"год":2009},

    {"Отрасль":"General-purpose Machinery","Профит":87.05,"TotalOutput":1557.54,"Number":1912,"Workers":33.30,"год":2009},
    {"Отрасль":"Special-purpose Machinery","Профит":84.07,"TotalOutput":1197.27,"Number":1878,"Workers":36.71,"год":2009},
    {"Отрасль":"Transport Equipment","Профит":401.31,"TotalOutput":4156.18,"Number":1267,"Workers":40.87,"год":2009},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":396.92,"TotalOutput":7365.41,"Number":5441,"Workers":174.38,"год":2009},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":717.23,"TotalOutput":15721.79,"Number":4645,"Workers":284.68,"год":2009},
    {"Отрасль":"Instruments and Office Machinery","Профит":64.24,"TotalOutput":1179.72,"Number":773,"Workers":32.98,"год":2009},
    {"Отрасль":"Handicraft and Other Manufactures","Профит":44.72,"TotalOutput":1084.81,"Number":1275,"Workers":34.12,"год":2009},
    {"Отрасль":"Recycling and Disposal of Waste","Профит":20.51,"TotalOutput":450.19,"Number":213,"Workers":2.82,"год":2009},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":298.38,"TotalOutput":3869.19,"Number":406,"Workers":19.85,"год":2009},
    {"Отрасль":"Gas Production and Supply","Профит":27.48,"TotalOutput":323.05,"Number":81,"Workers":1.05,"год":2009},
    {"Отрасль":"Water Production and Supply","Профит":15.30,"TotalOutput":222.78,"Number":308,"Workers":5.36,"год":2009}
    ]


    data2010 = [
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":364.74,"TotalOutput":599.90,"Number":10,"Workers":0.50,"год":2010},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":29.00,"TotalOutput":180.94,"Number":88,"Workers":1.22,"год":2010},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":29.98,"TotalOutput":125.15,"Number":52,"Workers":1.31,"год":2010},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":31.53,"TotalOutput":278.79,"Number":334,"Workers":3.34,"год":2010},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":115.08,"TotalOutput":1810.48,"Number":993,"Workers":16.86,"год":2010},
    {"Отрасль":"Manufacture of Food","Профит":136.65,"TotalOutput":1123.68,"Number":882,"Workers":17.20,"год":2010},
    {"Отрасль":"Manufacture of Beverage","Профит":40.77,"TotalOutput":649.57,"Number":294,"Workers":7.28,"год":2010},
    {"Отрасль":"Tobacco Products","Профит":47.21,"TotalOutput":321.84,"Number":15,"Workers":0.82,"год":2010},

    {"Отрасль":"Textile Industry","Профит":140.75,"TotalOutput":2632.69,"Number":3089,"Workers":81.18,"год":2010},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":124.88,"TotalOutput":2304.28,"Number":3572,"Workers":105.82,"год":2010},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":83.56,"TotalOutput":1543.69,"Number":1737,"Workers":91.56,"год":2010},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":42.26,"TotalOutput":540.17,"Number":689,"Workers":10.94,"год":2010},
    {"Отрасль":"Manufacture of Furniture","Профит":64.80,"TotalOutput":1098.51,"Number":1463,"Workers":36.66,"год":2010},
    {"Отрасль":"Papermaking and Paper Products","Профит":98.13,"TotalOutput":1656.31,"Number":1829,"Workers":30.13,"год":2010},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":65.47,"TotalOutput":837.56,"Number":1472,"Workers":24.39,"год":2010},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":47.34,"TotalOutput":1080.84,"Number":1237,"Workers":63.43,"год":2010},

    {"Отрасль":"Petroleum Refining, Coking and Nuclear Fuel Processing","Профит":132.63,"TotalOutput":2758.97,"Number":111,"Workers":2.56,"год":2010},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":409.19,"TotalOutput":4094.04,"Number":2740,"Workers":35.84,"год":2010},
    {"Отрасль":"Manufacture of Medicines","Профит":102.28,"TotalOutput":800.49,"Number":412,"Workers":10.56,"год":2010},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":11.89,"TotalOutput":188.20,"Number":87,"Workers":1.95,"год":2010},
    {"Отрасль":"Rubber Products","Профит":22.55,"TotalOutput":423.81,"Number":572,"Workers":13.94,"год":2010},
    {"Отрасль":"Plastic Products","Профит":201.77,"TotalOutput":3310.21,"Number":4577,"Workers":95.44,"год":2010},
    {"Отрасль":"Nonmetal Mineral Products","Профит":251.09,"TotalOutput":3055.65,"Number":2833,"Workers":59.06,"год":2010},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":89.29,"TotalOutput":1969.47,"Number":495,"Workers":9.08,"год":2010},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":136.02,"TotalOutput":2310.60,"Number":696,"Workers":15.71,"год":2010},
    {"Отрасль":"Metal Products","Профит":277.43,"TotalOutput":4092.78,"Number":4844,"Workers":89.62,"год":2010},

    {"Отрасль":"General-purpose Machinery","Профит":135.63,"TotalOutput":1906.68,"Number":1954,"Workers":37.36,"год":2010},
    {"Отрасль":"Special-purpose Machinery","Профит":117.14,"TotalOutput":1468.56,"Number":1834,"Workers":37.41,"год":2010},
    {"Отрасль":"Transport Equipment","Профит":587.35,"TotalOutput":5181.63,"Number":1262,"Workers":46.42,"год":2010},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":585.99,"TotalOutput":9353.08,"Number":5388,"Workers":194.20,"год":2010},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":1039.83,"TotalOutput":19228.34,"Number":4808,"Workers":324.46,"год":2010},
    {"Отрасль":"Instruments and Office Machinery","Профит":89.23,"TotalOutput":1400.85,"Number":745,"Workers":35.92,"год":2010},
    {"Отрасль":"Handicraft and Other Manufactures","Профит":80.82,"TotalOutput":1500.40,"Number":1230,"Workers":34.44,"год":2010},
    {"Отрасль":"Recycling and Disposal of Waste","Профит":36.73,"TotalOutput":860.75,"Number":242,"Workers":3.47,"год":2010},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":395.42,"TotalOutput":4466.71,"Number":432,"Workers":21.29,"год":2010},
    {"Отрасль":"Gas Production and Supply","Профит":50.65,"TotalOutput":422.92,"Number":85,"Workers":1.06,"год":2010},
    {"Отрасль":"Water Production and Supply","Профит":24.57,"TotalOutput":246.11,"Number":315,"Workers":5.56,"год":2010}
    ]


    data2011 = [
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":380.90,"TotalOutput":697.15,"Number":3,"Workers":0.16,"год":2011},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":35.96,"TotalOutput":239.36,"Number":73,"Workers":1.13,"год":2011},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":45.80,"TotalOutput":180.54,"Number":49,"Workers":1.01,"год":2011},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":31.14,"TotalOutput":305.37,"Number":238,"Workers":3.05,"год":2011},
    {"Отрасль":"Auxiliary Mining Operations","Профит":4.93,"TotalOutput":22.31,"Number":5,"Workers":0.13,"год":2011},
    {"Отрасль":"Mining and Dressing of Other Ores","Профит":0.04,"TotalOutput":0.39,"Number":1,"Workers":0.01,"год":2011},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":113.84,"TotalOutput":2252.00,"Number":792,"Workers":15.66,"год":2011},
    {"Отрасль":"Manufacture of Food","Профит":155.45,"TotalOutput":1287.65,"Number":574,"Workers":17.10,"год":2011},
    {"Отрасль":"Manufacture of Beverage","Профит":45.25,"TotalOutput":849.41,"Number":200,"Workers":7.75,"год":2011},
    {"Отрасль":"Tobacco Products","Профит":44.47,"TotalOutput":364.03,"Number":14,"Workers":0.82,"год":2011},

    {"Отрасль":"Textile Industry","Профит":127.48,"TotalOutput":2325.59,"Number":1810,"Workers":51.37,"год":2011},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":165.50,"TotalOutput":2901.79,"Number":2856,"Workers":104.97,"год":2011},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":99.05,"TotalOutput":1822.84,"Number":1514,"Workers":91.87,"год":2011},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":53.45,"TotalOutput":591.80,"Number":489,"Workers":9.55,"год":2011},
    {"Отрасль":"Manufacture of Furniture","Профит":71.01,"TotalOutput":1174.91,"Number":1086,"Workers":32.58,"год":2011},
    {"Отрасль":"Papermaking and Paper Products","Профит":72.71,"TotalOutput":1701.89,"Number":1196,"Workers":25.89,"год":2011},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":68.57,"TotalOutput":853.30,"Number":829,"Workers":20.44,"год":2011},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":126.64,"TotalOutput":2948.57,"Number":1509,"Workers":80.61,"год":2011},

    {"Отрасль":"Petroleum Refining, Coking and Nuclear Fuel Processing","Профит":24.32,"TotalOutput":3248.62,"Number":102,"Workers":2.79,"год":2011},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":394.90,"TotalOutput":4966.43,"Number":2046,"Workers":32.39,"год":2011},
    {"Отрасль":"Manufacture of Medicines","Профит":108.50,"TotalOutput":920.62,"Number":329,"Workers":10.27,"год":2011},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":8.40,"TotalOutput":175.42,"Number":61,"Workers":1.67,"год":2011},
    {"Отрасль":"Plastic Products","Профит":191.10,"TotalOutput":3558.22,"Number":3143,"Workers":83.44,"год":2011},
    {"Отрасль":"Nonmetal Mineral Products","Профит":248.18,"TotalOutput":3238.25,"Number":2113,"Workers":56.81,"год":2011},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":78.72,"TotalOutput":2557.69,"Number":593,"Workers":12.86,"год":2011},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":141.08,"TotalOutput":2518.95,"Number":654,"Workers":15.94,"год":2011},
    {"Отрасль":"Metal Products","Профит":285.64,"TotalOutput":4311.47,"Number":3289,"Workers":76.87,"год":2011},

    {"Отрасль":"General-purpose Machinery","Профит":153.05,"TotalOutput":2866.20,"Number":1315,"Workers":46.78,"год":2011},
    {"Отрасль":"Special-purpose Machinery","Профит":121.09,"TotalOutput":1606.13,"Number":1198,"Workers":33.32,"год":2011},
    {"Отрасль":"Automobile Manufacturing","Профит":505.65,"TotalOutput":4077.34,"Number":535,"Workers":29.81,"год":2011},
    {"Отрасль":"Railway/Ship/Aeronautics & Other Transport Equipment","Профит":77.16,"TotalOutput":1354.97,"Number":426,"Workers":17.30,"год":2011},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":583.48,"TotalOutput":10060.94,"Number":3934,"Workers":187.64,"год":2011},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":808.81,"TotalOutput":21460.03,"Number":3876,"Workers":330.93,"год":2011},
    {"Отрасль":"Instruments and Meters","Профит":45.25,"TotalOutput":568.81,"Number":390,"Workers":20.18,"год":2011},
    {"Отрасль":"Other Manufactures","Профит":11.81,"TotalOutput":240.76,"Number":232,"Workers":7.23,"год":2011},
    {"Отрасль":"Comprehensive Utilization of Waste","Профит":65.84,"TotalOutput":773.00,"Number":211,"Workers":4.24,"год":2011},
    {"Отрасль":"Metal Products/Machinery/Equipment Maintenance","Профит":5.48,"TotalOutput":113.29,"Number":55,"Workers":2.23,"год":2011},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":309.62,"TotalOutput":4904.00,"Number":284,"Workers":21.23,"год":2011},
    {"Отрасль":"Gas Production and Supply","Профит":44.94,"TotalOutput":582.32,"Number":73,"Workers":1.16,"год":2011},
    {"Отрасль":"Water Production and Supply","Профит":18.85,"TotalOutput":249.32,"Number":207,"Workers":4.65,"год":2011}
    ]


    data2012 = [
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":253.53,"TotalOutput":642.65,"Number":3,"Workers":0.31,"год":2012},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":15.45,"TotalOutput":154.20,"Number":59,"Workers":1.06,"год":2012},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":17.28,"TotalOutput":126.70,"Number":39,"Workers":0.91,"год":2012},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":22.39,"TotalOutput":232.15,"Number":208,"Workers":2.62,"год":2012},
    {"Отрасль":"Auxiliary Mining Operations","Профит":7.28,"TotalOutput":29.29,"Number":7,"Workers":0.14,"год":2012},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":121.74,"TotalOutput":2388.08,"Number":822,"Workers":16.49,"год":2012},
    {"Отрасль":"Manufacture of Food","Профит":206.37,"TotalOutput":1399.28,"Number":596,"Workers":17.70,"год":2012},
    {"Отрасль":"Manufacture of Wine, Beverage and Refined Tea","Профит":39.72,"TotalOutput":842.47,"Number":214,"Workers":7.97,"год":2012},
    {"Отрасль":"Tobacco Products","Профит":43.19,"TotalOutput":379.64,"Number":11,"Workers":0.80,"год":2012},

    {"Отрасль":"Textile Industry","Профит":117.90,"TotalOutput":2132.53,"Number":1673,"Workers":45.70,"год":2012},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":157.60,"TotalOutput":2995.82,"Number":2881,"Workers":101.77,"год":2012},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":81.49,"TotalOutput":1769.94,"Number":1529,"Workers":83.90,"год":2012},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":36.98,"TotalOutput":512.55,"Number":491,"Workers":8.66,"год":2012},
    {"Отрасль":"Manufacture of Furniture","Профит":68.59,"TotalOutput":1227.16,"Number":1070,"Workers":32.37,"год":2012},
    {"Отрасль":"Papermaking and Paper Products","Профит":68.73,"TotalOutput":1643.64,"Number":1152,"Workers":25.57,"год":2012},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":64.42,"TotalOutput":843.90,"Number":794,"Workers":20.95,"год":2012},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":125.50,"TotalOutput":3257.12,"Number":1450,"Workers":79.78,"год":2012},

    {"Отрасль":"Petroleum Refining, Coking and Nuclear Fuel Processing","Профит":38.94,"TotalOutput":3405.98,"Number":94,"Workers":2.72,"год":2012},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":382.92,"TotalOutput":4731.53,"Number":2003,"Workers":33.60,"год":2012},
    {"Отрасль":"Manufacture of Medicines","Профит":134.82,"TotalOutput":1027.73,"Number":352,"Workers":11.59,"год":2012},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":7.57,"TotalOutput":126.34,"Number":58,"Workers":1.50,"год":2012},
    {"Отрасль":"Rubber and Plastic Products","Профит":184.46,"TotalOutput":3590.79,"Number":3079,"Workers":83.22,"год":2012},
    {"Отрасль":"Nonmetal Mineral Products","Профит":194.07,"TotalOutput":3221.58,"Number":2146,"Workers":57.05,"год":2012},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":51.52,"TotalOutput":2265.41,"Number":518,"Workers":12.56,"год":2012},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":100.64,"TotalOutput":2365.70,"Number":651,"Workers":16.63,"год":2012},
    {"Отрасль":"Metal Products","Профит":267.24,"TotalOutput":4114.55,"Number":3032,"Workers":76.85,"год":2012},

    {"Отрасль":"General-purpose Machinery","Профит":153.46,"TotalOutput":2901.96,"Number":1309,"Workers":44.01,"год":2012},
    {"Отрасль":"Special-purpose Machinery","Профит":133.05,"TotalOutput":1638.58,"Number":1194,"Workers":32.95,"год":2012},
    {"Отрасль":"Automobile Manufacturing","Профит":366.93,"TotalOutput":3845.06,"Number":564,"Workers":31.58,"год":2012},
    {"Отрасль":"Railway/Ship/Aeronautics & Other Transport Equipment","Профит":22.02,"TotalOutput":1185.15,"Number":404,"Workers":16.09,"год":2012},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":566.23,"TotalOutput":9623.39,"Number":3928,"Workers":186.95,"год":2012},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":865.45,"TotalOutput":22865.39,"Number":4035,"Workers":337.65,"год":2012},
    {"Отрасль":"Instruments and Meters","Профит":47.43,"TotalOutput":617.70,"Number":397,"Workers":21.03,"год":2012},
    {"Отрасль":"Other Manufactures","Профит":10.57,"TotalOutput":212.38,"Number":214,"Workers":6.67,"год":2012},
    {"Отрасль":"Comprehensive Utilization of Waste","Профит":69.26,"TotalOutput":844.87,"Number":210,"Workers":3.93,"год":2012},
    {"Отрасль":"Metal Products/Machinery/Equipment Maintenance","Профит":3.74,"TotalOutput":90.07,"Number":44,"Workers":1.71,"год":2012},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":349.73,"TotalOutput":5520.78,"Number":289,"Workers":20.96,"год":2012},
    {"Отрасль":"Gas Production and Supply","Профит":46.78,"TotalOutput":553.03,"Number":71,"Workers":1.32,"год":2012},
    {"Отрасль":"Water Production and Supply","Профит":19.93,"TotalOutput":277.01,"Number":220,"Workers":4.87,"год":2012}
    ]


    data2013 = [
    {"Отрасль":"Mining and Washing of Coal","Профит":0.20,"TotalOutput":3.28,"Number":1,"Workers":0.02,"год":2013},
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":215.49,"TotalOutput":631.09,"Number":3,"Workers":0.44,"год":2013},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":26.69,"TotalOutput":174.52,"Number":61,"Workers":0.99,"год":2013},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":16.04,"TotalOutput":137.97,"Number":38,"Workers":0.89,"год":2013},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":24.80,"TotalOutput":274.42,"Number":219,"Workers":2.46,"год":2013},
    {"Отрасль":"Auxiliary Mining Operations","Профит":8.50,"TotalOutput":38.36,"Number":6,"Workers":0.14,"год":2013},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":134.12,"TotalOutput":2835.51,"Number":906,"Workers":17.21,"год":2013},
    {"Отрасль":"Manufacture of Food","Профит":238.75,"TotalOutput":1644.03,"Number":646,"Workers":19.91,"год":2013},
    {"Отрасль":"Manufacture of Wine, Beverage and Refined Tea","Профит":73.81,"TotalOutput":992.72,"Number":249,"Workers":8.66,"год":2013},
    {"Отрасль":"Tobacco Products","Профит":45.65,"TotalOutput":423.20,"Number":11,"Workers":0.82,"год":2013},

    {"Отрасль":"Textile Industry","Профит":140.31,"TotalOutput":2456.08,"Number":1643,"Workers":43.76,"год":2013},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":186.84,"TotalOutput":3478.72,"Number":3077,"Workers":100.92,"год":2013},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":83.23,"TotalOutput":2051.12,"Number":1773,"Workers":82.96,"год":2013},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":50.87,"TotalOutput":636.41,"Number":540,"Workers":8.91,"год":2013},
    {"Отрасль":"Manufacture of Furniture","Профит":74.07,"TotalOutput":1516.78,"Number":1205,"Workers":34.15,"год":2013},
    {"Отрасль":"Papermaking and Paper Products","Профит":70.05,"TotalOutput":1734.25,"Number":1148,"Workers":23.43,"год":2013},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":70.32,"TotalOutput":1074.69,"Number":892,"Workers":24.14,"год":2013},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":112.83,"TotalOutput":3752.54,"Number":1601,"Workers":82.45,"год":2013},

    {"Отрасль":"Petroleum Refining, Coking and Nuclear Fuel Processing","Профит":83.75,"TotalOutput":3652.02,"Number":92,"Workers":2.61,"год":2013},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":401.07,"TotalOutput":5461.28,"Number":2163,"Workers":34.33,"год":2013},
    {"Отрасль":"Manufacture of Medicines","Профит":150.13,"TotalOutput":1222.46,"Number":382,"Workers":11.81,"год":2013},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":9.62,"TotalOutput":134.90,"Number":61,"Workers":1.43,"год":2013},
    {"Отрасль":"Rubber and Plastic Products","Профит":215.33,"TotalOutput":4207.98,"Number":3328,"Workers":85.46,"год":2013},
    {"Отрасль":"Nonmetal Mineral Products","Профит":270.44,"TotalOutput":4033.36,"Number":2448,"Workers":59.16,"год":2013},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":104.67,"TotalOutput":2587.43,"Number":534,"Workers":11.71,"год":2013},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":99.07,"TotalOutput":3023.90,"Number":660,"Workers":16.30,"год":2013},
    {"Отрасль":"Metal Products","Профит":311.66,"TotalOutput":4918.96,"Number":3320,"Workers":80.05,"год":2013},

    {"Отрасль":"General-purpose Machinery","Профит":177.35,"TotalOutput":3237.58,"Number":1467,"Workers":46.38,"год":2013},
    {"Отрасль":"Special-purpose Machinery","Профит":137.73,"TotalOutput":1856.66,"Number":1319,"Workers":33.92,"год":2013},
    {"Отрасль":"Automobile Manufacturing","Профит":433.17,"TotalOutput":4707.60,"Number":620,"Workers":32.57,"год":2013},
    {"Отрасль":"Railway/Ship/Aeronautics & Other Transport Equipment","Профит":41.81,"TotalOutput":1224.23,"Number":422,"Workers":15.74,"год":2013},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":657.85,"TotalOutput":10895.32,"Number":4153,"Workers":180.15,"год":2013},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":1105.92,"TotalOutput":25835.51,"Number":4621,"Workers":330.90,"год":2013},
    {"Отрасль":"Instruments and Meters","Профит":53.48,"TotalOutput":762.25,"Number":453,"Workers":22.37,"год":2013},
    {"Отрасль":"Other Manufactures","Профит":7.59,"TotalOutput":220.00,"Number":228,"Workers":5.93,"год":2013},
    {"Отрасль":"Comprehensive Utilization of Waste","Профит":80.87,"TotalOutput":954.71,"Number":255,"Workers":4.19,"год":2013},
    {"Отрасль":"Metal Products/Machinery/Equipment Maintenance","Профит":5.54,"TotalOutput":91.37,"Number":44,"Workers":1.10,"год":2013},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":490.22,"TotalOutput":5862.80,"Number":308,"Workers":21.13,"год":2013},
    {"Отрасль":"Gas Production and Supply","Профит":50.70,"TotalOutput":615.19,"Number":77,"Workers":1.40,"год":2013},
    {"Отрасль":"Water Production and Supply","Профит":35.88,"TotalOutput":311.87,"Number":231,"Workers":4.95,"год":2013}
    ]


    data2014 = [
    {"Отрасль":"Mining and Washing of Coal","Профит":0.03,"TotalOutput":5.22,"Number":1,"Workers":0.01,"год":2014},
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":225.18,"TotalOutput":637.26,"Number":3,"Workers":0.53,"год":2014},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":19.17,"TotalOutput":175.07,"Number":54,"Workers":0.95,"год":2014},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":13.88,"TotalOutput":131.37,"Number":35,"Workers":0.79,"год":2014},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":24.88,"TotalOutput":322.75,"Number":239,"Workers":2.65,"год":2014},
    {"Отрасль":"Auxiliary Mining Operations","Профит":8.81,"TotalOutput":46.40,"Number":5,"Workers":0.12,"год":2014},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":121.79,"TotalOutput":3000.43,"Number":904,"Workers":16.84,"год":2014},
    {"Отрасль":"Manufacture of Food","Профит":226.31,"TotalOutput":1667.60,"Number":679,"Workers":19.13,"год":2014},
    {"Отрасль":"Manufacture of Wine, Beverage and Refined Tea","Профит":85.67,"TotalOutput":1090.80,"Number":252,"Workers":9.48,"год":2014},
    {"Отрасль":"Tobacco Products","Профит":46.34,"TotalOutput":458.81,"Number":11,"Workers":0.78,"год":2014},

    {"Отрасль":"Textile Industry","Профит":132.51,"TotalOutput":2530.59,"Number":1574,"Workers":39.25,"год":2014},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":184.98,"TotalOutput":3791.61,"Number":2977,"Workers":101.52,"год":2014},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":95.29,"TotalOutput":2279.49,"Number":1751,"Workers":77.24,"год":2014},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":52.80,"TotalOutput":736.35,"Number":515,"Workers":8.79,"год":2014},
    {"Отрасль":"Manufacture of Furniture","Профит":88.61,"TotalOutput":1709.17,"Number":1206,"Workers":34.37,"год":2014},
    {"Отрасль":"Papermaking and Paper Products","Профит":75.52,"TotalOutput":1880.92,"Number":1056,"Workers":22.70,"год":2014},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":85.20,"TotalOutput":1190.99,"Number":866,"Workers":24.09,"год":2014},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":128.61,"TotalOutput":4289.16,"Number":1590,"Workers":79.18,"год":2014},

    {"Отрасль":"Petroleum Refining, Coking and Nuclear Fuel Processing","Профит":48.68,"TotalOutput":3224.66,"Number":80,"Workers":2.74,"год":2014},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":419.37,"TotalOutput":6127.36,"Number":2141,"Workers":34.16,"год":2014},
    {"Отрасль":"Manufacture of Medicines","Профит":145.76,"TotalOutput":1368.06,"Number":385,"Workers":12.21,"год":2014},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":10.03,"TotalOutput":136.26,"Number":62,"Workers":1.53,"год":2014},
    {"Отрасль":"Rubber and Plastic Products","Профит":226.72,"TotalOutput":4582.36,"Number":3299,"Workers":84.70,"год":2014},
    {"Отрасль":"Nonmetal Mineral Products","Профит":319.48,"TotalOutput":4753.43,"Number":2642,"Workers":61.15,"год":2014},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":72.54,"TotalOutput":2524.52,"Number":493,"Workers":11.35,"год":2014},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":117.48,"TotalOutput":3266.23,"Number":651,"Workers":15.70,"год":2014},
    {"Отрасль":"Metal Products","Профит":314.29,"TotalOutput":5482.46,"Number":3270,"Workers":80.56,"год":2014},

    {"Отрасль":"General-purpose Machinery","Профит":214.80,"TotalOutput":3519.21,"Number":1515,"Workers":47.82,"год":2014},
    {"Отрасль":"Special-purpose Machinery","Профит":169.16,"TotalOutput":2170.60,"Number":1349,"Workers":36.51,"год":2014},
    {"Отрасль":"Automobile Manufacturing","Профит":479.55,"TotalOutput":5485.91,"Number":676,"Workers":36.42,"год":2014},
    {"Отрасль":"Railway/Ship/Aeronautics & Other Transport Equipment","Профит":42.95,"TotalOutput":1186.89,"Number":405,"Workers":14.90,"год":2014},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":762.02,"TotalOutput":12024.40,"Number":4116,"Workers":179.92,"год":2014},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":1272.15,"TotalOutput":28254.95,"Number":4671,"Workers":337.19,"год":2014},
    {"Отрасль":"Instruments and Meters","Профит":56.64,"TotalOutput":821.63,"Number":459,"Workers":21.88,"год":2014},
    {"Отрасль":"Other Manufactures","Профит":10.23,"TotalOutput":235.78,"Number":234,"Workers":6.30,"год":2014},
    {"Отрасль":"Comprehensive Utilization of Waste","Профит":100.73,"TotalOutput":1072.04,"Number":280,"Workers":4.36,"год":2014},
    {"Отрасль":"Metal Products/Machinery/Equipment Maintenance","Профит":4.68,"TotalOutput":100.20,"Number":47,"Workers":1.18,"год":2014},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":511.19,"TotalOutput":6357.18,"Number":329,"Workers":20.24,"год":2014},
    {"Отрасль":"Gas Production and Supply","Профит":54.75,"TotalOutput":729.08,"Number":93,"Workers":1.48,"год":2014},
    {"Отрасль":"Water Production and Supply","Профит":46.21,"TotalOutput":345.84,"Number":239,"Workers":5.08,"год":2014}
    ]


    data2015 = [
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":124.53,"TotalOutput":521.71,"Number":4,"Workers":0.57,"год":2015},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":10.53,"TotalOutput":127.53,"Number":54,"Workers":0.82,"год":2015},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":7.00,"TotalOutput":74.72,"Number":34,"Workers":0.79,"год":2015},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":33.39,"TotalOutput":385.54,"Number":267,"Workers":2.85,"год":2015},
    {"Отрасль":"Auxiliary Mining Operations","Профит":5.05,"TotalOutput":27.51,"Number":5,"Workers":0.24,"год":2015},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":136.41,"TotalOutput":3130.38,"Number":936,"Workers":17.00,"год":2015},
    {"Отрасль":"Manufacture of Food","Профит":233.69,"TotalOutput":1805.54,"Number":705,"Workers":19.16,"год":2015},
    {"Отрасль":"Manufacture of Wine, Beverage and Refined Tea","Профит":92.04,"TotalOutput":1146.10,"Number":259,"Workers":9.71,"год":2015},
    {"Отрасль":"Tobacco Products","Профит":46.59,"TotalOutput":460.90,"Number":11,"Workers":0.78,"год":2015},

    {"Отрасль":"Textile Industry","Профит":135.84,"TotalOutput":2639.51,"Number":1503,"Workers":37.96,"год":2015},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":171.61,"TotalOutput":4073.91,"Number":2925,"Workers":96.14,"год":2015},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":97.62,"TotalOutput":2460.87,"Number":1843,"Workers":72.75,"год":2015},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":57.02,"TotalOutput":841.51,"Number":548,"Workers":8.87,"год":2015},
    {"Отрасль":"Manufacture of Furniture","Профит":94.56,"TotalOutput":1873.33,"Number":1257,"Workers":34.32,"год":2015},
    {"Отрасль":"Papermaking and Paper Products","Профит":92.23,"TotalOutput":2013.29,"Number":1058,"Workers":23.13,"год":2015},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":84.07,"TotalOutput":1218.89,"Number":840,"Workers":23.09,"год":2015},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":131.99,"TotalOutput":3934.30,"Number":1598,"Workers":78.25,"год":2015},

    {"Отрасль":"Petroleum Refining, Coking and Nuclear Fuel Processing","Профит":125.92,"TotalOutput":2331.04,"Number":80,"Workers":2.66,"год":2015},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":478.76,"TotalOutput":6315.93,"Number":2165,"Workers":34.20,"год":2015},
    {"Отрасль":"Manufacture of Medicines","Профит":175.97,"TotalOutput":1484.49,"Number":398,"Workers":12.82,"год":2015},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":10.85,"TotalOutput":128.15,"Number":60,"Workers":1.44,"год":2015},
    {"Отрасль":"Rubber and Plastic Products","Профит":234.22,"TotalOutput":4860.96,"Number":3344,"Workers":83.90,"год":2015},
    {"Отрасль":"Nonmetal Mineral Products","Профит":291.65,"TotalOutput":5007.36,"Number":2812,"Workers":60.22,"год":2015},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":62.33,"TotalOutput":2332.54,"Number":462,"Workers":10.80,"год":2015},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":110.88,"TotalOutput":3181.13,"Number":630,"Workers":14.76,"год":2015},
    {"Отрасль":"Metal Products","Профит":342.87,"TotalOutput":5855.38,"Number":3347,"Workers":82.24,"год":2015},

    {"Отрасль":"General-purpose Machinery","Профит":235.39,"TotalOutput":3646.22,"Number":1614,"Workers":46.26,"год":2015},
    {"Отрасль":"Special-purpose Machinery","Профит":194.67,"TotalOutput":2479.64,"Number":1451,"Workers":39.77,"год":2015},
    {"Отрасль":"Automobile Manufacturing","Профит":468.72,"TotalOutput":5955.96,"Number":715,"Workers":38.02,"год":2015},
    {"Отрасль":"Railway/Ship/Aeronautics & Other Transport Equipment","Профит":58.97,"TotalOutput":1241.12,"Number":397,"Workers":13.26,"год":2015},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":820.83,"TotalOutput":12428.41,"Number":4203,"Workers":173.63,"год":2015},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":1680.27,"TotalOutput":30658.71,"Number":4869,"Workers":337.71,"год":2015},
    {"Отрасль":"Instruments and Meters","Профит":61.63,"TotalOutput":866.87,"Number":485,"Workers":21.89,"год":2015},
    {"Отрасль":"Other Manufactures","Профит":12.08,"TotalOutput":253.44,"Number":241,"Workers":5.84,"год":2015},
    {"Отрасль":"Comprehensive Utilization of Waste","Профит":95.36,"TotalOutput":1151.96,"Number":278,"Workers":4.33,"год":2015},
    {"Отрасль":"Metal Products/Machinery/Equipment Maintenance","Профит":9.69,"TotalOutput":133.86,"Number":47,"Workers":1.93,"год":2015},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":586.55,"TotalOutput":6405.36,"Number":338,"Workers":20.37,"год":2015},
    {"Отрасль":"Gas Production and Supply","Профит":55.74,"TotalOutput":789.54,"Number":96,"Workers":1.55,"год":2015},
    {"Отрасль":"Water Production and Supply","Профит":55.63,"TotalOutput":405.29,"Number":254,"Workers":5.30,"год":2015}
    ]

    data2016 = [
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":99.76,"TotalOutput":428.21,"Number":4,"Workers":0.57,"год":2016},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":7.78,"TotalOutput":122.58,"Number":37,"Workers":0.69,"год":2016},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":8.90,"TotalOutput":61.50,"Number":29,"Workers":0.74,"год":2016},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":33.93,"TotalOutput":400.44,"Number":272,"Workers":2.64,"год":2016},
    {"Отрасль":"Auxiliary Mining Operations","Профит":1.26,"TotalOutput":20.77,"Number":4,"Workers":0.23,"год":2016},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":163.17,"TotalOutput":3360.47,"Number":981,"Workers":17.41,"год":2016},
    {"Отрасль":"Manufacture of Food","Профит":262.52,"TotalOutput":1915.96,"Number":735,"Workers":19.20,"год":2016},
    {"Отрасль":"Manufacture of Wine, Beverage and Refined Tea","Профит":82.55,"TotalOutput":1177.29,"Number":263,"Workers":8.16,"год":2016},
    {"Отрасль":"Tobacco Products","Профит":50.39,"TotalOutput":431.26,"Number":11,"Workers":0.79,"год":2016},

    {"Отрасль":"Textile Industry","Профит":140.45,"TotalOutput":2724.90,"Number":1464,"Workers":36.53,"год":2016},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":182.03,"TotalOutput":4188.24,"Number":2806,"Workers":91.08,"год":2016},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":93.62,"TotalOutput":2504.05,"Number":1854,"Workers":65.51,"год":2016},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":55.45,"TotalOutput":882.24,"Number":548,"Workers":8.90,"год":2016},
    {"Отрасль":"Manufacture of Furniture","Профит":114.66,"TotalOutput":2081.34,"Number":1265,"Workers":34.53,"год":2016},
    {"Отрасль":"Papermaking and Paper Products","Профит":120.64,"TotalOutput":2146.85,"Number":1030,"Workers":22.31,"год":2016},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":82.59,"TotalOutput":1282.51,"Number":838,"Workers":22.99,"год":2016},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":146.87,"TotalOutput":3880.44,"Number":1595,"Workers":75.09,"год":2016},

    {"Отрасль":"Petroleum Refining, Coking and Nuclear Fuel Processing","Профит":209.62,"TotalOutput":2224.90,"Number":84,"Workers":2.54,"год":2016},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":490.46,"TotalOutput":6419.70,"Number":2193,"Workers":34.16,"год":2016},
    {"Отрасль":"Manufacture of Medicines","Профит":223.20,"TotalOutput":1646.25,"Number":421,"Workers":13.36,"год":2016},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":11.46,"TotalOutput":131.70,"Number":56,"Workers":1.37,"год":2016},
    {"Отрасль":"Rubber and Plastic Products","Профит":286.58,"TotalOutput":5257.97,"Number":3321,"Workers":83.25,"год":2016},
    {"Отрасль":"Nonmetal Mineral Products","Профит":317.58,"TotalOutput":5270.41,"Number":2865,"Workers":60.33,"год":2016},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":96.56,"TotalOutput":2590.24,"Number":427,"Workers":10.24,"год":2016},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":127.31,"TotalOutput":3438.83,"Number":616,"Workers":14.99,"год":2016},
    {"Отрасль":"Metal Products","Профит":338.33,"TotalOutput":6194.65,"Number":3372,"Workers":81.32,"год":2016},

    {"Отрасль":"General-purpose Machinery","Профит":257.01,"TotalOutput":3953.12,"Number":1672,"Workers":47.99,"год":2016},
    {"Отрасль":"Special-purpose Machinery","Профит":243.64,"TotalOutput":2892.39,"Number":1586,"Workers":41.53,"год":2016},
    {"Отрасль":"Automobile Manufacturing","Профит":542.10,"TotalOutput":6902.98,"Number":762,"Workers":39.90,"год":2016},
    {"Отрасль":"Railway/Ship/Aeronautics & Other Transport Equipment","Профит":62.36,"TotalOutput":1402.89,"Number":390,"Workers":13.01,"год":2016},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":1049.70,"TotalOutput":13612.98,"Number":4296,"Workers":169.09,"год":2016},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":1579.01,"TotalOutput":33714.46,"Number":5085,"Workers":335.35,"год":2016},
    {"Отрасль":"Instruments and Meters","Профит":71.69,"TotalOutput":1003.03,"Number":533,"Workers":22.17,"год":2016},
    {"Отрасль":"Other Manufactures","Профит":11.02,"TotalOutput":273.20,"Number":241,"Workers":5.71,"год":2016},
    {"Отрасль":"Comprehensive Utilization of Waste","Профит":92.60,"TotalOutput":1179.27,"Number":268,"Workers":4.35,"год":2016},
    {"Отрасль":"Metal Products/Machinery/Equipment Maintenance","Профит":7.85,"TotalOutput":144.21,"Number":49,"Workers":2.04,"год":2016},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":592.79,"TotalOutput":6592.35,"Number":364,"Workers":20.61,"год":2016},
    {"Отрасль":"Gas Production and Supply","Профит":59.45,"TotalOutput":868.26,"Number":98,"Workers":1.62,"год":2016},
    {"Отрасль":"Water Production and Supply","Профит":66.13,"TotalOutput":442.09,"Number":272,"Workers":5.54,"год":2016}
    ]


    data2017 = [
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":188.92,"TotalOutput":532.01,"Number":4,"Workers":0.59,"год":2017},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":3.08,"TotalOutput":65.63,"Number":28,"Workers":0.35,"год":2017},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":15.15,"TotalOutput":70.75,"Number":27,"Workers":0.81,"год":2017},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":29.83,"TotalOutput":279.08,"Number":264,"Workers":2.24,"год":2017},
    {"Отрасль":"Auxiliary Mining Operations","Профит":1.30,"TotalOutput":16.62,"Number":4,"Workers":0.15,"год":2017},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":160.58,"TotalOutput":3114.52,"Number":1022,"Workers":16.50,"год":2017},
    {"Отрасль":"Manufacture of Food","Профит":231.01,"TotalOutput":1860.36,"Number":765,"Workers":17.60,"год":2017},
    {"Отрасль":"Manufacture of Wine, Beverage and Refined Tea","Профит":86.96,"TotalOutput":1085.99,"Number":264,"Workers":7.83,"год":2017},
    {"Отрасль":"Tobacco Products","Профит":44.85,"TotalOutput":438.73,"Number":11,"Workers":0.75,"год":2017},

    {"Отрасль":"Textile Industry","Профит":132.08,"TotalOutput":2486.46,"Number":1464,"Workers":32.74,"год":2017},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":180.32,"TotalOutput":3843.72,"Number":2784,"Workers":82.93,"год":2017},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":84.14,"TotalOutput":2246.47,"Number":1868,"Workers":56.29,"год":2017},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":54.58,"TotalOutput":738.16,"Number":573,"Workers":8.22,"год":2017},
    {"Отрасль":"Manufacture of Furniture","Профит":128.82,"TotalOutput":2172.69,"Number":1438,"Workers":35.82,"год":2017},
    {"Отрасль":"Papermaking and Paper Products","Профит":155.08,"TotalOutput":2522.10,"Number":1150,"Workers":21.64,"год":2017},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":85.91,"TotalOutput":1296.52,"Number":956,"Workers":22.91,"год":2017},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":170.10,"TotalOutput":3816.15,"Number":1708,"Workers":72.91,"год":2017},

    {"Отрасль":"Petroleum Refining, Coking and Nuclear Fuel Processing","Профит":249.45,"TotalOutput":2553.92,"Number":91,"Workers":2.43,"год":2017},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":429.96,"TotalOutput":5594.37,"Number":2347,"Workers":33.07,"год":2017},
    {"Отрасль":"Manufacture of Medicines","Профит":296.83,"TotalOutput":1537.08,"Number":453,"Workers":13.20,"год":2017},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":14.11,"TotalOutput":171.70,"Number":61,"Workers":1.50,"год":2017},
    {"Отрасль":"Rubber and Plastic Products","Профит":267.52,"TotalOutput":5221.83,"Number":3811,"Workers":85.54,"год":2017},
    {"Отрасль":"Nonmetal Mineral Products","Профит":333.70,"TotalOutput":5049.66,"Number":3119,"Workers":58.67,"год":2017},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":134.04,"TotalOutput":2562.42,"Number":420,"Workers":9.16,"год":2017},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":129.51,"TotalOutput":3259.21,"Number":682,"Workers":14.90,"год":2017},
    {"Отрасль":"Metal Products","Профит":332.95,"TotalOutput":6204.02,"Number":3814,"Workers":83.89,"год":2017},

    {"Отрасль":"General-purpose Machinery","Профит":282.55,"TotalOutput":4150.17,"Number":2028,"Workers":49.81,"год":2017},
    {"Отрасль":"Special-purpose Machinery","Профит":296.56,"TotalOutput":3395.32,"Number":1969,"Workers":47.45,"год":2017},
    {"Отрасль":"Automobile Manufacturing","Профит":654.40,"TotalOutput":7853.18,"Number":833,"Workers":42.00,"год":2017},
    {"Отрасль":"Railway/Ship/Aeronautics & Other Transport Equipment","Профит":65.79,"TotalOutput":1187.96,"Number":388,"Workers":11.88,"год":2017},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":933.39,"TotalOutput":12931.73,"Number":5006,"Workers":168.22,"год":2017},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":1874.52,"TotalOutput":37301.89,"Number":5808,"Workers":341.58,"год":2017},
    {"Отрасль":"Instruments and Meters","Профит":89.30,"TotalOutput":1124.19,"Number":672,"Workers":22.70,"год":2017},
    {"Отрасль":"Other Manufactures","Профит":9.60,"TotalOutput":250.72,"Number":297,"Workers":5.54,"год":2017},
    {"Отрасль":"Comprehensive Utilization of Waste","Профит":78.54,"TotalOutput":998.23,"Number":262,"Workers":3.80,"год":2017},
    {"Отрасль":"Metal Products/Machinery/Equipment Maintenance","Профит":10.49,"TotalOutput":177.55,"Number":52,"Workers":2.06,"год":2017},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":471.32,"TotalOutput":6369.97,"Number":346,"Workers":18.00,"год":2017},
    {"Отрасль":"Gas Production and Supply","Профит":70.15,"TotalOutput":768.72,"Number":147,"Workers":1.96,"год":2017},
    {"Отрасль":"Water Production and Supply","Профит":86.94,"TotalOutput":468.76,"Number":286,"Workers":5.54,"год":2017}
    ]


    data2018 = [
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":285.56,"TotalOutput":692.39,"Number":4,"Workers":0.58,"год":2018},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":1.30,"TotalOutput":24.47,"Number":28,"Workers":0.28,"год":2018},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":13.72,"TotalOutput":66.09,"Number":29,"Workers":0.75,"год":2018},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":17.89,"TotalOutput":205.95,"Number":271,"Workers":1.94,"год":2018},
    {"Отрасль":"Auxiliary Mining Operations","Профит":2.62,"TotalOutput":27.13,"Number":4,"Workers":0.12,"год":2018},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":132.46,"TotalOutput":3006.28,"Number":1036,"Workers":14.58,"год":2018},
    {"Отрасль":"Manufacture of Food","Профит":190.12,"TotalOutput":1667.71,"Number":766,"Workers":15.92,"год":2018},
    {"Отрасль":"Manufacture of Wine, Beverage and Refined Tea","Профит":103.22,"TotalOutput":991.34,"Number":262,"Workers":7.22,"год":2018},
    {"Отрасль":"Tobacco Products","Профит":49.58,"TotalOutput":439.69,"Number":11,"Workers":0.70,"год":2018},

    {"Отрасль":"Textile Industry","Профит":117.44,"TotalOutput":2173.62,"Number":1494,"Workers":26.68,"год":2018},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":133.60,"TotalOutput":2955.94,"Number":2758,"Workers":64.93,"год":2018},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":44.82,"TotalOutput":1734.11,"Number":1877,"Workers":46.68,"год":2018},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":26.85,"TotalOutput":506.90,"Number":584,"Workers":6.34,"год":2018},
    {"Отрасль":"Manufacture of Furniture","Профит":114.65,"TotalOutput":2057.90,"Number":1454,"Workers":33.76,"год":2018},
    {"Отрасль":"Papermaking and Paper Products","Профит":144.41,"TotalOutput":2550.29,"Number":1172,"Workers":20.95,"год":2018},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":72.85,"TotalOutput":1230.32,"Number":945,"Workers":21.19,"год":2018},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":125.39,"TotalOutput":3628.21,"Number":1713,"Workers":65.05,"год":2018},

    {"Отрасль":"Petroleum Refining, Coking and Nuclear Fuel Processing","Профит":208.29,"TotalOutput":3389.60,"Number":102,"Workers":2.63,"год":2018},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":470.96,"TotalOutput":5852.56,"Number":2363,"Workers":31.51,"год":2018},
    {"Отрасль":"Manufacture of Medicines","Профит":277.62,"TotalOutput":1707.56,"Number":453,"Workers":13.09,"год":2018},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":11.50,"TotalOutput":136.65,"Number":58,"Workers":1.02,"год":2018},
    {"Отрасль":"Rubber and Plastic Products","Профит":221.78,"TotalOutput":4996.95,"Number":3818,"Workers":77.53,"год":2018},
    {"Отрасль":"Nonmetal Mineral Products","Профит":381.50,"TotalOutput":4983.91,"Number":3134,"Workers":53.84,"год":2018},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":146.22,"TotalOutput":2499.81,"Number":363,"Workers":6.99,"год":2018},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":101.11,"TotalOutput":3364.98,"Number":668,"Workers":13.51,"год":2018},
    {"Отрасль":"Metal Products","Профит":264.01,"TotalOutput":5861.85,"Number":3934,"Workers":77.79,"год":2018},

    {"Отрасль":"General-purpose Machinery","Профит":241.46,"TotalOutput":4087.48,"Number":2030,"Workers":48.04,"год":2018},
    {"Отрасль":"Special-purpose Machinery","Профит":315.75,"TotalOutput":3505.72,"Number":2019,"Workers":48.79,"год":2018},
    {"Отрасль":"Automobile Manufacturing","Профит":632.70,"TotalOutput":8558.88,"Number":833,"Workers":43.56,"год":2018},
    {"Отрасль":"Railway/Ship/Aeronautics & Other Transport Equipment","Профит":11.33,"TotalOutput":893.31,"Number":403,"Workers":10.24,"год":2018},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":925.36,"TotalOutput":13716.37,"Number":5051,"Workers":160.50,"год":2018},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":1690.41,"TotalOutput":39911.84,"Number":5793,"Workers":311.71,"год":2018},
    {"Отрасль":"Instruments and Meters","Профит":72.07,"TotalOutput":1085.73,"Number":631,"Workers":18.74,"год":2018},
    {"Отрасль":"Other Manufactures","Профит":11.29,"TotalOutput":256.81,"Number":304,"Workers":5.77,"год":2018},
    {"Отрасль":"Comprehensive Utilization of Waste","Профит":60.86,"TotalOutput":807.84,"Number":266,"Workers":2.81,"год":2018},
    {"Отрасль":"Metal Products/Machinery/Equipment Maintenance","Профит":11.12,"TotalOutput":169.52,"Number":51,"Workers":1.74,"год":2018},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":523.78,"TotalOutput":6669.41,"Number":360,"Workers":17.71,"год":2018},
    {"Отрасль":"Gas Production and Supply","Профит":75.74,"TotalOutput":1012.42,"Number":147,"Workers":1.96,"год":2018},
    {"Отрасль":"Water Production and Supply","Профит":78.36,"TotalOutput":456.90,"Number":286,"Workers":5.42,"год":2018}
    ]

    data2019 = [
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":313.95,"TotalOutput":684.62,"Number":4,"Workers":0.58,"год":2019},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":2.71,"TotalOutput":29.92,"Number":14,"Workers":0.20,"год":2019},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":10.08,"TotalOutput":67.58,"Number":27,"Workers":0.68,"год":2019},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":18.56,"TotalOutput":205.35,"Number":206,"Workers":1.50,"год":2019},
    {"Отрасль":"Auxiliary Mining Operations","Профит":2.59,"TotalOutput":31.29,"Number":5,"Workers":0.14,"год":2019},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":118.08,"TotalOutput":3100.63,"Number":1044,"Workers":14.69,"год":2019},
    {"Отрасль":"Manufacture of Food","Профит":226.18,"TotalOutput":2112.08,"Number":777,"Workers":18.44,"год":2019},
    {"Отрасль":"Manufacture of Wine, Beverage and Refined Tea","Профит":113.61,"TotalOutput":1002.55,"Number":233,"Workers":6.86,"год":2019},
    {"Отрасль":"Tobacco Products","Профит":33.02,"TotalOutput":465.67,"Number":15,"Workers":0.88,"год":2019},

    {"Отрасль":"Textile Industry","Профит":123.98,"TotalOutput":2132.95,"Number":1446,"Workers":24.68,"год":2019},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":143.96,"TotalOutput":3102.15,"Number":2744,"Workers":62.24,"год":2019},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":45.60,"TotalOutput":1765.89,"Number":1837,"Workers":43.43,"год":2019},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":28.08,"TotalOutput":521.70,"Number":551,"Workers":5.80,"год":2019},
    {"Отрасль":"Manufacture of Furniture","Профит":145.66,"TotalOutput":2234.76,"Number":1745,"Workers":34.24,"год":2019},
    {"Отрасль":"Papermaking and Paper Products","Профит":118.77,"TotalOutput":2498.11,"Number":1365,"Workers":21.07,"год":2019},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":80.57,"TotalOutput":1366.79,"Number":1069,"Workers":21.57,"год":2019},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":127.87,"TotalOutput":3427.99,"Number":1809,"Workers":59.05,"год":2019},

    {"Отрасль":"Petroleum Refining, Coking and Nuclear Fuel Processing","Профит":114.67,"TotalOutput":3133.07,"Number":112,"Workers":2.51,"год":2019},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":410.25,"TotalOutput":5604.78,"Number":2687,"Workers":31.51,"год":2019},
    {"Отрасль":"Manufacture of Medicines","Профит":247.99,"TotalOutput":1646.86,"Number":484,"Workers":13.74,"год":2019},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":14.29,"TotalOutput":178.76,"Number":67,"Workers":1.21,"год":2019},
    {"Отрасль":"Rubber and Plastic Products","Профит":301.72,"TotalOutput":5695.37,"Number":4681,"Workers":83.99,"год":2019},
    {"Отрасль":"Nonmetal Mineral Products","Профит":444.42,"TotalOutput":5889.83,"Number":3233,"Workers":54.35,"год":2019},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":109.75,"TotalOutput":2709.33,"Number":427,"Workers":7.36,"год":2019},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":121.75,"TotalOutput":3605.83,"Number":860,"Workers":14.52,"год":2019},
    {"Отрасль":"Metal Products","Профит":322.94,"TotalOutput":6630.31,"Number":4959,"Workers":82.82,"год":2019},

    {"Отрасль":"General-purpose Machinery","Профит":289.16,"TotalOutput":4697.44,"Number":2804,"Workers":52.67,"год":2019},
    {"Отрасль":"Special-purpose Machinery","Профит":330.57,"TotalOutput":4014.57,"Number":2967,"Workers":55.59,"год":2019},
    {"Отрасль":"Automobile Manufacturing","Профит":538.65,"TotalOutput":8291.08,"Number":949,"Workers":41.66,"год":2019},
    {"Отрасль":"Railway/Ship/Aeronautics & Other Transport Equipment","Профит":29.71,"TotalOutput":1027.72,"Number":434,"Workers":10.73,"год":2019},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":1105.26,"TotalOutput":14866.73,"Number":6300,"Workers":172.02,"год":2019},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":2154.81,"TotalOutput":41570.06,"Number":7096,"Workers":317.76,"год":2019},
    {"Отрасль":"Instruments and Meters","Профит":90.60,"TotalOutput":1302.98,"Number":865,"Workers":19.88,"год":2019},
    {"Отрасль":"Other Manufactures","Профит":17.64,"TotalOutput":365.07,"Number":379,"Workers":7.49,"год":2019},
    {"Отрасль":"Comprehensive Utilization of Waste","Профит":52.82,"TotalOutput":1041.41,"Number":225,"Workers":2.53,"год":2019},
    {"Отрасль":"Metal Products/Machinery/Equipment Maintenance","Профит":13.78,"TotalOutput":212.18,"Number":61,"Workers":2.11,"год":2019},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":643.86,"TotalOutput":7132.47,"Number":408,"Workers":17.47,"год":2019},
    {"Отрасль":"Gas Production and Supply","Профит":43.77,"TotalOutput":1239.80,"Number":198,"Workers":2.11,"год":2019},
    {"Отрасль":"Water Production and Supply","Профит":88.80,"TotalOutput":516.03,"Number":328,"Workers":5.72,"год":2019}
    ]



    data2020 = [
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":218.95,"TotalOutput":594.12,"Number":4,"Workers":0.58,"год":2020},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":2.95,"TotalOutput":25.65,"Number":10,"Workers":0.14,"год":2020},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":10.43,"TotalOutput":73.31,"Number":27,"Workers":0.68,"год":2020},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":16.39,"TotalOutput":213.76,"Number":209,"Workers":1.35,"год":2020},
    {"Отрасль":"Mining Specialized and Auxiliary Operations","Профит":5.50,"TotalOutput":37.77,"Number":4,"Workers":0.12,"год":2020},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":124.20,"TotalOutput":3356.27,"Number":1093,"Workers":13.81,"год":2020},
    {"Отрасль":"Manufacture of Food","Профит":254.88,"TotalOutput":2079.62,"Number":812,"Workers":18.68,"год":2020},
    {"Отрасль":"Manufacture of Wine, Beverage and Refined Tea","Профит":114.96,"TotalOutput":993.06,"Number":224,"Workers":6.58,"год":2020},
    {"Отрасль":"Tobacco Products","Профит":56.59,"TotalOutput":487.82,"Number":15,"Workers":1.47,"год":2020},

    {"Отрасль":"Textile Industry","Профит":149.27,"TotalOutput":2077.61,"Number":1545,"Workers":23.43,"год":2020},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":106.72,"TotalOutput":2633.34,"Number":2547,"Workers":49.90,"год":2020},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":19.58,"TotalOutput":1271.79,"Number":1601,"Workers":32.87,"год":2020},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":28.52,"TotalOutput":444.20,"Number":559,"Workers":5.34,"год":2020},
    {"Отрасль":"Manufacture of Furniture","Профит":112.82,"TotalOutput":2003.68,"Number":1740,"Workers":31.34,"год":2020},
    {"Отрасль":"Papermaking and Paper Products","Профит":149.89,"TotalOutput":2483.28,"Number":1372,"Workers":20.18,"год":2020},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":77.06,"TotalOutput":1319.52,"Number":1099,"Workers":20.44,"год":2020},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":111.17,"TotalOutput":3244.91,"Number":1727,"Workers":51.95,"год":2020},

    {"Отрасль":"Petroleum, Coal and other Fuel Processing","Профит":42.01,"TotalOutput":2853.29,"Number":109,"Workers":2.34,"год":2020},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":447.21,"TotalOutput":5551.01,"Number":2831,"Workers":31.10,"год":2020},
    {"Отрасль":"Manufacture of Medicines","Профит":299.19,"TotalOutput":1859.72,"Number":570,"Workers":15.30,"год":2020},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":20.04,"TotalOutput":178.97,"Number":72,"Workers":1.19,"год":2020},
    {"Отрасль":"Rubber and Plastic Products","Профит":304.71,"TotalOutput":5440.54,"Number":5100,"Workers":78.32,"год":2020},
    {"Отрасль":"Nonmetal Mineral Products","Профит":482.39,"TotalOutput":6266.94,"Number":3363,"Workers":52.46,"год":2020},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":133.35,"TotalOutput":2765.22,"Number":429,"Workers":6.64,"год":2020},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":95.58,"TotalOutput":3519.29,"Number":925,"Workers":14.11,"год":2020},
    {"Отрасль":"Metal Products","Профит":356.00,"TotalOutput":6974.39,"Number":5338,"Workers":81.85,"год":2020},

    {"Отрасль":"General-purpose Machinery","Профит":302.77,"TotalOutput":4750.40,"Number":3127,"Workers":52.26,"год":2020},
    {"Отрасль":"Special-purpose Machinery","Профит":451.86,"TotalOutput":4425.33,"Number":3370,"Workers":56.25,"год":2020},
    {"Отрасль":"Automobile Manufacturing","Профит":615.05,"TotalOutput":8986.03,"Number":990,"Workers":40.17,"год":2020},
    {"Отрасль":"Railway/Ship/Aeronautics & Other Transport Equipment","Профит":34.38,"TotalOutput":1240.53,"Number":437,"Workers":10.52,"год":2020},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":1221.18,"TotalOutput":15803.07,"Number":6749,"Workers":172.05,"год":2020},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":2298.03,"TotalOutput":42817.87,"Number":7832,"Workers":327.68,"год":2020},
    {"Отрасль":"Instruments and Meters","Профит":109.96,"TotalOutput":1313.68,"Number":942,"Workers":18.99,"год":2020},
    {"Отрасль":"Other Manufactures","Профит":18.96,"TotalOutput":397.10,"Number":420,"Workers":7.03,"год":2020},
    {"Отрасль":"Comprehensive Utilization of Waste","Профит":46.96,"TotalOutput":980.08,"Number":224,"Workers":2.09,"год":2020},
    {"Отрасль":"Metal Products/Machinery/Equipment Maintenance","Профит":12.26,"TotalOutput":189.40,"Number":68,"Workers":2.22,"год":2020},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":521.71,"TotalOutput":6925.33,"Number":456,"Workers":17.36,"год":2020},
    {"Отрасль":"Gas Production and Supply","Профит":84.17,"TotalOutput":1261.35,"Number":214,"Workers":2.17,"год":2020},
    {"Отрасль":"Water Production and Supply","Профит":114.45,"TotalOutput":630.42,"Number":350,"Workers":6.14,"год":2020}
    ]


    data2021 = [
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":358.34,"TotalOutput":792.18,"Number":4,"Workers":0.52,"год":2021},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":6.63,"TotalOutput":60.04,"Number":12,"Workers":0.15,"год":2021},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":16.14,"TotalOutput":97.17,"Number":28,"Workers":0.65,"год":2021},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":22.90,"TotalOutput":321.19,"Number":217,"Workers":1.41,"год":2021},
    {"Отрасль":"Mining Specialized and Auxiliary Operations","Профит":7.41,"TotalOutput":33.99,"Number":6,"Workers":0.13,"год":2021},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":136.03,"TotalOutput":3969.47,"Number":1185,"Workers":14.51,"год":2021},
    {"Отрасль":"Manufacture of Food","Профит":245.15,"TotalOutput":2220.05,"Number":870,"Workers":18.94,"год":2021},
    {"Отрасль":"Manufacture of Wine, Beverage and Refined Tea","Профит":129.57,"TotalOutput":1187.00,"Number":225,"Workers":7.30,"год":2021},
    {"Отрасль":"Tobacco Products","Профит":43.24,"TotalOutput":539.18,"Number":35,"Workers":1.22,"год":2021},

    {"Отрасль":"Textile Industry","Профит":120.12,"TotalOutput":2323.15,"Number":1641,"Workers":23.77,"год":2021},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":127.71,"TotalOutput":3066.40,"Number":2593,"Workers":49.82,"год":2021},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":34.11,"TotalOutput":1457.97,"Number":1638,"Workers":31.16,"год":2021},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":20.66,"TotalOutput":527.98,"Number":594,"Workers":5.33,"год":2021},
    {"Отрасль":"Manufacture of Furniture","Профит":101.26,"TotalOutput":2361.20,"Number":1925,"Workers":33.19,"год":2021},
    {"Отрасль":"Papermaking and Paper Products","Профит":134.70,"TotalOutput":2799.60,"Number":1543,"Workers":20.26,"год":2021},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":77.38,"TotalOutput":1471.81,"Number":1187,"Workers":21.03,"год":2021},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":135.28,"TotalOutput":3999.05,"Number":1891,"Workers":55.75,"год":2021},

    {"Отрасль":"Petroleum, Coal and other Fuel Processing","Профит":231.52,"TotalOutput":3938.66,"Number":111,"Workers":2.23,"год":2021},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":543.56,"TotalOutput":6816.92,"Number":3108,"Workers":32.95,"год":2021},
    {"Отрасль":"Manufacture of Medicines","Профит":423.68,"TotalOutput":2053.47,"Number":592,"Workers":15.75,"год":2021},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":33.32,"TotalOutput":256.40,"Number":87,"Workers":1.35,"год":2021},
    {"Отрасль":"Rubber and Plastic Products","Профит":327.31,"TotalOutput":6447.72,"Number":5814,"Workers":83.55,"год":2021},
    {"Отрасль":"Nonmetal Mineral Products","Профит":503.05,"TotalOutput":7289.47,"Number":3731,"Workers":54.26,"год":2021},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":177.90,"TotalOutput":3664.34,"Number":494,"Workers":6.93,"год":2021},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":125.69,"TotalOutput":4838.65,"Number":1075,"Workers":15.22,"год":2021},
    {"Отрасль":"Metal Products","Профит":450.77,"TotalOutput":8799.83,"Number":6513,"Workers":92.11,"год":2021},

    {"Отрасль":"General-purpose Machinery","Профит":324.48,"TotalOutput":5625.51,"Number":3731,"Workers":56.35,"год":2021},
    {"Отрасль":"Special-purpose Machinery","Профит":482.64,"TotalOutput":5295.40,"Number":3959,"Workers":63.30,"год":2021},
    {"Отрасль":"Automobile Manufacturing","Профит":628.28,"TotalOutput":9647.90,"Number":1064,"Workers":42.48,"год":2021},
    {"Отрасль":"Railway/Ship/Aeronautics & Other Transport Equipment","Профит":31.78,"TotalOutput":1510.47,"Number":503,"Workers":11.97,"год":2021},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":1351.35,"TotalOutput":19429.70,"Number":7814,"Workers":182.74,"год":2021},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":3222.42,"TotalOutput":45416.50,"Number":9112,"Workers":338.93,"год":2021},
    {"Отрасль":"Instruments and Meters","Профит":143.09,"TotalOutput":1525.94,"Number":1087,"Workers":20.05,"год":2021},
    {"Отрасль":"Other Manufactures","Профит":20.70,"TotalOutput":490.60,"Number":470,"Workers":7.74,"год":2021},
    {"Отрасль":"Comprehensive Utilization of Waste","Профит":31.67,"TotalOutput":624.85,"Number":250,"Workers":2.19,"год":2021},
    {"Отрасль":"Metal Products/Machinery/Equipment Maintenance","Профит":13.19,"TotalOutput":201.71,"Number":77,"Workers":2.31,"год":2021},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":267.18,"TotalOutput":8201.42,"Number":517,"Workers":17.31,"год":2021},
    {"Отрасль":"Gas Production and Supply","Профит":119.37,"TotalOutput":1916.80,"Number":251,"Workers":2.28,"год":2021},
    {"Отрасль":"Water Production and Supply","Профит":108.76,"TotalOutput":760.13,"Number":375,"Workers":6.43,"год":2021}
    ]


    data2022 = [
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":582.96,"TotalOutput":1159.37,"Number":3,"Workers":0.51,"год":2022},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":11.59,"TotalOutput":53.95,"Number":12,"Workers":0.14,"год":2022},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":22.37,"TotalOutput":114.99,"Number":28,"Workers":0.63,"год":2022},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":10.52,"TotalOutput":237.24,"Number":226,"Workers":1.38,"год":2022},
    {"Отрасль":"Mining Specialized and Auxiliary Operations","Профит":9.88,"TotalOutput":56.27,"Number":8,"Workers":0.18,"год":2022},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":145.71,"TotalOutput":4272.63,"Number":1285,"Workers":15.17,"год":2022},
    {"Отрасль":"Manufacture of Food","Профит":247.03,"TotalOutput":2232.95,"Number":930,"Workers":19.20,"год":2022},
    {"Отрасль":"Manufacture of Wine, Beverage and Refined Tea","Профит":100.64,"TotalOutput":1173.87,"Number":237,"Workers":7.38,"год":2022},
    {"Отрасль":"Tobacco Products","Профит":51.93,"TotalOutput":601.72,"Number":46,"Workers":1.81,"год":2022},

    {"Отрасль":"Textile Industry","Профит":126.54,"TotalOutput":2261.45,"Number":1685,"Workers":22.79,"год":2022},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":109.19,"TotalOutput":2798.78,"Number":2671,"Workers":46.35,"год":2022},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":56.20,"TotalOutput":1599.61,"Number":1757,"Workers":31.95,"год":2022},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":10.07,"TotalOutput":426.31,"Number":570,"Workers":5.15,"год":2022},
    {"Отрасль":"Manufacture of Furniture","Профит":135.17,"TotalOutput":2207.71,"Number":1956,"Workers":31.50,"год":2022},
    {"Отрасль":"Papermaking and Paper Products","Профит":55.45,"TotalOutput":2767.12,"Number":1598,"Workers":19.77,"год":2022},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":100.31,"TotalOutput":1438.37,"Number":1213,"Workers":20.07,"год":2022},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":131.31,"TotalOutput":4145.36,"Number":2081,"Workers":53.73,"год":2022},

    {"Отрасль":"Petroleum, Coal and other Fuel Processing","Профит":-23.95,"TotalOutput":4945.41,"Number":122,"Workers":2.39,"год":2022},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":379.95,"TotalOutput":7233.54,"Number":3321,"Workers":33.67,"год":2022},
    {"Отрасль":"Manufacture of Medicines","Профит":385.26,"TotalOutput":2264.35,"Number":628,"Workers":17.04,"год":2022},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":17.46,"TotalOutput":196.54,"Number":93,"Workers":1.22,"год":2022},
    {"Отрасль":"Rubber and Plastic Products","Профит":379.65,"TotalOutput":6283.50,"Number":6241,"Workers":79.92,"год":2022},
    {"Отрасль":"Nonmetal Mineral Products","Профит":270.66,"TotalOutput":6789.28,"Number":3890,"Workers":51.94,"год":2022},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":53.15,"TotalOutput":3845.87,"Number":531,"Workers":7.14,"год":2022},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":116.51,"TotalOutput":5066.77,"Number":1149,"Workers":15.08,"год":2022},
    {"Отрасль":"Metal Products","Профит":435.84,"TotalOutput":8816.38,"Number":7175,"Workers":92.42,"год":2022},

    {"Отрасль":"General-purpose Machinery","Профит":372.21,"TotalOutput":5793.28,"Number":4095,"Workers":59.06,"год":2022},
    {"Отрасль":"Special-purpose Machinery","Профит":509.29,"TotalOutput":5673.58,"Number":4234,"Workers":66.67,"год":2022},
    {"Отрасль":"Automobile Manufacturing","Профит":705.32,"TotalOutput":11593.39,"Number":1140,"Workers":46.57,"год":2022},
    {"Отрасль":"Railway/Ship/Aeronautics & Other Transport Equipment","Профит":80.39,"TotalOutput":1583.18,"Number":541,"Workers":11.71,"год":2022},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":1521.64,"TotalOutput":20991.10,"Number":8246,"Workers":176.42,"год":2022},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":2401.82,"TotalOutput":46693.22,"Number":9672,"Workers":332.06,"год":2022},
    {"Отрасль":"Instruments and Meters","Профит":137.75,"TotalOutput":1614.87,"Number":1186,"Workers":21.33,"год":2022},
    {"Отрасль":"Other Manufactures","Профит":59.72,"TotalOutput":632.72,"Number":535,"Workers":9.45,"год":2022},
    {"Отрасль":"Comprehensive Utilization of Waste","Профит":22.30,"TotalOutput":649.08,"Number":271,"Workers":2.16,"год":2022},
    {"Отрасль":"Metal Products/Machinery/Equipment Maintenance","Профит":12.31,"TotalOutput":236.63,"Number":89,"Workers":2.50,"год":2022},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":380.07,"TotalOutput":9184.45,"Number":567,"Workers":17.30,"год":2022},
    {"Отрасль":"Gas Production and Supply","Профит":117.07,"TotalOutput":2466.14,"Number":291,"Workers":2.39,"год":2022},
    {"Отрасль":"Water Production and Supply","Профит":87.95,"TotalOutput":832.44,"Number":402,"Workers":6.44,"год":2022}
    ]


    data2023 = [
    {"Отрасль":"Extraction of Petroleum and Natural Gas","Профит":537.97,"TotalOutput":1061.26,"Number":3,"Workers":0.55,"год":2023},
    {"Отрасль":"Mining and Dressing of Ferrous Metal Ores","Профит":6.32,"TotalOutput":45.70,"Number":9,"Workers":0.10,"год":2023},
    {"Отрасль":"Mining and Dressing of Nonferrous Metal Ores","Профит":16.16,"TotalOutput":92.65,"Number":29,"Workers":0.58,"год":2023},
    {"Отрасль":"Mining and Dressing of Nonmetal Ores","Профит":23.22,"TotalOutput":256.38,"Number":216,"Workers":1.32,"год":2023},
    {"Отрасль":"Mining Specialized and Auxiliary Operations","Профит":9.37,"TotalOutput":57.05,"Number":7,"Workers":0.17,"год":2023},

    {"Отрасль":"Processing of Farm and Sideline Food","Профит":107.50,"TotalOutput":4328.56,"Number":1338,"Workers":15.05,"год":2023},
    {"Отрасль":"Manufacture of Food","Профит":232.25,"TotalOutput":2180.43,"Number":1007,"Workers":19.46,"год":2023},
    {"Отрасль":"Manufacture of Wine, Beverage and Refined Tea","Профит":124.21,"TotalOutput":1246.30,"Number":230,"Workers":7.43,"год":2023},
    {"Отрасль":"Tobacco Products","Профит":78.25,"TotalOutput":824.76,"Number":98,"Workers":4.07,"год":2023},

    {"Отрасль":"Textile Industry","Профит":113.79,"TotalOutput":2257.43,"Number":1756,"Workers":22.21,"год":2023},
    {"Отрасль":"Manufacture of Textile Garments, Footwear and Headgear","Профит":97.41,"TotalOutput":2409.95,"Number":2484,"Workers":41.59,"год":2023},
    {"Отрасль":"Leather, Fur, Feather & Related Products and Footwear","Профит":49.53,"TotalOutput":1439.01,"Number":1755,"Workers":30.59,"год":2023},
    {"Отрасль":"Timber Processing, Bamboo/Cane/Palm/Straw Products","Профит":13.40,"TotalOutput":398.52,"Number":537,"Workers":4.62,"год":2023},
    {"Отрасль":"Manufacture of Furniture","Профит":121.09,"TotalOutput":2150.43,"Number":1838,"Workers":29.61,"год":2023},
    {"Отрасль":"Papermaking and Paper Products","Профит":29.59,"TotalOutput":2637.44,"Number":1566,"Workers":19.00,"год":2023},
    {"Отрасль":"Printing and Record Medium Reproduction","Профит":81.56,"TotalOutput":1310.68,"Number":1179,"Workers":18.65,"год":2023},
    {"Отрасль":"Cultural/Educational/Sports/Entertainment Articles","Профит":105.20,"TotalOutput":4020.44,"Number":2094,"Workers":47.22,"год":2023},

    {"Отрасль":"Petroleum, Coal and other Fuel Processing","Профит":98.21,"TotalOutput":5493.51,"Number":123,"Workers":2.45,"год":2023},
    {"Отрасль":"Raw Chemical Materials and Chemical Products","Профит":384.88,"TotalOutput":7384.32,"Number":3496,"Workers":34.71,"год":2023},
    {"Отрасль":"Manufacture of Medicines","Профит":249.90,"TotalOutput":2017.40,"Number":642,"Workers":16.70,"год":2023},
    {"Отрасль":"Manufacture of Chemical Fibers","Профит":14.16,"TotalOutput":191.27,"Number":95,"Workers":1.34,"год":2023},
    {"Отрасль":"Rubber and Plastic Products","Профит":314.83,"TotalOutput":6118.03,"Number":6461,"Workers":77.72,"год":2023},
    {"Отрасль":"Nonmetal Mineral Products","Профит":266.22,"TotalOutput":6351.17,"Number":3904,"Workers":49.24,"год":2023},
    {"Отрасль":"Smelting and Pressing of Ferrous Metals","Профит":90.44,"TotalOutput":4591.48,"Number":592,"Workers":7.87,"год":2023},
    {"Отрасль":"Smelting and Pressing of Nonferrous Metals","Профит":60.07,"TotalOutput":3973.63,"Number":1273,"Workers":14.55,"год":2023},
    {"Отрасль":"Metal Products","Профит":379.24,"TotalOutput":8794.14,"Number":7166,"Workers":92.17,"год":2023},

    {"Отрасль":"General-purpose Machinery","Профит":402.45,"TotalOutput":6157.39,"Number":4218,"Workers":59.94,"год":2023},
    {"Отрасль":"Special-purpose Machinery","Профит":609.56,"TotalOutput":5936.59,"Number":4230,"Workers":65.35,"год":2023},
    {"Отрасль":"Automobile Manufacturing","Профит":529.21,"TotalOutput":12846.58,"Number":1202,"Workers":49.11,"год":2023},
    {"Отрасль":"Railway/Ship/Aeronautics & Other Transport Equipment","Профит":66.22,"TotalOutput":1595.38,"Number":543,"Workers":11.07,"год":2023},
    {"Отрасль":"Electrical Machinery and Equipment","Профит":1584.71,"TotalOutput":22192.47,"Number":8463,"Workers":174.15,"год":2023},
    {"Отрасль":"Communication Equipment, Computers & Other Electronics","Профит":3628.09,"TotalOutput":47168.02,"Number":9966,"Workers":317.53,"год":2023},
    {"Отрасль":"Instruments and Meters","Профит":111.59,"TotalOutput":1503.82,"Number":1234,"Workers":20.27,"год":2023},
    {"Отрасль":"Other Manufactures","Профит":40.98,"TotalOutput":636.39,"Number":526,"Workers":9.47,"год":2023},
    {"Отрасль":"Comprehensive Utilization of Waste","Профит":19.63,"TotalOutput":783.85,"Number":283,"Workers":2.29,"год":2023},
    {"Отрасль":"Metal Products/Machinery/Equipment Maintenance","Профит":22.39,"TotalOutput":302.55,"Number":99,"Workers":2.77,"год":2023},

    {"Отрасль":"Electric Power & Heat Production/Supply","Профит":726.43,"TotalOutput":10511.89,"Number":604,"Workers":17.11,"год":2023},
    {"Отрасль":"Gas Production and Supply","Профит":145.80,"TotalOutput":3075.62,"Number":324,"Workers":2.47,"год":2023},
    {"Отрасль":"Water Production and Supply","Профит":103.38,"TotalOutput":811.69,"Number":406,"Workers":6.57,"год":2023}
    ]

    all_data = (data2002 + data2004 + data2005 + data2006 + data2007 + data2008 
    + data2009 + data2010 + data2011 + data2012 + data2013 + data2014
    + data2015 + data2016 + data2017 + data2018 + data2019 +data2020 
    + data2021 + data2022 +data2023);

    df = pd.DataFrame(all_data)

    return df

def load_gdp_composition():
    data = [
    [1990, 1541.99, 938.48, 502.90, 100.61],
    [1991, 1847.99, 1081.39, 610.18, 156.42],
    [1992, 2440.58, 1359.08, 987.96, 93.54],
    [1993, 3465.31, 1852.06, 1554.46, 58.79],
    [1994, 4618.25, 2598.57, 1930.86, 88.82],
    [1995, 5940.34, 3363.65, 2401.80, 174.89],
    [1996, 6848.22, 3859.84, 2795.64, 192.74],
    [1997, 7792.97, 4245.89, 2992.18, 554.90],
    [1998, 8555.33, 4583.10, 3354.63, 617.60],
    [1999, 9289.64, 5085.11, 3548.75, 655.78],
    [2000, 10810.21, 5717.11, 3917.11, 1175.99],
    [2001, 12126.59, 6259.29, 4476.48, 1390.82],
    [2002, 13601.89, 7290.47, 4858.53, 1452.89],
    [2003, 15979.77, 8647.86, 6022.16, 1309.75],
    [2004, 18658.34, 10167.48, 7350.24, 1140.62],
    [2005, 21962.99, 11457.36, 8399.25, 2106.38],
    [2006, 25961.24, 12643.78, 9512.26, 3805.20],
    [2007, 31742.61, 14853.52, 10967.58, 5921.51],
    [2008, 36704.16, 17215.48, 12590.33, 6898.35],
    [2009, 39464.69, 19196.56, 15378.86, 4889.27],
    [2010, 45944.62, 22501.78, 18226.60, 5216.24],
    [2011, 53072.79, 26235.01, 21689.40, 5148.38],
    [2012, 57007.74, 29581.98, 23699.14, 3726.62],
    [2013, 62503.41, 30900.24, 27020.20, 4582.97],
    [2014, 68173.03, 34595.53, 29850.24, 3727.26],
    [2015, 74732.44, 38116.43, 31602.04, 5013.97],
    [2016, 82163.22, 42095.22, 34647.12, 5420.89],
    [2017, 91648.73, 46682.78, 39657.57, 5308.39],
    [2018, 99945.22, 51531.96, 44379.92, 4033.34],
    [2019, 107986.92, 55827.36, 48076.62, 4082.94],
    [2020, 111151.63, 56585.06, 49319.71, 5246.86],
    [2021, 124719.53, 62237.05, 56914.11, 5568.37],
    [2022, 129513.55, 65167.52, 54600.37, 9745.65]
    ]

    df = pd.DataFrame(data, columns=[
        "Year", "GDP", "Final Consumption", "Gross Capital Formation", "Net Exports"
    ])
    return df

def load_strikes_by_industries(
    path,
    start_date="2024-01-01",
    end_date="2025-01-01",
    state="Guangdong",
    action_pattern="Strike"
):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data["chinese_strikes"])

    df["Start_Date"] = pd.to_datetime(df["Start_Date"], errors="coerce")

    filtered = df[
        (df["Start_Date"] >= start_date) &
        (df["Start_Date"] < end_date) &
        (df["State"] == state) &
        (df["Strike_or_Protest"].str.contains(action_pattern, na=False))
    ]

    return (
        filtered
        .groupby(["Industry", "subIndustry_name"])
        .size()
        .reset_index(name="total_strikes")
        .values.tolist()
    )

def load_wages():
    years = [
    1978,1979,1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,
    1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,
    2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,
    2017,2018,2019,2020,2021,2022,2023
    ]

    average_wage = [
    615,685,789,873,961,1021,1187,1393,1541,1743,2250,2678,2929,3358,4027,
    5327,7117,8250,9127,9698,10233,11309,13823,15682,17814,19986,22116,
    23959,26186,29443,33110,36355,40358,45152,50577,53611,59827,66296,
    72848,80020,89826,100689,110324,120299,126925,133452
    ]
    
    # DataFrame
    df = pd.DataFrame({
        "Year": years,
        "Average Wage": average_wage
    })
    df["Growth Rate (%)"] = df["Average Wage"].pct_change() * 100
    return df

def load_strikes_df(
    path,
    start_year=2011,
    end_year=2024,
    strike_pattern="Strike"
):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data["chinese_strikes"])

    df["Start_Date"] = pd.to_datetime(df["Start_Date"], errors="coerce")

    df = df[
        (df["Start_Date"].dt.year >= start_year) &
        (df["Start_Date"].dt.year <= end_year) &
        (df["Strike_or_Protest"].str.contains(strike_pattern, na=False))
    ]

    return df

def load_industry_data(year):
    """
    Возвращает DataFrame с отраслевыми данными для заданного года
    """

    if year == 2003:
        data = [
            {"Sector": "Processing of Food from Agricultural Products", "Enterprises": 611, "Output Value": 503.65, "Business Revenue": 484.23, "Total Profits": 10.26, "Employed Persons": 10.41},
            {"Sector": "Manufacturing of Foods", "Enterprises": 492, "Output Value": 297.51, "Business Revenue": 275.69, "Total Profits": 22.43, "Employed Persons": 10.25},
            {"Sector": "Textile Industry", "Enterprises": 1444, "Output Value": 784.52, "Business Revenue": 736.15, "Total Profits": 13.38, "Employed Persons": 38.64},
            {"Sector": "Manufacture of Textile Wearing Apparel, Clothing", "Enterprises": 2069, "Output Value": 765.07, "Business Revenue": 725.95, "Total Profits": 9.23, "Employed Persons": 70.88},
            {"Sector": "Manufacture of Culture and Education, Arts and Crafts, Sports and Entertainment Supplies", "Enterprises": 622, "Output Value": 333.28, "Business Revenue": 324.19, "Total Profits": 10.10, "Employed Persons": 41.03},
            {"Sector": "Processing of Petroleum, Coking, Processing of Nuclear", "Enterprises": 52, "Output Value": 553.03, "Business Revenue": 554.51, "Total Profits": 8.73, "Employed Persons": 1.82},
            {"Sector": "Manufacturing of Raw Chemical Material and Chemical Products", "Enterprises": 1310, "Output Value": 1140.98, "Business Revenue": 1109.71, "Total Profits": 108.55, "Employed Persons": 18.06},
            {"Sector": "Manufacturing of Medical and Pharmaceutical Products", "Enterprises": 280, "Output Value": 246.56, "Business Revenue": 209.60, "Total Profits": 21.71, "Employed Persons": 7.39},
            {"Sector": "Manufacture of Rubber and Plastic", "Enterprises": 1735, "Output Value": 802.17, "Business Revenue": 785.05, "Total Profits": 23.46, "Employed Persons": 39.27},
            {"Sector": "Manufacturing of Non-metallic Mineral Products", "Enterprises": 1665, "Output Value": 685.14, "Business Revenue": 639.01, "Total Profits": 18.79, "Employed Persons": 36.20},
            {"Sector": "Smelting and Pressing of Ferrous Metals", "Enterprises": 253, "Output Value": 332.26, "Business Revenue": 377.49, "Total Profits": 20.80, "Employed Persons": 4.72},
            {"Sector": "Smelting and Pressing of Non-ferrous Metals", "Enterprises": 306, "Output Value": 285.71, "Business Revenue": 270.61, "Total Profits": 6.63, "Employed Persons": 5.45},
            {"Sector": "Manufacturing of Metal Products", "Enterprises": 1870, "Output Value": 866.75, "Business Revenue": 845.39, "Total Profits": 29.72, "Employed Persons": 38.26},
            {"Sector": "Manufacturing of General Purpose Equipment", "Enterprises": 708, "Output Value": 312.47, "Business Revenue": 294.90, "Total Profits": 12.85, "Employed Persons": 12.91},
            {"Sector": "Manufacturing of Special Purpose Equipment", "Enterprises": 483, "Output Value": 218.30, "Business Revenue": 212.91, "Total Profits": 12.95, "Employed Persons": 10.00},
            {"Sector": "Manufacture of Automobile", "Enterprises": 613, "Output Value": 918.60, "Business Revenue": 915.31, "Total Profits": 95.26, "Employed Persons": 18.47},  # ~Transport Equipment Manufacturing
            {"Sector": "Manufacturing of Electric Machinery and Equipment", "Enterprises": 2190, "Output Value": 2160.43, "Business Revenue": 2081.48, "Total Profits": 79.49, "Employed Persons": 78.93},
            {"Sector": "Manufacture of Computers, Communications and Other Electronic Equipment", "Enterprises": 1768, "Output Value": 5932.21, "Business Revenue": 5732.69, "Total Profits": 246.51, "Employed Persons": 113.62},
            {"Sector": "Production and Supply of Electric Power and Heat Power", "Enterprises": 487, "Output Value": 880.31, "Business Revenue": 1683.40, "Total Profits": 131.10, "Employed Persons": 13.73},
        ]
    if year == 2013:
        data = [
            {"Sector": "Processing of Food from Agricultural Products", "Enterprises": 906, "Output Value": 2835.51, "Business Revenue": 2747.35, "Total Profits": 134.12, "Employed Persons": 17.21},
            {"Sector": "Manufacturing of Foods", "Enterprises": 646, "Output Value": 1644.03, "Business Revenue": 1664.78, "Total Profits": 238.75, "Employed Persons": 19.91},
            {"Sector": "Textile Industry", "Enterprises": 1643, "Output Value": 2456.08, "Business Revenue": 2375.58, "Total Profits": 140.31, "Employed Persons": 43.76},
            {"Sector": "Manufacture of Textile Wearing Apparel, Clothing", "Enterprises": 3077, "Output Value": 3478.72, "Business Revenue": 3352.80, "Total Profits": 186.84, "Employed Persons": 100.92},
            {"Sector": "Manufacture of Culture and Education, Arts and Crafts, Sports and Entertainment Supplies", "Enterprises": 1601, "Output Value": 3752.54, "Business Revenue": 3708.34, "Total Profits": 112.83, "Employed Persons": 82.45},
            {"Sector": "Processing of Petroleum, Coking, Processing of Nuclear", "Enterprises": 92, "Output Value": 3652.02, "Business Revenue": 3626.49, "Total Profits": 83.75, "Employed Persons": 2.61},
            {"Sector": "Manufacturing of Raw Chemical Material and Chemical Products", "Enterprises": 2163, "Output Value": 5461.28, "Business Revenue": 5292.94, "Total Profits": 401.07, "Employed Persons": 34.33},
            {"Sector": "Manufacturing of Medical and Pharmaceutical Products", "Enterprises": 382, "Output Value": 1222.46, "Business Revenue": 1144.59, "Total Profits": 150.13, "Employed Persons": 11.81},
            {"Sector": "Manufacture of Rubber and Plastic", "Enterprises": 3328, "Output Value": 4207.98, "Business Revenue": 4111.50, "Total Profits": 215.33, "Employed Persons": 85.46},
            {"Sector": "Manufacturing of Non-metallic Mineral Products", "Enterprises": 2448, "Output Value": 4033.36, "Business Revenue": 3825.19, "Total Profits": 270.44, "Employed Persons": 59.16},
            {"Sector": "Smelting and Pressing of Ferrous Metals", "Enterprises": 534, "Output Value": 2587.43, "Business Revenue": 2437.64, "Total Profits": 104.67, "Employed Persons": 11.71},
            {"Sector": "Smelting and Pressing of Non-ferrous Metals", "Enterprises": 660, "Output Value": 3023.90, "Business Revenue": 2910.44, "Total Profits": 99.07, "Employed Persons": 16.30},
            {"Sector": "Manufacturing of Metal Products", "Enterprises": 3320, "Output Value": 4918.96, "Business Revenue": 4730.51, "Total Profits": 311.66, "Employed Persons": 80.05},
            {"Sector": "Manufacturing of General Purpose Equipment", "Enterprises": 1467, "Output Value": 3237.58, "Business Revenue": 3127.16, "Total Profits": 177.35, "Employed Persons": 46.38},
            {"Sector": "Manufacturing of Special Purpose Equipment", "Enterprises": 1319, "Output Value": 1856.66, "Business Revenue": 1783.19, "Total Profits": 137.73, "Employed Persons": 33.92},
            {"Sector": "Manufacture of Automobile", "Enterprises": 620, "Output Value": 4707.60, "Business Revenue": 4714.55, "Total Profits": 433.17, "Employed Persons": 32.57},
            {"Sector": "Manufacturing of Electric Machinery and Equipment", "Enterprises": 4153, "Output Value": 10895.32, "Business Revenue": 10783.39, "Total Profits": 657.85, "Employed Persons": 180.15},
            {"Sector": "Manufacture of Computers, Communications and Other Electronic Equipment", "Enterprises": 4621, "Output Value": 25835.51, "Business Revenue": 24668.39, "Total Profits": 1105.92, "Employed Persons": 330.90},
            {"Sector": "Production and Supply of Electric Power and Heat Power", "Enterprises": 308, "Output Value": 5862.80, "Business Revenue": 5817.27, "Total Profits": 490.22, "Employed Persons": 21.13},
            {"Sector": "Production and Supply of Gas", "Enterprises": 77, "Output Value": 615.19, "Business Revenue": 594.42, "Total Profits": 50.70, "Employed Persons": 1.40},
        ]
    if year == 2023:
        data = [
            {"Sector": "Processing of Farm and Sideline Food", "Enterprises": 1338, "Output Value": 4328.56, "Business Revenue": 4770.2, "Total Profits": 107.5, "Employed Persons": 15.05},
            {"Sector": "Manufacture of Food", "Enterprises": 1007, "Output Value": 2180.43, "Business Revenue": 2398.02, "Total Profits": 232.25, "Employed Persons": 19.46},
            {"Sector": "Textile Industry", "Enterprises": 1756, "Output Value": 2257.43, "Business Revenue": 2136.08, "Total Profits": 113.79, "Employed Persons": 22.21},
            {"Sector": "Manufacture of Textile Garments, Footwear and Headgear", "Enterprises": 2484, "Output Value": 2409.95, "Business Revenue": 2209.83, "Total Profits": 97.41, "Employed Persons": 41.59},
            {"Sector": "Manufacture of Cultural, Educational, Sports and Entertainment Articles", "Enterprises": 2094, "Output Value": 4020.44, "Business Revenue": 4056.29, "Total Profits": 105.2, "Employed Persons": 47.22},
            {"Sector": "Petroleum, Coal and other Fuel Processing", "Enterprises": 123, "Output Value": 5493.51, "Business Revenue": 5599.09, "Total Profits": 98.21, "Employed Persons": 2.45},
            {"Sector": "Manufacture of Raw Chemical Materials and Chemical Products", "Enterprises": 3496, "Output Value": 7384.32, "Business Revenue": 7597.59, "Total Profits": 384.88, "Employed Persons": 34.71},
            {"Sector": "Manufacture of Medicines", "Enterprises": 642, "Output Value": 2017.4, "Business Revenue": 1937.89, "Total Profits": 249.9, "Employed Persons": 16.7},
            {"Sector": "Rubber and Plastic Products", "Enterprises": 6461, "Output Value": 6118.03, "Business Revenue": 5987.08, "Total Profits": 314.83, "Employed Persons": 77.72},
            {"Sector": "Nonmetal Mineral Products", "Enterprises": 3904, "Output Value": 6351.17, "Business Revenue": 6052.55, "Total Profits": 266.22, "Employed Persons": 49.24},
            {"Sector": "Smelting and Pressing of Ferrous Metals", "Enterprises": 592, "Output Value": 4591.48, "Business Revenue": 4621.68, "Total Profits": 90.44, "Employed Persons": 7.87},
            {"Sector": "Smelting and Pressing of Nonferrous Metals", "Enterprises": 1273, "Output Value": 3973.63, "Business Revenue": 4277.11, "Total Profits": 60.07, "Employed Persons": 14.55},
            {"Sector": "Metal Products", "Enterprises": 7166, "Output Value": 8794.14, "Business Revenue": 8610.65, "Total Profits": 379.24, "Employed Persons": 92.17},
            {"Sector": "Manufacture of General-purpose Machinery", "Enterprises": 4218, "Output Value": 6157.39, "Business Revenue": 6076.04, "Total Profits": 402.45, "Employed Persons": 59.94},
            {"Sector": "Manufacture of Special-purpose Machinery", "Enterprises": 4230, "Output Value": 5936.59, "Business Revenue": 5615.13, "Total Profits": 609.56, "Employed Persons": 65.35},
            {"Sector": "Manufacture of Automobile", "Enterprises": 1202, "Output Value": 12846.58, "Business Revenue": 13315.83, "Total Profits": 529.21, "Employed Persons": 49.11},
            {"Sector": "Manufacture of Electrical Machinery and Equipment", "Enterprises": 8463, "Output Value": 22192.47, "Business Revenue": 21702.98, "Total Profits": 1584.71, "Employed Persons": 174.15},
            {"Sector": "Manufacture of Communication Equipment, Computers and Other Electronic Equipment", "Enterprises": 9966, "Output Value": 47168.02, "Business Revenue": 47689.96, "Total Profits": 3628.09, "Employed Persons": 317.53},
            {"Sector": "Production and Supply of Electric Power and Heat Power", "Enterprises": 604, "Output Value": 10511.89, "Business Revenue": 10617.81, "Total Profits": 726.43, "Employed Persons": 17.11},
            {"Sector": "Production and Supply of Gas", "Enterprises": 324, "Output Value": 3075.62, "Business Revenue": 3166.36, "Total Profits": 145.8, "Employed Persons": 2.47},
        ]
    return pd.DataFrame(data)
    


