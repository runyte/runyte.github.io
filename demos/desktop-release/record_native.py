# SPDX-License-Identifier: MPL-2.0
import argparse, ctypes as C, json, os, pathlib, shutil, subprocess, time
P=pathlib.Path
ap=argparse.ArgumentParser()
for name in ['output','workspace','binary']:
    ap.add_argument('--'+name,type=P,required=True)
ap.add_argument('--pdf',type=P)
ap.add_argument('--source',help='Git URL of the Runyte repository shown in the demo')
ap.add_argument('--scene',choices=['demo','pdf-shot'],default='demo')
ap.add_argument('--size',default='2560x1380')
ap.add_argument('--theme',default='dark')
ap.add_argument('--font-size',type=int,default=22)
args=ap.parse_args()
W,H=map(int,args.size.split('x'))
args.output.mkdir(parents=True,exist_ok=False)
root=args.workspace.resolve(); root.mkdir(parents=True,exist_ok=False)
state=args.output/'state'; state.mkdir(exist_ok=True)
for part in ['config','cache','runtime']:(state/part).mkdir(exist_ok=True,mode=0o700)
if args.scene=='demo':
    subprocess.run(['git','clone','-q','--branch','main','--depth','200',args.source,str(root)],check=True)
else:
    shutil.copyfile(args.pdf,root/'RustBook.pdf')
    (root/'main.rs').write_text('''// Runyte — one workspace, every view.\n// Code, terminals, and files.\n\nstruct Workspace {\n    name: String,\n    panes: usize,\n}\n\nimpl Workspace {\n    fn new(name: &str) -> Self {\n        Self {\n            name: name.into(),\n            panes: 3,\n        }\n    }\n\n    fn open(&self) {\n        println!("{}: {} views", self.name, self.panes);\n    }\n}\n\nfn main() {\n    let workspace = Workspace::new("Runyte");\n    workspace.open();\n}\n''')
    subprocess.run(['git','init','-q',str(root)],check=True)
BASHRC=r'''PS1='runyte $ '
export GIT_PAGER=cat
PROMPT_COMMAND='printf "\033]0;%s\007" "$(HISTTIMEFORMAT= history 1 | sed "s/^ *[0-9]* *//")"'
'''
config=state/'config/config.yaml';config.write_text(f'mode: ide\ntheme: {args.theme}\nlsp:\n  enable: false\neditor:\n  font_size: {args.font_size}\n')
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
def text(s,delay=.03):
    syms={':':('semicolon',True),' ':('space',False),'.':('period',False),'/':('slash',False),'-':('minus',False),'\\':('backslash',False),'|':('backslash',True),'*':('8',True),'_':('minus',True),'=':('equal',False)}
    for c in s:
        sym,shift=syms.get(c,(c.lower(),c.isupper()));key(sym,('Shift_L',) if shift else (),delay)
def command(s,wait=.8,escape=True):
    if escape:key('Escape')
    text(':'+s);key('Return');time.sleep(wait)
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
pointer=[0,0]
def glide(px,py,steps=10,pause=.012):
    x0,y0=pointer
    for i in range(1,steps+1):move(round(x0+(px-x0)*i/steps),round(y0+(py-y0)*i/steps));time.sleep(pause)
    pointer[:]=[px,py]
def gesture(start,end,shift=True,alt=True):
    # A quick Alt-drag or Shift-Alt-drag: the pointer glides in, drags, and releases without lingering.
    glide(*start);time.sleep(.1)
    mods=[x.XKeysymToKeycode(d,x.XStringToKeysym(m)) for m in ((b'Alt_L',b'Shift_L') if shift else (b'Alt_L',) if alt else ())]
    for m in mods:xt.XTestFakeKeyEvent(d,m,1,0)
    xt.XTestFakeButtonEvent(d,1,1,0);x.XFlush(d);time.sleep(.07)
    glide(*end,steps=22,pause=.014);time.sleep(.2)
    xt.XTestFakeButtonEvent(d,1,0,0)
    for m in reversed(mods):xt.XTestFakeKeyEvent(d,m,0,0)
    x.XFlush(d);time.sleep(.42)
def shot(label):
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','x11grab','-video_size',args.size,'-i',os.environ['DISPLAY'],'-frames:v','1',str(args.output/(label+'.png'))],check=True)
env={k:v for k,v in os.environ.items() if not k.startswith('RUNYTE_') and k!='WAYLAND_DISPLAY'}
for var,part in [('XDG_CONFIG_HOME','config'),('XDG_CACHE_HOME','cache'),('XDG_RUNTIME_DIR','runtime')]:env[var]=str((state/part).resolve())
home=state/'home';home.mkdir(exist_ok=True);(home/'.bashrc').write_text(BASHRC);env.update(HOME=str(home.resolve()),SHELL='/bin/bash')
previous=set(children());log=open(args.output/'window.log','w');p=subprocess.Popen([str(args.binary.resolve()),'--window','--ide','--config',str(config.resolve()),'src/ui.rs' if args.scene=='demo' else 'main.rs'],cwd=root,env=env,stdout=log,stderr=log)
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
    time.sleep(1);x.XMoveResizeWindow(d,win,0,0,W,H);x.XSetInputFocus(d,win,1,0);x.XFlush(d);move(W-60,H-80);time.sleep(2)
    if args.scene=='pdf-shot':
        command('vsplit RustBook.pdf',2.5);move(W-40,H-140);time.sleep(.6);shot('everforest-pdf')
        raise SystemExit
    ctrl=('Control_L',)
    def focus(direction):key('w',ctrl);key(direction);time.sleep(.25)
    def to_normal():key('backslash',ctrl);time.sleep(.25)
    def run(cmd):text(cmd);key('Return');time.sleep(1.0);to_normal()
    # A: ui.rs, B: layout.rs, C: git log / D: input.rs, E: file sizes, F: explorer.
    # Other buffers and a third terminal stay open for the Navigator.
    command('vsplit src/layout.rs',.6);command('vsplit',.5)
    command('terminal',1.2);run('git log --oneline -40')
    command('hsplit',.6,escape=False)
    focus('h');command('hsplit',.5)
    command('terminal',1.2);run('wc -l src/*.rs | sort -n | tail -22')
    focus('h');command('hsplit src/terminal/mod.rs',.6)
    command('terminal',1.2);run('ls --color src')
    for name in ('Cargo.toml','README.md','src/app/input.rs'):command('edit '+name,.5,escape=False)
    focus('k')
    for c in '1276':key(c,delay=.05)
    key('g',delay=.05);key('g');time.sleep(.3);key('z',delay=.05);key('z');time.sleep(.4)
    key('w',ctrl);key('f');time.sleep(.8)
    pointer[:]=[W-60,H-80];move(*pointer);time.sleep(1.2)
    shot('start')
    rec=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','x11grab','-framerate','30','-video_size',args.size,'-draw_mouse','1','-i',os.environ['DISPLAY'],'-c:v','libx264','-preset','ultrafast','-crf','16','-pix_fmt','yuv420p',str(args.output/'raw.mp4')],stdin=subprocess.PIPE)
    start=time.monotonic();time.sleep(.9)
    def mark(label):marks.append({'name':label,'seconds':round(time.monotonic()-start,3)});print(marks[-1],flush=True)
    mark('Function')
    key('m',delay=.1);key('a',delay=.1);key('f');time.sleep(.55);mark('Function selected')
    key('slash');time.sleep(.2);text('\\barea\\b',.07);time.sleep(.15);key('Return');time.sleep(.85);mark('All matches');shot('matches')
    key('c');time.sleep(.2);text('bounds',.1);time.sleep(.35);key('Escape');time.sleep(.3);key('comma');time.sleep(.45);mark('Renamed');shot('renamed')
    key('w',ctrl);key('f');time.sleep(.9);mark('Grid');shot('grid')
    # Columns are 0-1278, 1278-1900 and 1900-2560. Terminals are only covered, never shrunk,
    # because a live shell loses its visible output when its pane gets shorter.
    X=(640,1590,2230);Y=(330,990)
    gesture((X[1],Y[0]),(X[1],Y[1]));mark('B extends down');shot('g1')
    gesture((X[2],Y[1]),(X[2],Y[0]));mark('F extends up');shot('g2')
    gesture((X[1],660),(X[2],660),shift=False);mark('Alt drag swaps columns');shot('g3')
    gesture((X[0],Y[1]),(X[1],Y[1]));mark('D extends right');shot('g4')
    gesture((X[1],Y[0]),(X[0],Y[0]));mark('F extends left');shot('g5')
    gesture((900,Y[1]),(900,Y[0]));mark('D extends up');shot('g6')
    glide(W-60,H-120,steps=12);time.sleep(.3)
    key('space',delay=.1);key('n');time.sleep(1.1);mark('Navigator');shot('nav')
    for _ in range(4):key('Down');time.sleep(.42)
    mark('Browse');shot('nav2')
    text('--color',.1);time.sleep(.8);mark('Filter');shot('nav3')
    key('Return');time.sleep(1.8);mark('Terminal back');shot('final')
    mark('end')
finally:
    if rec:
        rec.communicate(b'q',timeout=30)
    p.terminate()
    try:p.wait(timeout=10)
    except subprocess.TimeoutExpired:p.kill();p.wait()
    log.close();(args.output/'timings.json').write_text(json.dumps(marks,indent=2)+'\n')
