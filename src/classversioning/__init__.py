#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" __init__.py
Description:
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

# Downloaded Libraries #

# Local Libraries #
from .version import Version, VersionType
from .versions import *
from .versionregistry import VersionRegistry
from .versionedclass import VersionedMeta, VersionedClass

