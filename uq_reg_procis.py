# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 08:42:54 2025

@author: larab
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 10:38:41 2024

@author: Lara Buljan
"""

import plotly
import plotly.graph_objects as go
import plotly.io as pio
from plotly.offline import plot
#import plotly.dashboard_objs as dashboard_objs
import IPython.display
#from IPyhton.display import Image

from datetime import datetime

from os import listdir
from os.path import isfile, join

import pandas as pd


def graf_radna_jalova(df, unit):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Vrijeme"],
        y=df[f"{unit}_RADNA_SNAGA_GENERATORA"],
        mode="lines",
        name=f"RADNA SNAGA GENERATORA {unit} [MW]",
        line=dict(color="red")
        ))

    fig.add_trace(go.Scatter(
        x=df["Vrijeme"],
        y=df[f"{unit}_JALOVA_SNAGA_GENERATORA"],
        mode="lines",
        name=f"JALOVA SNAGA GENERATORA {unit} [Mvar]",
        line=dict(color="blue"),
        yaxis="y2"
        ))

    fig.update_layout(
        title=f"Radna i jalova snaga generatora {unit}",
        xaxis_title="Vrijeme",
        template="plotly_white",
        legend_title="Legenda",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True,
                   title="Pg [MW]",
                   titlefont=dict(color="red"),
                   tickfont=dict(color="red")),
        yaxis2=dict(showgrid=True,
                    title="Qg [Mvar]",
                    titlefont=dict(color="blue"),
                    tickfont=dict(color="blue"),
                    overlaying="y",
                    side="right")
        )
    return fig


def graf_naponi_gen(df, unit):
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df["Vrijeme"],
        y=df[f"{unit}_NAPON_GENERATORA_UL1L2"],
        mode="lines",
        name=f"NAPON GENERATORA {unit} - UL1L2 [V]",
        line=dict(color="blue")))

    fig.add_trace(go.Scatter(
        x=df["Vrijeme"],
        y=df[f"{unit}_NAPON_GENERATORA_UL2L3"],
        mode="lines",
        name=f"NAPON GENERATORA {unit} - UL2L3 [V]",
        line=dict(color="red")))

    fig.add_trace(go.Scatter(
        x=df["Vrijeme"],
        y=df[f"{unit}_NAPON_GENERATORA_UL3L1"],
        mode="lines",
        name=f"NAPON GENERATORA {unit} - UL3L1 [V]",
        line=dict(color="green")))

    fig.update_layout(
        title=f"Naponi generatora {unit}",
        xaxis_title="Timestamp",
        yaxis_title="Ug [V]",
        template="plotly_white",
        legend_title="Legenda",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
        )
    return fig


def graf_struje_gen(df, unit):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Vrijeme"],
        y=df[f"{unit}_STRUJA_GENERATORA_IL1"],
        mode="lines",
        name=f"STRUJA GENERATORA {unit} - IL1 [A]",
        line=dict(color="blue")))

    fig.add_trace(go.Scatter(
        x=df["Vrijeme"],
        y=df[f"{unit}_STRUJA_GENERATORA_IL2"],
        mode="lines",
        name=f"STRUJA GENERATORA {unit} - IL2 [A]",
        line=dict(color="red")))

    fig.add_trace(go.Scatter(
        x=df["Vrijeme"],
        y=df[f"{unit}_STRUJA_GENERATORA_IL3"],
        mode="lines",
        name=f"STRUJA GENERATORA {unit} - IL3 [A]",
        line=dict(color="green")))

    fig.update_layout(
        title=f"Struje generatora {unit}",
        xaxis_title="Vrijeme",
        yaxis_title="Ig [V]",
        template="plotly_white",
        legend_title="Legenda",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
        )
    
    return fig


def graf_uzbuda(df, unit):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Vrijeme"],
        y=df[f"{unit}_NAPON_UZBUDE"],
        mode="lines",
        name=f"NAPON UZBUDE GENERATORA {unit} [V]",
        line=dict(color="blue")))

    fig.add_trace(go.Scatter(
        x=df["Vrijeme"],
        y=df[f"{unit}_STRUJA_UZBUDE"],
        mode="lines",
        name=f"STRUJA UZBUDE GENERATORA {unit} [A]",
        line=dict(color="red"),
        yaxis="y2"))

    fig.update_layout(
        title=f"Napon i struja uzbude generatora {unit}",
        xaxis_title="Vrijeme",
        yaxis_title="Napon i struja uzbude",
        template="plotly_white",
        legend_title="Legenda",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True,
                   title="Uf [V]",
                   titlefont=dict(color="blue"),
                   tickfont=dict(color="blue")),
        yaxis2=dict(showgrid=True,
                    title="If [A]",
                    titlefont=dict(color="red"),
                    tickfont=dict(color="red"),
                    overlaying="y",
                    side="right")
        )
    return fig


def graf_brzine(df, unit):
    fig = go.Figure()
        
    fig.add_trace(go.Scatter(
        x=df["Vrijeme"],
        y=df[f"{unit}_FREKVENCIJA_GENERATORA"]/50*100,
        mode="lines",
        name=f"FREKVENCIJA GENERATORA {unit} [%]",
        line=dict(color="blue")
        ))
    
    fig.add_trace(go.Scatter(
        x=df["Vrijeme"],
        y=df[f"PB_{unit}_TR_ZADANA_BRZ"],
        mode="lines",
        name=f"ZADANA BRZINA VRNJE GENERATORA {unit} [%]",
        line=dict(color="black")
        ))
    
    fig.add_trace(go.Scatter(
        x=df["Vrijeme"],
        y=df[f"PB_{unit}_TR_BRZINA_VRTNJE"],
        mode="lines",
        name=f"BRZINA VRTINJE GENERATORA {unit} [%]",
        line=dict(color="green")
        ))
    
    fig.update_layout(
        title=f"Frekvencija, brzina vrtnje i zadana brzina vrtnje jedinice {unit}",
        xaxis_title="Vrijeme",
        yaxis_title="f, n, nset [%]",
        template="plotly_white",
        legend_title="Legenda",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
        )
    
    return fig


def graf_frekvencija(df, unit):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df["Vrijeme"],
        y=df[f"{unit}_FREKVENCIJA_GENERATORA"],
        mode="lines",
        name=f"FREKVENCIJA GENERATORA {unit} [Hz]",
        line=dict(color="purple")
        ))
    
    fig.update_layout(
        title=f"Frekvencija jedinice {unit}",
        xaxis_title="Vrijeme",
        yaxis_title="f [Hz]",
        template="plotly_white",
        legend_title="Legenda",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)        
        )
    return fig


def graf_otvor_pk(df, unit):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df["Vrijeme"],
        y=df[f"PB_{unit}_TR_OTVOR_PK"],
        mode="lines",
        name=f"OTVOR PRIVODNOG KOLA {unit} [%]",
        line=dict(color="blue")
        ))
    
    fig.update_layout(
        title=f"Otvor privodnog kola jedinice {unit}",
        xaxis_title="Vrijeme",
        yaxis_title="y [%]",
        template="plotly_white",
        legend_title="Legenda",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
        )
    return fig


def graf_tlak(df, unit):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df["Vrijeme"],
        y=df[f"{unit}_TLAK_U_SPIRALI_TURBINE"],
        mode="lines",
        name=f"TLAK U SPIRALI TURBINE JEDINICE {unit} [bar]",
        line=dict(color="blue")
        ))
    
    fig.add_trace(go.Scatter(
        x=df["Vrijeme"],
        y=df[f"{unit}_TLAK_U_TLACNOM_CJEVOVODU"],
        mode="lines",
        name=f"TLAK U TLACNOM CJEVOVODU [bar]",
        line=dict(color="red")
        ))
    
    fig.update_layout(
        title=f"Tlakovi za vrijeme CS jedinice {unit}",
        xaxis_title="Vrijeme",
        yaxis_title="p [bar]",
        template="plotly_white",
        legend_title="Legenda",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)        
        )
    return fig


def graf(gen, df, bay, signal_dict, annotations):
    print(f"U funkciji: {gen}")
    fig = go.Figure()
    
    if isinstance(signal_dict["yaxis"], list):
        print(f"U if dijelu: {gen}")
        fig.add_trace(go.Scatter(
            x=df["Vrijeme"],
            y=df[signal_dict["signals"][0].format(unit=gen, bay=bay)],
            mode="lines",
            name=signal_dict["name"][0].format(unit=gen),
            line=dict(color=signal_dict["colors"][0])
            ))
        fig.add_trace(go.Scatter(
            x=df["Vrijeme"],
            y=df[signal_dict["signals"][1].format(unit=gen, bay=bay)],
            mode="lines",
            name=signal_dict["name"][1].format(unit=gen),
            line=dict(color=signal_dict["colors"][1]),
            yaxis="y2"
            ))
        fig.update_layout(
            title=signal_dict["title"].format(unit=gen),
            xaxis_title="Vrijeme",
            template="plotly",
            legend_title="Legenda",
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True,
                       title=signal_dict["yaxis"][0],
                       titlefont=dict(color=signal_dict["colors"][0]),
                       tickfont=dict(color=signal_dict["colors"][0])),
            yaxis2=dict(showgrid=True,
                        title=signal_dict["yaxis"][1],
                        titlefont=dict(color=signal_dict["colors"][1]),
                        tickfont=dict(color=signal_dict["colors"][1]),
                        overlaying="y",
                        side="right")
            )
    else:
        print(f"U else dijelu: {gen}")
        for index, signal in enumerate(signal_dict["signals"]):
            fig.add_trace(go.Scatter(
                x=df["Vrijeme"],
                y=df[signal.format(unit=gen, bay=bay)],
                mode="lines",
                name=signal_dict["name"][index].format(unit=gen),
                line=dict(color=signal_dict["colors"][index])
                ))
        fig.update_layout(
            title=signal_dict["title"].format(unit=gen, bay=bay),
            xaxis_title="Vrijeme",
            yaxis_title=signal_dict["yaxis"],
            template="plotly",
            legend_title="Legenda",
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True)        
            )
    
    for i in range(0, len(annotations), 2):
        fig.add_vline(
            x=pd.to_datetime(annotations[i+1]).to_pydatetime(),
            line_width=1,
            line_dash="dash",
            line_color="#754FC5"
            )
        if i==2 :
            ay_set = -60
        else:
            ay_set = -40
            
        if i == 6:
            ax_set = 80
        else:
            ax_set = 20
            
        fig.add_annotation(
            x=pd.to_datetime(annotations[i+1]).to_pydatetime(),
            y=0.9,  # Set a relevant y-axis value
            xref="x",
            yref="paper",
            text=annotations[i],
            showarrow=True,
            arrowhead=2,
            ax=ax_set,  # Arrow shift in x direction
            ay=ay_set,  # Arrow shift in y direction
            font=dict(color="#754FC5", size=12),
            bordercolor="#754FC5",
            borderwidth=1,
            bgcolor="rgba(255,255,255,0.7)"
            )
    return fig


# =============================================================================
#                   START - LOKACIJA FILEOVA
# =============================================================================

mypath = r"""C:\Users\larab\Documents\GitHub\uq_vn_regulacija\hrvoje_procis_data"""
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

savepath = r"""C:\Users\larab\Documents\GitHub\uq_vn_regulacija\hrvoje_procis_htmls"""

for file in files:
    print(file)
    print("\n")

# VN mjerenja imaju i oznaku vodnog polja u kojem je spojen agregat
gens=["A", "D"]
bays=["E3", "E5"]

# u df se spremaju očitani podatci 
units = {"A": {},
         "D": {}}


# =============================================================================
#                           SVI SIGNALI
# =============================================================================

# Ovisno o strukturi dictionaryja unutar mjerenja crtaju se na različit način
# unutar graf funkcije 
mjerenja = {"Naponi": {"signals": ["{unit}_NAPON_GENERATORA_UL1L2",
                                   "{unit}_NAPON_GENERATORA_UL2L3",
                                   "{unit}_NAPON_GENERATORA_UL3L1"],
                       "colors": ["red", "blue", "green"],
                       "name": ["NAPON GENERATORA {unit} - UL1L2 [V]",
                                "NAPON GENERATORA {unit} - UL2L3 [V]",
                                "NAPON GENERATORA {unit} - UL3L1 [V]"],
                       "yaxis": "Ug [V]",
                       "title": "Naponi generatora {unit}"
                       },
            "Struje": {"signals": ["{unit}_STRUJA_GENERATORA_IL1",
                                   "{unit}_STRUJA_GENERATORA_IL2",
                                   "{unit}_STRUJA_GENERATORA_IL3"],
                       "colors": ["red", "blue", "green"],
                       "name": ["STRUJA GENERATORA {unit} - IL1 [A]",
                                "STRUJA GENERATORA {unit} - IL2 [A]",
                                "STRUJA GENERATORA {unit} - IL3 [A]"],
                       "yaxis": "Ig [A]",
                       "title": "Struje generatora {unit}"},
            "Uzbuda": {"signals": ["{unit}_NAPON_UZBUDE",
                                   "{unit}_STRUJA_UZBUDE"],
                       "colors": ["red", "blue"],
                       "name": ["NAPON UZBUDE GENERATORA {unit} [V]",
                                "STRUJA UZBUDE GENERATORA {unit} [A]"],
                       "yaxis": ["Uf [V]", "If [V]"],
                       "title": "Napon i struja uzbude generatora {unit}"},
            "Snaga": {"signals": ["{unit}_RADNA_SNAGA_GENERATORA",
                                  "{unit}_JALOVA_SNAGA_GENERATORA"],
                      "colors": ["red", "blue"],
                      "name": ["RADNA SNAGA GENERATORA {unit} [MW]",
                               "JALOVA SNAGA GENERATORA {unit} [Mvar]"],
                      "yaxis": ["P [MW]", "Q [Mvar]"],
                      "title": "Radna i jalova snaga generatora {unit}"},
            "Snaga_VN": {"signals": ["{unit}_{bay}_110KV_RADNA_SNAGA_",
                                     "{unit}_{bay}_110KV_JALOVA_SNAGA_"],
                         "colors": ["red", "blue"],
                         "name": ["RADNA SNAGA NA VN STRANI 110 kV {unit} [MW]",
                                  "JALOVA SNAGA NA VN STRANI 110 kV {unit} [Mvar]"],
                         "yaxis": ["P(VN) [MW]", "Q(VN) [Mvar]"],
                         "title": "Radna i jalova snaga na VN strani 110 kV za {unit}"},
            "Napon_VN": {"signals": ["{unit}_{bay}_110KV_NAPON_RS_", 
                                     "{unit}_{bay}_110KV_NAPON_ST_",
                                     "{unit}_{bay}_110KV_NAPON_TR_"],
                         "colors": ["red", "blue", "green"],
                         "name": ["NAPON NA VN STRANI (110 kV) - RS",
                                  "NAPON NA VN STRANI (110 kV) - ST",
                                  "NAPON NA VN STRANI (110 kV) - TR"],
                         "yaxis": "U(VN) [kV]",
                         "title": "Linijski naponi na VN strani (110 kV) - {unit}"},
            "Struje_VN": {"signals": ["{unit}_{bay}_110KV_STRUJA_R_",
                                      "{unit}_{bay}_110KV_STRUJA_S_",
                                      "{unit}_{bay}_110KV_STRUJA_T_"],
                          "colors": ["red", "blue", "green"],
                          "name": ["STRUJA NA VN STRANI (110 kV) - R",
                                   "STRUJA NA VN STRANI (110 kV) - S",
                                   "STRUJA NA VN STRANI (110 kV) - T"],
                          "yaxis": "I(VN) [A]",
                          "title": "Struje na VN strani (110 kV) - {unit}"},
            "Cosphi": {"signals": ["{unit}_{bay}_110KV_COS_FI_"],
                       "colors": ["red"],
                       "name": ["COS PHI NA VN STRANI (110 KV)"],
                       "yaxis": "cos phi (VN)",
                       "title": "Faktor snage na sučelju (110 kV) - {unit}"}
            }

# u slucaju da je nesto potrebno anotirati, graf funkcija ima to handleano, 
# samo je potrebno ispostovati formu anotacija kako ih funkcija prihvaca:
# za svaki od agregata potrebno je poslati listu: 
#   1. Tekst prve anotacije
#   2. Datetime za 1. anotaciju
#   3. Tekst druge anotacije
#   4. Datetime za 2. anotaciju
# itd, moraju se izmjenjivati. 
# Moguće je anotacije dodati u dict units vezano za svaki agregat zasebno.
annotations = []

# PROCIS datoteke s vrijednostima u svom nazivu imaju rijec flat, pa ovako samo
# te fileove izvlacimo ukoliko su poslani i KRD zapisi i PROCIS zapisi.
files = [file for file in files if "flat" in file]
#print(files)

# citamo te fileove u zasebne dataframeove ovisno o tome o koliko agregata se radi
for i in range(len(gens)):
    if gens[i] in files[i]:
        print(gens[i])
        print(files[i])
    
        df = pd.read_excel(mypath+"\\"+files[i], header=0)
        
        # Timestamp za agregat A je bio drugaciji iz nekog razloga (promijenjeno)
        #if gens[i] == "A":
        #    df["Vrijeme"] = pd.to_datetime(df["Vrijeme"], format="%d-%m-%Y %H:%M:%S")
        #else:
        #    df["Vrijeme"] = pd.to_datetime(df["Vrijeme"], format="%d-%m-%Y %H:%M:%S", dayfirst=True)
        
        df["Vrijeme"] = pd.to_datetime(df["Vrijeme"], format="%d-%m-%Y %H:%M:%S", dayfirst=True)
        units[gens[i]]["df"] = df
        units[gens[i]]["bay"] = bays[i]
        print(f"Done - {files[i]}")
        
# kreiranje grafova za svaku vrijednost i spremanje u jedan html file 
for unit, value in units.items():
    fig_list = []
    for mjerenje_naziv, mjerenje_podatci in mjerenja.items():
        fig0 = graf(unit, value["df"], value["bay"], mjerenja[mjerenje_naziv], annotations)
        fig_list.append(fig0)
    
    html_list = []
    for fig in fig_list:
        if not html_list:
            html = pio.to_html(fig, full_html=False, include_plotlyjs="cdn")
            html_list.append(html)
        else:
            html = pio.to_html(fig, full_html=False, include_plotlyjs=False)
            html_list.append(html)
    divs_html = "\n".join(f"<div>{html}</div>" for html in html_list)
        
    html_page = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>gen-{unit}</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <h2>Vizualizacija podataka - PROCIS</h2>
        {divs_html}
    </body>
    </html>
    """
    
    # Save the HTML page
    with open(f"{savepath}\\procis-gen-{unit.lower()}.html", "w") as f:
        f.write(html_page)
    
    print(f"Dashboard saved as procis-gen-{unit.lower()}.html")