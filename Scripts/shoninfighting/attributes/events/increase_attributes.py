"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""

from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.events.event_dispatchers.interaction.events.bb_on_interaction_completed_event import \
    BBOnInteractionCompletedEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.instances.bb_interaction_utils import BBInteractionUtils
from shoninfighting.attributes.enums.attribute_types import SFAttributeType
from shoninfighting.attributes.utils.sf_attribute_utils import SFAttributeUtils
from shoninfighting.mod_identity import ModIdentity

log = BBLogRegistry().register_log(ModIdentity(), 'sf_increase_attributes')
# log.enable()


class SFIncreaseAttributesOnInteractionComplete:
    STRENGTH_INTERACTION_IDS = (
        14625,  # WorkoutMachine_Workout
        164317,  # treadmill_Rock_ClimbingWall_Climb
        166297,  # treadmill_Rock_ClimbingWall_Climb_2
        166406,  # treadmill_Rock_ClimbingWall_Climb_3
        166424,  # treadmill_Rock_ClimbingWall_Climb_4
        165301,  # treadmill_Rock_ClimbingWall_Climb_Challenge_1
        165954,  # treadmill_Rock_ClimbingWall_Climb_Challenge_2
        166973,  # treadmill_Rock_ClimbingWall_Climb_Challenge_3
        166975,  # treadmill_Rock_ClimbingWall_Climb_Challenge_4
        166976,  # treadmill_Rock_ClimbingWall_Climb_Challenge_5
    )

    SPEED_INTERACTION_IDS = (
        14484,  # treadmill_Workout
        98221,  # treadmill_Workout_PushTheLimits
    )


@BBEventHandlerRegistry.register(ModIdentity(), BBOnInteractionCompletedEvent)
def _bbl_handle_on_interaction_completed(event: BBOnInteractionCompletedEvent) -> BBRunResult:
    if event.was_user_cancelled:
        return BBRunResult.TRUE
    if not event.finished_naturally:
        return BBRunResult.TRUE
    interaction_id = BBInteractionUtils.to_interaction_guid(event.interaction)
    if interaction_id in SFIncreaseAttributesOnInteractionComplete.STRENGTH_INTERACTION_IDS:
        result = SFAttributeUtils.increase_attribute(event.sim_info, SFAttributeType.STRENGTH, 0.01)
        log.debug('Finished increasing strength attribute', interactions=event.interaction, result=result, sim=event.sim_info)
    if interaction_id in SFIncreaseAttributesOnInteractionComplete.SPEED_INTERACTION_IDS:
        result = SFAttributeUtils.increase_attribute(event.sim_info, SFAttributeType.SPEED, 0.01)
        log.debug('Finished increasing speed attribute', interactions=event.interaction, result=result, sim=event.sim_info)
    return BBRunResult.TRUE
