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

    def test_non_executable_high_score_cannot_win(self):
        blocked = ActionCandidate("blocked", "valuable but provider boundary unavailable",
            {"operator_impact": 10, "external_leverage": 10, "result_power": 10, "readiness": 2}, True, False, (), False, "provider write path unavailable")
        executable = ActionCandidate("executable", "lower raw score but executable now",
            {"operator_impact": 7, "result_power": 7, "readiness": 10}, True)
        self.assertEqual(self.engine.evaluate(self.snap(actions=(blocked, executable))).selected_action, "executable")

    def test_only_non_executable_actions_yield_boundary_not_fake_work(self):
        blocked = ActionCandidate("blocked", "provider boundary unavailable",
            {"operator_impact": 10, "result_power": 10}, True, False, (), False, "provider write path unavailable")
        self.assertIsNone(self.engine.evaluate(self.snap(actions=(blocked,))).selected_action)

if __name__ == "__main__":
    unittest.main()

class AmbitionTests(unittest.TestCase):
    def setUp(self):
        self.good_system = q(purpose_fit=9.5, capability=9.5, reliability=9.5)
        self.weak_results = q(mission_progress=5, leverage=5, verified_outcome=5)
        self.completion = q(completeness=4, polish=4, reuse=4)

    def snap(self, actions, state="mission:v1"):
        return MissionSnapshot(
            self.good_system,
            self.weak_results,
            self.completion,
            False,
            tuple(actions),
            (),
            None,
            state,
        )

    def test_ambition_pressure_accumulates_when_mission_state_does_not_change(self):
        engine = ImpactEngine()
        direct = ActionCandidate("direct", "execute real mission work", {"operator_impact": 9, "result_power": 9}, True)
        first = engine.evaluate(self.snap((direct,)))
        second = engine.evaluate(self.snap((direct,)))
        third = engine.evaluate(self.snap((direct,)))
        self.assertEqual(first.no_progress_cycles, 0)
        self.assertEqual(second.no_progress_cycles, 1)
        self.assertEqual(third.no_progress_cycles, 2)
        self.assertGreater(third.ambition_pressure, second.ambition_pressure)

    def test_repeated_non_progress_forces_material_route_change_when_available(self):
        engine = ImpactEngine()
        repeat = ActionCandidate("repeat", "repeat same route", {"operator_impact": 10, "result_power": 10}, True)
        alternate = ActionCandidate("alternate", "take materially different executable route", {"operator_impact": 7, "result_power": 7}, True)
        first = engine.evaluate(self.snap((repeat, alternate)))
        second = engine.evaluate(self.snap((repeat, alternate)))
        self.assertEqual(first.selected_action, "repeat")
        self.assertTrue(second.route_change_required)
        self.assertEqual(second.selected_action, "alternate")
        self.assertGreater(second.ambition_pressure, 0)

    def test_real_state_change_resets_ambition_pressure(self):
        engine = ImpactEngine()
        action = ActionCandidate("execute", "execute", {"operator_impact": 9, "result_power": 9}, True)
        engine.evaluate(self.snap((action,), "mission:v1"))
        engine.evaluate(self.snap((action,), "mission:v1"))
        pressured = engine.evaluate(self.snap((action,), "mission:v1"))
        self.assertGreater(pressured.ambition_pressure, 0)
        advanced = engine.evaluate(self.snap((action,), "mission:v2"))
        self.assertEqual(advanced.no_progress_cycles, 0)
        self.assertEqual(advanced.ambition_pressure, 0)

    def test_ambition_never_makes_fake_work_selectable(self):
        engine = ImpactEngine()
        support = ActionCandidate("status", "write another status report", {"operator_impact": 10}, False, False, ("status_only",))
        for _ in range(5):
            decision = engine.evaluate(self.snap((support,)))
        self.assertIsNone(decision.selected_action)

    def test_ambition_state_persists_across_engine_restart(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as td:
            state = Path(td) / "ambition.json"
            action = ActionCandidate("execute", "execute", {"operator_impact": 9, "result_power": 9}, True)
            first = ImpactEngine(ambition_state_path=state)
            first.evaluate(self.snap((action,), "mission:persist"))
            first.evaluate(self.snap((action,), "mission:persist"))
            restored = ImpactEngine(ambition_state_path=state)
            decision = restored.evaluate(self.snap((action,), "mission:persist"))
            self.assertGreaterEqual(decision.no_progress_cycles, 2)
            self.assertTrue(state.is_file())
