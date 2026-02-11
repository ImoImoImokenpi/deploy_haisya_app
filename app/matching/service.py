from .algorithms import get_algorithm

def run_matching(drivers, passengers, mode="score"):
    """
    mode:
        score   : 属性スコア最大化
        random  : ランダム
        section : セクション優先
    """

    algorithm = get_algorithm(mode)

    matches, assigned = algorithm(drivers, passengers)

    return matches, assigned
