# SPDX-License-Identifier: MPL-2.0
import argparse, json, pathlib, subprocess
P=pathlib.Path
ap=argparse.ArgumentParser()
for name in ['intro','native','output','font']:
    ap.add_argument('--'+name,type=P,required=True)
args=ap.parse_args()
out=args.output.resolve();out.mkdir(parents=True,exist_ok=False)
old=args.intro.resolve();native=args.native.resolve();font=str(args.font.resolve())
def title(text,start=0,end=100):
    # Text files avoid ffmpeg's nested text escaping.
    path=out/('caption-'+str(len(list(out.glob('caption-*'))))+'.txt');path.write_text(text)
    return f"drawtext=fontfile={font}:textfile={path}:fontcolor=white:fontsize=30:x=40:y=10:enable='between(t,{start},{end})'"
segments=[(0,7,'Modal editing + file navigation'),(9.5,5,'Integrated terminals + Navigator'),(21.5,7,'Markdown + persistent sessions')]
paths=[]
for i,(start,duration,caption) in enumerate(segments):
    dest=out/f'part-{i}.mp4'; paths.append(dest)
    vf=f'pad=2560:1440:80:100:color=0x0b1c26,fps=30,tpad=stop_mode=clone:stop_duration=0.1,setsar=1,'+title(caption)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(start),'-i',str(old),'-t',str(duration),'-vf',vf,'-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],check=True)
vf='pad=2560:1440:0:60:color=0x0b1c26,setsar=1,'+','.join([
 title('runyte --window  |  Code + animated images',0,4.1),
 title('Images + PDFs, inside your workspace',4.1,9.6),
 title('Alt + drag  |  Swap panes',9.6,13.7),
 title('Shift + Alt + drag  |  Expand a pane',13.7,18.2),
 title('PDF zoom + fit',18.2,20.1),
 title('Alt + drag  |  Arrange your references',20.1,23.7),
 title('Runyte  |  Terminal + desktop editions',23.7,26)])
dest=out/'runyte-desktop-demo.mp4';paths.append(dest)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(native),'-t','26','-vf',vf,'-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],check=True)
concat=out/'concat.txt';concat.write_text(''.join("file '"+str(p)+"'\n" for p in paths))
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(out/'runyte-demo.mp4')],check=True)
for name,t in [('runyte-demo',25.7),('runyte-desktop-demo',6.7)]:
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(out/(name+'.mp4')),'-frames:v','1','-quality','88',str(out/(name+'-poster.webp'))],check=True)
(out/'edit.json').write_text(json.dumps({'old_segments':[{'start':s,'duration':d,'caption':c} for s,d,c in segments],'native_seconds':26,'duration':45,'native_source_revision':'f0692a1','native_theme':'ocean-dark','native_font_size':22,'geometry':[2560,1440],'fps':30,'cuts':'Repeated Navigator visits and the old four-pane construction/hold removed; retained footage stays at original speed.'},indent=2)+'\n')
