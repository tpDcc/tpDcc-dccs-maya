#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for tpMayaLib
"""

from __future__ import print_function, division, absolute_import

import os
import types
import pkgutil
import importlib
from collections import OrderedDict

# Do not remove Maya imports
import maya.cmds as cmds
import maya.mel as mel
import maya.utils as utils
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaAnim as OpenMayaAnim

new_api = True
try:
    import maya.api.OpenMaya as OpenMayaV2
    import maya.api.OpenMayaUI as OpenMayaUIV2
    import maya.api.OpenMayaAnim as OpenMayaAnimV2
except Exception:
    new_api = False

from tpPyUtils import logger as logger_utils

# =================================================================================

logger = None

# =================================================================================

api = {
    'OpenMaya': OpenMaya,
    'OpenMayaUI': OpenMayaUI,
    'OpenMayaAnim': OpenMayaAnim
}

if new_api:
    api2 = {
        'OpenMaya': OpenMayaV2,
        'OpenMayaUI': OpenMayaUIV2,
        'OpenMayaAnim': OpenMayaAnimV2
    }
else:
    api2 = api

OpenMaya = OpenMaya
OpenMayaUI = OpenMayaUI
OpenMayaAnim = OpenMayaAnim

# =================================================================================


class tpMayaLib(object):

    loaded_modules = OrderedDict()
    reload_modules = list()

    @classmethod
    def initialize(cls, do_reload=False):

        import tpMayaLib

        # By default, we use new Maya API
        use_new_api(True)

        cls.create_logger()
        cls.import_modules(tpMayaLib.__path__[0], only_packages=True, order=['tpMayaLib.data', 'tpMayaLib.managers', 'tpMayaLib.core'])

        if do_reload:
            cls.reload_all()

    @staticmethod
    def create_logger():
        """
        Creates and initializes tpMayaLib logger
        """

        global logger
        logger = logger_utils.Logger(name='tpMayaLib', level=logger_utils.LoggerLevel.WARNING)
        logger.debug('Initializing tpMayaLib logger ...')
        return logger

    @staticmethod
    def _explore_package(module_name, only_packages=False):
        """
        Load module iteratively
        :param module_name: str, name of the module
        :return: list<str>, list<str>, list of loaded module names and list of loaded module paths
        """

        import tpMayaLib

        module_names = list()
        module_paths = list()

        def foo(name, only_packages):
            for importer, m_name, is_pkg in pkgutil.iter_modules([name]):
                mod_path = name + "//" + m_name
                mod_name = 'tpMayaLib.' + os.path.relpath(mod_path, tpMayaLib.__path__[0]).replace('\\', '.')
                if only_packages:
                    if is_pkg:
                        module_paths.append(mod_path)
                        module_names.append(mod_name)
                else:
                    module_paths.append(mod_path)
                    module_names.append(mod_name)
                # foo(mod_path, only_packages)

        foo(module_name, only_packages)

        return module_names, module_paths

    @staticmethod
    def _import_module(package_name):

        import tpMayaLib

        try:
            mod = importlib.import_module(package_name)
            tpMayaLib.logger.debug('Imported: {}'.format(package_name))
            if mod and isinstance(mod, types.ModuleType):
                return mod
            return None
        except (ImportError, AttributeError) as e:
            tpMayaLib.logger.debug('FAILED IMPORT: {} -> {}'.format(package_name, str(e)))
            pass

    @classmethod
    def import_modules(cls, module_name, only_packages=False, order=[]):
        names, paths = cls._explore_package(module_name=module_name, only_packages=only_packages)
        ordered_names = list()
        ordered_paths = list()
        temp_index = 0
        i = -1
        for o in order:
            for n, p in zip(names, paths):
                if str(n) == str(o):
                    i += 1
                    temp_index = i
                    ordered_names.append(n)
                    ordered_paths.append(p)
                elif n.endswith(o):
                    ordered_names.insert(temp_index + 1, n)
                    ordered_paths.insert(temp_index + 1, n)
                    temp_index += 1
                elif str(o) in str(n):
                    ordered_names.append(n)
                    ordered_paths.append(p)

        ordered_names.extend(names)
        ordered_paths.extend(paths)

        names_set = set()
        paths_set = set()
        module_names = [x for x in ordered_names if not (x in names_set or names_set.add(x))]
        module_paths = [x for x in ordered_paths if not (x in paths_set or paths_set.add(x))]

        reloaded_names = list()
        reloaded_paths = list()
        for n, p in zip(names, paths):
            reloaded_names.append(n)
            reloaded_paths.append(p)

        for name, _ in zip(module_names, module_paths):
            if name not in cls.loaded_modules.keys():
                mod = cls._import_module(name)
                if mod:
                    if isinstance(mod, types.ModuleType):
                        cls.loaded_modules[mod.__name__] = [os.path.dirname(mod.__file__), mod]
                        cls.reload_modules.append(mod)

        for name, path in zip(module_names, module_paths):
            order = list()
            if name in cls.loaded_modules.keys():
                mod = cls.loaded_modules[name][1]
                if hasattr(mod, 'order'):
                    order = mod.order
            cls.import_modules(module_name=path, only_packages=False, order=order)

    @classmethod
    def reload_all(cls):
        """
        Reload all current loaded modules
        """

        import tpMayaLib

        tpMayaLib.logger.debug(' =========> Reloading tpMayaLib ...')

        for mod in cls.reload_modules:
            if not hasattr(mod, 'no_reload'):
                tpMayaLib.logger.debug('RELOADING: {}'.format(mod.__name__))
                reload(mod)
            else:
                tpMayaLib.logger.debug('AVOIDING RELOAD OF {}'.format(mod))
        tpMayaLib.logger.debug(' =========> tpMayaLib reloaded successfully!')

    @staticmethod
    def create_metadata_manager():
        from tpMayaLib.managers import metadatamanager
        metadatamanager.MetaDataManager.register_meta_classes()
        metadatamanager.MetaDataManager.register_meta_types()
        metadatamanager.MetaDataManager.register_meta_nodes()

# =================================================================================


def use_new_api(flag=False):
    """
    Enables new Maya API usage
    """

    global OpenMaya
    global OpenMayaUI
    global OpenMayaAnim

    if new_api:
        if flag:
            OpenMaya = api2['OpenMaya']
            OpenMayaUI = api2['OpenMayaUI']
            OpenMayaAnim = api2['OpenMayaAnim']
        else:
            OpenMaya = api['OpenMaya']
            OpenMayaUI = api['OpenMayaUI']
            OpenMayaAnim = api['OpenMayaAnim']
    else:
        OpenMaya = api['OpenMaya']
        OpenMayaUI = api['OpenMayaUI']
        OpenMayaAnim = api['OpenMayaAnim']


def is_new_api():
    """
    Returns whether new Maya API is used or not
    :return: bool
    """

    return not OpenMaya == api['OpenMaya']

# =================================================================================


def init(do_reload=False):
    tpMayaLib.initialize(do_reload=do_reload)
