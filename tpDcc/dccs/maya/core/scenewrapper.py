#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Maya scene wrapper class implementation
"""

from __future__ import print_function, division, absolute_import

import tpDcc as tp
from tpDcc.abstract import scenewrapper
import tpDcc.dccs.maya as maya
from tpDcc.dccs.maya.core import node as node_utils


class MayaSceneWrapper(scenewrapper.AbstractSceneWrapper, object):
    def __init__(self, scene, native_dcc_object):

        # NOTE: Instead of working with Maya MObjects (which in some scenarios such as long time, opening new
        # file ..., are automatically invalidated and Maya will crash if we try to use them because we are accessing
        # an invalid memory, we use MObjectHandles which does not suffer this problem.
        self._native_handle = None

        super(MayaSceneWrapper, self).__init__(scene=scene, native_dcc_object=native_dcc_object)

    # ==============================================================================================
    # PROPERTIES
    # ==============================================================================================

    @property
    def _dcc_native_object(self):
        return self._native_handle.object()

    @_dcc_native_object.setter
    def _dcc_native_object(self, dcc_object):
        if dcc_object is None:
            dcc_object = maya.OpenMaya.MObject()
        self._native_handle = maya.OpenMaya.MObjectHandle(dcc_object)

    # ==============================================================================================
    # OVERRIDES
    # ==============================================================================================

    def name(self):
        """
        Returns the name of the DCC object in current DCC scene
        :return: str, current name of the DCC object
        """

        return node_utils.get_name(mobj=self._dcc_native_object, fullname=False)

    def display_name(self):
        """
        Returns the name of DCC object without special characters used by DCC.
        :return: str
        """

        return self.name().split(':')[-1]

    def set_display_name(self, new_name):
        """
        Sets the display name of the DCC object
        :param new_name: str, new display name
        """

        return maya.cmds.rename(self.path(), ':'.join([self.namespace(), new_name]))

    def path(self):
        """
        Returns the full path of the DCC object in current DCC scene
        :return: str, current full path of the DCC object
        """

        return node_utils.get_name(mobj=self._dcc_native_object, fullname=True)

    def namespace(self):
        """
        Returns DCC object namespace
        :return: str
        """

        node_name = node_utils.get_name(self._dcc_native_object, fullname=False)
        split = node_name.split(':')[0]
        if len(split) > 1:
            return ':'.join(split[:-1])

        return ''

    def set_namespace(self, namespace):
        """
        Sets DCC object namespace
        :param namespace: str, new namespace for the DCC object
        """

        node_name = node_utils.get_name(self._dcc_native_object, fullname=False)
        display_name = node_name.split(':')[-1]
        if not namespace:
            maya.cmds.rename(self.path(), self.display_name())
        else:
            if not maya.cmds.namespace(exists=namespace):
                maya.cmds.namespace(add=namespace)
            maya.cmds.rename(self.path(), ':'.join([namespace, display_name]))

        return True

    def unique_id(self):
        """
        Returns the unique identifier of the wrapped native DCC object in current DCC scene
        :return: int or str
        """

        property_value = self._dcc_native_property('uuid')
        if property_value is None:
            return self._native_handle.hashCode()

    def has_attribute(self, attribute_name):
        """
        Returns whether or not wrapped native DCC object has an attribute with the given name
        :param attribute_name: str, name of the attribute we are looking for
        :return: bool, True if the attribute exists in the wrapped native DCC object; False otherwise.
        """

        raise NotImplementedError('Maya Scene Wrapper has_attribute function not implemented!')

    def attribute_names(self, keyable=False, short_names=False, unlocked=True):
        """
        Returns a list of the attributes names linked to wrapped native DCC object
        :param keyable: bool, Whether or not list keyable attributes (animatable properties)
        :param short_names: bool, Whether or not to list attributes with their short name
        :param unlocked: bool, Whether or not list unlocked properties
        :return: list
        """

        raise NotImplementedError('Maya Scene Wrapper attribute_names function not implemented!')

    def _dcc_native_copy(self):
        """
        Internal function that returns a copy/duplicate of the wrapped DCC object
        :return: variant
        """

        raise NotImplementedError('Maya Scene Wrapper _dcc_native_copy function not implemented!')

    def _dcc_native_attribute(self, attribute_name, default=None):
        """
        Internal function that returns the value of the attribute of the wrapped DCC object
        :param attribute_name: str, name of the attribute we want retrieve value of
        :param default: variant, fallback default value if attribute does not exists in wrapped DCC object
        :return:
        """

        node_name = node_utils.get_name(self._dcc_native_object, fullname=True)
        try:
            return tp.Dcc.get_attribute_value(node_name, attribute_name)
        except Exception:
            return default

    def _set_dcc_native_attribute(self, attribute_name, value):
        """
        Sets the value of the property defined by the given attribute name
        :param attribute_name: str, name of the attribute we want to set the value of
        :param value: variant, new value of the attribute
        :return: bool, True if the operation was successful; False otherwise.
        """

        node_name = node_utils.get_name(self._dcc_native_object, fullname=True)

        return tp.Dcc.set_attribute_value(node_name, attribute_name, value)
