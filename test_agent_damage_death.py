# tests/test_agent_death.py
import pytest
from agents import Archer

def test_agent_dies_and_triggers_callback():
    removed_agents = []

    def fake_remove(agent):
        removed_agents.append(agent)

    # Create archer with 1 HP
    archer = Archer(player_id=1, position=(0, 0), hp=1)
    archer.death_callback = fake_remove

    # Take damage that should kill it
    archer.take_damage(1)

    # Assertions
    assert archer.hp <= 0, "Agent should have zero or less HP"
    assert removed_agents == [archer], "Death callback should be triggered exactly once"
