import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import datetime
import streamlit as st
import pandas as pd
import plotly.express as px

# --- USER AUTHENTICATION ---

names = ["admin", "visitor"]
usernames = ["admin", "visitor"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

credentials = {
        "usernames":{
            usernames[0]:{
                "name":names[0],
                "password":hashed_passwords[0]
                },
            usernames[1]:{
                "name":names[1],
                "password":hashed_passwords[1]
                }
            }
        }


authenticator = stauth.Authenticate(credentials, "indomarkt_dashboard", "abcdef",
                                    cookie_expiry_days=30)

name, authentication_status, usernames = authenticator.login(location="main")



# how many transaction within certain time

# the averate rate transaction in this certain time: year, month, day

# perbandingan dengan data yang lain pada tahun ini


class App:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    st.sidebar.markdown("""
                        Upload data-data terbaru disini
                        """)

    upload_button_visibility = "visible"

    # flour verkaufuebersicht
    flour_verkaufuebersicht_upload = st.sidebar.file_uploader("Upload flour verkaufübersicht excel data here!",
                                                              accept_multiple_files=False, type=['csv', 'xlsx'],
                                                              key="flour_verkauf",
                                                              label_visibility=upload_button_visibility)

    flour_verkaufuebersicht = pd.DataFrame()

    if flour_verkaufuebersicht_upload is not None:
        st.text("New Data Uploaded")
        flour_verkaufuebersicht = pd.read_excel(flour_verkaufuebersicht_upload)

    # flour topseller
    flour_topseller_upload = st.sidebar.file_uploader("Upload flour topseller excel data here!", accept_multiple_files=False,
                                                      type=['csv', 'xlsx'], key="flour_topseller",
                                                      label_visibility=upload_button_visibility)
    flour_topseller = pd.DataFrame()

    if flour_topseller_upload is not None:
        flour_topseller = pd.read_excel(flour_topseller_upload)

    flour_belege_upload = st.sidebar.file_uploader("Upload belege excel data here!", accept_multiple_files=False,
                                                   type=['csv', 'xlsx'], key="flour_belege",
                                                   label_visibility=upload_button_visibility)
    flour_belege = pd.DataFrame()

    if flour_belege_upload is not None:
        flour_belege = pd.read_excel(flour_belege_upload)

    prestashop_beliebt_artikel_upload = st.sidebar.file_uploader("Upload prestashop beliebt artikel excel data here!",
                                                                 accept_multiple_files=False,
                                                                 type=['csv', 'xlsx'], key="prestashop_beliebt_artikel",
                                                                 label_visibility=upload_button_visibility)
    prestashop_beliebt_artikel = pd.DataFrame()

    if prestashop_beliebt_artikel_upload is not None:
        prestashop_beliebt_artikel = pd.read_excel(prestashop_beliebt_artikel_upload)

    erloese_prestashop_upload = st.sidebar.file_uploader("Upload erloese prestashop excel data here!",
                                                         accept_multiple_files=False,
                                                         type=['csv', 'xlsx'], key="erloese_prestashop",
                                                         label_visibility=upload_button_visibility)
    erloese_prestashop = pd.DataFrame()

    if erloese_prestashop_upload is not None:
        erloese_prestashop = pd.read_excel(erloese_prestashop_upload)

    daterange_visibility = True

    if daterange_visibility:
        show_daterange = st.empty()

        daterange = show_daterange.date_input(label="Choose the daterange",
                                              value=(datetime.date(2020, 6, 1), datetime.date(2020, 7, 1)))
        if daterange is None:
            daterange("today")
        else:
            st.text(f"The choosen date {str(daterange[0])} - {str(daterange[1])} ")

    show = st.sidebar.selectbox("Choose the data", ["Flour Verkaufübersicht", "Flour Belege", "Erlöse PrestaShop", "PrestaShop Beliebteste Artikel", "Produkt Analyze"])

    def __init__(self):

        pass

    # Reconstruct the data of flour sale overview
    @st.cache_data(persist='disk')
    def construct_fv(_self):

        if _self.flour_verkaufuebersicht_upload is not None:
            st.text("Data Flour Übersicht has been uploaded")
            _self.flour_verkaufuebersicht = pd.read_excel(_self.flour_verkaufuebersicht_upload)
        else:
            flour_verkaufuebersicht_path = Path(__file__).parent / 'Indomarkt' / 'Flour' / 'Verkaufsübersicht' / 'export_articlessold_59e7472e57e9fa358c9c2c31__1655561202.xlsx'
            flour_verkaufuebersicht_path = "Indomarkt/Flour/Verkaufsübersicht/export_articlessold_59e7472e57e9fa358c9c2c31__1655561202.xlsx"
            _self.flour_verkaufuebersicht = pd.read_excel(flour_verkaufuebersicht_path)

        flour_verkaufuebersicht = _self.flour_verkaufuebersicht[
            ["Datum", "Nummer", "Name", "Gesamt Netto", "Gesamt Brutto"]].copy()
        flour_verkaufuebersicht['Tag'] = pd.DatetimeIndex(flour_verkaufuebersicht['Datum']).day
        flour_verkaufuebersicht['Monat'] = pd.DatetimeIndex(flour_verkaufuebersicht['Datum']).month
        flour_verkaufuebersicht['Jahr'] = pd.DatetimeIndex(flour_verkaufuebersicht['Datum']).year
        flour_verkaufuebersicht['Name'] = flour_verkaufuebersicht['Name'].str.lower().str.replace(',', '')
        flour_verkaufuebersicht['Nummer'] = flour_verkaufuebersicht['Nummer'].astype(str).copy()
        return flour_verkaufuebersicht

    @st.cache_data(persist='disk')
    def construct_ftp(_self):
        if _self.flour_topseller_upload is not None:
            st.text("Data Flour Topseller has been uploaded")
            _self.flour_topseller = pd.read_excel(_self.flour_topseller_upload)
        else:
            flour_topseller_path = Path(__file__).parent / 'Indomarkt' / 'Flour' / 'Topseller' / 'topseller_1655561028_topseller_20150101_20220618.xlsx'
            flour_topseller_path = "Indomarkt/Flour/Topseller/topseller_1655561028_topseller_20150101_20220618.xlsx"
            _self.flour_topseller = pd.read_excel(flour_topseller_path)

    # Reconstruct the data of flour receipt
    @st.cache_data(persist='disk')
    def construct_fb(_self):

        if _self.flour_belege_upload is not None:
            st.text("Data Flour Belege has been uploaded")
            _self.flour_belege = pd.read_excel(_self.flour_belege_upload)
        else:
            flour_belege_path = Path(__file__).parent / 'Indomarkt' / 'Flour' / 'Belege' / 'export_documents_1655561149.xlsx'
            flour_belege_path = "Indomarkt/Flour/Belege/export_documents_1655561149.xlsx"
            _self.flour_belege = pd.read_excel(flour_belege_path)

        _self.flour_belege['Datum'] = pd.to_datetime(_self.flour_belege['Datum'], utc=True)
        flour_belege = _self.flour_belege[
            ['Datum', 'Nummer', 'Dokumententyp', 'Kundennummer', 'Netto', 'Brutto', 'Kasse']].copy()
        flour_belege['Zeit'] = flour_belege['Datum']
        flour_belege['Datum'] = pd.DatetimeIndex(flour_belege['Datum']).date
        flour_belege['Tag'] = pd.DatetimeIndex(flour_belege['Datum']).day
        flour_belege['Monat'] = pd.DatetimeIndex(flour_belege['Datum']).month
        flour_belege['Jahr'] = pd.DatetimeIndex(flour_belege['Datum']).year
        flour_belege['Datum'] = pd.to_datetime(flour_belege['Datum'], utc=False)
        return flour_belege

    @st.cache_data(persist='disk')
    def construct_pba(_self):

        if _self.prestashop_beliebt_artikel_upload is not None:
            st.text("Data PrestaShop Beliebteste Artikel has been uploaded")
            _self.prestashop_beliebt_artikel = pd.read_excel(_self.prestashop_beliebt_artikel_upload)
        else:
            prestashop_beliebt_artikel_path = Path(__file__).parent / 'Indomarkt' / 'Statistiken' / 'Beliebteste Artikel' / 'Beliebteste Artikel - 1655460124.xlsx'
            prestashop_beliebt_artikel_path = "Indomarkt/Statistiken/Beliebteste Artikel/Beliebteste Artikel - 1655460124.xlsx"
            _self.prestashop_beliebt_artikel = pd.read_excel(prestashop_beliebt_artikel_path)

        _self.prestashop_beliebt_artikel['Artikel-Nr.'] = _self.prestashop_beliebt_artikel['Artikel-Nr.'].fillna(
            0).astype(int).astype(str).copy()
        _self.prestashop_beliebt_artikel['Marke'] = \
            _self.prestashop_beliebt_artikel['Name'].str.split(',', expand=True)[
                0].str.lower().copy()
        _self.prestashop_beliebt_artikel['Umsatz'] = _self.prestashop_beliebt_artikel['Umsatz']. \
            str.replace('\xa0€', '').str.replace('.', '', regex=True).str.replace(',', '.').astype(float).copy()

        return _self.prestashop_beliebt_artikel.copy()

    @st.cache_data(persist='disk')
    def construct_ep(_self):

        if _self.erloese_prestashop_upload is not None:
            st.text("Data Statistiken Katalog has been uploaded")
            _self.erloese_prestashop = pd.read_excel(_self.erloese_prestashop_upload)
        else:
            erloese_prestashop_path = Path(__file__).parent / 'Indomarkt' / 'Statistiken' / 'Statistiken Katalog' / 'Erlöse Prestashop.xlsx'
            erloese_prestashop_path = "Indomarkt/Statistiken/Statistiken Katalog/Erlöse Prestashop.xlsx"
            _self.erloese_prestashop = pd.read_excel(erloese_prestashop_path)

        _self.erloese_prestashop['Erlöse'] = _self.erloese_prestashop['Erlöse'].astype(str).str.replace('\xa0€',
                                                                                                        '').str.replace(
            ',', '.')
        _self.erloese_prestashop['Erlöse'] = _self.erloese_prestashop['Erlöse'].astype(float).copy()
        _self.erloese_prestashop['Tag'] = pd.DatetimeIndex(_self.erloese_prestashop['Datum']).day
        _self.erloese_prestashop['Monat'] = pd.DatetimeIndex(_self.erloese_prestashop['Datum']).month
        _self.erloese_prestashop['Jahr'] = pd.DatetimeIndex(_self.erloese_prestashop['Datum']).year
        return _self.erloese_prestashop[
            ['Datum', 'Tag', 'Monat', 'Jahr', 'Anmeldungen', 'Bestellungen', 'Gekaufte Artikel', 'Erlöse']].copy()

    def show_fv(self):
        st.header("Data of Flour Verkaufsübersicht / of overall Selling")
        # masukan tanggal flour_verkaufuebersicht_chart = flour_verkaufuebersicht.loc[(flour_verkaufuebersicht[
        # "Jahr"] == jahr_input) & (flour_verkaufuebersicht["Monat"] == monat_input)]
        first_date = self.daterange[0]
        last_date = self.daterange[1]
        flour_verkaufuebersicht_chart = self.construct_fv().loc[
            (self.construct_fv().Datum >= str(first_date)) & (self.construct_fv().Datum <= str(last_date))]

        # flour_verkaufuebersicht_chart = flour_verkaufuebersicht.loc[(flour_verkaufuebersicht['Monat'] == monat)&(
        # flour_verkaufuebersicht['Jahr'] == number)].sort_values(by='Gesamt Netto', ascending=False) Analyse the
        # time series of sale overview on the store
        if flour_verkaufuebersicht_chart.empty:
            st.warning("The requested data isn't available")
        else:

            st.line_chart(flour_verkaufuebersicht_chart, x="Datum", y=["Gesamt Netto", "Gesamt Brutto"])
            st.header(f"The result of data from {first_date} to {last_date} ")
            # looking for the average rate, the higgest and total of netto
            fvc_mean = flour_verkaufuebersicht_chart['Gesamt Netto'].mean().round(decimals=2)
            st.text(f"Average netto in this timerange is {fvc_mean} €")
            st.text(f"The biggest netto : {flour_verkaufuebersicht_chart['Gesamt Netto'].max()} €")
            st.text(f"Netto Total : {flour_verkaufuebersicht_chart['Gesamt Netto'].sum()} €")

            # looking for the highest netto of product
            fvc_product_max = flour_verkaufuebersicht_chart.loc[
                flour_verkaufuebersicht_chart['Gesamt Netto'] == flour_verkaufuebersicht_chart[
                    'Gesamt Netto'].max()].copy()
            st.text(f"Products sold at the highest price:")
            fvc_product_max["Nummer"] = fvc_product_max["Nummer"].astype(str)
            st.dataframe(
                fvc_product_max[["Datum", "Nummer", "Name", "Gesamt Netto", "Gesamt Brutto"]].reset_index(drop=True))

            barier_number = round(st.number_input(label=' Input the value here! ', value=fvc_mean), 2)
            st.text(f"The products sold above {barier_number}")
            fvc_above = flour_verkaufuebersicht_chart.loc[
                flour_verkaufuebersicht_chart['Gesamt Netto'] > barier_number].reset_index(drop=True).copy()
            fvc_above["Nummer"] = fvc_above["Nummer"].astype(str)
            fvc_above_view = st.button("Show the table")
            if fvc_above_view == True:
                st.text(f"The amount of data: {fvc_above.Name.count()}")
                st.dataframe(fvc_above[["Datum", "Nummer", "Name", "Gesamt Netto", "Gesamt Brutto"]])

            st.subheader("Pie Chart")
            pie_show_number = st.number_input("Number of products to view", value=10)
            st.text(f"Top {pie_show_number} Products with net worth above {barier_number} €")
            pie_data = flour_verkaufuebersicht_chart[["Name", "Gesamt Netto"]].groupby(['Name']).sum(
                numeric_only=True).sort_values(by='Gesamt Netto', ascending=False)[:pie_show_number]
            pie_data['Name'] = pie_data.index
            plotly_fig = px.pie(pie_data, values='Gesamt Netto', names='Name', title=f'Top {pie_show_number}', hole=.3,
                                color_discrete_sequence=px.colors.sequential.Aggrnyl)
            st.text(f"Overal Net Total {round(pie_data['Gesamt Netto'].sum(), 2)} € ")
            st.plotly_chart(plotly_fig, use_container_width=True)
            # plotly_fig.to_image() plotly_fig.write_image("plot/plot.png") # still error: FileNotFoundError: [Errno
            # 2] No such file or directory: 'plot/plot.png' st.dataframe(flour_verkaufuebersicht_chart.sort_values(
            # by='Gesamt Netto', ascending=False).reset_index(drop=True))
            if st.button("Show the table"):
                st.dataframe(pie_data.reset_index(drop=True))

    def show_fb(self):
        st.header("Data of Flour Belege / Transactions in the shop")
        first_date = self.daterange[0]
        last_date = self.daterange[1]
        # Analyse the time series of receipt on the store
        fb_data = self.construct_fb().loc[
            (self.construct_fb().Datum >= str(first_date)) & (self.construct_fb().Datum <= str(last_date))].reset_index(
            drop=True).copy()
        st.text(f"Amount of transaction {fb_data.index.size}")
        st.text(f"Total amount of transaction {fb_data.Netto.sum()} €")
        st.text(f"Averate amount of transaction {round(fb_data.Netto.mean(), 2)} €")
        #st.text(f"Daily average transaction {0}")  # formula is still unknown

        st.line_chart(fb_data, x="Datum", y=['Netto', 'Brutto'])
        nama_hari = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        fb_data['Wochentag'] = fb_data.Datum.dt.dayofweek
        fb_data['Hari'] = fb_data.Datum.dt.dayofweek.map(
            {0: nama_hari[0], 1: nama_hari[1], 2: nama_hari[2], 3: nama_hari[3], 4: nama_hari[4], 5: nama_hari[5],
             6: nama_hari[6]})

        fb_data_wochentag = fb_data[['Wochentag', 'Hari', 'Datum', 'Nummer', 'Netto', 'Brutto']].groupby(
            ['Wochentag', 'Hari']).sum(numeric_only=True)
        st.dataframe(fb_data_wochentag)

        # time in senin, selasa, rabu, kamis, jumat, sabtu,
        fb_data_senin = fb_data[['Wochentag', 'Hari', 'Datum', 'Zeit', 'Nummer', 'Netto', 'Brutto']].loc[
            fb_data.Hari == 'Monday']
        hari_pilihan = st.selectbox("Choose the day", nama_hari)
        fb_data_senin_tanggal = fb_data_senin.loc[fb_data.Hari == hari_pilihan]['Datum']
        # jam berapa saja paling banyak terjadi transaksi
        if fb_data_senin_tanggal.drop_duplicates().empty:
            st.warning("Data is unavailable")
        else:

            for tanggal in fb_data_senin_tanggal.drop_duplicates().tolist():
                st.text(f"Transaction on {hari_pilihan} {str(tanggal)}")
                line_chart_senin = fb_data_senin.loc[fb_data_senin.Datum == tanggal][['Zeit', 'Netto', 'Brutto']]
                st.line_chart(line_chart_senin, x='Zeit', y=['Netto', 'Brutto'])

        fb_data_datum = fb_data[['Hari', 'Datum', 'Nummer', 'Netto', 'Brutto']].groupby(['Datum']).sum(
            numeric_only=True).sort_values(by='Netto', ascending=False)

        # merge data based on datum to show day
        st.text(f"The date with the lowest transaction {fb_data_datum.index[0]} ")
        st.text(f"The date with the lowest transaction {fb_data_datum.index[-1]} ")
        st.dataframe(fb_data_datum)
        # tunjukan barang apa saja dalam tanggal tertentu dengan membandingkan data verkaufübersicht dan belege

        flour_verkaufuebersicht = self.construct_fv()[["Datum", "Nummer", "Name", "Gesamt Netto", "Gesamt Brutto"]]
        flour_verkaufuebersicht['Tag'] = pd.DatetimeIndex(flour_verkaufuebersicht['Datum']).day
        flour_verkaufuebersicht['Monat'] = pd.DatetimeIndex(flour_verkaufuebersicht['Datum']).month
        flour_verkaufuebersicht['Jahr'] = pd.DatetimeIndex(flour_verkaufuebersicht['Datum']).year
        flour_verkaufuebersicht['Name'] = flour_verkaufuebersicht['Name'].str.lower().str.replace(',', '')
        fv_fb_datum = flour_verkaufuebersicht.loc[flour_verkaufuebersicht.Datum == fb_data_datum.index[0]].reset_index(
            drop=True)
        fv_fb_datum_produkt = fv_fb_datum[['Datum', 'Nummer', 'Name', 'Gesamt Netto', 'Gesamt Brutto']].groupby(
            ['Name', 'Gesamt Netto']).sum(numeric_only=True).sort_values(by='Gesamt Netto', ascending=False)
        st.dataframe(fv_fb_datum_produkt)

        fb_data['Bulan'] = fb_data['Monat'].map(
            {1: 'January',
             2: 'February',
             3: 'March',
             4: 'April',
             5: 'May',
             6: 'June',
             7: 'July',
             8: 'August',
             9: 'September',
             10: 'October',
             11: 'November',
             12: 'Desember'
             })

        fb_data_monat = fb_data[['Monat', 'Bulan', 'Jahr', 'Netto', 'Brutto']].groupby(['Monat', 'Jahr']).sum(
            numeric_only=True)
        if st.button("Total monthly transaction ") is True:
            st.dataframe(fb_data_monat)
            # rata-rata transaksi bulanan
            # kenapa tingkat belanja di bulan tertentu bisa tinggi, perlu netapin seasonal date

    def show_pba(self):
        st.header("Data of PrestaShop Beliebt Artikel")
        pba_data = self.construct_pba()
        st.dataframe(pba_data)
        # mencari produk dengan omset tertinggi
        total_omset = round(pba_data['Umsatz'].sum(), 2)
        highest_produk = pba_data['Name'].loc[pba_data['Umsatz'] == pba_data['Umsatz'].max()].item()
        highest_umsatz = pba_data['Umsatz'].max()
        menge_highest_produk = pba_data['Verkaufte Menge'].loc[pba_data['Umsatz'] == pba_data['Umsatz'].max()].item()
        difference_pba = round((highest_umsatz / total_omset), 2) * 100
        # mencari produk dengan nama yang sama di data yang lain
        st.markdown(f"""
        ### Product with the highest revenue
        {highest_produk}
        with revenue of {highest_umsatz} 
        by amount of {menge_highest_produk} products sold
        with {difference_pba} % of {total_omset} € .
        """)
        above_average_product_menge = pba_data.loc[
            pba_data['Verkaufte Menge'] >= pba_data['Verkaufte Menge'].mean()].copy()
        st.text(f"Products above average amount of sold items {above_average_product_menge.size} " +
                f"with average value of {round(pba_data['Verkaufte Menge'].mean(), 2)}")

        above_average_product_preis = pba_data.loc[
            pba_data['Umsatz'] >= pba_data['Umsatz'].mean()].copy()
        st.text(f"Products above revenue average {above_average_product_preis.size} " +
                f"with average value of{round(pba_data['Umsatz'].mean(), 2)} €")

        # opsi mencari produk lain di dalam omset berdasarkan merek
        marke_option = st.selectbox("Choose the brand",
                                    options=pba_data['Marke'].drop_duplicates().to_list())
        option_result = pba_data.loc[pba_data['Marke'] == marke_option].reset_index(
            drop=True).sort_values(by='Umsatz', ascending=False)
        st.dataframe(option_result)

    def show_ep(self):
        st.header("Data of Erlöse PrestaShop")
        ep_data = self.construct_ep().loc[
            (self.construct_ep()['Datum'] >= pd.to_datetime(self.daterange[0])) & (
                    self.construct_ep()['Datum'] <= pd.to_datetime(self.daterange[1]))][
            ['Datum', 'Tag', 'Monat', 'Jahr', 'Erlöse']]
        st.line_chart(ep_data, x="Datum", y="Erlöse")
        st.dataframe(ep_data)

    # identify if the product has certain seasonal penetration exp: tolak angin is high on sale in october because winter time
    def identify_season(self):

        pass

    search_result_prestashop = False
    search_result_flour = False

    # analisa produk dengan memilih produk yang tersedia
    # improve visualisasi diagram pakai bar diagram untuk perbulan dan line chart time series.
    @st.cache_data(persist='disk', experimental_allow_widgets=True)
    def product_analyze(_self):
        _self.daterange_visibility = False

        pba_data = _self.construct_pba()
        fv_data = _self.construct_fv()
        # by input only certain alphabet the script will help to find relevant products contain the character
        search_word = str(st.text_input("Input a product name here")).lower()
        # the data will be searched in prestashop beliebt artikel data
        search_result = pba_data.loc[pba_data['Name'].str.lower().str.contains(search_word, regex=True)]
        st.text(
            f"The searching result with the {search_word} are {search_result.size} products in PrestaShop Beliebt Artikel")
        _self.search_result_prestashop = st.button("Show the detail", key='search_result_prestashop')
        if _self.search_result_prestashop:
            st.dataframe(search_result.reset_index(drop=True))

        # the data will also be searched in flour verkaufuebersicht

        search_result_flour = fv_data.loc[fv_data['Name'].fillna("").str.lower().str
        .contains(search_word)][["Nummer", "Name", "Gesamt Netto", "Gesamt Brutto"]] \
            .groupby(["Nummer", "Name"]).sum(numeric_only=True)

        st.text(f" The searching result with the {search_word} are {search_result_flour.size} products in Flour Verkaufsübersicht")
        _self.search_result_flour = st.button("Show the detail", key='search_result_flour')
        if _self.search_result_flour:
            search_result_flour['Name'] = search_result_flour.index
            st.dataframe(search_result_flour.reset_index(drop=True))

        st.markdown(f"""
                    
        To search a product in Flour Verkaufübersicht, you can input the name or article nummer.
                    
        ## Searching Result
        """)

        produk_detail = st.selectbox("Choose product", search_result['Name']
                                     .str.lower().str.replace(",", "").to_list())
        nummer_list = search_result['Artikel-Nr.'].astype(str).drop_duplicates().to_list()
        produk_detail_nummer = st.selectbox("Choose article nummer", nummer_list)

        st.write("Article number affiliated with PrestaShop and Flour")
        produk_detail_nummer_example = search_result.loc[
            search_result['Name'].fillna("kosong").str.lower().str.replace(",", "").str.match(str(produk_detail))][
            'Artikel-Nr.'].astype(str)
        st.write(produk_detail_nummer_example)

        # detail_produk_result_flour = fv_data.loc[(fv_data['Name'].fillna("kosong").str.lower().str.contains(str(produk_detail))) | (fv_data['Nummer'].str.contains(produk_detail_nummer))].reset_index(drop=True)
        search_parameter1 = fv_data['Name'].fillna("empty").str.lower().str.contains(str(produk_detail))
        search_parameter2 = fv_data['Nummer'].str.contains(produk_detail_nummer, regex=True)
        st.text(f"Searching Parameter {produk_detail} atau {produk_detail_nummer}")
        if produk_detail_nummer == "0":
            detail_produk_result_flour = fv_data.loc[
                (search_parameter1) & (search_parameter2)].reset_index(drop=True)
        else:
            detail_produk_result_flour = fv_data.loc[
                (search_parameter1) | (search_parameter2)].reset_index(drop=True)

        st.text(
            f" Total of sold products {detail_produk_result_flour.size} items with net sales {round(detail_produk_result_flour['Gesamt Netto'].sum(), 2)} €")

        # ketersediaan data

        st.text(f"Data is available from {detail_produk_result_flour['Datum'].min()} to" +
                f" {detail_produk_result_flour['Datum'].max()}")

        st.dataframe(detail_produk_result_flour)

        st.header("Monthly Diagram FLour Verkaufübersicht")
        detail_produk_result_flour['Monatname'] = detail_produk_result_flour['Monat'].sort_values(ascending=False).map(
            {1: 'Januari',
             2: 'Februari',
             3: 'Maret',
             4: 'April',
             5: 'Mei',
             6: 'Juni',
             7: 'Juli',
             8: 'Agustus',
             9: 'September',
             10: 'Oktober',
             11: 'November',
             12: 'Desember'
             })
        if st.button("Annual Sales"):
            # inform monthly total of netto and brutto
            fig = px.bar(detail_produk_result_flour, x='Jahr', y=['Gesamt Netto', 'Gesamt Brutto'],
                         title=f"Penjualan produk {produk_detail} di setiap tahun ")
            st.plotly_chart(fig, use_container_width=True)

        if st.button("Monthly Sales"):
            fig = px.bar(detail_produk_result_flour, x='Monatname', y=['Gesamt Netto', 'Gesamt Brutto'],
                         title=f"Penjualan produk {produk_detail} bulanan ")
            fig.update_layout(barmode='stack', xaxis={'categoryorder': 'array',
                                                      'categoryarray': ['Januari', 'Februari', 'Maret', 'April', 'Mei',
                                                                        'Juni', 'Juli', 'Agustus', 'September',
                                                                        'Oktober', 'November', 'Desember']})
            st.plotly_chart(fig, use_container_width=True)

        # summary terkait produk bulanan terkait seasonal produk
        if st.button("Sales based on the date"):
            fig = px.bar(detail_produk_result_flour, x='Tag', y=['Gesamt Netto', 'Gesamt Brutto'],
                         title=f"Product selling {produk_detail}")
            st.plotly_chart(fig, use_container_width=True)

        nama_hari = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        detail_produk_result_flour['Wochentag'] = detail_produk_result_flour.Datum.dt.dayofweek
        detail_produk_result_flour['Hari'] = detail_produk_result_flour.Datum.dt.dayofweek.map(
            {0: nama_hari[0], 1: nama_hari[1], 2: nama_hari[2], 3: nama_hari[3], 4: nama_hari[4], 5: nama_hari[5],
             6: nama_hari[6]})

        if st.button("Penjualan Harian"):
            detail_produk_result_flour = detail_produk_result_flour.sort_values(by='Wochentag', ascending=False)
            fig = px.bar(detail_produk_result_flour, x='Hari', y=['Gesamt Netto', 'Gesamt Brutto'],
                         title=f"{produk_detail} in Daily Sales")

            fig.update_layout(barmode='stack', xaxis={'categoryorder': 'array',
                                                      'categoryarray': nama_hari})
            st.plotly_chart(fig, use_container_width=True)

        # memprediksi atau merekomendasi jumlah produk yang sebaiknya dibeli pada pengadaan selanjutnya

    # recommending product based on researching which product bring most profit and
    # when also where it was purchased at most

    def product_recomendation(self):

        # Analysis available time in data

        # how many years in this dataset
        # how high is average yearly
        # how many month in this dataset

        pass

    def menu(self):

        if self.show == "Flour Verkaufübersicht":
            self.show_fv()
        if self.show == "PrestaShop Beliebteste Artikel":
            self.show_pba()
        if self.show == "Flour Belege":
            self.show_fb()
        if self.show == "Erlöse PrestaShop":
            self.show_ep()
        if self.show == "Produkt Analyze":
            self.daterange_visibility = False
            self.product_analyze()


if __name__ == "__main__":
    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter  your username and password")

    if authentication_status:
        ds = App()
        ds.menu()
