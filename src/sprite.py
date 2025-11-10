from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Container
from textual.reactive import reactive

'''
This class is experimental and is not used in the current project as it conflicts with the curses lib
'''
class Sprite(Static):
    """A simple textual 'sprite' widget."""
    # Reactive property to store the position (e.g., left offset)
    left_offset = reactive(0)

    def on_mount(self) -> None:
        """Animate the sprite when the app starts."""
        self.animate("left_offset", value=50, duration=3, easing="out_quad")

    def watch_left_offset(self, left_offset: int) -> None:
        """Called when the left_offset changes to update the style."""
        self.styles.offset = (left_offset, 0) # Apply the offset (x, y)

    def render(self) -> str:
        return "[bold yellow]>_<[/bold yellow]"

class SpriteApp(App):
    CSS = """
    Screen {
        layout: vertical;
        align: left top;
    }
    Sprite {
        width: auto;
        height: auto;
        padding: 0 1; /* Add some padding so it doesn't touch the edge */
    }
    """

    def compose(self) -> ComposeResult:
        yield Sprite()