import sublime
import sublime_plugin
from glob import glob
import os
from os.path import abspath, dirname


class OpenVimPrjCommand(sublime_plugin.WindowCommand):
    def run(self):
        active_sheet = self.window.active_sheet()
        active_view = active_sheet.view()
        current_file = active_view.file_name()
        if not current_file.endswith('prj'):
            print('Open in Vim, file must be terminated with "prj"')
            return
        current_dir = dirname(current_file)
        os.chdir(current_dir)

        window = self.window
        active_group = window.active_group()

        prjList = []
        for v in window.views_in_group(active_group):
            file_name = v.file_name()
            if file_name:
                if file_name != current_file:
                    if file_name.endswith('prj'):
                        prjList.append(file_name)
                    window.focus_view(v)
                    window.run_command("close")
        prjList.insert(0, current_file)  # project at top of Open Files
        file_list_regions = active_view.split_by_newlines(sublime.Region(0, active_view.size()))
        filesList = []
        for region in file_list_regions:
            if (region.size() == 0):
                continue
            line = active_view.substr(region)
            if line and not line.startswith('#'):
                files = glob(line)
                filesList += files
        window.run_command("close")
        for file in prjList + sorted(filesList):
            self.window.open_file(abspath(file))

# End
