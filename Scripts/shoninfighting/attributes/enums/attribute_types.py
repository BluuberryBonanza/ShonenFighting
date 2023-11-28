"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""

from bluuberrylibrary.enums.classes.bb_int import BBInt
from shoninfighting.attributes.enums.statistic_ids import SFStatisticId


class SFAttributeType(BBInt):
    INVALID = ...
    STRENGTH = ...
    SPEED = ...

    @classmethod
    def to_statistic_guid(cls, attribute: 'SFAttributeType') -> int:
        mapping = {
            SFAttributeType.STRENGTH: SFStatisticId.ATTRIBUTE_STRENGTH,
            SFAttributeType.SPEED: SFStatisticId.ATTRIBUTE_SPEED
        }

        return mapping.get(attribute, 0)
