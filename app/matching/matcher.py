# from ..models import CheckedDriver, CheckedPassenger

# def calc_score(d, p):
#     score = 0
#     if d.section == p.section: score += 5
#     if d.jenre == p.jenre: score += 4
#     if d.old == p.old: score += 3
#     if d.rehersal == p.rehersal: score += 6
#     return score

# def run_matching(drivers, passengers):

#     driver_remaining = {d.id: d.capacity for d in drivers}
#     matches = {d.id: [] for d in drivers}

#     pair_scores = []
#     for d in drivers:
#         for p in passengers:
#             pair_scores.append((calc_score(d,p), d.id, p.id))

#     pair_scores.sort(reverse=True)

#     assigned = set()

#     for score, d_id, p_id in pair_scores:
#         if driver_remaining[d_id] == 0: continue
#         if p_id in assigned: continue

#         matches[d_id].append(p_id)
#         driver_remaining[d_id] -= 1
#         assigned.add(p_id)

#     return matches, assigned
