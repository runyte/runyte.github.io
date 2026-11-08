# SPDX-License-Identifier: MPL-2.0
"""Cut the reviewed agent-channel capture into the Features page clip."""
import argparse, json, pathlib, subprocess
P=pathlib.Path
ap=argparse.ArgumentParser()
for name in ['native','output']:
    ap.add_argument('--'+name,type=P,required=True)
args=ap.parse_args()
out=args.output.resolve();out.mkdir(parents=True,exist_ok=False)
# (start, end, speed): prompts and arriving messages play at normal speed; waits are shortened.
SEGMENTS=[(1.2,4.0,1),(15.5,18.5,1),(49.4,52.6,1),(52.6,84.0,10.5),(84.0,87.5,1),(103.2,105.0,1),(105.0,114.5,6),(114.5,118.5,1)]
parts=[f'[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{speed}[s{i}]' for i,(a,b,speed) in enumerate(SEGMENTS)]
graph=';'.join(parts)+';'+''.join(f'[s{i}]' for i in range(len(SEGMENTS)))+f'concat=n={len(SEGMENTS)}:v=1:a=0,fps=30[v]'
base=['ffmpeg','-hide_banner','-loglevel','error','-y']
subprocess.run(base+['-i',str(args.native.resolve()),'-filter_complex',graph,'-map','[v]','-an','-c:v','libx264','-preset','slow','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'agents.mp4')],check=True)
subprocess.run(base+['-sseof','-0.2','-i',str(out/'agents.mp4'),'-frames:v','1','-quality','88',str(out/'agents-poster.webp')],check=True)
(out/'edit.json').write_text(json.dumps({'segments':SEGMENTS},indent=2)+'\n')
