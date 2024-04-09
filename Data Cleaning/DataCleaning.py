import pandas as pd
import pathlib

DATA_PATH: pathlib.Path = pathlib.Path("C:/Users/umitc/Desktop/python_vscode/Aselsan proje/proje/data/dataset_train.csv")
df: pd.DataFrame = pd.read_csv(DATA_PATH)

#print(df.head(15))

df_processed: pd.DataFrame = df.drop(columns=["Pressure_switch", "gpsLat", "gpsLong", "gpsQuality"])\
    .astype({
        "timestamp" : "datetime64[ns]",
        "TP2" : "float16",
        "TP3" : "float16",
        "H1"  : "float16",
        "DV_pressure" : "float16",
        "Reservoirs" : "float16",
        "Oil_temperature" : "float16",
        "Flowmeter" : "float16",
        "Motor_current" : "float16",
        "COMP" : "bool",
        "DV_eletric" : "bool",
        "Towers" : "bool",
        "MPG" : "bool",
        "LPS" : "bool",
        "Oil_level" : "bool",
        "Caudal_impulses" : "bool",
        "gpsSpeed" : "int16",   
    })

#df_processed.info()

OUT_PATH: pathlib.Path = pathlib.Path("C:/Users/umitc/Desktop/python_vscode/Aselsan proje/proje/data/")
df_processed.to_feather(OUT_PATH / "Processed.feather")