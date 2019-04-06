#! /usr/bin/env python
# # -*- coding: utf-8 -*-

"""
Module that contains functions and classes related with attributes
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import *

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import tpMayaLib as maya
from tpPyUtils import osplatform
# from tpRigToolkit.core import abstractdcc
# from tpRigToolkit.core.gui import window
from tpMayaLib.core import gui, helpers, directory, scene


class MayaDcc(abstractdcc.AbstractDCC, object):

    @staticmethod
    def get_name():
        return tpRigToolkit.Dccs.Maya

    @staticmethod
    def get_main_window():
        return gui.get_maya_window()

    @staticmethod
    def get_version():
        return helpers.get_maya_version()

    @staticmethod
    def get_dockable_window_class():
        return MayaDockedWindow

    @staticmethod
    def get_progress_bar(**kwargs):
        return MayaProgessBar(**kwargs)

    @staticmethod
    def get_progress_bar_class():
        """
        Return class of progress bar
        :return: class
        """

        return MayaProgessBar

    @staticmethod
    def new_scene(force=True, do_save=True):
        scene.new_scene(force=force, do_save=do_save)

    @staticmethod
    def select_file(caption, filters, start_dir=None):
        """
        Opens a select file dialog with DCC dialog
        :param caption: str, caption of the dialog
        :param filters: str, filter to use
        :param start_dir: str, start directory of the dialog
        :return: str, selected path
        """

        return directory.get_file(caption=caption, filters=filters)


class MayaProgessBar(abstractdcc.AbstractProgressBar, object):
    """
    Util class to manipulate Maya progress bar
    """

    def __init__(self, title='', count=None, begin=True):
        super(MayaProgessBar, self).__init__(title=title, count=count, begin=begin)

        if cmds.about(batch=True):
            self.title = title
            self.count = count
            msg = '{} count: {}'.format(title, count)
            self.status_string = ''
            tpRigToolkit.logger.debug(msg)
            return
        else:
            self.progress_ui = gui.get_progress_bar()
            if begin:
                self.__class__.inc_value = 0
                self.end()
            if not title:
                title = cmds.progressBar(self.progress_ui, query=True, status=True)
            if not count:
                count = cmds.progressBar(self.progress_ui, query=True, maxValue=True)

            cmds.progressBar(self.progress_ui, edit=True, beginProgress=begin, isInterruptable=True, status=title, maxValue=count)

    # region Public Functions
    def set_count(self, count_number):
        cmds.progressBar(self.progress_ui, edit=True, maxValue=int(count_number))

    def get_count(self):
        return cmds.progressBar(self.progress_ui, query=True, maxValue=True)

    def inc(self, inc=1):
        """
        Set the current increment
        :param inc: int, increment value
        """

        if cmds.about(batch=True):
            return

        super(MayaProgessBar, self).inc(inc)

        cmds.progressBar(self.progress_ui, edit=True, step=inc)

    def step(self):
        """
        Increments current progress value by one
        """

        if cmds.about(batch=True):
            return

        self.__class__.inc_value += 1
        cmds.progressBar(self.progress_ui, edit=True, step=1)

    def status(self, status_str):
        """
        Set the status string of the progress bar
        :param status_str: str
        """

        if cmds.about(batch=True):
            self.status_string = status_str
            return

        cmds.progressBar(self.progress_ui, edit=True, status=status_str)

    def end(self):
        """
        Ends progress bar
        """

        if cmds.about(batch=True):
            return

        if cmds.progressBar(self.progress_ui, query=True, isCancelled=True):
            cmds.progressBar(self.progress_ui, edit=True, beginProgress=True)

        cmds.progressBar(self.progress_ui, edit=True, ep=True)

    def break_signaled(self):
        """
        Breaks the progress bar loop so that it stop and disappears
        """

        if cmds.about(batch=True):
            return False

        break_progress = cmds.progressBar(self.progress_ui, query=True, isCancelled=True)
        if break_progress:
            self.end()
            if osplatform.get_env_var('RIGTASK_RUN') == 'True':
                osplatform.set_env_var('RIGTASK_STOP', True)
            return True

        return False
    # endregion


class MayaDockedWindow(MayaQWidgetDockableMixin, window.MainWindow):
    def __init__(self, parent=None, **kwargs):
        self._dock_area = kwargs.get('dock_area', 'right')
        self._dock = kwargs.get('dock', False)
        super(MayaDockedWindow, self).__init__(parent=parent, **kwargs)

        self.setProperty('saveWindowPref', True)

        if self._dock:
            self.show(dockable=True, floating=False, area=self._dock_area)

    def ui(self):
        if self._dock:
            ui_name = str(self.objectName())
            if cmds.about(version=True) >= 2017:
                workspace_name = '{}WorkspaceControl'.format(ui_name)
                workspace_name = workspace_name.replace(' ', '_')
                workspace_name = workspace_name.replace('-', '_')
                if cmds.workspaceControl(workspace_name, exists=True):
                    cmds.deleteUI(workspace_name)
            else:
                dock_name = '{}DockControl'.format(ui_name)
                dock_name = dock_name.replace(' ', '_')
                dock_name = dock_name.replace('-', '_')
                # dock_name = 'MayaWindow|%s' % dock_name       # TODO: Check if we need this
                if cmds.dockControl(dock_name, exists=True):
                    cmds.deleteUI(dock_name, control=True)

            self.setAttribute(Qt.WA_DeleteOnClose, True)

        super(MayaDockedWindow, self).ui()


tpRigToolkit.Dcc = MayaDcc
