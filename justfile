# just add numpy
add +packages:
    uv add {{packages}} && uv pip install -e . --config-settings editable_mode=compat

# just rm numpy
rm +packages:
    uv remove {{packages}} && uv pip install -e . --config-settings editable_mode=compat

# just sync
sync:
    uv sync && uv pip install -e . --config-settings editable_mode=compat

# just run
run *args:
    uv run src/g_game {{args}}
