from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.dialogs.icons.bb_sim_icon_info import BBSimIconInfo
from bluuberrylibrary.dialogs.notifications.bb_notification import BBNotification
from bluuberrylibrary.utils.sims.bb_sim_statistic_utils import BBSimStatisticUtils
from bluuberrylibrary.utils.text.bb_localization_utils import BBLocalizationUtils
from bluuberrylibrary.utils.text.bb_localized_string_data import BBLocalizedStringData
from shoninfighting.attributes.enums.attribute_types import SFAttributeType
from shoninfighting.attributes.enums.string_ids import SFStringId
from shoninfighting.mod_identity import ModIdentity
from sims.sim_info import SimInfo
from sims4.localization import LocalizationHelperTuning


class SFAttributeUtils:
    """Utilities for manipulating the attributes of Sims."""
    @classmethod
    def increase_attribute(cls, sim_info: SimInfo, attribute: SFAttributeType, amount: float) -> BBRunResult:
        statistic_id = SFAttributeType.to_statistic_guid(attribute)
        if not statistic_id:
            return BBRunResult(False, f'No Statistic Available for Attribute {attribute}.')
        statistic_value = BBSimStatisticUtils.get_statistic_value(sim_info, statistic_id)
        if not statistic_value:
            statistic_value = 0

        statistic_value += amount
        return BBSimStatisticUtils.set_statistic_value(sim_info, statistic_id, statistic_value)

    @classmethod
    def show_attributes_notification(cls, sim_info: SimInfo):
        attribute_strings = list()
        strength_statistic_id = SFAttributeType.to_statistic_guid(SFAttributeType.STRENGTH)
        strength_amount = round(BBSimStatisticUtils.get_statistic_value(sim_info, strength_statistic_id), 3)
        attribute_strings.append(BBLocalizationUtils.to_localized_string(SFStringId.STRENGTH_STRING, tokens={str(strength_amount),}))

        speed_statistic_id = SFAttributeType.to_statistic_guid(SFAttributeType.SPEED)
        speed_amount = round(BBSimStatisticUtils.get_statistic_value(sim_info, speed_statistic_id), 3)
        attribute_strings.append(BBLocalizationUtils.to_localized_string(SFStringId.SPEED_STRING, tokens={str(speed_amount),}))

        average_amount = round(cls.calculate_average(sim_info), 3)
        attribute_strings.append(BBLocalizationUtils.to_localized_string(SFStringId.AVERAGE_STRING, tokens={str(average_amount),}))

        bulleted_list = LocalizationHelperTuning.get_bulleted_list((None,), *attribute_strings)

        BBNotification(
            ModIdentity(),
            BBLocalizedStringData(SFStringId.ATTRIBUTES),
            BBLocalizedStringData(bulleted_list)
        ).show(icon=BBSimIconInfo(sim_info))

    @classmethod
    def calculate_average(cls, sim_info: SimInfo) -> float:
        strength_statistic_id = SFAttributeType.to_statistic_guid(SFAttributeType.STRENGTH)
        strength_amount = BBSimStatisticUtils.get_statistic_value(sim_info, strength_statistic_id)
        speed_statistic_id = SFAttributeType.to_statistic_guid(SFAttributeType.SPEED)
        speed_amount = BBSimStatisticUtils.get_statistic_value(sim_info, speed_statistic_id)

        amounts = (
            strength_amount,
            speed_amount
        )

        average_value = 0
        for amount in amounts:
            average_value += amount

        return average_value/len(amounts)
