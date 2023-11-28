"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Tuple

from bluuberrylibrary.interactions.registration.bb_interaction_registry import BBInteractionRegistry
from bluuberrylibrary.interactions.registration.handlers.bb_sim_interaction_handler import BBSimInteractionHandler
from shonenfighting.attributes.enums.interaction_ids import SFInteractionId


@BBInteractionRegistry.register()
class _BBLSimInteractionRegistration(BBSimInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            SFInteractionId.EVALUATE_ATTRIBUTES,
        )