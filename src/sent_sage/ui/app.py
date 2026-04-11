from textual.app import App
from sent_sage.ui.screens.home import ContainersTest
from pathlib import Path


class SentSageApp(App):
    CSS_PATH = Path(__file__).parent / "css" / "main.css"
    ...

    def on_mount(self):
        self.push_screen(ContainersTest())

