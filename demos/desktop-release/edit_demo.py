# SPDX-License-Identifier: MPL-2.0
"""Encode the reviewed native capture into the site's shared demo and its parts."""
import argparse, json, pathlib, subprocess
P=pathlib.Path
ap=argparse.ArgumentParser()
for name in ['native','output']:
    ap.add_argument('--'+name,type=P,required=True)
args=ap.parse_args()
out=args.output.resolve();out.mkdir(parents=True,exist_ok=False)
native=str(args.native.resolve())
DURATION,PANES_START,PANES_SECONDS=23.0,6.3,9.7
base=['ffmpeg','-hide_banner','-loglevel','error','-y']
encode=['-an','-c:v','libx264','-preset','slow','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart']
subprocess.run(base+['-i',native,'-t',str(DURATION)]+encode+[str(out/'runyte-demo.mp4')],check=True)
subprocess.run(base+['-ss',str(PANES_START),'-i',native,'-t',str(PANES_SECONDS)]+encode+[str(out/'runyte-desktop-demo.mp4')],check=True)
# The homepage shows the first frame before the video starts, so the two must match.
subprocess.run(base+['-i',str(out/'runyte-demo.mp4'),'-frames:v','1','-quality','90',str(out/'runyte-demo-poster.webp')],check=True)
subprocess.run(base+['-i',str(out/'runyte-desktop-demo.mp4'),'-frames:v','1','-quality','88',str(out/'runyte-desktop-demo-poster.webp')],check=True)
(out/'edit.json').write_text(json.dumps({'duration':DURATION,'panes_start':PANES_START,'panes_seconds':PANES_SECONDS,'geometry':[2560,1380],'fps':30},indent=2)+'\n')
