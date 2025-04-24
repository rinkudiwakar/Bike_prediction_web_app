import pickle
import os
from datetime import datetime
import pandas as pd
import numpy as np
import xgboost as xgb

class Inference:
    def __init__(self, model_path: str, sc_path: str):
        if not os.path.exists(model_path) or not os.path.exists(sc_path):
            raise FileNotFoundError(
                f"Model not found at {model_path} or scaler not found at {sc_path}"
            )
        self.model  = pickle.load(open(model_path,  'rb'))
        self.scaler = pickle.load(open(sc_path,     'rb'))
        if isinstance(self.model, (xgb.XGBRegressor, xgb.XGBClassifier)):
            self.model.set_params(tree_method='hist')
            
    def _parse_date(self, date_str: str) -> dict:
        dt = datetime.strptime(date_str, "%d/%m/%Y")
        return {
            "day":     dt.day,
            "month":   dt.month,
            "year":    dt.year,
            "weekday": dt.strftime("%A"),
        }

    def _one_hot_season(self, season: str) -> pd.DataFrame:
        # only the seasons you trained on
        cols = ["Spring", "Summer", "Winter"]
        df   = pd.DataFrame([[0]*len(cols)], columns=cols)
        if season in cols:
            df.at[0, season] = 1
        return df

    def _one_hot_weekday(self, weekday: str) -> pd.DataFrame:
        # only the weekdays you trained on
        cols = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Saturday", "Sunday"]
        df   = pd.DataFrame([[0]*len(cols)], columns=cols)
        if weekday in cols:
            df.at[0, weekday] = 1
        return df

    def preprocess(self, data: dict) -> pd.DataFrame:
        """
        data must contain:
          date (DD/MM/YYYY), hour, temperature, humidity,
          wind_speed, visibility, solar_radiation,
          rainfall, snowfall, holiday, seasons, functioning_day
        """
        d = self._parse_date(data["date"])
        basic = {
            "Hour":                    data["hour"],
            "Temperature(°C)":         data["temperature"],
            "Humidity(%)":             data["humidity"],
            "Wind speed (m/s)":        data["wind_speed"],
            "Visibility (10m)":        data["visibility"],
            "Solar Radiation (MJ/m2)": data["solar_radiation"],
            "Rainfall(mm)":            data["rainfall"],
            "Snowfall (cm)":           data["snowfall"],
            "Holiday":                 1 if data["holiday"] == "Holiday" else 0,
            "Functioning Day":         1 if data["functioning_day"] == "Yes" else 0,
            "Day":                     d["day"],
            "Month":                   d["month"],
            "Year":                    d["year"],
        }
        df_basic  = pd.DataFrame([basic])
        df_season = self._one_hot_season(data["seasons"])
        df_weekday= self._one_hot_weekday(d["weekday"])
        df = pd.concat([df_basic, df_season, df_weekday], axis=1)

        # Enforce exact feature order that your scaler expects:
        expected = list(self.scaler.feature_names_in_)
        return df[expected]

    def predict(self, data: dict) -> float:
        """
        Accepts the JSON dict straight from Flask:
        result = infer.predict(request.get_json())
        """
        df     = self.preprocess(data)
        scaled = self.scaler.transform(df)
        pred   = self.model.predict(scaled)
        return float(pred[0])


if __name__ == "__main__":
    # CLI mode
    BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    model_path  = os.path.join(BASE, "Models", "xgboost_regressor_r2_0_917_v1.pkl")
    scaler_path = os.path.join(BASE, "Models",  "sc.pkl")
    inf = Inference(model_path, scaler_path)

    payload = {
        "date":            input("Date (DD/MM/YYYY): "),
        "hour":            int(input("Hour (0-23): ")),
        "temperature":     float(input("Temperature (°C): ")),
        "humidity":        float(input("Humidity (%): ")),
        "wind_speed":      float(input("Wind speed (m/s): ")),
        "visibility":      float(input("Visibility (10m): ")),
        "solar_radiation": float(input("Solar radiation (MJ/m2): ")),
        "rainfall":        float(input("Rainfall (mm): ")),
        "snowfall":        float(input("Snowfall (cm): ")),
        "holiday":         input("Holiday? (Holiday/No Holiday): "),
        "seasons":         input("Season (Spring, Summer, Winter): "),
        "functioning_day": input("Functioning day? (Yes/No): "),
    }
    print(f"Predicted rentals: {round(inf.predict(payload))}")
