from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule


class RiskRule(BaseTenderRiskRule):
    identifier = "sas-2-16"
    name = "Відмова переможця від підписання договору"
    description = (
        "Даний індикатор виявляє ситуації, коли переможець за результатами тендеру/спрощеної закупівлі, в яких не "
        "передбачено забезпечення тендерної пропозиції/про-позиції, у строки, встановлені законодавством, "
        "не укладає договір про закупівлю, внаслідок чого замовник обирає дорожчу тендерну пропозицію."
    )
    legitimateness = "Індикатор вводиться для ідентифікації можливої змови замовника та постачальника."
    development_basis = "Цей індикатор було розроблено, оскільки система не відстежує дії постачальників."
    procurement_methods = ("aboveThresholdEU", "aboveThresholdUA")
    tender_statuses = ("active.qualification", "active.awarded")
    procuring_entity_kinds = (
        "authority",
        "central",
        "general",
        "social",
        "special",
    )

    def process_tender(self, tender):
        if self.tender_matches_requirements(tender, category=False):
            for award in tender["awards"]:
                if award.get("complaints"):
                    return RiskNotFound()
                if award["status"] == "cancelled":
                    return RiskFound()
        return RiskNotFound()
