import pandas as pd
import sqlite3

class CreateMinardDB:
    def __init__(self):
        # 載入欄位資料
        with open("data/minard.txt") as f:
            lines = f.readlines() # 將檔案中的每一行都讀進來，並以 list 形式儲存
        column_names = lines[2].split()

        #調整欄位內容
        patterns_to_be_replace = {"(","$",")",","}
        adjusted_column_names = []
        for column_name in column_names:
            for pattern in patterns_to_be_replace:
                if pattern in column_name:
                    column_name = column_name.replace(pattern,"")
            adjusted_column_names.append(column_name)

        #將欄位名稱分成三部分
        self.lines = lines
        self.column_names_city = adjusted_column_names[:3]
        self.column_names_temperature = adjusted_column_names[3:7]
        self.column_names_troop = adjusted_column_names[7:]

    #載入城市資料(文字檔6~25列，資料皆正常)
    def create_city_dataframe(self):
        i = 6
        longitudes, latitudes, cities = [], [], [] 
        while i <= 25:
            long, lat, city = self.lines[i].split()[:3]
            longitudes.append(float(long))
            latitudes.append(float(lat))
            cities.append(city)
            i += 1
        city_data = (longitudes, latitudes, cities)
        city_df = pd.DataFrame() # 建立空的 DataFrame
        for column_name, data in zip(self.column_names_city, city_data):
            city_df[column_name] = data
        return city_df
 
    #載入氣溫資料(資料有缺的情況)
    def create_temperature_dataframe(self):
        i = 6 
        longitudes, temperatures, days, dates = [], [], [], []
        while i <= 14:
            lines_split = self.lines[i].split()
            longitudes.append(float(lines_split[3]))
            temperatures.append(int(lines_split[4]))
            days.append(int(lines_split[5]))
            if i == 10:
                dates.append("Nov 24")
            else:
                dates_str = lines_split[6] + " " + lines_split[7] #原本的date欄位因切割變成兩個欄位
                dates.append(dates_str)
            i += 1 
        temperature_data = (longitudes, temperatures, days, dates)
        temperature_df = pd.DataFrame()
        for colume_name, data in zip(self.column_names_temperature, temperature_data):
            temperature_df[colume_name] = data
        return temperature_df

    #載入軍隊資料
    def create_troop_dataframe(self):
        i = 6 
        longitudes, latitudes, survivals, directions, divisions = [], [], [], [], []
        while i <= 53:
            lines_split = self.lines[i].split()
            longitudes.append(float(lines_split[-5]))
            latitudes.append(float(lines_split[-4]))
            survivals.append(int(lines_split[-3]))
            directions.append(lines_split[-2])
            divisions.append(int(lines_split[-1]))
            i += 1
        troop_data = (longitudes, latitudes, survivals, directions, divisions)
        troop_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_troop, troop_data):
            troop_df[column_name] = data
        return troop_df

    # 建立資料庫
    def create_database(self):       
        connection = sqlite3.connect("data/minard.db")
        city_df = self.create_city_dataframe()
        temperature_df = self.create_temperature_dataframe()
        troop_df = self.create_troop_dataframe()
        df_dict = {
            "cities": city_df,
            "temperatures": temperature_df,
            "troops": troop_df
        }
        for k, v in df_dict.items():
            v.to_sql(name=k, con=connection, index=False, if_exists="replace")

create_minard_db = CreateMinardDB()
create_minard_db.create_database()