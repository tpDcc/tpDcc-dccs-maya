#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains DCC functionality for Maya
"""

from __future__ import print_function, division, absolute_import

from tpQtLib.Qt.QtCore import *

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import tpDccLib
import tpMayaLib as maya
from tpDccLib.abstract import dcc as abstract_dcc, progressbar
from tpQtLib.core import window
from tpMayaLib.core import gui, helpers, name, shelf, namespace


class MayaDcc(abstract_dcc.AbstractDCC, object):

    @staticmethod
    def get_name():
        """
        Returns the name of the DCC
        :return: str
        """

        return tpDccLib.Dccs.Maya

    @staticmethod
    def get_version():
        """
        Returns version of the DCC
        :return: int
        """

        return helpers.get_maya_version()

    @staticmethod
    def is_batch():
        """
        Returns whether DCC is being executed in batch mode or not
        :return: bool
        """

        return maya.cmds.about(batch=True)

    @staticmethod
    def get_main_window():
        """
        Returns Qt object that references to the main DCC window
        :return:
        """

        return gui.get_maya_window()

    @staticmethod
    def execute_deferred(fn):
        """
        Executes given function in deferred mode
        """

        maya.utils.executeDeferred(fn)

    @staticmethod
    def object_exists(node):
        """
        Returns whether given object exists or not
        :return: bool
        """

        return maya.cmds.objExists(node)

    @staticmethod
    def object_type(node):
        """
        Returns type of given object
        :param node: str
        :return: str
        """

        return maya.cmds.objectType(node)

    @staticmethod
    def check_object_type(node, node_type):
        """
        Returns whether give node is of the given type or not
        :param node: str
        :param node_type: str
        :return: bool
        """

        return maya.cmds.objectType(node, isType=node_type)

    @staticmethod
    def node_handle(node):
        """
        Returns unique identifier of the given node
        :param node: str
        :return: str
        """

        return maya.cmds.ls(node, uuid=True)

    @staticmethod
    def node_type(node):
        """
        Returns node type of given object
        :param node: str
        :return: str
        """

        return maya.cmds.nodeType(node)

    @staticmethod
    def all_scene_objects(full_path=True):
        """
        Returns a list with all scene nodes
        :param full_path: bool
        :return: list<str>
        """

        return maya.cmds.ls(l=full_path)

    @staticmethod
    def rename_node(node, new_name):
        """
        Renames given node with new given name
        :param node: str
        :param new_name: str
        :return: str
        """

        return maya.cmds.rename(node, new_name)

    @staticmethod
    def select_object(node, replace_selection=False, **kwargs):
        """
        Selects given object in the current scene
        :param replace_selection: bool
        :param node: str
        """

        maya.cmds.select(node, replace=replace_selection, **kwargs)

    @staticmethod
    def select_hierarchy(root=None, add=False):
        """
        Selects the hierarchy of the given node
        If no object is given current selection will be used
        :param root: str
        :param add: bool, Whether new selected objects need to be added to current selection or not
        """

        if not root or not MayaDcc.object_exists(root):
            sel = maya.cmds.ls(selection=True)
            for obj in sel:
                if not add:
                    maya.cmds.select(clear=True)
                maya.cmds.select(obj, hi=True, add=True)
        else:
            maya.cmds.select(root, hi=True, add=add)

    @staticmethod
    def clear_selection():
        """
        Clears current scene selection
        """

        maya.cmds.select(clear=True)

    @staticmethod
    def delete_object(node):
        """
        Removes given node from current scene
        :param node: str
        """

        maya.cmds.delete(node)

    @staticmethod
    def selected_nodes(full_path=True):
        """
        Returns a list of selected nodes
        :param full_path: bool
        :return: list<str>
        """

        return maya.cmds.ls(sl=True, l=full_path)

    @staticmethod
    def all_shapes_nodes(full_path=True):
        """
        Returns all shapes nodes in current scene
        :param full_path: bool
        :return: list<str>
        """

        return maya.cmds.ls(shapes=True, l=full_path)

    @staticmethod
    def default_scene_nodes(full_path=True):
        """
        Returns a list of nodes that are created by default by the DCC when a new scene is created
        :param full_path: bool
        :return: list<str>
        """

        return maya.cmds.ls(defaultNodes=True)

    @staticmethod
    def node_short_name(node):
        """
        Returns short name of the given node
        :param node: str
        :return: str
        """

        return name.get_short_name(node)

    @staticmethod
    def node_object_color(node):
        """
        Returns the color of the given node
        :param node: str
        :return: list(int, int, int, int)
        """

        return maya.cmds.getAttr('{}.objectColor'.format(node))

    @staticmethod
    def node_override_enabled(node):
        """
        Returns whether the given node has its display override attribute enabled or not
        :param node: str
        :return: bool
        """

        return maya.cmds.getAttr('{}.overrideEnabled'.format(node))

    @staticmethod
    def namespace_separator():
        """
        Returns character used to separate namespace from the node name
        :return: str
        """

        return '|'

    @staticmethod
    def node_namespace(node):
        """
        Returns namespace of the given node
        :param node: str
        :return: str
        """

        return maya.cmds.referenceQuery(node, namespace=True)

    @staticmethod
    def node_parent_namespace(node):
        """
        Returns namespace of the given node parent
        :param node: str
        :return: str
        """

        return maya.cmds.referenceQuery(node, parentNamespace=True)

    @staticmethod
    def node_is_referenced(node):
        """
        Returns whether given node is referenced or not
        :param node: str
        :return: bool
        """

        return maya.cmds.referenceQuery(node, isNodeReferenced=True)

    @staticmethod
    def node_reference_path(node, without_copy_number=False):
        """
        Returns reference path of the referenced node
        :param node: str
        :param without_copy_number: bool
        :return: str
        """

        return maya.cmds.referenceQuery(node, filename=True, wcn=without_copy_number)

    @staticmethod
    def node_is_loaded(node):
        """
        Returns whether given node is loaded or not
        :param node: str
        :return: bool
        """

        return maya.cmds.referenceQuery(node, isLoaded=True)

    @staticmethod
    def node_is_locked(node):
        """
        Returns whether given node is locked or not
        :param node: str
        :return: bool
        """

        return maya.cmds.lockNode(node, q=True, l=True)

    @staticmethod
    def node_children(node, all_hierarchy=True, full_path=True):
        """
        Returns a list of children of the given node
        :param node: str
        :param all_hierarchy: bool
        :param full_path: bool
        :return: list<str>
        """

        return maya.cmds.listRelatives(node, children=True, allDescendents=all_hierarchy, shapes=False, fullPath=full_path)

    @staticmethod
    def node_parent(node, full_path=True):
        """
        Returns parent node of the given node
        :param node: str
        :param full_path: bool
        :return: str
        """

        node_parent = maya.cmds.listRelatives(node, parent=True, fullPath=full_path)
        if node_parent:
            node_parent = node_parent[0]

        return node_parent

    @staticmethod
    def node_root(node, full_path=True):
        """
        Returns hierarchy root node of the given node
        :param node: str
        :param full_path: bool
        :return: str
        """

        if not node:
            return None

        n = node
        while True:
            parent = maya.cmds.listRelatives(n, parent=True, fullPath=full_path)
            if not parent:
                break
            n = parent[0]

        return n

    @staticmethod
    def set_parent(node, parent):
        """
        Sets the node parent to the given parent
        :param node: str
        :param parent: str
        """

        maya.cmds.parent(node, parent)

    @staticmethod
    def node_nodes(node):
        """
        Returns referenced nodes of the given node
        :param node: str
        :return: list<str>
        """

        return maya.cmds.referenceQuery(node, nodes=True)

    @staticmethod
    def node_filename(node, no_copy_number=True):
        """
        Returns file name of the given node
        :param node: str
        :param no_copy_number: bool
        :return: str
        """

        return maya.cmds.referenceQuery(node, filename=True, withoutCopyNumber=no_copy_number)

    @staticmethod
    def list_node_types(type_string):
        """
        List all dependency node types satisfying given classification string
        :param type_string: str
        :return:
        """

        return maya.cmds.listNodeTypes(type_string)

    @staticmethod
    def list_nodes(node_name=None, node_type=None):
        """
        Returns list of nodes with given types. If no type, all scene nodes will be listed
        :param node_name:
        :param node_type:
        :return:  list<str>
        """

        if not node_name and not node_type:
            return maya.cmds.ls()

        if node_name and node_type:
            return maya.cmds.ls(node_name, type=node_type)
        elif node_name and not node_type:
            return maya.cmds.ls(node_name)
        elif not node_name and node_type:
            return maya.cmds.ls(type=node_type)

    @staticmethod
    def list_children(node, all_hierarchy=True, full_path=True, children_type=None):
        """
        Returns a list of chlidren nodes of the given node
        :param node:
        :param all_hierarchy:
        :param full_path:
        :param children_type:
        :return:
        """

        if children_type:
            return maya.cmds.listRelatives(node, children=True, allDescendents=all_hierarchy, fullPath=full_path, type=children_type)
        else:
            return maya.cmds.listRelatives(node, children=True, allDescendents=all_hierarchy, fullPath=full_path)

    @staticmethod
    def list_relatives(node, all_hierarchy=True, full_path=True, relative_type=None, shapes=False, intermediate_shapes=False):
        """
        Returns a list of relative nodes of the given node
        :param node:
        :param all_hierarchy:
        :param full_path:
        :param relative_type:
        :param shapes:
        :param intermediate_shapes:
        :return:
        """

        if relative_type:

            return maya.cmds.listRelatives(node, allDescendents=all_hierarchy, fullPath=full_path, type=relative_type, shapes=shapes, noIntermediate=not intermediate_shapes)
        else:
            return maya.cmds.listRelatives(node, allDescendents=all_hierarchy, fullPath=full_path, shapes=shapes, noIntermediate=not intermediate_shapes)

    @staticmethod
    def list_shapes(node, full_path=True, intermediate_shapes=False):
        """
        Returns a list of shapes of the given node
        :param node: str
        :param full_path: bool
        :param intermediate_shapes: bool
        :return: list<str>
        """

        return maya.cmds.listRelatives(node, shapes=True, fullPath=full_path, children=True, noIntermediate=not intermediate_shapes)

    @staticmethod
    def list_children_shapes(node, all_hierarchy=True, full_path=True, intermediate_shapes=False):
        """
        Returns a list of children shapes of the given node
        :param node:
        :param all_hierarchy:
        :param full_path:
        :param intermediate_shapes:
        :return:
        """

        return maya.cmds.listRelatives(node, shapes=True, fullPath=full_path, children=True, allDescendents=all_hierarchy, noIntermediate=not intermediate_shapes)

    @staticmethod
    def list_materials():
        """
        Returns a list of materials in the current scene
        :return: list<str>
        """

        return maya.cmds.ls(materials=True)

    @staticmethod
    def scene_namespaces():
        """
        Returns all the available namespaces in the current scene
        :return: list(str)
        """

        return namespace.get_all_namespaces()

    @staticmethod
    def change_namespace(old_namespace, new_namespace):
        """
        Changes old namespace by a new one
        :param old_namespace: str
        :param new_namespace: str
        """

        return maya.cmds.namespace(rename=[old_namespace, new_namespace])

    @staticmethod
    def change_filename(node, new_filename):
        """
        Changes filename of a given reference node
        :param node: str
        :param new_filename: str
        """

        return maya.cmds.file(new_filename, loadReference=node)

    @staticmethod
    def import_reference(filename):
        """
        Imports object from reference node filename
        :param filename: str
        """

        return maya.cmds.file(filename, importReference=True)

    @staticmethod
    def list_attributes(node, **kwargs):
        """
        Returns list of attributes of given node
        :param node: str
        :return: list<str>
        """

        return maya.cmds.listAttr(node, **kwargs)

    @staticmethod
    def list_user_attributes(node):
        """
        Returns list of user defined attributes
        :param node: str
        :return: list<str>
        """

        return maya.cmds.listAttr(node, userDefined=True)

    @staticmethod
    def add_string_attribute(node, attribute_name, keyable=False):
        """
        Adds a new string attribute into the given node
        :param node: str
        :param attribute_name: str
        :param keyable: bool
        """

        return maya.cmds.addAttr(node, ln=attribute_name, dt='string', k=keyable)

    @staticmethod
    def add_string_array_attribute(node, attribute_name, keyable=False):
        """
        Adds a new string array attribute into the given node
        :param node: str
        :param attribute_name: str
        :param keyable: bool
        """

        return maya.cmds.addAttr(node, ln=attribute_name, dt='stringArray', k=keyable)

    @staticmethod
    def attribute_query(node, attribute_name, **kwargs):
        """
        Returns attribute qyer
        :param node: str
        :param attribute_name: str
        :param kwargs:
        :return:
        """

        return maya.cmds.attributeQuery(attribute_name, node=node, **kwargs)

    @staticmethod
    def attribute_exists(node, attribute_name):
        """
        Returns whether given attribute exists in given node
        :param node: str
        :param attribute_name: str
        :return: bool
        """

        return maya.cmds.attributeQuery(attribute_name, node=node, exists=True)

    @staticmethod
    def is_attribute_locked(node, attribute_name):
        """
        Returns whether atribute is locked or not
        :param node: str
        :param attribute_name: str
        :return: bool
        """

        return maya.cmds.getAttr('{}.{}'.format(node, attribute_name, lock=True))

    @staticmethod
    def lock_attribute(node, attribute_name):
        """
        Locks given attribute in given node
        :param node: str
        :param attribute_name: str
        """

        return maya.cmds.setAttr('{}.{}'.format(node, attribute_name), lock=True)

    @staticmethod
    def unlock_attribute(node, attribute_name):
        """
        Locks given attribute in given node
        :param node: str
        :param attribute_name: str
        """

        return maya.cmds.setAttr('{}.{}'.format(node, attribute_name), lock=False)

    @staticmethod
    def get_attribute_value(node, attribute_name):
        """
        Returns the value of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :return: variant
        """

        return maya.cmds.getAttr('{}.{}'.format(node, attribute_name))

    @staticmethod
    def get_attribute_type(node, attribut_name):
        """
        Returns the type of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :return: variant
        """

        return maya.cmds.getAttr('{}.{}'.format(node, attribut_name), type=True)

    @staticmethod
    def set_attribute_by_type(node, attribute_name, attribute_value, attribute_type):
        """
        Sets the value of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :param attribute_value: variant
        :param attribute_type: str
        """

        return maya.cmds.setAttr('{}.{}'.format(node, attribute_name), attribute_value, type=attribute_type)

    @staticmethod
    def set_numeric_attribute_value(node, attribute_name, attribute_value, clamp=False):
        """
        Sets the integer value of the given attribute in the given node
       :param node: str
        :param attribute_name: str
        :param attribute_value: int
        :param clamp: bool
        :return:
        """

        return maya.cmds.setAttr('{}.{}'.format(node, attribute_name), attribute_value, clamp=clamp)

    @staticmethod
    def set_integer_attribute_value(node, attribute_name, attribute_value, clamp=False):
        """
        Sets the integer value of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :param attribute_value: int
        :param clamp: bool
        :return:
        """

        return maya.cmds.setAttr('{}.{}'.format(node, attribute_name), int(attribute_value), clamp=clamp)

    @staticmethod
    def set_float_attribute_value(node, attribute_name, attribute_value, clamp=False):
        """
        Sets the integer value of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :param attribute_value: int
        :param clamp: bool
        :return:
        """

        return maya.cmds.setAttr('{}.{}'.format(node, attribute_name), float(attribute_value), clamp=clamp)

    @staticmethod
    def set_string_attribute_value(node, attribute_name, attribute_value):
        """
        Sets the string value of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :param attribute_value: str
        """

        return maya.cmds.setAttr('{}.{}'.format(node, attribute_name), str(attribute_value), type='string')

    @staticmethod
    def delete_attribute(node, attribute_name):
        """
        Deletes given attribute of given node
        :param node: str
        :param attribute_name: str
        """

        return maya.cmds.deleteAttr(n=node, at=attribute_name)

    @staticmethod
    def list_connections(node, attribute_name):
        """
        List the connections of the given out attribute in given node
        :param node: str
        :param attribute_name: str
        :return: list<str>
        """

        return maya.cmds.listConnections('{}.{}'.format(node, attribute_name))

    @staticmethod
    def list_connections_of_type(node, connection_type):
        """
        Returns a list of connections with the given type in the given node
        :param node: str
        :param connection_type: str
        :return: list<str>
        """

        return maya.cmds.listConnections(node, type=connection_type)

    @staticmethod
    def list_source_destination_connections(node):
        """
        Returns source and destination connections of the given node
        :param node: str
        :return: list<str>
        """

        return maya.cmds.listConnections(node, source=True, destination=True)

    @staticmethod
    def list_source_connections(node):
        """
        Returns source connections of the given node
        :param node: str
        :return: list<str>
        """

        return maya.cmds.listConnections(node, source=True, destination=False)

    @staticmethod
    def list_destination_connections(node):
        """
        Returns source connections of the given node
        :param node: str
        :return: list<str>
        """

        return maya.cmds.listConnections(node, source=False, destination=True)

    @staticmethod
    def new_file(force=True):
        """
        Creates a new file
        :param force: bool
        """

        maya.cmds.file(new=True, f=force)

    @staticmethod
    def open_file(file_path, force=True):
        """
        Open file in given path
        :param file_path: str
        :param force: bool
        """

        return maya.cmds.file(file_path, o=True, f=force)

    @staticmethod
    def is_plugin_loaded(plugin_name):
        """
        Return whether given plugin is loaded or not
        :param plugin_name: str
        :return: bool
        """

        return maya.cmds.pluginInfo(plugin_name, query=True, loaded=True)

    @staticmethod
    def load_plugin(plugin_path, quiet=True):
        """
        Loads given plugin
        :param plugin_path: str
        :param quiet: bool
        """

        maya.cmds.loadPlugin(plugin_path, quiet=True)

    @staticmethod
    def unload_plugin(plugin_path):
        """
        Unloads the given plugin
        :param plugin_path: str
        """

        maya.cmds.unloadPlugin(plugin_path)

    @staticmethod
    def list_old_plugins():
        """
        Returns a list of old plugins in the current scene
        :return: list<str>
        """

        return maya.cmds.unknownPlugin(query=True, list=True)

    @staticmethod
    def remove_old_plugin(plugin_name):
        """
        Removes given old plugin from current scene
        :param plugin_name: str
        """

        return maya.cmds.unknownPlugin(plugin_name, remove=True)

    @staticmethod
    def is_component_mode():
        """
        Returns whether current DCC selection mode is component mode or not
        :return: bool
        """

        return maya.cmds.selectMode(query=True, component=True)

    @staticmethod
    def scene_name():
        """
        Returns the name of the current scene
        :return: str
        """

        return maya.cmds.file(query=True, sceneName=True)

    @staticmethod
    def scene_is_modified():
        """
        Returns whether current scene has been modified or not since last save
        :return: bool
        """

        return maya.cmds.file(query=True, modified=True)

    @staticmethod
    def save_current_scene(force=True):
        """
        Saves current scene
        :param force: bool
        """

        return maya.cmds.file(save=True, f=force)

    @staticmethod
    def confirm_dialog(title, message, button=None, cancel_button=None, default_button=None, dismiss_string=None):
        """
        Shows DCC confirm dialog
        :param title:
        :param message:
        :param button:
        :param cancel_button:
        :param default_button:
        :param dismiss_string:
        :return:
        """

        if button and cancel_button and dismiss_string and default_button:
            return maya.cmds.confirmDialog(title=title, message=message, button=button, cancelButton=cancel_button, defaultButton=default_button, dismissString=dismiss_string)

        if button:
            return maya.cmds.confirmDialog(title=title, message=message)
        else:
            return maya.cmds.confirmDialog(title=title, message=message, button=button)

    @staticmethod
    def warning(message):
        """
        Prints a warning message
        :param message: str
        :return:
        """

        maya.cmds.warning(message)

    @staticmethod
    def add_shelf_menu_item(parent, label, command='', icon=''):
        """
        Adds a new menu item
        :param parent:
        :param label:
        :param command:
        :param icon:
        :return:
        """

        return maya.cmds.menuItem(parent=parent, label=label, command=command, image=icon or '')

    @staticmethod
    def add_shelf_sub_menu_item(parent, label, icon=''):
        """
        Adds a new sub menu item
        :param parent:
        :param label:
        :param icon:
        :return:
        """

        return maya.cmds.menuItem(parent=parent, label=label, icon=icon or '', subMenu=True)

    @staticmethod
    def add_shelf_separator(shelf_name):
        """
        Adds a new separator to the given shelf
        :param shelf_name: str
        """

        return maya.cmds.separator(parent=shelf_name, manage=True, visible=True, horizontal=False, style='shelf', enableBackground=False, preventOverride=False)


    @staticmethod
    def shelf_exists(shelf_name):
        """
        Returns whether given shelf already exists or not
        :param shelf_name: str
        :return: bool
        """

        return shelf.shelf_exists(shelf_name=shelf_name)

    @staticmethod
    def create_shelf(shelf_name, shelf_label=None):
        """
        Creates a new shelf with the given name
        :param shelf_name: str
        :param shelf_label: str
        """

        return shelf.create_shelf(name=shelf_name)

    @staticmethod
    def delete_shelf(shelf_name):
        """
        Deletes shelf with given name
        :param shelf_name: str
        """

        return shelf.delete_shelf(shelf_name=shelf_name)

    @staticmethod
    def select_file_dialog(title, start_directory=None, pattern=None):
        """
        Shows select file dialog
        :param title: str
        :param start_directory: str
        :param pattern: str
        :return: str
        """

        res = maya.cmds.fileDialog2(fm=1, dir=start_directory, cap=title, ff=pattern)
        if res:
            res = res[0]

        return res

    @staticmethod
    def select_folder_dialog(title, start_directory=None):
        """
        Shows select folder dialog
        :param title: str
        :param start_directory: str
        :return: str
        """

        res = maya.cmds.fileDialog2(fm=3, dir=start_directory, cap=title)
        if res:
            res = res[0]

        return res

    @staticmethod
    def save_file_dialog(title, start_directory=None, pattern=None):
        """
        Shows save file dialog
        :param title: str
        :param start_directory: str
        :param pattern: str
        :return: str
        """

        res = maya.cmds.fileDialog2(fm=0, dir=start_directory, cap=title, ff=pattern)
        if res:
            res = res[0]

        return res

    @staticmethod
    def get_current_frame():
        """
        Returns current frame set in time slider
        :return: int
        """

        return gui.get_current_frame()

    @staticmethod
    def get_time_slider_range():
        """
        Return the time range from Maya time slider
        :return: list<int, int>
        """

        return gui.get_time_slider_range(highlighted=False)

    @staticmethod
    def fit_view(animation=True):
        """
        Fits current viewport to current selection
        :param animation: bool, Animated fit is available
        """

        maya.cmds.viewFit(an=animation)

    @staticmethod
    def refresh_viewport():
        """
        Refresh current DCC viewport
        """

        maya.cmds.refresh()

    @staticmethod
    def set_key_frame(node, attribute_name, **kwargs):
        """
        Sets keyframe in given attribute in given node
        :param node: str
        :param attribute_name: str
        :param kwargs:
        :return:
        """

        return maya.cmds.setKeyframe('{}.{}'.format(node, attribute_name), **kwargs)

    @staticmethod
    def copy_key(node, attribute_name, time=None):
        """
        Copy key frame of given node
        :param node: str
        :param attribute_name: str
        :param time: bool
        :return:
        """

        if time:
            return maya.cmds.copyKey('{}.{}'.format(node, attribute_name), time=time)
        else:
            return maya.cmds.copyKey('{}.{}'.format(node, attribute_name))

    @staticmethod
    def cut_key(node, attribute_name, time=None):
        """
        Cuts key frame of given node
        :param node: str
        :param attribute_name: str
        :param time: str
        :return:
        """

        if time:
            return maya.cmds.cutKey('{}.{}'.format(node, attribute_name), time=time)
        else:
            return maya.cmds.cutKey('{}.{}'.format(node, attribute_name))

    @staticmethod
    def paste_key(node, attribute_name, option, time, connect):
        """
        Paste copied key frame
        :param node: str
        :param attribute_name: str
        :param option: str
        :param time: (int, int)
        :param connect: bool
        :return:
        """

        return maya.cmds.pasteKey('{}.{}'.format(node, attribute_name), option=option, time=time, connect=connect)

    @staticmethod
    def offset_keyframes(node, attribute_name, start_time, end_time, duration):
        """
        Offset given node keyframes
        :param node: str
        :param attribute_name: str
        :param start_time: int
        :param end_time: int
        :param duration: float
        """

        return maya.cmds.keyframe('{}.{}'.format(node, attribute_name), relative=True, time=(start_time, end_time), timeChange=duration)

    @staticmethod
    def find_next_key_frame(node, attribute_name, start_time, end_time):
        """
        Returns next keyframe of the given one
        :param node: str
        :param attribute_name: str
        :param start_time: int
        :param end_time: int
        """

        return maya.cmds.findKeyframe('{}.{}'.format(node, attribute_name), time=(start_time, end_time), which='next')

    @staticmethod
    def set_flat_key_frame(self, node, attribute_name, start_time, end_time):
        """
        Sets flat tangent in given keyframe
        :param node: str
        :param attribute_name: str
        :param start_time: int
        :param end_time: int
        """

        return maya.cmds.keyTangent('{}.{}'.format(node, attribute_name), time=(start_time, end_time), itt='flat')

    @staticmethod
    def find_first_key_in_anim_curve(curve):
        """
        Returns first key frame of the given curve
        :param curve: str
        :return: int
        """

        return maya.cmds.findKeyframe(curve, which='first')

    @staticmethod
    def find_last_key_in_anim_curve(curve):
        """
        Returns last key frame of the given curve
        :param curve: str
        :return: int
        """

        return maya.cmds.findKeyframe(curve, which='last')

    @staticmethod
    def copy_anim_curve(curve, start_time, end_time):
        """
        Copies given anim curve
        :param curve: str
        :param start_time: int
        :param end_time: int
        """

        return maya.cmds.copyKey(curve, time=(start_time, end_time))

    @staticmethod
    def get_current_model_panel():
        """
        Returns the current model panel name
        :return: str | None
        """

        current_panel = maya.maya.cmds.getPanel(withFocus=True)
        current_panel_type = maya.maya.cmds.getPanel(typeOf=current_panel)

        if current_panel_type not in ['modelPanel']:
            return None

        return current_panel

    @staticmethod
    def enable_undo():
        """
        Enables undo functionality
        """

        maya.cmds.undoInfo(openChunk=True)


    @staticmethod
    def disable_undo():
        """
        Disables undo functionality
        """

        maya.cmds.undoInfo(closeChunk=True)

    @staticmethod
    def focus(object_to_focus):
        """
        Focus in given object
        :param object_to_focus: str
        """

        maya.cmds.setFocus(object_to_focus)

    @staticmethod
    def find_available_name(node_name, **kwargs):
        """
        Returns an available object name in current DCC scene
        :param node_name: str
        :param kwargs: dict
        :return: str
        """

        suffix = kwargs.get('suffix', None)
        index = kwargs.get('index', 0)
        padding = kwargs.get('padding', 0)
        letters = kwargs.get('letters', False)
        capital = kwargs.get('capital', False)

        return name.find_available_name(name=node_name, suffix=suffix, index=index, padding=padding, letters=letters, capital=capital)

    # =================================================================================================================

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


class MayaProgessBar(progressbar.AbstractProgressBar, object):
    """
    Util class to manipulate Maya progress bar
    """

    def __init__(self, title='', count=None, begin=True):
        super(MayaProgessBar, self).__init__(title=title, count=count, begin=begin)

        if maya.cmds.about(batch=True):
            self.title = title
            self.count = count
            msg = '{} count: {}'.format(title, count)
            self.status_string = ''
            maya.logger.debug(msg)
            return
        else:
            self.progress_ui = gui.get_progress_bar()
            if begin:
                self.__class__.inc_value = 0
                self.end()
            if not title:
                title = maya.cmds.progressBar(self.progress_ui, query=True, status=True)
            if not count:
                count = maya.cmds.progressBar(self.progress_ui, query=True, maxValue=True)

            maya.cmds.progressBar(self.progress_ui, edit=True, beginProgress=begin, isInterruptable=True, status=title, maxValue=count)

    # region Public Functions
    def set_count(self, count_number):
        maya.cmds.progressBar(self.progress_ui, edit=True, maxValue=int(count_number))

    def get_count(self):
        return maya.cmds.progressBar(self.progress_ui, query=True, maxValue=True)

    def inc(self, inc=1):
        """
        Set the current increment
        :param inc: int, increment value
        """

        if maya.cmds.about(batch=True):
            return

        super(MayaProgessBar, self).inc(inc)

        maya.cmds.progressBar(self.progress_ui, edit=True, step=inc)

    def step(self):
        """
        Increments current progress value by one
        """

        if maya.cmds.about(batch=True):
            return

        self.__class__.inc_value += 1
        maya.cmds.progressBar(self.progress_ui, edit=True, step=1)

    def status(self, status_str):
        """
        Set the status string of the progress bar
        :param status_str: str
        """

        if maya.cmds.about(batch=True):
            self.status_string = status_str
            return

        maya.cmds.progressBar(self.progress_ui, edit=True, status=status_str)

    def end(self):
        """
        Ends progress bar
        """

        if maya.cmds.about(batch=True):
            return

        if maya.cmds.progressBar(self.progress_ui, query=True, isCancelled=True):
            maya.cmds.progressBar(self.progress_ui, edit=True, beginProgress=True)

        maya.cmds.progressBar(self.progress_ui, edit=True, ep=True)

    def break_signaled(self):
        """
        Breaks the progress bar loop so that it stop and disappears
        """

        if maya.cmds.about(batch=True):
            return False

        break_progress = maya.cmds.progressBar(self.progress_ui, query=True, isCancelled=True)
        if break_progress:
            self.end()
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
            if maya.cmds.about(version=True) >= 2017:
                workspace_name = '{}WorkspaceControl'.format(ui_name)
                workspace_name = workspace_name.replace(' ', '_')
                workspace_name = workspace_name.replace('-', '_')
                if maya.cmds.workspaceControl(workspace_name, exists=True):
                    maya.cmds.deleteUI(workspace_name)
            else:
                dock_name = '{}DockControl'.format(ui_name)
                dock_name = dock_name.replace(' ', '_')
                dock_name = dock_name.replace('-', '_')
                # dock_name = 'MayaWindow|%s' % dock_name       # TODO: Check if we need this
                if maya.cmds.dockControl(dock_name, exists=True):
                    maya.cmds.deleteUI(dock_name, control=True)

            self.setAttribute(Qt.WA_DeleteOnClose, True)

        super(MayaDockedWindow, self).ui()


tpDccLib.Dcc = MayaDcc