#!/usr/bin/python

import sublime
import sublime_plugin

history = []
history_index = 0


class ClipboardDisplayCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if not history:
            return
        # sublime has been known to choke and die on really big clipboard
        # items getting displayed in the quick panel. Also, the truncation
        # it uses for stuff that long is basically unreadable. Ergo...
        summary = [item.strip()[:100] for item in history]
        self.view.window().show_quick_panel(summary, self.panel_done)

    def panel_done(self, picked):
        global history_index
        if 0 > picked < len(history):
            return

        history_index = picked

        s = sublime.load_settings("ClipboardHistory.sublime-settings")

        sublime.set_clipboard(history[picked])
        if s.get('paste_and_indent'):
            self.view.run_command('paste_and_indent')
        else:
            self.view.run_command('paste')

class ClipboardPastePreviousCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global history_index
        if history:
            history_index = min(history_index + 1, len(history) - 1)
            sublime.set_clipboard(history[history_index])

        s = sublime.load_settings("ClipboardHistory.sublime-settings")

        if s.get('paste_and_indent'):
            self.view.run_command('paste_and_indent')
        else:
            self.view.run_command('paste')

class ClipboardPasteNextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global history_index
        if history:
            history_index = max(history_index - 1, 0)
            sublime.set_clipboard(history[history_index])

        s = sublime.load_settings("ClipboardHistory.sublime-settings")

        if s.get('paste_and_indent'):
            self.view.run_command('paste_and_indent')
        else:
            self.view.run_command('paste')

# Here we see a cunning plan. We listen for a key, but never say we
# support it. This lets us respond to ctrl-c and ctrl-x, without having
# to re-implement the copy and cut commands. (Important, since
# run_command("copy") doesn't do anything.)
class ClipboardListner(sublime_plugin.EventListener):
    def on_query_context(self, view, key, *args):
        global history_index
        if key != "clipboardcopy_fake":
            return None
        for selected in view.sel():
            selected = view.sel()[0]
            if selected.empty():
                selected = view.line(selected)

            text = view.substr(selected)

            if not history or history[0] != text:
                history.insert(0, text)
                history_index = 0

        s = sublime.load_settings("ClipboardHistory.sublime-settings")
        if s.get("limit") < len(history):
            for i in xrange(len(history) - s.get("limit")):
                history.pop()

        return None
