# SPDX-License-Identifier: MPL-2.0
"""Join the editor take and the agent-channel take into the site's demo, ending in black."""
import argparse, json, pathlib, subprocess
P=pathlib.Path
ap=argparse.ArgumentParser()
for name in ['native','agents','output']:
    ap.add_argument('--'+name,type=P,required=True)
args=ap.parse_args()
out=args.output.resolve();out.mkdir(parents=True,exist_ok=False)
# The editor take plays uncut: rename, Rust Book PDF from the explorer, three pane
# gestures, Navigator, then Space f opening src/diff.rs.
NATIVE_END=36.0
# (start, end, speed) in the agent take. Each message or wake-up line plays at normal
# speed; the typed prompt runs four times faster and the agents' work is shortened.
AGENTS=[(0.6,5.7,4),(5.7,15.9,15),
        (15.9,18.3,1),   # Claude asks Codex in the channel
        (18.3,22.9,8),
        (22.9,25.4,1),   # Claude's wake-up line arrives at Codex's prompt
        (25.4,49.9,16),
        (49.9,52.9,1),   # Codex answers, citing src/diff.rs
        (52.9,54.1,3),
        (54.1,56.3,1),   # Codex's wake-up line arrives at Claude's prompt
        (56.3,61.4,8),
        (61.4,65.4,1)]   # Claude confirms against the code; the picture fades out
FADE=1.5
duration=NATIVE_END+sum((b-a)/s for a,b,s in AGENTS)
parts=[f'[0:v]trim=0:{NATIVE_END},setpts=PTS-STARTPTS[n]']
parts+=[f'[1:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{speed}[a{i}]' for i,(a,b,speed) in enumerate(AGENTS)]
graph=';'.join(parts)+';[n]'+''.join(f'[a{i}]' for i in range(len(AGENTS)))+f'concat=n={len(AGENTS)+1}:v=1:a=0,fps=30,fade=t=out:st={duration-FADE:.3f}:d={FADE}[v]'
base=['ffmpeg','-hide_banner','-loglevel','error','-y']
encode=['-an','-c:v','libx264','-preset','slow','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart']
subprocess.run(base+['-i',str(args.native.resolve()),'-i',str(args.agents.resolve()),'-filter_complex',graph,'-map','[v]']+encode+[str(out/'runyte-demo.mp4')],check=True)
# The homepage shows the first frame before the video starts, so the two must match.
subprocess.run(base+['-i',str(out/'runyte-demo.mp4'),'-frames:v','1','-quality','90',str(out/'runyte-demo-poster.webp')],check=True)
(out/'edit.json').write_text(json.dumps({'native_end':NATIVE_END,'agents':AGENTS,'fade':FADE,'duration':round(duration,3),'geometry':[2560,1380],'fps':30},indent=2)+'\n')
