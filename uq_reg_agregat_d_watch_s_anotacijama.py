# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 08:38:31 2025

@author: larab
"""

# Iste funkcije za vizualizaciju Watch fileova uz izmjenu za anotacije grafova.
# Iz izvještaja s lokacije napisan je excel file ListaDogadaja u kojem su popisane
# manipulacije koje su rađene. Bez tog filea (kojeg je potrebno rucno napraviti ili
# modificirati ako je dostupan samo KRD) ova skripta nece raditi i potrebno je 
# koristiti samo originalnu koja radi samo vizualizaciju Watch fileova.

import pandas as pd
import re
from os import listdir
from os.path import isfile, join
from os import getcwd

from datetime import datetime
from datetime import timedelta

import plotly
import plotly.graph_objects as go
import plotly.io as pio

def add_annotations(fig, event_log_filtered):
    """Adds vertical lines and text annotations for events within the log's time range."""
    for _, row in event_log_filtered.iterrows():
        event_time = row['datetime']
        event_text = row['event'] if 'event' in row else "Event"

        fig.add_vline(x=event_time, line_width=2, line_dash="dash", line_color="red")

        fig.add_annotation(
            x=event_time,
            y=1,  # Adjust based on your data scaling
            text=event_text,
            showarrow=True,
            arrowhead=2,
            ay=-40,  # Adjust position
            font=dict(color="red", size=12),
            align="left"
        )


def draw(table_df, signal_name, signal_data, event_log_filtered):    
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

    # Add event annotations
    add_annotations(fig, event_log_filtered)

    return fig


def draw_binary_signals(table_df, binary_signals, event_log_filtered):
    """Draws a single graph with all binary signals and includes event annotations."""
    fig = go.Figure()
    
    y_offset = 0  # Starting offset
    offset_step = 3.0  # Distance between signals

    for signal_name in binary_signals:
        fig.add_trace(go.Scatter(
            x=table_df["Datetime"],
            y=table_df[signal_name] + y_offset,  # Apply offset
            mode="lines",
            name=binary_signals[signal_name]['label'],
            showlegend=True,
            line=dict(width=2)  # Thicker line for better visibility
        ))
        y_offset += offset_step  # Increase offset for the next signal
        
    fig.update_layout(
        title="Binarni signali",
        template="plotly_white",
        legend_title="Binarni signali",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True, title="Razine binarnih singala"),
    )    

    # Add event annotations
    add_annotations(fig, event_log_filtered)

    return fig


def draw_multiple_signals(table_df, signal_names, signal_data, event_log_filtered):
    """Draws multiple graphs and includes event annotations."""
    fig_list = []

    if table_df.empty:
        print("Warning: Table dataframe is empty, skipping graph creation.")
        return fig_list  

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

    # Add event annotations
    add_annotations(fig, event_log_filtered)

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
        'longtxt': 'Napon generatora'},
    'PACT': {
        'intbase': 23405,
        'baseval': 160.0,
        'unit': 'MW',
        'label': 'PACT',
        'longtxt': 'Radna snaga generatora'},
    'QACT': {
        'intbase': 23405,
        'baseval': 160.0,
        'unit': 'Mvar',
        'label': 'QACT',
        'longtxt': 'Jalova snaga generatora'},
    'VGACT': {
        'intbase': -23405,
        'baseval': 16.0,
        'unit': 'kV',
        'label': 'VGACT',
        'longtxt': 'Napon generatora'},
    'VGREF': {
        'intbase': 23405,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'VGREF',
        'longtxt': 'Referenca Ug'},
    'PACTH': {
        'intbase': 23405,
        'baseval': 160.0,
        'unit': 'MW',
        'label': 'PACTH',
        'longtxt': 'Radna snaga - VN mjerenje'},
    'QACTH': {
        'intbase': 23405,
        'baseval': 160.0,
        'unit': 'Mvar',
        'label': 'QACTH',
        'longtxt': 'Jalova snaga - VN mjerenje'},
    'QHREF': {
        'intbase': 23405,
        'baseval': 160.0,
        'unit': 'Mvar',
        'label': 'QHREF',
        'longtxt': 'Jalova snaga - VN referenca'},
    'VHACT': {
        'intbase': -23405,
        'baseval': 110.0,
        'unit': 'kV',
        'label': 'VHACT',
        'longtxt': 'Napon - VN mjerenje'},
    'VHREF': {
        'intbase': 23405,
        'baseval': 110.0,
        'unit': 'kV',
        'label': 'VHREF',
        'longtxt': 'Napon - VN referenca'},
    'IGACTINV': {
        'intbase': 16384,
        'baseval': 5774.0,
        'unit': 'A',
        'label': 'IGACTINV',
        'longtxt': 'Struja generatora'},
    'IGACT': {
        'intbase': 16384,
        'baseval': 5774.0,
        'unit': 'A',
        'label': 'IGACT',
        'longtxt': 'Struja generatora'},
    'UFACT': {
        'intbase': 4096,
        'baseval': 74.0,
        'unit': 'V',
        'label': 'UFACT',
        'longtxt': 'Napon uzbude'},
    'IFACT': {
        'intbase': 4096,
        'baseval': 725.0,
        'unit': 'A',
        'label': 'IFACT',
        'longtxt': 'Struja uzbude'},
    'QHINC' : {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'QHINC',
        'longtxt': 'Impuls Qref više - VN'},
    'QHDEC': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'QHDEC',
        'longtxt': 'Impuls Qref niže - VN'},
    'VHDEC': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'VHDEC',
        'longtxt': 'Impuls Vref niže - VN'},
    'VHINC': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'VHINC',
        'longtxt': 'Impuls Vref više - VN'},
    'VRINC': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'VRINC',
        'longtxt': 'Impuls Vref više - NN'},
    'VRDEC': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'VRDEC',
        'longtxt': 'Impuls Vref niže - NN'},
    'COSPHIH': {
        'intbase': 100.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'cosphi - VN',
        'longtxt': 'cosphi - VN'},
    'COSHREF': {
        'intbase': 100.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'cosphi ref - VN',
        'longtxt': 'cosphi - VN referenca'},
    'OEXLIMON': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'OEXLIMON',
        'longtxt': 'Overexcitation limiter ON'},
    'QACTHMAX': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'QACTHMAX',
        'longtxt': 'Max granica Q (VN)'},
    'QHREFCM': {
        'intbase': 23405,
        'baseval': 100.0,
        'unit': '%',
        'label': 'QHREFCM',
        'longtxt': 'QHREFCM'},
    'QHREFC': {
        'intbase': 23405,
        'baseval': 100.0,
        'unit': '%',
        'label': 'QHREFC',
        'longtxt': 'QHREFC'},
    'PACTHI': {
        'intbase': 23405,
        'baseval': 160.0,
        'unit': 'MW',
        'label': 'PACTHI',
        'longtxt': 'Radna snaga (VN) I'},
    'QACTHI': {
        'intbase': 23405,
        'baseval': 160.0,
        'unit': 'Mvar',
        'label': 'QACTHI',
        'longtxt': 'Jalova snaga (VN) I'},
    'ACQHCOF': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'ACQHCOF',
        'longtxt': 'Potvrda o iskljucenom Q regulatoru na VN strani'},
    'ACQHCON': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'ACQHCON',
        'longtxt': 'Potvrda o ukljucenom Q regulatoru na VN strani'},
    'ACKQ0OF0': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'ACKQ0OF0',
        'longtxt': 'Potvrda Q0 off ?'},
    'VHCTRON': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'VHCTRON',
        'longtxt': 'U (VN) control - ON'},
    'QHENABLE': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'QHENABLE',
        'longtxt': 'Ukljucenje Q regulatora (VN)'},
    'COSHINC': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'cosphi (VN) VIŠE',
        'longtxt': 'Povećanje cosphi (VN)'},
    'COSHDEC': {
        'intbase': 1.0,
        'baseval': 1.0,
        'unit': 'pu',
        'label': 'cosphi (VN) NIŽE',
        'longtxt': 'Smanjenje cosphi (VN)'}
    }


savepath = r"""C:\Users\larab\Documents\DRIVE_D\uq_zakucac\htmls_agregat_d"""
#atapath = getcwd()
datapath = r"""C:\Users\larab\Documents\DRIVE_D\uq_zakucac\Watch_snimke_D"""

files = [f for f in listdir(datapath) if isfile(join(datapath, f))]

paired_signals = [
    ("VHACT", "VHREF"),
    ("QACTH", "QHREF"),
    ("QACTH", "QACT"),
    ("VGACT", "VGREF")
]


# =============================================================================
#                       EVENT LOGS
# =============================================================================

event_log = pd.read_excel("ListaDogadaja.xlsx", header=0)
event_log['datetime'] = pd.to_datetime(event_log['date']) + pd.to_timedelta(event_log['time'].astype(str))
event_log['datetime'] = pd.to_datetime(event_log['datetime'])


# =============================================================================
#                       MAIN
# =============================================================================

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
    
    table_df = pd.DataFrame()
    table_df["Datetime"] = df["Datetime"]

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
    
    datetime_start = datetime.strptime(header_info["datetime"], '%d.%m.%Y. %H:%M:%S')
    datetime_end = table_df["Datetime"].max()

    event_log_filtered = event_log[(event_log["datetime"] >= datetime_start) &
                                   (event_log["datetime"]<=datetime_end)]
    
    fig_list = []
    plotted_signals = set()
    
    for group in paired_signals:
        present_signals = [s for s in group if s in int_columns]
        if len(present_signals) > 1:
            fig = draw_multiple_signals(table_df, present_signals, int_signals, event_log_filtered)
            fig_list.extend(fig)
            plotted_signals.update(present_signals)

    for column in int_columns:
        if column not in plotted_signals:
            fig = draw(table_df, column, int_signals[column], event_log_filtered)
            fig_list.append(fig)

    if binary_columns:
        binary_fig = draw_binary_signals(table_df, binary_signals, event_log_filtered)
        fig_list.append(binary_fig)

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
    
    with open(f"{savepath}\\{file_name}.html", "w") as file:
        file.write(html_content)

    print("Going to next log file...")
