#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Cut service waits; reserve three seconds for typing and twelve for Finder."""
import argparse
import json
import math
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('raw', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Output exists; use a new destination.')
    meta = json.loads(args.raw.with_suffix('.recording.json').read_text())
    fps, total = meta['fps'], meta['frames']
    target = 60 * fps
    marks = {step['name']: step for step in meta['timeline'] if 'name' in step}

    def frame(name):
        return math.floor(marks[name]['start'] * fps)

    cuts = []
    for begin, end, head, tail in [
        ('Codex startup begins', 'Codex ready', 0, 0),
        ('Codex response wait begins', 'Codex answered', .8, 1.2),
        ('Diagnostics wait begins', 'Rust type error ready', .3, .1),
    ]:
        first = math.floor((marks[begin]['start'] + head) * fps)
        last = math.floor((marks[end]['start'] - tail) * fps)
        if last > first:
            cuts.append((first, last))
    typing = (frame('Prompt typing begins'), frame('Prompt typing ends'))
    finder = (frame('Finder begins'), total)
    boundaries = sorted({0, total, *typing, *finder,
                         *[point for cut in cuts for point in cut]})
    segments = []
    for begin, end in zip(boundaries, boundaries[1:]):
        if any(begin >= start and end <= stop for start, stop in cuts):
            continue
        kind = ('prompt_typing' if typing[0] <= begin < typing[1] else
                'finder' if begin >= finder[0] else 'workflow')
        segments.append({'start_frame': begin, 'end_frame': end, 'kind': kind})
    budgets = {'prompt_typing': 3 * fps, 'finder': 12 * fps, 'workflow': 45 * fps}
    source_frames = {
        kind: sum(s['end_frame'] - s['start_frame'] for s in segments if s['kind'] == kind)
        for kind in budgets
    }
    if any(count <= 0 for count in source_frames.values()):
        raise RuntimeError('Recording is missing typing, workflow, or Finder footage')
    scales = {kind: budgets[kind] / count for kind, count in source_frames.items()}
    if not .85 <= scales['workflow'] <= 1.6 or not .7 <= scales['finder'] <= 1.6:
        raise SystemExit(f'Adjust scene pacing before editing: time scales {scales}')

    # Round cumulative boundaries per category, so every budget is exact and
    # rounding individual cuts cannot steal frames from the Finder ending.
    consumed = dict.fromkeys(budgets, 0)
    allocated = dict.fromkeys(budgets, 0)
    filters = []
    output_frame = 0
    for i, segment in enumerate(segments):
        kind = segment['kind']
        count = segment['end_frame'] - segment['start_frame']
        consumed[kind] += count
        cumulative = round(consumed[kind] * scales[kind])
        frames = cumulative - allocated[kind]
        allocated[kind] = cumulative
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
    assert output_frame == target
    filters.append(''.join(f'[v{i}]' for i in range(len(segments))) +
                   f'concat=n={len(segments)}:v=1:a=0[out]')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.runyte-edit-', dir=args.output.parent) as tmp:
        tmp = Path(tmp)
        (tmp / 'filter.txt').write_text(';\n'.join(filters))
        subprocess.run([
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', str(args.raw),
            '-filter_complex_script', str(tmp / 'filter.txt'), '-map', '[out]',
            '-an', '-c:v', 'libx264', '-crf', '18', '-preset', 'fast',
            '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-frames:v', str(target),
            str(tmp / 'final.mp4'),
        ], check=True, timeout=300)
        info = json.loads(subprocess.check_output([
            'ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0',
            '-show_entries', 'stream=nb_read_frames,duration,width,height',
            '-of', 'json', str(tmp / 'final.mp4'),
        ]))['streams'][0]
        if int(info['nb_read_frames']) != target or abs(float(info['duration']) - 60) > .001:
            raise RuntimeError('Final frame count or duration is incorrect')
        (tmp / 'final.mp4').rename(args.output)
    args.output.with_suffix('.edit.json').write_text(json.dumps({
        'source': args.raw.name, 'fps': fps, 'source_frames': total,
        'output_frames': target, 'duration': 60, 'cuts': cuts, 'segments': segments,
        'section_seconds': {kind: frames / fps for kind, frames in budgets.items()},
    }, indent=2) + '\n')
    print(json.dumps({'video': str(args.output), 'duration': 60, 'frames': target,
                      'pixels': [info['width'], info['height']], 'time_scales': scales}))


if __name__ == '__main__':
    main()
