"""
traversal.py – public API shim.
Real logic lives in traversal_engine.py and traversal_playback.py.
"""
from traversal_engine import (
    clear_any_active_timer,
    trigger_ring_spark,
    trigger_edge_travel,
    find_edge_id_between,
)

from traversal_playback import (
    start_bfs_mode,
    start_dfs_mode,
    reset_visual_state,
    initialize_search_sequence,
    run_bfs,
    run_dfs,
    run_animation_loop,
    apply_step_state,
    toggle_pause,
    step_backward,
    step_forward,
    restart_traversal,
)
