#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Cut service waits and fit each of the three acts to exactly twenty seconds.

Each act has its own theme, so the switch to gruvbox lands on 0:20 and the
switch to matrix on 0:40. Waiting for Claude Code is cut, never sped up.
"""
import argparse
import json
import math
from pathlib import Path
import subprocess
import tempfile

ACT_SECONDS = 20
ACTS = ('Act 1', 'Act 2', 'Act 3')
# (begin checkpoint, end checkpoint, seconds kept after begin, seconds kept before end)
CUTS = [
    ('Claude startup begins', 'Claude ready', .6, .3),
    ('Claude wait begins', 'Claude finished', .5, 0),
]
SCALE_LIMITS = (.5, 2.0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('raw', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Output exists; use a new destination.')
    meta = json.loads(args.raw.with_suffix('.recording.json').read_text())
    fps, total = meta['fps'], meta['frames']
    marks = {step['name']: step['start'] for step in meta['timeline'] if 'name' in step}
    missing = [name for name in ACTS if name not in marks]
    if missing:
        raise SystemExit(f'Recording lacks checkpoints: {missing}')

    cuts = []
    for begin, end, head, tail in CUTS:
        first = math.floor((marks[begin] + head) * fps)
        last = math.floor((marks[end] - tail) * fps)
        if last > first:
            cuts.append((first, last))
    act_starts = [0] + [math.floor(marks[name] * fps) for name in ACTS[1:]]
    act_bounds = list(zip(act_starts, act_starts[1:] + [total]))
    boundaries = sorted({0, total, *act_starts, *[point for cut in cuts for point in cut]})
    segments = []
    for begin, end in zip(boundaries, boundaries[1:]):
        if any(begin >= start and end <= stop for start, stop in cuts):
            continue
        act = next(i for i, (start, stop) in enumerate(act_bounds) if start <= begin < stop)
        segments.append({'start_frame': begin, 'end_frame': end, 'act': act})

    budget = ACT_SECONDS * fps
    source = [sum(s['end_frame'] - s['start_frame'] for s in segments if s['act'] == act)
              for act in range(len(ACTS))]
    scales = [budget / count if count else 0 for count in source]
    if not all(SCALE_LIMITS[0] <= scale <= SCALE_LIMITS[1] for scale in scales):
        raise SystemExit(f'Adjust scene pacing before editing: act time scales {scales}')

    # Round cumulative boundaries per act, so every act is exactly twenty seconds.
    consumed = [0] * len(ACTS)
    allocated = [0] * len(ACTS)
    filters = []
    output_frame = 0
    for i, segment in enumerate(segments):
        act = segment['act']
        count = segment['end_frame'] - segment['start_frame']
        consumed[act] += count
        cumulative = round(consumed[act] * scales[act])
        frames = cumulative - allocated[act]
        allocated[act] = cumulative
        if frames < 1:
            raise RuntimeError('A retained segment is shorter than one output frame')
        segment.update(output_start_frame=output_frame, output_frames=frames,
                       time_scale=frames / count)
        output_frame += frames
        filters.append(
            f"[0:v]trim=start_frame={segment['start_frame']}:end_frame={segment['end_frame']},"
            f"setpts={frames/count:.12f}*(PTS-STARTPTS),fps={fps},"
            f"tpad=stop_mode=clone:stop_duration=0.2,trim=end_frame={frames},"
            f"setpts=PTS-STARTPTS[v{i}]"
        )
    target = budget * len(ACTS)
    assert output_frame == target
    filters.append(''.join(f'[v{i}]' for i in range(len(segments))) +
                   f'concat=n={len(segments)}:v=1:a=0[out]')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.runyte-edit-', dir=args.output.parent) as tmp:
        tmp = Path(tmp)
        (tmp/'filter.txt').write_text(';\n'.join(filters))
        subprocess.run([
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', str(args.raw),
            '-filter_complex_script', str(tmp/'filter.txt'), '-map', '[out]',
            '-an', '-c:v', 'libx264', '-crf', '18', '-preset', 'fast',
            '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-frames:v', str(target),
            str(tmp/'final.mp4'),
        ], check=True, timeout=300)
        info = json.loads(subprocess.check_output([
            'ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0',
            '-show_entries', 'stream=nb_read_frames,duration,width,height',
            '-of', 'json', str(tmp/'final.mp4'),
        ]))['streams'][0]
        seconds = ACT_SECONDS * len(ACTS)
        if int(info['nb_read_frames']) != target or abs(float(info['duration']) - seconds) > .001:
            raise RuntimeError('Final frame count or duration is incorrect')
        (tmp/'final.mp4').rename(args.output)
    args.output.with_suffix('.edit.json').write_text(json.dumps({
        'source': args.raw.name, 'fps': fps, 'source_frames': total, 'output_frames': target,
        'duration': seconds, 'cuts': cuts, 'segments': segments,
        'act_seconds': ACT_SECONDS, 'act_time_scales': scales,
    }, indent=2) + '\n')
    print(json.dumps({'video': str(args.output), 'duration': seconds, 'frames': target,
                      'pixels': [info['width'], info['height']], 'act_time_scales': scales}))


if __name__ == '__main__':
    main()
