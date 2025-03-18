# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 12:29:41 2025

@author: larab
"""

import pandas as pd
import re
from os import listdir
from os.path import isfile, join
import os

from datetime import datetime
from datetime import timedelta

import plotly
import plotly.graph_objects as go
import plotly.io as pio
#import plotly.graph_objects as go


def draw(table_df, signal_name, signal_data):    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=table_df["Datetime"],
        y=table_df[signal_name],
        mode="lines",
        name=signal_data['label'] + " [" + signal_data['unit']+ "]",
        line=dict(color="blue")
        ))
        
    fig.update_layout(
        title=f"{signal_data['longtxt']}",
        template="plotly_white",
        legend_title="Legenda",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True,
                   title=signal_data['label'] + " [" + signal_data['unit']+ "]",
                   titlefont=dict(color="blue"),
                   tickfont=dict(color="blue"))
        )    
    return fig


def draw_binary_signals(table_df, binary_signals):
    fig = go.Figure()
    
    y_offset = 0  # Offset za prvi graf
    offset_step = 3.0  # Razmak izmedu signala na y osi

    for signal_name in binary_signals:
        # Check if signal changes at any point
        unique_values = table_df[signal_name].unique()
        if len(unique_values) == 1:
            if unique_values[0] == 0:
                line_style = "dot"
                opacity = 0.5
            else:
                line_style = "dash"
                opacity = 1.0
        else:
            line_style = "solid"
            opacity = 1.0

        fig.add_trace(go.Scatter(
            x=table_df["Datetime"],
            y=table_df[signal_name] + y_offset,  # Apply offset
            mode="lines",
            name=binary_signals[signal_name]['label'],
            showlegend=True,
            opacity=opacity,
            line=dict(width=2, dash=line_style)  # Dashed if unchanged
        ))
        y_offset += offset_step  # Increase offset for the next signal
        
    fig.update_layout(
        title="Binarni signali",
        template="plotly_white",
        legend_title="Binarni signali",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True, title="Razine binarnih singala"),
    )    

    return fig


def draw_multiple_signals(table_df, signal_names, signal_data):
    """Draws multiple graphs: One with original values and one with normalized values for QACT & QACTH."""
    fig_list = []

    if table_df.empty:
        print("Warning: Table dataframe is empty, skipping graph creation.")
        return fig_list  # Return empty list to prevent errors

    if set(signal_names) == {"QACT", "QACTH"}:
        print("Creating both normalized and original graphs for QACT and QACTH")

        fig_original = go.Figure()
        for signal_name in signal_names:
            if table_df[signal_name].empty:
                print(f"Warning: Signal {signal_name} has no data, skipping.")
                continue  # Skip if no data

            fig_original.add_trace(go.Scatter(
                x=table_df["Datetime"],
                y=table_df[signal_name],
                mode="lines",
                name=f"Originali - {signal_data[signal_name]['label']} [{signal_data[signal_name]['unit']}]"
            ))

        fig_original.update_layout(
            title="Originalne vrijednosti: QACT & QACTH",
            template="plotly_white",
            legend_title="Legenda",
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True, title="Originalne vrijednosti"),
        )
        fig_list.append(fig_original)  # Add to the figure list

        fig_normalized = go.Figure()
        for signal_name in signal_names:
            if table_df[signal_name].empty:
                print(f"Warning: Signal {signal_name} has no data, skipping normalization.")
                continue  # Skip if no data

            first_value = table_df[signal_name].iloc[0]  # Get first value
            adjusted_values = table_df[signal_name] - first_value  # Normalize

            fig_normalized.add_trace(go.Scatter(
                x=table_df["Datetime"],
                y=adjusted_values,
                mode="lines",
                name=f"Normalizirani - {signal_data[signal_name]['label']} [{signal_data[signal_name]['unit']}]"
            ))

        fig_normalized.update_layout(
            title="Normalizirane vrijednosti: QACT & QACTH",
            template="plotly_white",
            legend_title="Legenda",
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True, title="Normalizirane vrijednosti"),
        )
        fig_list.append(fig_normalized)  

    else:
        fig = go.Figure()
        for signal_name in signal_names:
            if table_df[signal_name].empty:
                print(f"Warning: Signal {signal_name} has no data, skipping.")
                continue

            fig.add_trace(go.Scatter(
                x=table_df["Datetime"],
                y=table_df[signal_name],
                mode="lines",
                name=signal_data[signal_name]['label'] + " [" + signal_data[signal_name]['unit']+ "]"
            ))

        fig.update_layout(
            title=" / ".join([signal_data[name]['longtxt'] for name in signal_names]),
            template="plotly_white",
            legend_title="Legenda",
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True, title="[" + signal_data[signal_names[0]]['unit'] + "]"),
        )

        fig_list.append(fig)

    return fig_list


def extract_signals(lines):
    signals = []
    signals_start = False
    for line in lines:
        if line.startswith("Signals:"):
            signals_start = True
        elif signals_start and re.match(r"\d+\.\s", line.strip()):
            match = re.match(r"\d+\.\s+(\S+)\s+(\S+)", line.strip())
            if match:
                signal_name, signal_type = match.groups()
                signals.append((signal_name, signal_type))
        elif signals_start and not line.strip():
            break
    return signals


def extract_data(lines):
    data = []
    data_start = False
    for line in lines:
        if line.startswith("Data:"):
            data_start = True
        elif data_start and line.strip():
            data.append(line.strip())
    return data


signali = {
    'VGACTINV': {
        'intbase': 23405,
        'baseval': 16.0,
        'unit': 'kV',
        'label': 'VGACTINV',
        'longtxt': 'Napon generatora',
        'desc': "Stvarni napon generatora (inverz)"},
    'PACT': {
        'intbase': 23405,
        'baseval': 160.0,
        'unit': 'MW',
        'label': 'PACT',
        'longtxt': 'Radna snaga generatora',
        'desc': 'Radna snaga generatora'},
    'QACT': {
        'intbase': 23405,
        'baseval': 160.0,
        'unit': 'Mvar',
        'label': 'QACT',
        'longtxt': 'Jalova snaga generatora',
        'desc': 'Jalova snaga generatora'},
    'VGACT': {
        'intbase': -23405,
        'baseval': 16.0,
        'unit': 'kV',
        'label': 'VGACT',
        'longtxt': 'Napon generatora',
        'desc': 'Napon generatora'},
    'VGREF': {
        'intbase': 23405,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'VGREF',
        'longtxt': 'Referenca Ug',
        'desc': 'Referenca napona na generatoru'},
    'PACTH': {
        'intbase': 23405,
        'baseval': 160.0,
        'unit': 'MW',
        'label': 'PACTH',
        'longtxt': 'Radna snaga - VN mjerenje',
        'desc': 'Radna snaga na sučelju'},
    'QACTH': {
        'intbase': 23405,
        'baseval': 160.0,
        'unit': 'Mvar',
        'label': 'QACTH',
        'longtxt': 'Jalova snaga - VN mjerenje',
        'desc': 'Jalova snaga na sučelju'},
    'QHREF': {
        'intbase': 23405,
        'baseval': 160.0,
        'unit': 'Mvar',
        'label': 'QHREF',
        'longtxt': 'Jalova snaga - VN referenca',
        'desc': 'Referenca jalove snage na sučelju'},
    'VHACT': {
        'intbase': -23405,
        'baseval': 121.0,
        'unit': 'kV',
        'label': 'VHACT',
        'longtxt': 'Napon - VN mjerenje',
        'desc': 'Napon na sučelju'},
    'VHREF': {
        'intbase': 23405,
        'baseval': 121.0,
        'unit': 'kV',
        'label': 'VHREF',
        'longtxt': 'Napon - VN referenca',
        'desc': 'Referenca napona na sučelju'},
    'IGACTINV': {
        'intbase': 16384,
        'baseval': 5774.0,
        'unit': 'A',
        'label': 'IGACTINV',
        'longtxt': 'Struja generatora',
        'desc': 'Struja generatora (inverz)'},
    'IGACT': {
        'intbase': 16384,
        'baseval': 5774.0,
        'unit': 'A',
        'label': 'IGACT',
        'longtxt': 'Struja generatora',
        'desc': 'Struja generatora'},
    'UFACT': {
        'intbase': 4096,
        'baseval': 74.0,
        'unit': 'V',
        'label': 'UFACT',
        'longtxt': 'Napon uzbude',
        'desc': 'Napon uzbude'},
    'IFACT': {
        'intbase': 4096,
        'baseval': 725.0,
        'unit': 'A',
        'label': 'IFACT',
        'longtxt': 'Struja uzbude',
        'desc': 'Struja uzbude'},
    'QHINC' : {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'log16',
        'label': 'Qref VIŠE',
        'longtxt': 'Impuls Qref više - VN',
        'desc': 'Nalog za povećanje reference Q na VN (binarni signal)'},
    'QHDEC': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'log16',
        'label': 'Qref NIŽE',
        'longtxt': 'Impuls Qref niže - VN',
        'desc': 'Nalog za snižavanje reference Q na VN (binarni signal)'},
    'VHDEC': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'log16',
        'label': 'Vref NIŽE',
        'longtxt': 'Impuls Vref niže - VN',
        'desc': 'Nalog za smanjenje reference U na VN (binarni signal)'},
    'VHINC': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'log16',
        'label': 'Vref VIŠE',
        'longtxt': 'Impuls Vref više - VN',
        'desc': 'Nalog za povećanje reference U na VN (binarni signal)'},
    'COSPHIH': {
        'intbase': 100.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'cosphi - VN',
        'longtxt': 'cosphi - VN',
        'desc': 'Faktor snage na sučelju'},
    'COSHREF': {
        'intbase': 100.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'cosphi ref - VN',
        'longtxt': 'cosphi - VN referenca',
        'desc': 'Referenca faktora snage na sučelju'},
    'OEXLIMON': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'log16',
        'label': 'OEXLIMON',
        'longtxt': 'Overexcitation limiter ON',
        'desc': 'Aktivan limiter u naduzbudi (binarni signal)'},
    'QACTHMAX': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'log16',
        'label': 'QACTHMAX',
        'longtxt': 'Max granica Q (VN)',
        'desc': 'Granica maksimalne jalove snage na VN dosegnuta (binarni signal)'},
    'QHREFCM': {
        'intbase': 23405,
        'baseval': 100.0,
        'unit': '%',
        'label': 'QHREFCM',
        'longtxt': 'QHREFCM',
        'desc': 'Jedan od signala za formiranje reference QHREF'},
    'QHREFC': {
        'intbase': 23405,
        'baseval': 100.0,
        'unit': '%',
        'label': 'QHREFC',
        'longtxt': 'QHREFC',
        'desc': 'Jedan od signala za formiranje reference QHREF'},
    'PACTHI': {
        'intbase': 23405,
        'baseval': 160.0,
        'unit': 'MW',
        'label': 'PACTHI',
        'longtxt': 'Radna snaga (VN) I',
        'desc': 'PACTHI [MW] - Radna snaga na sučelju (inverz)'},
    'QACTHI': {
        'intbase': 23405,
        'baseval': 160.0,
        'unit': 'Mvar',
        'label': 'QACTHI',
        'longtxt': 'Jalova snaga (VN) I',
        'desc': 'Jalova snaga na sučelju (inverz)'},
    'ACQHCOF': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'log16',
        'label': 'ACQHCOF',
        'longtxt': 'Potvrda o iskljucenom Q regulatoru na VN strani', 
        'desc': 'Potvrda o isključenom Q regulatoru na VN strani (binarni signal)'},
    'ACQHCON': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'log16',
        'label': 'ACQHCON',
        'longtxt': 'Potvrda o ukljucenom Q regulatoru na VN strani',
        'desc': 'Potvrda o isključenom Q regulatoru na VN strani (binarni signal)'},
    'VHCTRON': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'log16',
        'label': 'VHCTRON',
        'longtxt': 'U (VN) control - ON',
        'desc': 'Uključena regulacija U na sučelju (binarni signal)'},
    'QHENABLE': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'log16',
        'label': 'QHENABLE',
        'longtxt': 'Ukljucenje Q regulatora (VN)',
        'desc': 'Uključena regulacija Q na sučelju (binarni signal)'},
    'COSHINC': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'log16',
        'label': 'cosphi (VN) VIŠE',
        'longtxt': 'Povećanje cosphi (VN)',
        'desc': 'Nalog za povećanje cosphi na sučelju (binarni signal)'},
    'COSHDEC': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'log16',
        'label': 'cosphi (VN) NIŽE',
        'longtxt': 'Smanjenje cosphi (VN)',
        'desc': 'Nalog za smanjenje cosphi na sučelju (binarni signal)'}
    }


# MARKDOWN TEMPLATE
md_template = """---
layout: default
title: KONČAR INEM - WATCH GEN A
---

### KONČAR INEM - WATCH LOG - AGREGAT A 

### UQ regulacija na sučelju s mrežom

#### Watch {number}

Na grafovima niže prikazani su zapisi veličina dostavljeni od strane Končar INEM-a. 
Sve veličine su preuzete iz dostavljene log datoteke `watch-zakuca1a-zakuca1a-{number}.log`.
                               
Prikazane veličine su:
{signals_list}

<div class="wide-graph">
    <iframe src="{{{{ site.baseurl }}}}/watch-htmls-a/{name_of_html}" width="100%" height="800px" frameborder="0"></iframe>
</div>
"""


# FOLDER ZA MARKDOWN DATOTEKE 
output_dir = "_pages"
os.makedirs(output_dir, exist_ok=True)


# FOLDERI ZA WATCH LOGOVE I GENERIRANE HTML DATOTEKE
savepath = r"""C:/Users/larab/Documents/GitHub/uq_vn_regulacija/watch-htmls-a"""
datapath = r"""C:/Users/larab/Documents/GitHub/uq_vn_regulacija/Watch_snimke_A"""
files = [f for f in listdir(datapath) if isfile(join(datapath, f))]


paired_signals = [
    ("VHACT", "VHREF"),
    ("QACTH", "QHREF"),
    ("QACTH", "QACT")
]

timestamps_path = "C:/Users/larab/Documents/GitHub/uq_vn_regulacija/timestamps_agregat_a.xlsx"
if os.path.exists(timestamps_path):
    os.remove(timestamps_path)

timestamps_df = pd.DataFrame(columns=["File Name", "Start", "End"])
timestamps_df.to_excel(timestamps_path, sheet_name="Timestamps", index=False)

for file in files:
    path = datapath + "\\" + file
    file_name = file.split(".")[0]
    
    with open(path, "r") as file:
        log_lines = file.readlines()

    header_info = {}
    for line in log_lines:
        # Match the Start time line
        if match := re.match(r"Start time:\s+([\d.]+)\s+([\d:]+)", line):
            header_info["date"] = match.group(1)
            header_info["time"] = match.group(2)
            header_info["datetime"] = header_info["date"] + " " + header_info["time"]
            
    signals = extract_signals(log_lines)
    data_lines = extract_data(log_lines)
    
    # Step 3: Convert Data to DataFrame
    columns = ["Time"] + [signal[0] for signal in signals]
    
    # Split and convert data lines to numeric values
    data_lines = [line for line in data_lines if not line.strip().startswith("***")]
    data = [list(map(float, re.split(r"\s+", line))) for line in data_lines]
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=columns)
    
    datetime_str = header_info['datetime']
    datetime_start = datetime.strptime(datetime_str, '%d.%m.%Y. %H:%M:%S')    
    
    #dt = timedelta(milliseconds = int(sample_data["Sample Time"]))
    df['Timedelta'] = pd.to_timedelta(df['Time'], unit='s')
    df["Datetime"] = datetime_start + df["Timedelta"]
    
    extracted_signal_names = {signal[0] for signal in signals}  # Set of signal names in the log

    # Filter from `signali` based on what was extracted from the log
    binary_signals = {k: v for k, v in signali.items() if k in extracted_signal_names 
                      and v['intbase'] == 1.0 and v['baseval'] == 1.0 and v['unit'] == 'pu'}

    int_signals = {k: v for k, v in signali.items() if k in extracted_signal_names and k not in binary_signals}    

    column_skip = ['Time', 'Timedelta', 'Datetime', 'OEXLIMON', 'QACTHMAX',
                   'Q2IN', 'Q1IN', 'ACKQ0OF', 'ACKQ0OF0', 'VAUXACTP', 'VAUXP1',
                   'INVERTP', 'COHREFCC']
    
    int_columns = [col for col in df.columns if col in int_signals]
    binary_columns = [col for col in df.columns if col in binary_signals]
    
    signals_for_md = int_columns+binary_columns
    
    table_df = pd.DataFrame()
    table_df["Datetime"] = df["Datetime"]

    #Za kasnije prikazivanje na Github pages, izvlacimo prvi i zadnji timestamp
    #Sprema se u excel file zajedno s nazivom filea:
    
    try:
        # ne prikazuje milisekunde u excelu!
        # start = table_df["Datetime"].iloc[0]
        # end = table_df["Datetime"].iloc[-1]
        start = table_df["Datetime"].iloc[0].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        end = table_df["Datetime"].iloc[-1].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        new_row = pd.DataFrame([[file_name, start, end]], columns=["File Name", "Start", "End"])

        try:
            with pd.ExcelWriter(timestamps_path, mode="a", engine="openpyxl", if_sheet_exists="overlay", datetime_format="yyyy-mm-dd hh:mm:ss.000") as writer:
                new_row.to_excel(writer, sheet_name="Timestamps", startrow=writer.sheets["Timestamps"].max_row, index=False, header=False)
        except FileNotFoundError:
            # If file doesn't exist, create a new one
            timestamps_df.to_excel(timestamps_path, sheet_name="Timestamps", index=False)
    except IndexError:
        continue

    for column in int_columns:
        if column == 'DEINVERT':
            continue
        column_data = int_signals[column]
        table_df[column] = df[column]/column_data['intbase']
        table_df[column] = table_df[column]*column_data['baseval']    

    for column in binary_columns:
        if column in df.columns:
            table_df[column] = df[column]
        else:
            print(f"Warning: Binary signal {column} is missing from df.")

    
    # =============================================================================
    # GENERIRANJE SLIKA KOJE IDU U HTML DATOTEKE PREMA GORE IZVUCENIM SIGNALIMA 
    # =============================================================================

    fig_list = []
    plotted_signals = set()
    
    for group in paired_signals:
        present_signals = [s for s in group if s in int_columns]
        if len(present_signals) > 1:
            fig = draw_multiple_signals(table_df, present_signals, int_signals)
            fig_list.extend(fig)
            plotted_signals.update(present_signals)

    for column in int_columns:
        if column not in plotted_signals:
            fig = draw(table_df, column, int_signals[column])
            fig_list.append(fig)

    if binary_columns:
        binary_fig = draw_binary_signals(table_df, binary_signals)
        fig_list.append(binary_fig)

    # =============================================================================
    # GENERIRANJE HTML DATOTEKA ZA SVAKI LOG    
    # =============================================================================

    html_list = []
    for index,fig in enumerate(fig_list):
        if index == 0:
            html = pio.to_html(fig, full_html=False, include_plotlyjs="cdn")
        else:
            html = pio.to_html(fig, full_html=False, include_plotlyjs=False)
        html_list.append(html)

    divs_html = "\n".join(f"<div>{html}</div>" for html in html_list)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{file}</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        {divs_html}
        </body>
    </html>
    """
    
    with open(f"{savepath}\\{file_name.lower().replace('_', '-')}.html", "w") as file:
        file.write(html_content)


    # =============================================================================
    #   GENERIRANJE MARKDOWN DATOTEKE ZA SVAKI LOG I HTML
    # =============================================================================
    #signals_md = "\n".join([f"    - {sig}" for sig in signals_for_md])  # Format as bullet points with indentation
    signals_md = "\n".join([
    f"    - {signali[sig].get('desc', signali[sig]['longtxt'])}" if sig in signali else f"    - {sig}" 
    for sig in signals_for_md
    ])
    signals_md = "| Signal | Jedinica | Opis |\n|---|---|---|\n" + "\n".join([
        f"| **{sig}** | [{signali[sig]['unit']}] | {signali[sig]['desc']} |" 
        if sig in signali else f"| **{sig}** | - | - |" 
        for sig in signals_for_md
        ])
    
    number = file_name[-3:]
    html_file_name = (file_name+".html").lower().replace("_", "-")
    
    # Popunjavanje templatea za markdown
    md_content = md_template.format(number=number, name_of_html=html_file_name, signals_list=signals_md)

    # Save to .md file
    md_filename = f"{file_name.lower()}.md".replace("_", "-")
    md_path = os.path.join(output_dir, md_filename)
    
    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write(md_content)

    print(f"Generated: {md_path}")
    print("Going to next log file...")
    print()