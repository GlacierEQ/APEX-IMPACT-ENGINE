import unittest

from apex_impact import ActionCandidate, ImpactEngine, ImpactSignal, MissionSnapshot, Phase, QualityMetric, QualitySet

def q(**scores):
    return QualitySet(tuple(QualityMetric(k, v, evidence=(f"receipt:{k}",)) for k, v in scores.items()))

class ImpactEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = ImpactEngine()
        self.good_system = q(purpose_fit=9.4, capability=9.3, reliability=9.1, integration=9.2)
        self.good_results = q(mission_progress=9.2, leverage=9.4, verified_outcome=9.1)
        self.good_completion = q(completeness=9.3, polish=9.2, reuse=9.1)

    def snap(self, system=None, results=None, completion=None, achieved=False, actions=(), previous=None, impacts=()):
        return MissionSnapshot(system or self.good_system, results or q(mission_progress=5, leverage=5, verified_outcome=5),
            completion or q(completeness=3, polish=3, reuse=3), achieved, tuple(actions), tuple(impacts), previous)

    def test_build_until_every_required_system_dimension_is_nine_plus(self):
        self.assertEqual(self.engine.evaluate(self.snap(system=q(purpose_fit=9.8, capability=8.9, reliability=9.8))).phase, Phase.BUILD)

    def test_unverified_nine_plus_does_not_pass(self):
        unverified = QualitySet((QualityMetric("purpose_fit", 9.8, evidence=()), QualityMetric("capability", 9.5, evidence=("r",))))
        d = self.engine.evaluate(self.snap(system=unverified))
        self.assertEqual(d.phase, Phase.BUILD)
        self.assertIn("system.purpose_fit:UNVERIFIED", d.deficits)

    def test_use_when_system_is_exceptional_but_results_are_not(self):
        self.assertEqual(self.engine.evaluate(self.snap()).phase, Phase.USE)

    def test_polish_only_after_results_and_objective_are_nine_plus(self):
        self.assertEqual(self.engine.evaluate(self.snap(results=self.good_results, achieved=True)).phase, Phase.POLISH)

    def test_complete_requires_three_independent_nine_plus_gates(self):
        self.assertEqual(self.engine.evaluate(self.snap(results=self.good_results, completion=self.good_completion, achieved=True)).phase, Phase.COMPLETE)

    def test_new_evidence_can_regress_complete_back_to_build(self):
        s = self.snap(system=q(purpose_fit=9.4, capability=8.0, reliability=9.2), results=self.good_results,
            completion=self.good_completion, achieved=True, previous=Phase.COMPLETE,
            impacts=(ImpactSignal("prod-failure", "production failure observed"),))
        d = self.engine.evaluate(s)
        self.assertEqual(d.phase, Phase.BUILD)
        self.assertTrue(d.strategy_adjusted)
        self.assertIn("New evidence invalidated", d.rationale)

    def test_real_mission_action_beats_heartbeat(self):
        heartbeat = ActionCandidate("heartbeat", "run another health check", {"readiness": 10}, False, True, ("heartbeat_only",))
        use = ActionCandidate("use", "use the working system against the actual mission", {"operator_impact": 9.5, "result_power": 9.5}, True)
        self.assertEqual(self.engine.evaluate(self.snap(actions=(heartbeat, use))).selected_action, "use")

    def test_support_without_unblock_or_target_delta_is_not_selectable(self):
        support = ActionCandidate("summary", "make another status report", {"readiness": 10}, False, False, ("support_only",))
        self.assertIsNone(self.engine.evaluate(self.snap(actions=(support,))).selected_action)

    def test_use_phase_rewards_external_result_power(self):
        infra = ActionCandidate("infra", "optional internal hardening", {"capability_gain": 9, "readiness": 9}, True)
        outcome = ActionCandidate("outcome", "drive external mission outcome", {"operator_impact": 9, "external_leverage": 10, "result_power": 10}, True)
        self.assertEqual(self.engine.evaluate(self.snap(actions=(infra, outcome))).selected_action, "outcome")

    def test_material_impact_can_invalidate_prior_best_action(self):
        first = ActionCandidate("first", "previous best action", {"operator_impact": 10, "result_power": 10}, True)
        second = ActionCandidate("second", "new viable action", {"operator_impact": 8, "result_power": 8}, True)
        impact = ImpactSignal("external-response", "counterparty response makes first action obsolete", invalidates_actions=("first",))
        d = self.engine.evaluate(self.snap(actions=(first, second), impacts=(impact,)))
        self.assertEqual(d.selected_action, "second")
        self.assertTrue(d.strategy_adjusted)

    def test_material_impact_can_reprioritize_without_invalidating(self):
        a = ActionCandidate("a", "candidate a", {"operator_impact": 8, "result_power": 8}, True)
        b = ActionCandidate("b", "candidate b", {"operator_impact": 8, "result_power": 8}, True)
        impact = ImpactSignal("deadline", "new deadline sharply raises b", score_adjustments={"b": 30})
        self.assertEqual(self.engine.evaluate(self.snap(actions=(a, b), impacts=(impact,))).selected_action, "b")

if __name__ == "__main__":
    unittest.main()
