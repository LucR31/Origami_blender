TESTS = []

def test(fn=None, *, group=None):
    """
    Decorator to register a test function.
    Optionally assign a group (e.g. 'constraints', 'energy').
    """

    def wrapper(func):
        TESTS.append({
            "fn": func,
            "name": func.__name__,
            "group": group
        })
        return func

    return wrapper(fn) if fn else wrapper

def ok(msg):
    print("\033[92m✔ " + msg + "\033[0m")

def fail(msg):
    print("\033[91m✘ " + msg + "\033[0m")


def run_tests(filter_group=None):
    passed = 0
    failed = 0

    print("\n=== ORIGAMI TEST RUNNER ===\n")

    for t in TESTS:
        fn = t["fn"]
        name = t["name"]
        group = t["group"]

        if filter_group and group != filter_group:
            continue

        try:
            fn()
            ok(f"{name} PASSED")
            passed += 1

        except Exception as e:
            fail(f"{name} FAILED")
            print(f"   Group: {group}")
            print(f"   Error: {e}")
            failed += 1

    print("\n--- SUMMARY ---")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    return failed == 0