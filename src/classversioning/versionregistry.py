""" versionregistry.py
VersionRegistry creates registries of the Versions which keep track of several versioning schemas. For example, there
could be two different file types that both use TriNumberVersions, this registry keeps the class versions from these
different files separate from each other.
"""
# Package Header #
from .header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
import bisect
from collections import UserDict
from collections.abc import Iterable
from typing import Any

# Third-Party Packages #

# Local Packages #
from .version import VersionType


# Definitions #
# Classes #
class VersionRegistry(UserDict):
    """A dictionary like class that holds versioned objects.

    The keys distinguish different types of objects from one another, so their version are not mixed together. The items
    are lists containing the versioned objects in order by version.
    """

    # Instance Methods
    def get_version(self, type_: str | VersionType, key: Iterable[int] | str | int, exact: bool = False) -> Any:
        """Gets an object from the registry based on the type and version of object.

        Args:
            type_: The type of versioned object to get.
            key: The key to search for the versioned object with.
            exact: Determines whether the exact version is need or return the closest version.
        Returns
            obj: The versioned object.

        Raises
            ValueError: If there is no closest version.
        """
        if isinstance(type_, VersionType):
            type_ = type_.name

        versions = self.data[type_]["list"]
        if isinstance(key, str) or isinstance(key, list) or isinstance(key, tuple):
            version_class = self.data[type_]["type"].class_
            key = version_class.cast(key)

        if exact:
            index = versions.index(key)
        else:
            index = bisect.bisect(versions, key)

        if index < 0:
            raise ValueError(f"Version needs to be greater than {str(versions[0])}, {str(key)} is not.")
        else:
            return versions[index-1]

    def get_version_type(self, name: str) -> VersionType:
        """Gets the type object being used as a key.

        Args:
            name: The name of the type object.

        Returns:
            The type object requested.
        """
        return self.data[name]["type"]

    def add_item(self, item: Any, type_: str | None = None) -> None:
        """Adds a versioned item into the registry.

        Args
            item: The versioned object to add.
            type_: The type of versioned object to add.
        """
        if isinstance(type_, str):
            name = type_
            type_ = self.data[name]["type"]
        else:
            if type_ is None:
                type_ = item.version_type
            name = type_.name

        if name in self.data:
            bisect.insort(self.data[name]["list"], item)
        else:
            self.data[name] = {"type": type_, "list": [item]}

    def sort(self, type_: str | None = None, **kwargs: Any) -> None:
        """Sorts the registry.

        Args:
            type_: The type of versioned object to add.
            **kwargs: Keyword arguments that are passed to the list sort function.
        """
        if type_ is None:
            for versions in self.data.values():
                versions["list"].sort(**kwargs)
        else:
            if isinstance(type_, VersionType):
                type_ = type_.name
            self.data[type_]["list"].sort(**kwargs)
