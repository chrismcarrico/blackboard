def pytest_collection_modifyitems(config, items):
    """Leave out tests marked slow unless the -m expression asks about them."""

    if "slow" in config.option.markexpr:
        return

    slow = [item for item in items if item.get_closest_marker("slow")]
    if slow:
        items[:] = [item for item in items if not item.get_closest_marker("slow")]
        config.hook.pytest_deselected(items=slow)
