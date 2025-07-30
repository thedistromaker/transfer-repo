import time
import random
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

def create_progress_bars():
    voltage_bar = Progress(
        TextColumn("[bold blue]Battery Voltage: "),
        BarColumn(bar_width=30),
        VoltageColumn(),
        expand=True,
    )
    charge_bar = Progress(
        TextColumn("[bold green]Battery Charge:  "),
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
        TextColumn("[bold yellow]CPU Temp:       "),
        BarColumn(bar_width=30),
        TemperatureColumn(),
        expand=True,
    )
    return voltage_bar, charge_bar, motor_bar, cpu_bar

def main():
    battery_charge = 100.0
    last_discharge_time = time.time()

    voltage_bar, charge_bar, motor_bar, cpu_bar = create_progress_bars()

    # Start all progress bars
    voltage_bar.start()
    charge_bar.start()
    motor_bar.start()
    cpu_bar.start()

    voltage_task = voltage_bar.add_task("voltage", total=15.0, completed=12.6)
    charge_task = charge_bar.add_task("charge", total=100.0, completed=battery_charge)
    motor_task = motor_bar.add_task("motor", total=120.0, completed=40.0)
    cpu_task = cpu_bar.add_task("cpu", total=100.0, completed=50.0)

    def generate_layout():
        table = Table.grid(padding=1)
        table.add_row(voltage_bar)
        table.add_row(charge_bar)
        table.add_row(motor_bar)
        table.add_row(cpu_bar)
        return table

    with Live(generate_layout(), refresh_per_second=2, screen=False) as live:
        try:
            while True:
                now = time.time()

                # Simulated data
                battery_voltage = random.uniform(11.8, 12.6)
                motor_temp = random.uniform(35.0, 65.0)
                cpu_temp = random.uniform(45.0, 70.0)

                # Decrease battery charge every 10 seconds
                if now - last_discharge_time >= 10:
                    battery_charge = max(0.0, battery_charge - random.uniform(1.0, 3.0))
                    last_discharge_time = now

                voltage_bar.update(voltage_task, completed=battery_voltage)
                charge_bar.update(charge_task, completed=battery_charge)
                motor_bar.update(motor_task, completed=motor_temp)
                cpu_bar.update(cpu_task, completed=cpu_temp)

                time.sleep(1)
        finally:
            voltage_bar.stop()
            charge_bar.stop()
            motor_bar.stop()
            cpu_bar.stop()

if __name__ == "__main__":
    main()
