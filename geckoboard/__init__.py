from __future__ import unicode_literals

from .session import Session
from .dataset import Dataset, Field
from .__about__ import (
    __package_name__, __title__, __author__, __author_email__,
    __license__, __copyright__, __version__, __revision__,
    __url__,
)


__all__ = (
    Session,
    Dataset,
    Field,
    # Metadata attributes
    '__package_name__',
    '__title__',
    '__author__',
    '__author_email__',
    '__license__',
    '__copyright__',
    '__version__',
    '__revision__',
    '__url__',
)
