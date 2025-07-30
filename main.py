import time
import random
from rich.console import Console
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn, ProgressColumn
from rich.table import Table
from rich.text import Text

# Custom columns for units
class VoltageColumn(ProgressColumn):
    def render(self, task):
        return Text(f"{task.completed:.2f} V")

class TemperatureColumn(ProgressColumn):
    def render(self, task):
        return Text(f"{task.completed:.1f} °C")

class PercentColumn(ProgressColumn):
    def render(self, task):
        return Text(f"{task.completed:.0f} %")

# Console and battery initial state
console = Console()
battery_charge = 100.0
last_discharge_time = time.time()

# Initialize progress bars
voltage_bar = Progress(
    TextColumn("[bold blue]Battery Voltage:"),
    BarColumn(bar_width=30),
    VoltageColumn(),
    expand=True,
)

charge_bar = Progress(
    TextColumn("[bold green]Battery Charge: "),
    BarColumn(bar_width=30),
    PercentColumn(),
    expand=True,
)

motor_bar = Progress(
    TextColumn("[bold red]Motor Temp:      "),
    BarColumn(bar_width=30),
    TemperatureColumn(),
    expand=True,
)

cpu_bar = Progress(
    TextColumn("[bold yellow]CPU Temp:        "),
    BarColumn(bar_width=30),
    TemperatureColumn(),
    expand=True,
)

# Add tasks to each bar
voltage_task = voltage_bar.add_task("voltage", total=15.0, completed=12.6)
charge_task = charge_bar.add_task("charge", total=100.0, completed=battery_charge)
motor_task = motor_bar.add_task("motor", total=120.0, completed=40.0)
cpu_task = cpu_bar.add_task("cpu", total=100.0, completed=50.0)

# Start the bars (required to render inside Live)
voltage_bar.start()
charge_bar.start()
motor_bar.start()
cpu_bar.start()

# Layout builder
def generate_layout():
    table = Table.grid(padding=1)
    table.add_row(voltage_bar)
    table.add_row(charge_bar)
    table.add_row(motor_bar)
    table.add_row(cpu_bar)
    return table

# Live dashboard loop
with Live(generate_layout(), refresh_per_second=2, screen=False) as live:
    try:
        while True:
            now = time.time()

            # Simulate values
            battery_voltage = random.uniform(11.8, 12.7)
            motor_temp = random.uniform(35.0, 60.0)
            cpu_temp = random.uniform(45.0, 70.0)

            # Discharge battery every 10s
            if now - last_discharge_time >= 10:
                battery_charge = max(0.0, battery_charge - random.uniform(1.0, 3.0))
                last_discharge_time = now

            # Update progress bars
            voltage_bar.update(voltage_task, completed=battery_voltage)
            charge_bar.update(charge_task, completed=battery_charge)
            motor_bar.update(motor_task, completed=motor_temp)
            cpu_bar.update(cpu_task, completed=cpu_temp)

            time.sleep(1)

    finally:
        # Stop all progress bars on exit
        voltage_bar.stop()
        charge_bar.stop()
        motor_bar.stop()
        cpu_bar.stop()
