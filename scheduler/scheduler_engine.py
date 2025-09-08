import random

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
random.seed(42)


def build_schedule(sections, subjects, faculty, subject_to_fac, weekly_quota, periods_per_day, classrooms):
    schedules = {sec: {d: [None] * periods_per_day for d in DAYS} for sec in sections}

    # Global usage trackers
    classroom_usage = {d: {p: set() for p in range(periods_per_day)} for d in DAYS}
    faculty_usage = {d: {p: set() for p in range(periods_per_day)} for d in DAYS}

    # Round-robin classroom order
    classroom_map = {}
    idx = 0
    for d in DAYS:
        classroom_map[d] = {}
        for p in range(periods_per_day):
            rotated = classrooms[idx % len(classrooms):] + classrooms[:idx % len(classrooms)]
            classroom_map[d][p] = rotated
            idx += 1

    # Expand subject quotas
    events_per_section = {}
    for sec in sections:
        events = []
        for s in subjects:
            for _ in range(weekly_quota[s]["T"]):
                events.append((s, "T", subject_to_fac.get(s)))
            for _ in range(weekly_quota[s]["P"]):
                events.append((s, "P", subject_to_fac.get(s)))
        random.shuffle(events)
        events_per_section[sec] = events

    # Assign events
    for sec in sections:
        events = events_per_section[sec]
        positions = [(d, p) for d in DAYS for p in range(periods_per_day)]
        random.shuffle(positions)

        for ev in events:
            s, typ, teacher = ev
            placed = False
            for (d, p) in positions:
                if schedules[sec][d][p] is not None:
                    continue
                if teacher in faculty_usage[d][p]:
                    continue

                # 🚫 Prevent same faculty teaching consecutive periods in the same section
                if p > 0 and schedules[sec][d][p - 1] is not None:
                    prev_sub, prev_typ, prev_teacher, prev_cr = schedules[sec][d][p - 1]
                    if prev_teacher == teacher:
                        continue

                for cr in classroom_map[d][p]:
                    if cr not in classroom_usage[d][p]:
                        schedules[sec][d][p] = (s, typ, teacher, cr)
                        classroom_usage[d][p].add(cr)
                        faculty_usage[d][p].add(teacher)
                        placed = True
                        break
                if placed:
                    break
            if not placed:
                raise RuntimeError(f"Could not place {ev} for section {sec}")

    return schedules


def format_schedule(schedule, periods_per_day):
    rows = []
    for d in DAYS:
        row = []
        for p in range(periods_per_day):
            cell = schedule[d][p]
            if cell is None:
                row.append("FREE")
            else:
                sub, typ, teacher, cr = cell
                row.append(f"{cr}: {sub} ({teacher}, {typ})")
        rows.append((d, row))
    return rows

