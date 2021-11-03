import requests

from mobio.libs.profiling_mf import CommonMerchant
from mobio.libs.profiling_mf.merchant_config import MerchantConfig
from mobio.libs.profiling_mf.merge_v2_helpers.dynamic_import_module import (
    dynamic_import_merge_v2,
)
from mobio.libs.profiling_mf.profiling_common import (
    UnificationStructure,
    UnificationDefaultDataSource
)


class ProfilingHelper:
    def __get_unification_rules__(self, merchant_id):
        profiling_host = MerchantConfig().get_merchant_config(merchant_id=merchant_id)[
            MerchantConfig.PROFILING_HOST
        ]
        headers = {
            "Authorization": CommonMerchant.MOBIO_TOKEN,
            "X-Merchant-ID": merchant_id,
        }
        response = requests.get(
            profiling_host + "/profiling/v3.0/unification/list", headers=headers
        )
        response.raise_for_status()
        unification_rules = response.json().get("unification_rules") or []
        return unification_rules

    def check_data_source_valid(self, merchant_id, data):
        all_rules = self.__get_unification_rules__(merchant_id=merchant_id)
        source = data.get("source")
        or_operator = []
        rule = next(
            (
                x
                for x in all_rules
                if x.get(UnificationStructure.SOURCE).lower() == str(source).lower()
            ),
            None,
        )
        if not rule:
            rule = next(
                (
                    x
                    for x in all_rules
                    if x.get(UnificationStructure.SOURCE)
                    == UnificationDefaultDataSource.OTHER
                ),
                None,
            )
        lst_field_required = []
        for rule_operator in rule.get(UnificationStructure.OPERATORS):
            match_all_rule = []
            fields = []
            for rule_by_field in rule_operator.get(UnificationStructure.FIELDS):
                for k, v in rule_by_field.items():
                    fields.append(k)
                    instance = dynamic_import_merge_v2(k)
                    if not instance:
                        print(
                            "KEY: {} is not has rule in dynamic_import_merge_v2".format(
                                k
                            )
                        )
                        continue
                    instance_value = instance.get_normalized_value(data=data)

                    if instance_value:
                        match_all_rule.append(True)
                    else:
                        match_all_rule.append(False)
                        # break
                lst_field_required.append(fields)
                if all(match_all_rule):
                    return True, []
        if not or_operator:
            return False, lst_field_required


if __name__ == "__main__":
    r = ProfilingHelper().check_data_source_valid(merchant_id="0ff54084-a607-46f7-aeb4-8854ab8e6292", data={
        "source": "EzTicket",
        "primary_phone1": "p1",
        "name": "n1"
    })
    print(r)
