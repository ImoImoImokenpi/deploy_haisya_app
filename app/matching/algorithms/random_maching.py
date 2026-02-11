import random

def random_matching(drivers, passengers):

    shuffled_passengers = passengers[:]
    random.shuffle(shuffled_passengers)

    driver_remaining = {d.id: d.capacity for d in drivers}
    matches = {d.id: [] for d in drivers}

    assigned = set()
    driver_list = list(drivers)

    d_index = 0

    for p in shuffled_passengers:
        tried = 0
        while tried < len(driver_list):
            d = driver_list[d_index % len(driver_list)]

            if driver_remaining[d.id] > 0:
                matches[d.id].append(p.id)
                driver_remaining[d.id] -= 1
                assigned.add(p.id)
                break

            d_index += 1
            tried += 1

    return matches, assigned
