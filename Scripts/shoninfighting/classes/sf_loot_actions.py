"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from interactions import ParticipantType
from interactions.utils.loot import LootActions, LootActionVariant
from interactions.utils.loot_basic_op import BaseTargetedLootOperation
from shoninfighting.attributes.utils.sf_attribute_utils import SFAttributeUtils
from shoninfighting.mod_identity import ModIdentity
from sims4.tuning.tunable import TunableList, TunableEnumEntry

log = BBLogRegistry().register_log(ModIdentity(), 'sf_loot_actions')
# log.enable()


class SFEvaluateAttributesLootOp(BaseTargetedLootOperation):
    FACTORY_TUNABLES = {
        'subject': TunableEnumEntry(
            description='\n            The Sim doing the evaluation.\n            ',
            tunable_type=ParticipantType,
            default=ParticipantType.Actor
        ),
        'target': TunableEnumEntry(
            description='\n            The Sim being evaluated.\n            ',
            tunable_type=ParticipantType,
            default=ParticipantType.TargetSim
        ),
    }

    __slots__ = {'subject', 'target'}

    def __init__(self, *_, subject=ParticipantType.Actor, target=ParticipantType.TargetSim, **__) -> None:
        super().__init__(*_, **__)
        self.subject = subject
        self.target = target

    def _apply_to_subject_and_target(self, subject, target, resolver) -> None:
        if self._tests:
            test_result = self._tests.run_tests(resolver)
            if not test_result:
                return test_result
        sim_info = BBSimUtils.to_sim_info(subject)
        target_sim = resolver.get_participant(self.target)
        target_sim_info = BBSimUtils.to_sim_info(target_sim)
        SFAttributeUtils.show_attributes_notification(target_sim_info)


class SFLootActionVariant(LootActionVariant):
    def __init__(self, *args, statistic_pack_safe=False, **kwargs) -> None:
        super().__init__(
            *args,
            statistic_pack_safe=statistic_pack_safe,
            evaluate_attributes=SFEvaluateAttributesLootOp.TunableFactory(
                target_participant_type_options={
                    'description': '\n                    The participant of the interaction\n                    ',
                    'default_participant': ParticipantType.Object
                }
            ),
            **kwargs
        )


class SFLootActions(LootActions):
    INSTANCE_TUNABLES = {
        'loot_actions': TunableList(
            description='\n           List of loots operations that will be awarded.\n           ',
            tunable=SFLootActionVariant(statistic_pack_safe=True)
        ),
    }