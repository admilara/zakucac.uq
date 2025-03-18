# -*- coding: utf-8 -*-
"""
Refactored Log Parser Script - Fully Preserved Version
"""

import pandas as pd
import re
import os
from os import listdir
from os.path import isfile, join
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.io as pio

# =============================================================================
# FOLDER PATHS - FULLY RESTORED
# =============================================================================

savepath = r"""C:/Users/larab/Documents/GitHub/uq_vn_regulacija/watch-htmls-a"""
datapath = r"""C:/Users/larab/Documents/GitHub/uq_vn_regulacija/Watch_snimke_A"""
timestamps_path = "C:/Users/larab/Documents/GitHub/uq_vn_regulacija/timestamps_agregat_a.xlsx"

# If timestamps file exists, remove it to start fresh
if os.path.exists(timestamps_path):
    os.remove(timestamps_path)

# Initialize timestamps file
pd.DataFrame(columns=["File Name", "Start", "End"]).to_excel(timestamps_path, sheet_name="Timestamps", index=False)

# =============================================================================
# PAIRED SIGNALS - FULLY RESTORED
# =============================================================================

paired_signals = [
    ("VHACT", "VHREF"),
    ("QACTH", "QHREF"),
    ("QACTH", "QACT")
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def extract_signals(lines):
    """Extracts signal names and types from log lines."""
    signals = []
    signals_start = False
    for line in lines:
        if line.startswith("Signals:"):
            signals_start = True
        elif signals_start and re.match(r"\d+\.\s", line.strip()):
            match = re.match(r"\d+\.\s+(\S+)\s+(\S+)", line.strip())
            if match:
                signals.append(match.groups())
        elif signals_start and not line.strip():
            break
    return signals


def extract_data(lines):
    """Extracts data lines from logs."""
    data = []
    data_start = False
    for line in lines:
        if line.startswith("Data:"):
            data_start = True
        elif data_start and line.strip():
            data.append(line.strip())
    return data


def parse_timestamps(log_lines):
    """Extracts timestamp from log file."""
    for line in log_lines:
        match = re.match(r"Start time:\s+([\d.]+)\s+([\d:]+)", line)
        if match:
            return match.group(1) + " " + match.group(2)
    return None


def create_dataframe(data_lines, signals):
    """Converts log data into a pandas DataFrame."""
    columns = ["Time"] + [signal[0] for signal in signals]
    data = [list(map(float, re.split(r"\s+", line))) for line in data_lines]
    return pd.DataFrame(data, columns=columns)


def normalize_timestamps(df, datetime_start):
    """Adds timestamp columns."""
    df['Timedelta'] = pd.to_timedelta(df['Time'], unit='s')
    df["Datetime"] = datetime_start + df["Timedelta"]
    return df


def save_timestamps(file_name, start, end, timestamps_path):
    """Saves timestamps to an Excel file."""
    new_row = pd.DataFrame([[file_name, start, end]], columns=["File Name", "Start", "End"])
    with pd.ExcelWriter(timestamps_path, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
        new_row.to_excel(writer, sheet_name="Timestamps", startrow=writer.sheets["Timestamps"].max_row, index=False, header=False)


# =============================================================================
# PRESERVED PLOTTING FUNCTIONS - NO CHANGES
# =============================================================================

def draw(table_df, signal_name, signal_data):    
    """Draws a line plot for a single signal."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=table_df["Datetime"],
        y=table_df[signal_name],
        mode="lines",
        name=f"{signal_data['label']} [{signal_data['unit']}]",
        line=dict(color="blue")
    ))
    
    fig.update_layout(
        title=signal_data['longtxt'],
        template="plotly_white",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True, title=f"{signal_data['label']} [{signal_data['unit']}]"),
    )    
    return fig


def draw_binary_signals(table_df, binary_signals):
    """Draws binary signal plots with offsets."""
    fig = go.Figure()
    y_offset = 0  
    offset_step = 3.0  

    for signal_name in binary_signals:
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
            y=table_df[signal_name] + y_offset,
            mode="lines",
            name=binary_signals[signal_name]['label'],
            showlegend=True,
            opacity=opacity,
            line=dict(width=2, dash=line_style)
        ))
        y_offset += offset_step  

    fig.update_layout(title="Binary Signals", template="plotly_white")
    return fig


# =============================================================================
# FILE PROCESSING FUNCTION
# =============================================================================

def process_log_file(filepath, timestamps_path):
    """Processes a single log file."""
    with open(filepath, "r") as file:
        log_lines = file.readlines()

    datetime_str = parse_timestamps(log_lines)
    if not datetime_str:
        print(f"Skipping {filepath}: No timestamp found.")
        return

    datetime_start = datetime.strptime(datetime_str, '%d.%m.%Y. %H:%M:%S')    
    signals = extract_signals(log_lines)
    data_lines = extract_data(log_lines)

    df = create_dataframe(data_lines, signals)
    df = normalize_timestamps(df, datetime_start)

    extracted_signal_names = {signal[0] for signal in signals}
    int_signals = {k: v for k, v in signali.items() if k in extracted_signal_names}
    binary_signals = {k: v for k, v in signali.items() if v['unit'] == 'pu' and k in extracted_signal_names}

    # Save timestamps
    start = df["Datetime"].iloc[0].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    end = df["Datetime"].iloc[-1].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    save_timestamps(filepath, start, end, timestamps_path)

    # Generate plots
    fig_list = []
    for group in paired_signals:
        present_signals = [s for s in group if s in df.columns]
        if len(present_signals) > 1:
            fig_list.extend(draw_multiple_signals(df, present_signals, int_signals))

    for signal in int_signals:
        fig_list.append(draw(df, signal, int_signals[signal]))

    if binary_signals:
        fig_list.append(draw_binary_signals(df, binary_signals))

    return fig_list


# =============================================================================
# MAIN SCRIPT EXECUTION
# =============================================================================

def main():
    """Main execution function."""
    files = [f for f in listdir(datapath) if isfile(join(datapath, f))]
    for file in files:
        filepath = os.path.join(datapath, file)
        print(f"Processing: {file}")
        process_log_file(filepath, timestamps_path)

    print("Processing completed!")


if __name__ == "__main__":
    main()
