import streamlit as st
import pandas as pd
import datetime

class Resource:

    data = pd.DataFrame()
    daterange = st.date_input("Masukan Tanggal", value=(datetime.date(2020, 6, 1), datetime.date(2020, 7, 1)))
    def __init__(self):
        pass

    @st.cache_data
    def load_resource(_self):
        _self.data = pd.read_excel(
            "Indomarkt/Flour/Verkaufsübersicht/export_articlessold_59e7472e57e9fa358c9c2c31__1655561202.xlsx")

        data = _self.data[["Datum", "Nummer", "Name", "Gesamt Netto", "Gesamt Brutto"]].copy()
        return data

    def view_resource(self):
        data = self.load_resource()
        data = data.loc[(data.Datum >= str(self.daterange[0])) & (data.Datum <= str(self.daterange[1]))]
        st.dataframe(data)
        st.line_chart(data, x="Datum", y=["Gesamt Netto", "Gesamt Brutto"])



if __name__ == "__main__":
    trial = Resource()
    trial.view_resource()