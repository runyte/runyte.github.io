# SPDX-License-Identifier: MPL-2.0
import argparse, ctypes as C, json, os, pathlib, shutil, subprocess, time
P=pathlib.Path
ap=argparse.ArgumentParser()
for name in ['output','workspace','binary','gif','pdf']:
    ap.add_argument('--'+name,type=P,required=True)
args=ap.parse_args()
args.output.mkdir(parents=True,exist_ok=False)
root=args.workspace.resolve(); root.mkdir(parents=True,exist_ok=False)
state=args.output/'state'; state.mkdir(exist_ok=True)
for part in ['config','cache','runtime']:(state/part).mkdir(exist_ok=True,mode=0o700)
shutil.copyfile(args.gif,root/'giphy.gif'); shutil.copyfile(args.pdf,root/'RustBook.pdf')
(root/'main.rs').write_text('''// Runyte — one workspace, every view.\n// Code, animated images, and PDFs.\n\nstruct Workspace {\n    name: String,\n    panes: usize,\n}\n\nimpl Workspace {\n    fn new(name: &str) -> Self {\n        Self {\n            name: name.into(),\n            panes: 3,\n        }\n    }\n\n    fn open(&self) {\n        println!("{}: {} views", self.name, self.panes);\n    }\n}\n\nfn main() {\n    let workspace = Workspace::new("Runyte");\n    workspace.open();\n}\n''')
subprocess.run(['git','init','-q',str(root)],check=True)
config=state/'config/config.yaml';config.write_text('mode: ide\ntheme: ocean-dark\nlsp:\n  enable: false\neditor:\n  font_size: 22\n')
x=C.CDLL('libX11.so.6');xt=C.CDLL('libXtst.so.6')
for name,types,ret in [('XOpenDisplay',[C.c_char_p],C.c_void_p),('XDefaultRootWindow',[C.c_void_p],C.c_ulong),('XQueryTree',[C.c_void_p,C.c_ulong,C.POINTER(C.c_ulong),C.POINTER(C.c_ulong),C.POINTER(C.POINTER(C.c_ulong)),C.POINTER(C.c_uint)],C.c_int),('XFetchName',[C.c_void_p,C.c_ulong,C.POINTER(C.c_char_p)],C.c_int),('XFree',[C.c_void_p],C.c_int),('XSetInputFocus',[C.c_void_p,C.c_ulong,C.c_int,C.c_ulong],C.c_int),('XFlush',[C.c_void_p],C.c_int),('XStringToKeysym',[C.c_char_p],C.c_ulong),('XKeysymToKeycode',[C.c_void_p,C.c_ulong],C.c_uint),('XMoveResizeWindow',[C.c_void_p,C.c_ulong,C.c_int,C.c_int,C.c_uint,C.c_uint],C.c_int)]:
    f=getattr(x,name);f.argtypes=types;f.restype=ret
xt.XTestFakeKeyEvent.argtypes=[C.c_void_p,C.c_uint,C.c_int,C.c_ulong];xt.XTestFakeMotionEvent.argtypes=[C.c_void_p,C.c_int,C.c_int,C.c_int,C.c_ulong];xt.XTestFakeButtonEvent.argtypes=[C.c_void_p,C.c_uint,C.c_int,C.c_ulong]
d=x.XOpenDisplay(None);assert d
r=x.XDefaultRootWindow(d)
x.XCreateFontCursor.argtypes=[C.c_void_p,C.c_uint];x.XCreateFontCursor.restype=C.c_ulong
x.XDefineCursor.argtypes=[C.c_void_p,C.c_ulong,C.c_ulong]
x.XDefineCursor(d,r,x.XCreateFontCursor(d,68))
def children():
    rr=C.c_ulong();parent=C.c_ulong();items=C.POINTER(C.c_ulong)();n=C.c_uint();x.XQueryTree(d,r,C.byref(rr),C.byref(parent),C.byref(items),C.byref(n)); result=[items[i] for i in range(n.value)]; x.XFree(items);return result
def key(s,mods=(),delay=.03):
    codes=[x.XKeysymToKeycode(d,x.XStringToKeysym(m.encode())) for m in mods]
    for c in codes:xt.XTestFakeKeyEvent(d,c,1,0)
    c=x.XKeysymToKeycode(d,x.XStringToKeysym(s.encode()));assert c,s
    xt.XTestFakeKeyEvent(d,c,1,0);xt.XTestFakeKeyEvent(d,c,0,0)
    for c in reversed(codes):xt.XTestFakeKeyEvent(d,c,0,0)
    x.XFlush(d);time.sleep(delay)
def text(s):
    syms={':':('semicolon',True),' ':('space',False),'.':('period',False),'/':('slash',False),'-':('minus',False)}
    for c in s:
        sym,shift=syms.get(c,(c.lower(),c.isupper()));key(sym,('Shift_L',) if shift else ())
def command(s,wait=.8):
    key('Escape');text(':'+s);key('Return');time.sleep(wait)
def move(px,py):xt.XTestFakeMotionEvent(d,-1,px,py,0);x.XFlush(d)
def click(px,py):
    move(px,py);xt.XTestFakeButtonEvent(d,1,1,0);xt.XTestFakeButtonEvent(d,1,0,0);x.XFlush(d);time.sleep(.15)
def drag(start,end,shift=False):
    mods=['Alt_L']+(['Shift_L'] if shift else [])
    move(*start);time.sleep(.3)
    for m in mods:xt.XTestFakeKeyEvent(d,x.XKeysymToKeycode(d,x.XStringToKeysym(m.encode())),1,0)
    xt.XTestFakeButtonEvent(d,1,1,0);x.XFlush(d);time.sleep(.2)
    for i in range(1,61):move(round(start[0]+(end[0]-start[0])*i/60),round(start[1]+(end[1]-start[1])*i/60));time.sleep(.022)
    time.sleep(.7);xt.XTestFakeButtonEvent(d,1,0,0)
    for m in reversed(mods):xt.XTestFakeKeyEvent(d,x.XKeysymToKeycode(d,x.XStringToKeysym(m.encode())),0,0)
    x.XFlush(d);time.sleep(1.0)
def shot(label):
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','x11grab','-video_size','2560x1380','-i',os.environ['DISPLAY'],'-frames:v','1',str(args.output/(label+'.png'))],check=True)
env={k:v for k,v in os.environ.items() if not k.startswith('RUNYTE_') and k!='WAYLAND_DISPLAY'}
for var,part in [('XDG_CONFIG_HOME','config'),('XDG_CACHE_HOME','cache'),('XDG_RUNTIME_DIR','runtime')]:env[var]=str((state/part).resolve())
previous=set(children());log=open(args.output/'window.log','w');p=subprocess.Popen([str(args.binary.resolve()),'--window','--ide','--config',str(config.resolve()),'main.rs'],cwd=root,env=env,stdout=log,stderr=log)
rec=None;marks=[];start=0
try:
    win=None
    for _ in range(200):
        if p.poll() is not None:raise RuntimeError((args.output/'window.log').read_text())
        for w in set(children())-previous:
            name=C.c_char_p();x.XFetchName(d,w,C.byref(name));title=name.value or b''
            if name:x.XFree(name)
            if b'Runyte' in title:win=w;break
        if win:break
        time.sleep(.1)
    assert win,'no window'
    time.sleep(1);x.XMoveResizeWindow(d,win,0,0,2560,1380);x.XSetInputFocus(d,win,1,0);x.XFlush(d);move(2500,1300);time.sleep(2)
    shot('start')
    rec=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','x11grab','-framerate','30','-video_size','2560x1380','-draw_mouse','1','-i',os.environ['DISPLAY'],'-c:v','libx264','-preset','ultrafast','-crf','16','-pix_fmt','yuv420p',str(args.output/'raw.mp4')],stdin=subprocess.PIPE)
    start=time.monotonic();time.sleep(1)
    def mark(label):marks.append({'name':label,'seconds':round(time.monotonic()-start,3)});print(marks[-1],flush=True)
    command('vsplit giphy.gif',1.3);mark('Animated GIF');shot('gif');time.sleep(1)
    command('hsplit RustBook.pdf',1.6);mark('PDF and image');shot('media');time.sleep(1.1)
    time.sleep(1.6);mark('Media overview')
    drag((1850,300),(600,600));mark('Alt drag swaps GIF and source');shot('alt-drag')
    drag((1880,1030),(1880,300),True);mark('Shift Alt drag expands PDF upward');shot('expand');time.sleep(1)
    key('equal');time.sleep(1);key('Escape');time.sleep(.6);mark('PDF zoom and fit')
    drag((1880,650),(650,650));mark('Alt drag swaps PDF and GIF');shot('swap');time.sleep(2)
    mark('end')
finally:
    if rec:
        rec.communicate(b'q',timeout=30)
    p.terminate()
    try:p.wait(timeout=10)
    except subprocess.TimeoutExpired:p.kill();p.wait()
    log.close();(args.output/'timings.json').write_text(json.dumps(marks,indent=2)+'\n')
