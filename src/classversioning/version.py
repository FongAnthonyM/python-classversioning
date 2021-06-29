#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" version.py

Provides version tools to create versioning. The Version class is a dataclass like class which uses the three number
version convention. Subsequent classes use the Version class to do useful version comparisons. The versioning framework
can be used for normal objects, but it is primarily designed around versioning classes. This is useful for creating
classes that have to interface with datastructures that change frequently and support for previous version are needed.
For example, a file type may change how data is stored within it but you might have files of the new and previous
version. In this case an appropriate class which addresses each version can be chosen based on the version of the file.

"""
__author__ = "Anthony Fong"
__copyright__ = "Copyright 2021, Anthony Fong"
__credits__ = ["Anthony Fong"]
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "Anthony Fong"
__email__ = ""
__status__ = "Prototype"

# Default Libraries #
from abc import abstractmethod

# Downloaded Libraries #
from baseobjects import BaseObject

# Local Libraries #


# Definitions #
# Classes #
class VersionType(BaseObject):
    """A dataclass like object that contains a str name and associated class for a version.

    Attributes:
        name (str, optional): The string name of this object.
        class_ (:class:, optional): The class of the version.

    Args:
        name (str): The string name of this object.
        class_ (:class:): The class of the version.
    """
    __slots__ = ["name", "class_"]

    # Construction/Destruction
    def __init__(self, name=None, class_=None, init=True):
        self.name = None
        self.class_ = None

        if init:
            self.construct(name=name, class_=class_)

    # Type Conversion
    def __str__(self):
        """Returns the str representation of the version.

        Returns:
            str: A str with the version numbers in order.
        """
        return self.name

    # Comparison
    def __eq__(self, other):
        """Expands on equals comparison to include comparing the version number.

        Args:
            other (:obj:): The object to compare to this object.

        Returns:
            bool: True if the other object or version number is equivalent.
        """
        if isinstance(other, type(self)):
            return other.name == self.name
        if isinstance(other, str):
            return other == self.name
        else:
            return super().__eq__(other)

    def __ne__(self, other):
        """Expands on not equals comparison to include comparing the version number.

        Args:
            other (:obj:): The object to compare to this object.

        Returns:
            bool: True if the other object or version number is not equivalent.
        """
        if isinstance(other, type(self)):
            return other.name != self.name
        if isinstance(other, str):
            return other != self.name
        else:
            return super().__ne__(other)

    # Methods
    def construct(self, name=None, class_=None):
        """Constructs the version type object based on inputs.

        Args:
            name (str, optional): The string name of this object.
            class_ (:class:, optional): The class of the version.
        """
        self.name = name
        self.class_ = class_


class Version(BaseObject):
    """An abstract class for creating versions which dataclass like classes that stores and handles a versioning.

    Class Attributes:
        version_name (str): The name of the version.

    Attributes:
        version_type (:obj:`VersionType`): The type of version object this object is.

    Args:
        obj (:obj:, optional): An object to derive a version from.
        ver_name (str, optional): The name of the version type being used.
        init (bool, optional): Determines if the object should be initialized.
    """
    default_version_name = "default"

    # Class Methods
    @classmethod
    def cast(cls, other, pass_=False):
        """A cast method that optionally returns the original object rather than raise an error

        Args:
            other (:obj:): An object to convert to this type.
            pass_ (bool, optional): True to return original object rather than raise an error.

        Returns:
            obj: The converted object of this type or the original object.
        """
        try:
            other = cls(other)
        except TypeError as e:
            if not pass_:
                raise e

        return other

    @classmethod
    def create_version_type(cls, name=None):
        """Create the version type of this version class.

        Args:
            name (str): The which this type will referred to.

        Returns:
            :obj:`VersionType`: The version type of this version.
        """
        if name is None:
            name = cls.default_version_name
        return VersionType(name, cls)

    # Construction/Destruction
    @abstractmethod
    def __init__(self, obj=None, ver_name=None, init=True, **kwargs):
        self.version_type = None

        if init:
            self.construct(obj=obj, ver_name=ver_name, **kwargs)

    # Type Conversion
    @abstractmethod
    def __str__(self):
        """Returns the str representation of the version.

        Returns:
            str: A str with the version numbers in order.
        """
        return super().__str__()

    # Comparison
    @abstractmethod
    def __eq__(self, other):
        """Expands on equals comparison to include comparing the version number.

        Args:
            other (:obj:): The object to compare to this object.

        Returns:
            bool: True if the other object or version number is equivalent.
        """
        return super().__ne__(other)

    @abstractmethod
    def __ne__(self, other):
        """Expands on not equals comparison to include comparing the version number.

        Args:
            other (:obj:): The object to compare to this object.

        Returns:
            bool: True if the other object or version number is not equivalent.
        """
        return super().__ne__(other)

    @abstractmethod
    def __lt__(self, other):
        """Creates the less than comparison for these objects which includes str, list, and tuple.

        Args:
            other (:obj:): The object to compare to this object.

        Returns:
            bool: True if this object is less than to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        other = self.cast(other, pass_=True)

        if isinstance(other, Version):
            return self.tuple() < other.tuple()
        else:
            raise TypeError(f"'>' not supported between instances of '{str(self)}' and '{str(other)}'")

    @abstractmethod
    def __gt__(self, other):
        """Creates the greater than comparison for these objects which includes str, list, and tuple.

        Args:
            other (:obj:): The object to compare to this object.

        Returns:
            bool: True if this object is greater than to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        other = self.cast(other, pass_=True)

        if isinstance(other, Version):
            return self.tuple() > other.tuple()
        else:
            raise TypeError(f"'>' not supported between instances of '{str(self)}' and '{str(other)}'")

    @abstractmethod
    def __le__(self, other):
        """Creates the less than or equal to comparison for these objects which includes str, list, and tuple.

        Args:
            other (:obj:): The object to compare to this object.

        Returns:
            bool: True if this object is less than or equal to to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        other = self.cast(other, pass_=True)

        if isinstance(other, Version):
            return self.tuple() <= other.tuple()
        else:
            raise TypeError(f"'<=' not supported between instances of '{str(self)}' and '{str(other)}'")

    @abstractmethod
    def __ge__(self, other):
        """Creates the greater than or equal to comparison for these objects which includes str, list, and tuple.

        Args:
            other (:obj:): The object to compare to this object.

        Returns:
            bool: True if this object is greater than or equal to to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        other = self.cast(other, pass_=True)

        if isinstance(other, Version):
            return self.tuple() >= other.tuple()
        else:
            raise TypeError(f"'>=' not supported between instances of '{str(self)}' and '{str(other)}'")

    # Methods
    @abstractmethod
    def construct(self, obj=None, ver_name=None, **kwargs):
        """Constructs the version object based on inputs

        Args:
            obj (:obj:, optional): An object to derive a version from.
            ver_name (str, optional): The name of the version type being used.
        """
        self.version_type = self.create_version_type(ver_name)

    @abstractmethod
    def list(self):
        """Returns the list representation of the version.

        Returns:
            :obj:`list` of :obj:`str`: The list representation of the version.
        """
        pass

    @abstractmethod
    def tuple(self):
        """Returns the tuple representation of the version.

        Returns:
            :obj:`tuple` of :obj:`str`: The tuple representation of the version.
        """
        pass

    def str(self):
        """Returns the str representation of the version.

        Returns:
            str: A str with the version numbers in order.
        """
        return str(self)

    def set_version_type(self, name):

        self.version_type = VersionType(name, type(self))
