from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static
from textual.screen import Screen  
from pathlib import Path

class ContainersTest(Screen):
    
    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(classes="column"):
                yield Static("One")
                yield Static("Two")

            with Vertical(classes="column"):
                yield Static("Three")
                yield Static("Four")

