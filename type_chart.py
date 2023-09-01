"""Gen 3 type chart."""

import json
import numpy as np

with open('type-chart.json') as f:
  data = json.load(f)

Type = str
TYPES = tuple(data.keys())

def get_multiplier(attacker_type: str, defender_type: str):
  """Returns the multiplier for an attack of attacker_type against defender_type."""
  return data[attacker_type][defender_type]

TypeCombination = tuple[Type, ...]

def get_multiplier_for_combination(
    attacker_type: Type,
    defender_types: TypeCombination):
  return np.prod([
    get_multiplier(attacker_type, defender_type)
    for defender_type in defender_types])

def get_best_multiplier(
    attacker: TypeCombination,
    defender: TypeCombination,
) -> float:
  return max([get_multiplier_for_combination(attacker_type, defender)
              for attacker_type in attacker])

def compare(x, y) -> int:
  if x < y:
    return -1
  if x > y:
    return 1
  assert x == y
  return 0

def matchup(attacker: TypeCombination, defender: TypeCombination) -> int:
  """Returns the matchup between attacker and defender.

  Returns -1 if attacker is weak against defender.
  Returns 1 if attacker is strong against defender.
  Returns 0 if attacker is neutral against defender.
  """
  return compare(get_best_multiplier(attacker, defender),
                 get_best_multiplier(defender, attacker))

def symmetric_matchup_matrix(type_combinations: list[TypeCombination]) -> np.ndarray:
  """Returns the matchup matrix for the given type combinations."""
  n = len(type_combinations)
  matrix = np.zeros((n, n), dtype=int)
  for i, attacker in enumerate(type_combinations):
    for j, defender in enumerate(type_combinations):
      matrix[i, j] = matchup(attacker, defender)
  return matrix


def asymmetric_matchup_matrix(
    attacker_type_combinations: list[TypeCombination],
    defender_type_combinations: list[TypeCombination],
) -> np.ndarray:
  """Returns matrix for damage dealt."""
  n = len(attacker_type_combinations)
  m = len(defender_type_combinations)
  matrix = np.zeros((n, m), dtype=int)
  for i, attacker in enumerate(attacker_type_combinations):
    for j, defender in enumerate(defender_type_combinations):
      matrix[i, j] = get_best_multiplier(attacker, defender)
  return matrix
