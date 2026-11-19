from core import plan_clips, shuffle_clips, Clip


def test_full_clips_only():
    assert plan_clips(44, 5) == [(0, 5), (5, 5), (10, 5), (15, 5), (20, 5), (25, 5), (30, 5), (35, 5)]


def test_no_partial_clip():
    assert plan_clips(4.99, 5) == []


def test_shuffle_keeps_sources_separate_when_possible():
    clips = [Clip("a", "a1.mp4"), Clip("a", "a2.mp4"), Clip("b", "b1.mp4")]
    result = shuffle_clips(clips, seed=42)
    assert all(result[i].source != result[i + 1].source for i in range(len(result) - 1))
