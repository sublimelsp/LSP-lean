from __future__ import annotations

from typing import TYPE_CHECKING

from LSP.plugin import LspPlugin, Session, SessionViewProtocol
from typing_extensions import override

from .plugin_infoview import LeanInfoview
from .plugin_unicode import unicode_input

if TYPE_CHECKING:
    import weakref


class Lean(LspPlugin):

    def __init__(self, weaksession: weakref.ref[Session]) -> None:
        super().__init__(weaksession)
        self.lean_infoview: LeanInfoview = LeanInfoview()

    @override
    def on_selection_modified_async(self, session_view: SessionViewProtocol) -> None:
        """Call when cursor position changes, performs goal state request."""
        session = session_view.session
        view = session_view.view
        # Get cursor position
        sel = view.sel()
        if len(sel) == 0:
            return
        point = sel[0].begin()
        row, col = view.rowcol(point)
        # Request goal state from Lean server
        self.lean_infoview.request_goal_state(session, view, row, col)


def plugin_loaded() -> None:
    Lean.register()
    unicode_input.load_abbreviations()  # Initialize unicode input


def plugin_unloaded() -> None:
    Lean.unregister()
