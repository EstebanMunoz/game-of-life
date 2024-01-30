from src.game_of_life.rules import game_rules


def test_rules() -> None:
    # A non populated cell becomes alive only if it is surrounded by 3 live cells
    assert game_rules(0, 0) == 0
    assert game_rules(0, 1) == 0
    assert game_rules(0, 2) == 0
    assert game_rules(0, 3) == 1
    assert game_rules(0, 4) == 0
    assert game_rules(0, 5) == 0
    assert game_rules(0, 6) == 0
    assert game_rules(0, 7) == 0
    assert game_rules(0, 8) == 0

    # A populated cell keeps alive only if it is surrounded by 2 or 3 live cells
    assert game_rules(1, 0) == 0
    assert game_rules(1, 1) == 0
    assert game_rules(1, 2) == 1
    assert game_rules(1, 3) == 1
    assert game_rules(1, 4) == 0
    assert game_rules(1, 5) == 0
    assert game_rules(1, 6) == 0
    assert game_rules(1, 7) == 0
    assert game_rules(1, 8) == 0
