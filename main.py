import time
import random
from rich.console import Console
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn, ProgressColumn
from rich.table import Table
from rich.text import Text

class VoltageColumn(ProgressColumn):
    def render(self, task):
        return Text(f"{task.completed:.2f} V")

class TemperatureColumn(ProgressColumn):
    def render(self, task):
        return Text(f"{task.completed:.1f} °C")

class PercentColumn(ProgressColumn):
    def render(self, task):
        return Text(f"{task.completed:.0f} %")

# Initialize console and progress bars
console = Console()
battery_charge = 100.0  # in %
last_discharge_time = time.time()

progress = Progress(
    TextColumn("[bold blue]Battery Voltage:"),
    BarColumn(bar_width=30),
    VoltageColumn(),
    expand=True,
)

battery_bar = Progress(
    TextColumn("[bold green]Battery Charge:"),
    BarColumn(bar_width=30),
    PercentColumn(),
    expand=True,
)

motor_temp_bar = Progress(
    TextColumn("[bold red]Motor Temp:      "),
    BarColumn(bar_width=30),
    TemperatureColumn(),
    expand=True,
)

cpu_temp_bar = Progress(
    TextColumn("[bold yellow]CPU Temp:        "),
    BarColumn(bar_width=30),
    TemperatureColumn(),
    expand=True,
)

battery_task = progress.add_task("battery_voltage", total=15.0, completed=12.6)
charge_task = battery_bar.add_task("battery_charge", total=100.0, completed=battery_charge)
motor_task = motor_temp_bar.add_task("motor_temp", total=120.0, completed=40.0)
cpu_task = cpu_temp_bar.add_task("cpu_temp", total=100.0, completed=50.0)

# Create layout
def generate_layout():
    table = Table.grid(padding=1)
    table.add_row(progress)
    table.add_row(battery_bar)
    table.add_row(motor_temp_bar)
    table.add_row(cpu_temp_bar)
    return table

with Live(generate_layout(), refresh_per_second=2, screen=False) as live:
    while True:
        # Simulate realistic sensor values
        battery_voltage = random.uniform(11.8, 12.7)
        motor_temp = random.uniform(35, 60)
        cpu_temp = random.uniform(45, 70)

        now = time.time()
        if now - last_discharge_time >= 10:
            battery_charge = max(0.0, battery_charge - random.uniform(1, 3))
            last_discharge_time = now

        # Update tasks
        progress.update(battery_task, completed=battery_voltage)
        battery_bar.update(charge_task, completed=battery_charge)
        motor_temp_bar.update(motor_task, completed=motor_temp)
        cpu_temp_bar.update(cpu_task, completed=cpu_temp)

        time.sleep(1)
