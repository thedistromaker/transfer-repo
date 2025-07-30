from rich.progress import Progress, BarColumn, TextColumn
from rich.live import Live
from rich.table import Table
import time
import random

def get_mock_data():
    return {
        "Battery Voltage": round(random.uniform(10.5, 13.0), 2),  # volts
        "Motor Temp": round(random.uniform(30.0, 90.0), 1),       # Celsius
        "CPU Temp": round(random.uniform(40.0, 75.0), 1),         # Celsius
    }

def scale_value(value, min_val, max_val):
    """Scale value to 0-100 range."""
    return max(0, min(100, int((value - min_val) / (max_val - min_val) * 100)))

def make_table(data):
    table = Table(title="System Telemetry", expand=True)

    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_column("Progress")

    for name, value in data.items():
        if name == "Battery Voltage":
            percent = scale_value(value, 10.0, 13.0)
        elif name == "Motor Temp":
            percent = scale_value(value, 20.0, 100.0)
        elif name == "CPU Temp":
            percent = scale_value(value, 30.0, 85.0)
        else:
            percent = 0

        progress_bar = f"[blue]{'█' * (percent // 5)}{' ' * (20 - percent // 5)}[/]"
        table.add_row(name, f"{value}", progress_bar)

    return table

if __name__ == "__main__":
    with Live(refresh_per_second=4) as live:
        while True:
            mock_data = get_mock_data()
            table = make_table(mock_data)
            live.update(table)
            time.sleep(1)
