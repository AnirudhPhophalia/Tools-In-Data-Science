import json

with open("base.json", "r", encoding="utf-8") as f:
    base = json.load(f)

with open("branch_a.json", "r", encoding="utf-8") as f:
    branch_a = json.load(f)

with open("branch_b.json", "r", encoding="utf-8") as f:
    branch_b = json.load(f)

conflicts = 0

for key in base:
    base_value = base[key]["value"]
    a_value = branch_a[key]["value"]
    b_value = branch_b[key]["value"]

    changed_in_a = a_value != base_value
    changed_in_b = b_value != base_value

    if changed_in_a and changed_in_b and a_value != b_value:
        conflicts += 1

print(conflicts)