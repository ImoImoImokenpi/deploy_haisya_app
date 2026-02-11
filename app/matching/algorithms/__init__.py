# app/matching/algorithms/__init__.py
from .score_matching import score_matching
from .random_maching import random_matching
from .section_priority import section_priority_matching

ALGORITHMS = {
    "score": score_matching,
    "random": random_matching,
    "section": section_priority_matching,
}

def get_algorithm(name: str):
    return ALGORITHMS.get(name, score_matching)
