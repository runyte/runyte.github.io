"""A tiny release checklist."""


def pending_tasks(tasks):
    pending = [task for task in tasks if not task["done"]]
    return sorted(pending, key=lambda task: task["priority"])


def summarize(tasks):
    pending = pending_tasks(tasks)
    return f"{len(pending)} tasks left before release"


tasks = [
    {"title": "Write release notes", "done": False, "priority": 1},
    {"title": "Run the tests", "done": False, "priority": 2},
    {"title": "Publish the package", "done": True, "priority": 3},
]

print(summarize(tasks))
