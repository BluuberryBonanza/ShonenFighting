"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from bluuberrylibrary.utils.instances.bb_statistic_utils import BBStatisticUtils
from event_testing.results import TestResult
from event_testing.statistic_tests import RelativeStatTest
from shoninfighting.attributes.enums.attribute_types import SFAttributeType
from shoninfighting.mod_identity import ModIdentity
from sims4.math import Threshold, Operator

log = BBLogRegistry().register_log(ModIdentity(), 'sf_fitness_override')
# log.enable()


@BBInjectionUtils.inject(ModIdentity(), RelativeStatTest, '__call__')
def _sf_override_fitness_check(original, self, source_objects=None, target_objects=None):
    if self.stat is None:
        return original(self, source_objects=source_objects, target_objects=target_objects)

    stat_id = getattr(self.stat, 'guid64')
    if stat_id != 16659:  # skill_Fitness
        return original(self, source_objects=source_objects, target_objects=target_objects)

    strength_stat = BBStatisticUtils.load_statistic_by_guid(SFAttributeType.to_statistic_guid(SFAttributeType.STRENGTH))
    if strength_stat is None:
        return original(self, source_objects=source_objects, target_objects=target_objects)
    speed_stat = BBStatisticUtils.load_statistic_by_guid(SFAttributeType.to_statistic_guid(SFAttributeType.SPEED))
    if speed_stat is None:
        return original(self, source_objects=source_objects, target_objects=target_objects)
    statistics_to_test = (
        strength_stat,
        speed_stat,
    )
    for source_obj in source_objects:
        if source_obj is None:
            # log.debug('Trying to call RelativeStatThresholdTest on {source_obj} which is None for {}')
            return TestResult(False, 'Target({}) does not exist', self.source)
        # Source average
        source_curr_value = 0
        for target_stat in statistics_to_test:
            source_curr_value += self.score_to_use.get_value(source_obj, target_stat)
        source_curr_value /= len(statistics_to_test)
        source_curr_value += self.difference
        for target_obj in target_objects:
            if target_obj is None:
                # log.debug('Trying to call RelativeStatThresholdTest on {target_obj} which is None for {}')
                return TestResult(False, 'Target({}) does not exist', self.target)
            # Target average
            target_curr_value = 0
            for target_stat in statistics_to_test:
                target_curr_value += self.score_to_use.get_value(target_obj, target_stat)
            target_curr_value /= len(statistics_to_test)
            threshold = Threshold(target_curr_value, self.comparison)
            operator_symbol = Operator.from_function(self.comparison).symbol
            if not threshold.compare(source_curr_value):
                # log.debug('Sim failed {} failed relative stat check: {} {} {} (current value: {})'.format(source_obj, target_obj, operator_symbol, target_curr_value, source_curr_value), sim=source_obj, target_obj=target_obj, target_stat=target_stat, compare=self.comparison)
                return TestResult(False, '{} failed relative stat check: {} {} {} (current value: {})', source_obj, target_obj, operator_symbol, target_curr_value, source_curr_value)
            # log.debug('Sim passed {} success relative stat check: {} {} {} (current value: {})'.format(source_obj, target_obj, operator_symbol, target_curr_value, source_curr_value), sim=source_obj, target_obj=target_obj, target_stat=target_stat, compare=self.comparison)
    return TestResult.TRUE
