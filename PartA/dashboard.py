# imports
import os
from datetime import datetime

import pandas as pd
import serial
import serial.tools.list_ports

from dash import Dash, dcc, html, dash_table, Input, Output, State, ctx
import plotly.express as px

import webbrowser
import threading

# The CSV file where readings are saved or appended.
DATA_FILE = "moisture_history.csv"
# Arduino default baud rate must math baud rate in arduino code
DEFAULT_BAUD_RATE = 9600
# Dry soil threshold, minimum moisture content in arduino code to turn the LED Red
DRY_THRESHOLD = 25

arduino = None

# HELPER FUNCTIONS ---------------------------------------------------------------------
def get_available_ports():
    """
    Finds available serial ports on the computer.
    """
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def load_saved_data():
    """
    Loads old readings from the CSV file when the dashboard starts.

    If the file does not exist yet, an empty table is created.
    """
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df

    return pd.DataFrame(columns=["timestamp", "moisture", "status"])

def parse_arduino_line(line):
    """
    Converts one Arduino Serial line into a moisture reading.

    Accepted examples: "45" "45.5" "45,OK" "32,DRY"
    Returns: moisture value as a float

    If the line cannot be read as a number, it returns None.
    """
    try:
        # Remove spaces and new line characters.
        line = line.strip()
        # If Arduino sends "45,OK", split it and take only "45".
        first_value = line.split(",")[0]
        # Convert the value to a number.
        moisture = float(first_value)
        return moisture
    
    except ValueError:
        # if Arduino sends something that is not a number.
        return None

def read_from_arduino():
    """
    Reads one line from the Arduino.

    Returns:
        moisture value if a valid reading is received
        None if there is no reading or if Arduino is not connected
    """
    global arduino
    
    if arduino is None:
        return None

    if not arduino.is_open:
        return None

    try:
        # Read one line from Serial.
        raw_line = arduino.readline().decode("utf-8", errors="ignore")

        if raw_line:
            return parse_arduino_line(raw_line)

    except Exception:
        return None
    
    return None

def calculate_status(moisture):
    """
    Decides whether the plant is OK or needs watering.
    """
    if moisture < DRY_THRESHOLD:
        return "DRY - Water Needed"

    return "OK"

def make_card(title, value):
    """
    Creates a simple dashboard card.
    """
    return html.Div(
        [
            html.Div(title, style={"fontSize": "14px", "color": "#666"}),
            html.Div(value, style={"fontSize": "26px", "fontWeight": "bold"}),
        ],
        style={
            "backgroundColor": "white",
            "padding": "18px",
            "borderRadius": "12px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.12)",
            "minWidth": "190px",
            "flex": "1",
        },
    )

def build_line_graph(df):
    """
    Builds the moisture-over-time line graph.
    """
    if df.empty:
        fig = px.line(title="No readings yet")
        fig.update_yaxes(range=[0, 100])
        return fig
    
    # Sort data by timestamp before plotting
    df = df.sort_values("timestamp")

    fig = px.line(
        df,
        x="timestamp",
        y="moisture",
        markers=True,
        title="Soil Moisture Over Time",
    )

    # Add a horizontal line showing the dry threshold.
    fig.add_hline(
        y=DRY_THRESHOLD,
        line_dash="dash",
        annotation_text="Dry Threshold",
    )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Moisture (%)",
        template="plotly_white",
    )
    fig.update_yaxes(range=[0, 100])

    return fig

# LOADING DATA ---------------------------------------------------------------------

# Load old data when the dashboard starts.
starting_df = load_saved_data()

# Detect ports when the dashboard starts.
available_ports = get_available_ports()

# Select first detected port if available, else show COM3.
default_port = available_ports[0] if available_ports else "COM3"

# APP LAYOUT ---------------------------------------------------------------------

app = Dash(__name__)
app.title = "Plant Monitor Dashboard"

app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f2f4f8",
        "padding": "24px",
        "minHeight": "100vh",
    },
    children=[
        html.H1("Remote Plant Monitor Dashboard"),

        # This hidden storage keeps the readings inside the browser.
        dcc.Store(id="data-store", data=starting_df.to_dict("records")),

        # This timer updates the dashboard every 2 seconds.
        dcc.Interval(id="update-timer", interval=2000, n_intervals=0),

        # Connection controls
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Serial Port"),
                        dcc.Dropdown(
                            id="port-dropdown",
                            options=[{"label": port, "value": port} for port in available_ports]
                            if available_ports
                            else [{"label": default_port, "value": default_port}],
                            value=default_port,
                            clearable=False,
                        ),
                    ],
                    style={"flex": "1"},
                ),

                html.Div(
                    [
                        html.Label("Baud Rate"),
                        dcc.Input(
                            id="baud-input",
                            type="number",
                            value=DEFAULT_BAUD_RATE,
                            style={"width": "100%", "padding": "8px"},
                        ),
                    ],
                    style={"flex": "1"},
                ),
            ],
            style={"display": "flex", "gap": "16px", "marginBottom": "16px"},
        ),
        
        # Buttons
        html.Div(
            [
                html.Button("Connect", id="connect-button", n_clicks=0),
                html.Button("Save & Disconnect", id="save_disconnect-button", n_clicks=0),
            ],
            style={"display": "flex", "gap": "10px", "marginBottom": "16px"},
        ),

        html.Div(id="connection-message", style={"fontWeight": "bold", "marginBottom": "20px"}),

        # Summary cards
        html.Div(
            id="summary-cards",
            style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "marginBottom": "20px"},
        ),

        # Graph
        dcc.Graph(id="moisture-graph"),

        # Recent readings table
        html.H2("Recent Readings (Logs)"),
        dash_table.DataTable(
            id="readings-table",
            page_size=10,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "padding": "8px"},
            style_header={"fontWeight": "bold", "backgroundColor": "#e9ecef"},
        ),
    ],
)

# CALLBACK: CONNECT / DISCONNECT / SAVE ---------------------------------------------------------------------

@app.callback(
    Output("connection-message", "children"),
    Input("connect-button", "n_clicks"),
    Input("save_disconnect-button", "n_clicks"),
    State("port-dropdown", "value"),
    State("baud-input", "value"),
    State("data-store", "data"),
    prevent_initial_call=True,
)

def handle_buttons(connect_clicks, save_disconnect_clicks, port, baud_rate, stored_data):
    """
    This function runs when the user clicks any button
        - Connect
        - Save & Disconnect
    """
    
    global arduino
    
    button_clicked = ctx.triggered_id

    if button_clicked == "connect-button":
        try:
            arduino = serial.Serial(port, int(baud_rate), timeout=1)
            print(arduino)
            return f"Connected to Arduino on {port} at {baud_rate} baud."

        except Exception as error:
            arduino = None
            return f"Connection failed: {error}"

    if button_clicked == "save_disconnect-button":
        # Save the current dashboard data
        df = pd.DataFrame(stored_data)
        df.to_csv(DATA_FILE, index=False)

        # Disconnect from Arduino
        if arduino is not None and arduino.is_open:
            arduino.close()

        arduino = None

        return f"Data saved to {DATA_FILE} and Arduino disconnected."

    return "No action selected."

# CALLBACK: READ ARDUINO AND UPDATE DASHBOARD ---------------------------------------------------------------------

@app.callback(
    Output("data-store", "data"),
    Output("summary-cards", "children"),
    Output("moisture-graph", "figure"),
    Output("readings-table", "data"),
    Output("readings-table", "columns"),
    Input("update-timer", "n_intervals"),
    State("data-store", "data"),
)
def update_dashboard(n_intervals, stored_data):
    """
    This function runs automatically every 2 seconds.

    It:
    1. Reads a new Arduino value, if available.
    2. Adds it to the stored data.
    3. Calculates latest, daily average, and weekly average.
    4. Updates the graph and table.
    """

    # Convert stored browser data back into a Pandas DataFrame.
    df = pd.DataFrame(stored_data)

    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Try to read one new value from the Arduino.
    moisture = read_from_arduino()

    if moisture is not None:
        new_row = {
            "timestamp": datetime.now(),
            "moisture": moisture,
            "status": calculate_status(moisture),
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # If there is still no data, show empty dashboard.
    if df.empty:
        cards = [
            make_card("Latest Moisture", "N/A"),
            make_card("Today's Average", "N/A"),
            make_card("This Week's Average", "N/A"),
            make_card("Plant Status", "N/A"),
        ]

        return [], cards, build_line_graph(df), [], []

    # Make sure timestamp is treated as a datetime.
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Latest reading.
    latest_moisture = df["moisture"].iloc[-1]
    latest_status = df["status"].iloc[-1]

    # Today's readings.
    today = pd.Timestamp.now().date()
    today_df = df[df["timestamp"].dt.date == today]

    # Last 7 days readings.
    one_week_ago = pd.Timestamp.now() - pd.Timedelta(days=7)
    week_df = df[df["timestamp"] >= one_week_ago]

    # Calculate averages.
    today_average = today_df["moisture"].mean()
    week_average = week_df["moisture"].mean()

    cards = [
        make_card("Latest Moisture", f"{latest_moisture:.1f}%"),
        make_card("Today's Average", f"{today_average:.1f}%"),
        make_card("This Week's Average", f"{week_average:.1f}%"),
        make_card("Plant Status", latest_status),
    ]

    # Build graph.
    graph = build_line_graph(df)

    # Prepare recent readings table.
    recent_df = df.sort_values("timestamp", ascending=False).head(10).copy()
    recent_df["timestamp"] = recent_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")

    table_data = recent_df.to_dict("records")
    table_columns = [{"name": column.title(), "id": column} for column in recent_df.columns]

    # Return updated values to the dashboard.
    return df.to_dict("records"), cards, graph, table_data, table_columns

# RUN APP ---------------------------------------------------------------------

if __name__ == "__main__":
    url = "http://127.0.0.1:8050"
    
    print(">> Starting Plant Monitor Dashboard...")
    print(">> Open this link in your browser: http://127.0.0.1:8050")
    
    threading.Timer(1, lambda: webbrowser.open(url)).start()
    
    app.run(debug=False, use_reloader=False, threaded=False)
