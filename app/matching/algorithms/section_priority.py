def section_priority_matching(drivers, passengers):

    driver_remaining = {d.id: d.capacity for d in drivers}
    matches = {d.id: [] for d in drivers}

    assigned = set()

    # ① まず同セクションを割り当て
    for d in drivers:
        for p in passengers:
            if p.id in assigned:
                continue
            if driver_remaining[d.id] == 0:
                break

            if d.section == p.section:
                matches[d.id].append(p.id)
                driver_remaining[d.id] -= 1
                assigned.add(p.id)

    # ② 残りを通常割当
    for d in drivers:
        for p in passengers:
            if p.id in assigned:
                continue
            if driver_remaining[d.id] == 0:
                break

            matches[d.id].append(p.id)
            driver_remaining[d.id] -= 1
            assigned.add(p.id)

    return matches, assigned
