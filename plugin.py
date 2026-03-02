from __future__ import annotations

from .plugin_infoview import LeanInfoview
from .plugin_unicode import unicode_input
from .plugin_utils import PACKAGE_NAME
from .plugin_utils import SETTINGS_FILE
from LSP.plugin import AbstractPlugin
from LSP.plugin import register_plugin
from LSP.plugin import Session
from LSP.plugin import SessionViewProtocol
from LSP.plugin import unregister_plugin
from typing import override
import sublime
import weakref


class Lean(AbstractPlugin):
    """
    Represents the plugin itself
    """

    @classmethod
    def name(cls) -> str:
        return PACKAGE_NAME

    @classmethod
    def configuration(cls) -> tuple[sublime.Settings, str]:
        file_name = SETTINGS_FILE
        file_path = f"Packages/{PACKAGE_NAME}/{file_name}"
        return sublime.load_settings(file_name), file_path

    def __init__(self, weaksession: 'weakref.ref[Session]') -> None:
        super().__init__(weaksession)
        self.lean_infoview: LeanInfoview = LeanInfoview()

    @override
    def on_selection_modified_async(self, session_view: SessionViewProtocol):
        """
        Called when cursor position changes, performs goal state request
        """
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
    register_plugin(Lean)
    unicode_input.load_abbreviations()  # Initialize unicode input


def plugin_unloaded() -> None:
    unregister_plugin(Lean)
