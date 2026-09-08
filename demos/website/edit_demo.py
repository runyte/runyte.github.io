#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Cut service waits and gently retime the website demo to one minute."""
import argparse
import json
import math
from pathlib import Path
import subprocess
import tempfile


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('raw',type=Path)
    p.add_argument('output',type=Path)
    a=p.parse_args()
    if a.output.exists():raise SystemExit('Output exists; use a new destination.')
    meta=json.loads(a.raw.with_suffix('.recording.json').read_text())
    fps=meta['fps']; total=meta['frames']; target=60*fps
    marks={s['name']:s for s in meta['timeline'] if 'name' in s}
    cuts=[]
    for begin,end,head,tail in [
        ('Codex startup begins','Codex ready',0,0),
        ('Codex response wait begins','Codex answered',.8,1.2),
        ('Diagnostics wait begins','Rust type error ready',.3,.1),
    ]:
        first=math.floor((marks[begin]['start']+head)*fps)
        last=math.floor((marks[end]['start']-tail)*fps)
        if last>first:cuts.append((first,last))
    boundaries=sorted({0,total,*[point for cut in cuts for point in cut]})
    segments=[{'start_frame':begin,'end_frame':end} for begin,end in zip(boundaries,boundaries[1:]) if not any(begin>=start and end<=stop for start,stop in cuts)]
    kept=sum(s['end_frame']-s['start_frame'] for s in segments)
    scale=target/kept
    if not .85<=scale<=1.5:
        raise SystemExit(f'Action footage is {kept/fps:.1f}s. Adjust the scene pacing before making a one-minute edit.')
    filters=[]
    for i,s in enumerate(segments):
        filters.append(f"[0:v]trim=start_frame={s['start_frame']}:end_frame={s['end_frame']},setpts=PTS-STARTPTS[v{i}]")
    filters.append(''.join(f'[v{i}]' for i in range(len(segments)))+f'concat=n={len(segments)}:v=1:a=0,setpts={scale:.12f}*PTS,fps={fps},tpad=stop_mode=clone:stop_duration=0.2[out]')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.runyte-edit-',dir=a.output.parent) as tmp:
        tmp=Path(tmp)
        (tmp/'filter.txt').write_text(';\n'.join(filters))
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(a.raw),'-filter_complex_script',str(tmp/'filter.txt'),'-map','[out]','-an','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart','-frames:v',str(target),str(tmp/'final.mp4')],check=True,timeout=300)
        info=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,duration,width,height','-of','json',str(tmp/'final.mp4')]))['streams'][0]
        if int(info['nb_read_frames'])!=target or abs(float(info['duration'])-60)>.001:raise RuntimeError('Final frame count or duration is incorrect')
        (tmp/'final.mp4').rename(a.output)
    a.output.with_suffix('.edit.json').write_text(json.dumps({'source':a.raw.name,'fps':fps,'source_frames':total,'output_frames':target,'duration':60,'cuts':cuts,'segments':segments,'time_scale':scale},indent=2)+'\n')
    print(json.dumps({'video':str(a.output),'duration':60,'frames':target,'pixels':[info['width'],info['height']],'time_scale':scale}))

if __name__=='__main__':main()
