from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich.panel import Panel as RichPanel
import json

def Panel():
    with open("./utils/config.json", "r") as json_file:
        data = json.load(json_file)
    print(" ")
    # Define custom styles for ON and OFF
    on_style = Style(color="green", bold=True)
    off_style = Style(color="red", bold=True)

    # Create a table with 2 columns
    table = Table(title="Discord Server Cloner", show_header=True, header_style="bold")
    table.add_column("Setting", style="cyan", no_wrap=True, width=30)
    table.add_column("Status", justify="center", width=10)

    for setting, status in data["copy_settings"].items():
        table.add_row(setting.capitalize(), Text("ON" if status else " OFF", style=on_style if status else off_style))

    console = Console()
    console.print(table)

    # Paragraph with change logs
    paragraph = """Discord has removed the functionality for bots to create a server automatically. You will have to create a server manually and provide the server ID and the server you want to clone."""
    console.print(RichPanel(paragraph, style="bold blue", width=47))
    
    # Version information
    version = "2.0.1"
    console.print(RichPanel(f"Version: {version}", style="bold magenta", width=47))


def Panel_Run(guild, user):
    with open("./utils/config.json", "r") as json_file:
        data = json.load(json_file)
    print(" ")
    # Define custom styles for ON and OFF
    on_style = Style(color="green", bold=True)
    off_style = Style(color="red", bold=True)

    # Create a table with 2 columns
    table = Table(title="Discord Server Cloner", show_header=True, header_style="bold")
    table.add_column("Cloner is Running...", style="cyan", no_wrap=True, width=30)
    table.add_column("Status", justify="center", width=10)

    for setting, status in data["copy_settings"].items():
        table.add_row(setting.capitalize(), Text("ON" if status else " OFF", style=on_style if status else off_style))

    # Stick a new table in the footer
    footer = Table(show_header=False, header_style="bold", show_lines=False, width=47)
    footer.add_column(justify="center")
    footer.add_row(f"[bold magenta]Server ID: [green]{guild}")
    footer.add_row(f"[bold magenta]Logged in as: [green]{user}")

    console = Console()
    console.print(table)
    console.print(footer)

    # Paragraph with change logs
    paragraph = """Discord has removed the functionality for bots to create a server automatically. You will have to create a server manually and provide the server ID and the server you want to clone."""
    console.print(RichPanel(paragraph, style="bold blue", width=47))
    
    # Version information
    version = "2.0.1"
    console.print(RichPanel(f"Version: {version}", style="bold magenta", width=47))
