"""Regression cases: evidence-backed outcomes outrank arbitrary quality score gates."""
import unittest

from apex_impact import (
    ActionCandidate, ImpactEngine, ImpactSignal, MissionSnapshot,
    Phase, QualityMetric, QualitySet,
)


def metrics(**values):
    return QualitySet(tuple(QualityMetric(name, score, evidence=(f"receipt:{name}",)) for name, score in values.items()))


class SolutionPrecedenceTests(unittest.TestCase):
    def setUp(self):
        self.engine = ImpactEngine()
        self.system = metrics(capability=8.9, readiness=7.5)
        self.results = metrics(delivery=5.0)
        self.completion = metrics(archive=6.0)
        self.action = ActionCandidate("execute", "advance mission", {"operator_impact": 8.0}, True)

    def snapshot(self, *, system=None, results=None, completion=None, achieved=False, previous=None, impacts=()):
        return MissionSnapshot(
            system_quality=system if system is not None else self.system,
            result_quality=results if results is not None else self.results,
            completion_quality=completion if completion is not None else self.completion,
            objective_achieved=achieved,
            actions=(self.action,),
            previous_phase=previous,
            impacts=impacts,
        )

    def test_verified_system_can_be_used_despite_numeric_score_below_nine(self):
        decision = self.engine.evaluate(self.snapshot())
        self.assertEqual(decision.phase, Phase.USE)
        self.assertEqual(decision.selected_action, "execute")

    def test_verified_objective_and_handoff_can_complete_below_nine(self):
        decision = self.engine.evaluate(self.snapshot(achieved=True))
        self.assertEqual(decision.phase, Phase.COMPLETE)
        self.assertEqual(decision.deficits, ())

    def test_failed_unrelated_attempt_does_not_undo_completed_objective(self):
        unrelated = ImpactSignal("transient-provider-failure", "unrelated attempt failed")
        decision = self.engine.evaluate(
            self.snapshot(achieved=True, previous=Phase.COMPLETE, impacts=(unrelated,))
        )
        self.assertEqual(decision.phase, Phase.COMPLETE)
        self.assertNotIn("regress", decision.rationale.lower())

    def test_actual_loss_of_objective_reopens_work_instead_of_stale_complete(self):
        decision = self.engine.evaluate(self.snapshot(achieved=False, previous=Phase.COMPLETE))
        self.assertEqual(decision.phase, Phase.USE)

    def test_missing_result_receipt_does_not_invent_completion(self):
        no_receipt = QualitySet((QualityMetric("delivery", 10.0, evidence=()),))
        decision = self.engine.evaluate(self.snapshot(results=no_receipt, achieved=True))
        self.assertEqual(decision.phase, Phase.USE)
        self.assertIn("result.delivery:UNVERIFIED", decision.deficits)

    def test_missing_handoff_receipt_limits_completion_only(self):
        unverified = QualitySet((QualityMetric("archive", 10.0, evidence=()),))
        decision = self.engine.evaluate(self.snapshot(completion=unverified, achieved=True))
        self.assertEqual(decision.phase, Phase.POLISH)
        self.assertIn("completion.archive:UNVERIFIED", decision.deficits)

    def test_an_unverified_system_does_not_block_independent_executable_action(self):
        unverified = QualitySet((QualityMetric("architecture", 3.0, evidence=()),))
        decision = self.engine.evaluate(self.snapshot(system=unverified))
        self.assertEqual(decision.phase, Phase.USE)
        self.assertEqual(decision.selected_action, "execute")


if __name__ == "__main__":
    unittest.main()
