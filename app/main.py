# -*- coding: utf-8 -*-
"""مولّد الجذاذة – التربية الإسلامية
تطبيق سطح مكتب محلي، بلا خادم أو اتصال شبكي.
"""
import json, os, shutil, uuid, webbrowser, zipfile
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

APP_NAME = "مولّد الجذاذة – التربية الإسلامية"
# Store user data outside the installation directory so updates do not erase it.
if os.name == 'nt' and os.environ.get('LOCALAPPDATA'):
    DATA_DIR = Path(os.environ['LOCALAPPDATA']) / 'Tarbawi-Jodada'
else:
    DATA_DIR = Path.home() / 'Documents' / 'مولد الجذاذة - التربية الإسلامية'
DATA_FILE = DATA_DIR / 'data.json'
EXPORT_DIR = DATA_DIR / 'exports'

PEDAGOGICAL_DEFAULTS = {
    'diagnostic': {
        'abilities': ['استحضار المكتسبات السابقة', 'التعبير الشفهي', 'تشخيص التعلمات'],
        'aids': ['أسئلة التقويم التشخيصي', 'سبورة القسم'],
        'indicators': ['يستحضر المتعلم مكتسباته السابقة', 'يجيب عن الأسئلة الأولية', 'يحدد مكامن القوة والتعثر']},
    'problem': {
        'abilities': ['الملاحظة والفهم', 'طرح التساؤلات', 'اقتراح الفرضيات'],
        'aids': ['الوضعية المشكلة', 'نص أو صورة أو سند منطلق', 'سبورة القسم'],
        'indicators': ['يفهم عناصر الوضعية', 'يحدد السؤال الإشكالي', 'يقترح فرضية مع تعليل أولي']},
    'task': {
        'abilities': ['الفهم والتحليل', 'الاستدلال والمناقشة', 'التعاون وبناء التعلم'],
        'aids': ['النصوص الشرعية أو السندات', 'الكتاب المدرسي', 'السبورة والوسائل التعليمية'],
        'indicators': ['يستثمر السندات بشكل سليم', 'ينجز المهمة وفق المطلوب', 'يبني خلاصة مرتبطة بالدرس']},
    'formative': {
        'abilities': ['الاستيعاب والتطبيق', 'التعبير عن التعلمات', 'التصحيح الذاتي'],
        'aids': ['أسئلة التقويم المرحلي', 'شبكة التقويم', 'دفتر المتعلم'],
        'indicators': ['يجيب عن أسئلة التقويم', 'يوظف المفاهيم المكتسبة', 'يصوب أخطاءه اعتماداً على التغذية الراجعة']},
    'scrutiny': {
        'abilities': ['النقد والتمحيص', 'الاستدلال', 'إصدار الحكم'],
        'aids': ['الفرضيات السابقة', 'السندات والأدلة الشرعية', 'شبكة تمحيص الفرضيات'],
        'indicators': ['يقارن الفرضية بالأدلة', 'يصدر حكماً معللاً', 'يميز بين الصحيح وما يحتاج إلى تعديل']},
    'values': {
        'abilities': ['استخراج القيم', 'الربط بين التعلم والسلوك', 'الالتزام والمسؤولية'],
        'aids': ['النصوص والسندات', 'مواقف حياتية', 'شبكة استثمار القيم'],
        'indicators': ['يستخرج قيمة من التعلم', 'يستدل عليها من النص أو النشاط', 'يقترح سلوكاً يجسدها']},
    'summative': {
        'abilities': ['التركيب والتقويم', 'توظيف التعلمات', 'الاستقلالية'],
        'aids': ['وضعية إدماجية', 'أسئلة التقويم الإجمالي', 'شبكة التصحيح'],
        'indicators': ['يوظف مكتسباته في وضعية جديدة', 'ينظم جوابه ويعلله', 'يحقق الهدف التعلمي']},
    'self_learning': {
        'abilities': ['التعلم الذاتي', 'البحث والاستقصاء', 'تنظيم العمل'],
        'aids': ['الكتاب المدرسي', 'مصادر موثوقة يحددها الأستاذ', 'بطاقة التعلم الذاتي'],
        'indicators': ['ينجز المهمة باستقلالية', 'ينتج أثراً قابلاً للتقويم', 'يستعد للتعلم اللاحق']},
}

DEFAULT_STAGES = [
    {"name":"التقويم التشخيصي", "kind":"diagnostic", "purpose":"استحضار المكتسبات السابقة وربطها بالحصة التالية", "activities":[]},
    {"name":"تقديم الوضعية المشكلة", "kind":"problem", "purpose":"تشويق المتعلم وطرح السؤال الإشكالي واستقبال الفرضيات", "problem":"", "study":[], "hypotheses":[]},
    {"name":"المهمة الأولى", "kind":"task", "purpose":"بناء المفاهيم والعلاقات", "title":"", "goal":"", "duration":"", "evidences":[], "questions":[], "teacher":"", "learner":"", "abilities":[], "aids":[], "summary":"", "indicators":[]},
    {"name":"التقويم المرحلي", "kind":"formative", "purpose":"تثبيت ما تم شرحه وتقويم الفهم المرحلي", "questions":[]},
    {"name":"التقويم التشخيصي", "kind":"diagnostic", "purpose":"الوقوف على المكتسبات وربطها بالحصة التالية", "questions":[]},
    {"name":"المهمة الثانية", "kind":"task", "purpose":"استثمار السندات وبناء المحاور", "title":"", "goal":"", "duration":"", "evidences":[], "questions":[], "teacher":"", "learner":"", "abilities":[], "aids":[], "summary":"", "indicators":[]},
    {"name":"التقويم المرحلي", "kind":"formative", "purpose":"تقويم مرحلي", "questions":[]},
    {"name":"تمحيص الفرضيات", "kind":"scrutiny", "purpose":"العودة إلى الفرضيات وإصدار الحكم مع الدليل والتعليل"},
    {"name":"القيم المستنبطة", "kind":"values", "purpose":"استخراج القيم وتوظيفها", "values":[]},
    {"name":"التقويم الإجمالي", "kind":"summative", "purpose":"تثبيت المعارف وتقويم المكتسبات", "questions":[]},
    {"name":"التعلم الذاتي", "kind":"self_learning", "purpose":"أن يتعلم ذاتياً ويستعد للدرس القادم", "task":"", "instructions":"", "product":"", "resources":"", "deadline":""},
]

def now(): return datetime.now().isoformat(timespec="seconds")
def uid(): return uuid.uuid4().hex[:12]
def normalize_lesson(lesson):
    """يضمن اكتمال الحقول التربوية التلقائية دون الكتابة فوق إدخالات الأستاذ."""
    lesson.setdefault('subject', 'التربية الإسلامية')
    lesson.setdefault('stages', json.loads(json.dumps(DEFAULT_STAGES, ensure_ascii=False)))
    for stage in lesson.get('stages', []):
        defaults = PEDAGOGICAL_DEFAULTS.get(stage.get('kind'), {})
        for key in ('abilities', 'aids', 'indicators'):
            current = stage.get(key)
            if not isinstance(current, list) or not any(str(x).strip() for x in current):
                stage[key] = list(defaults.get(key, []))
            else:
                stage[key] = [str(x).strip() for x in current if str(x).strip()]
    return lesson


def blank_lesson(template_id="default"):
    lesson = {"id":uid(), "title":"جذاذة جديدة", "institution":"", "academy":"", "directorate":"", "teacher":"", "subject":"التربية الإسلامية", "level":"", "school_year":"", "entry":"", "domain":"التزكية (عقيدة)", "unit":"", "lesson_title":"", "sessions":"", "period":"", "date":"", "references":[], "skills":[], "objectives":[], "resources":[], "competency":"", "template_id":template_id, "stages":json.loads(json.dumps(DEFAULT_STAGES, ensure_ascii=False)), "created_at":now(), "updated_at":now()}
    return normalize_lesson(lesson)

def default_data():
    return {"lessons":[], "templates":[{"id":"default","name":"القالب الأساسي – الإيمان والفلسفة","description":"المراحل التربوية الرسمية المعتمدة","stages":DEFAULT_STAGES}], "settings":{"auto_save":True,"teacher":"","institution":""}}

class Store:
    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True); EXPORT_DIR.mkdir(exist_ok=True); self.data=self.load()
    def load(self):
        if DATA_FILE.exists():
            try: return json.loads(DATA_FILE.read_text(encoding="utf-8"))
            except Exception: pass
        return default_data()
    def save(self):
        tmp=DATA_FILE.with_suffix('.tmp'); tmp.write_text(json.dumps(self.data,ensure_ascii=False,indent=2),encoding='utf-8'); tmp.replace(DATA_FILE)
    def lesson(self,lid): return next((x for x in self.data['lessons'] if x['id']==lid),None)
    def template(self,tid): return next((x for x in self.data['templates'] if x['id']==tid),None)

class App(tk.Tk):
    def __init__(self):
        super().__init__(); self.title(APP_NAME); self.geometry('1280x820'); self.minsize(1050,700); self.configure(bg='#f5f7fb'); self.store=Store(); self.current=None; self.current_stage=0; self.search_var=tk.StringVar(); self.protocol('WM_DELETE_WINDOW', self.close)
        self.style(); self.build_shell(); self.show_home()
    def style(self):
        s=ttk.Style(self); s.theme_use('clam'); s.configure('TButton',font=('Segoe UI',11),padding=8); s.configure('TLabel',font=('Segoe UI',11),background='#f5f7fb'); s.configure('Header.TLabel',font=('Segoe UI',22,'bold'),foreground='#183b56'); s.configure('Card.TFrame',background='white'); s.configure('Treeview',rowheight=32,font=('Segoe UI',10)); s.configure('Treeview.Heading',font=('Segoe UI',10,'bold'))
    def build_shell(self):
        self.nav=tk.Frame(self,bg='#183b56',width=235); self.nav.pack(side='right',fill='y'); self.nav.pack_propagate(False)
        tk.Label(self.nav,text='مولّد الجذاذة',font=('Segoe UI',20,'bold'),fg='white',bg='#183b56').pack(pady=(35,3)); tk.Label(self.nav,text='التربية الإسلامية',font=('Segoe UI',11),fg='#b9d8e8',bg='#183b56').pack(pady=(0,35))
        for text,cmd in [('الرئيسية',self.show_home),('جذاذة جديدة',self.new_lesson),('جذاذاتي',self.show_lessons),('القوالب',self.show_templates),('الإعدادات',self.show_settings)]:
            tk.Button(self.nav,text=text,command=cmd,anchor='e',font=('Segoe UI',12),fg='white',bg='#183b56',activebackground='#2c617c',activeforeground='white',relief='flat',bd=0,padx=25,pady=12).pack(fill='x')
        self.main=tk.Frame(self,bg='#f5f7fb'); self.main.pack(side='left',fill='both',expand=True)
    def clear(self):
        for w in self.main.winfo_children(): w.destroy()
    def header(self,title,subtitle=''):
        f=tk.Frame(self.main,bg='#f5f7fb'); f.pack(fill='x',padx=35,pady=(28,15)); ttk.Label(f,text=title,style='Header.TLabel').pack(anchor='e');
        if subtitle: ttk.Label(f,text=subtitle,foreground='#64748b').pack(anchor='e',pady=5)
    def card(self):
        f=tk.Frame(self.main,bg='white',highlightbackground='#e2e8f0',highlightthickness=1); f.pack(fill='x',padx=35,pady=8); return f
    def show_home(self):
        self.clear(); self.header('مرحباً بك في مولّد الجذاذة','أنشئ جذاذاتك واحفظها محلياً بسهولة ووضوح')
        c=self.card(); tk.Label(c,text='ابدأ العمل',font=('Segoe UI',16,'bold'),bg='white',fg='#183b56').pack(anchor='e',padx=25,pady=(22,10));
        b=tk.Frame(c,bg='white'); b.pack(anchor='e',padx=25,pady=(0,22)); ttk.Button(b,text='+ جذاذة جديدة',command=self.new_lesson).pack(side='right',padx=5); ttk.Button(b,text='عرض جذاذاتي',command=self.show_lessons).pack(side='right',padx=5); ttk.Button(b,text='القوالب',command=self.show_templates).pack(side='right',padx=5)
        stats=self.card(); count=len(self.store.data['lessons']); last=max(self.store.data['lessons'],key=lambda x:x.get('updated_at',''),default=None)
        for label,val in [('عدد الجذاذات',str(count)),('آخر تعديل',last.get('lesson_title') or last.get('title') if last else 'لا توجد جذاذات'),('المؤسسة',self.store.data.get('settings',{}).get('institution') or 'غير محددة')]:
            q=tk.Frame(stats,bg='white'); q.pack(side='right',expand=True,fill='x',padx=15,pady=22); tk.Label(q,text=label,bg='white',fg='#64748b',font=('Segoe UI',10)).pack(anchor='e'); tk.Label(q,text=val,bg='white',fg='#183b56',font=('Segoe UI',14,'bold')).pack(anchor='e',pady=5)
        recent=self.card(); tk.Label(recent,text='آخر الجذاذات',font=('Segoe UI',14,'bold'),bg='white',fg='#183b56').pack(anchor='e',padx=25,pady=15)
        for l in sorted(self.store.data['lessons'],key=lambda x:x.get('updated_at',''),reverse=True)[:5]:
            row=tk.Frame(recent,bg='white'); row.pack(fill='x',padx=25,pady=4); tk.Label(row,text=l.get('lesson_title') or l.get('title'),bg='white',font=('Segoe UI',11)).pack(side='right'); ttk.Button(row,text='فتح',command=lambda x=l['id']:self.edit_lesson(x)).pack(side='left');
    def new_lesson(self): self.current=blank_lesson(); self.current_stage=0; self.show_editor()
    def show_lessons(self):
        self.clear(); self.header('جذاذاتي','إدارة الجذاذات المحفوظة محلياً والبحث فيها');
        top=self.card(); tk.Label(top,text='بحث',bg='white',font=('Segoe UI',11)).pack(side='right',padx=15,pady=15); e=tk.Entry(top,textvariable=self.search_var,justify='right',font=('Segoe UI',11),width=40); e.pack(side='right',pady=15); e.bind('<KeyRelease>',lambda _:self.refresh_lessons(tree)); ttk.Button(top,text='+ جذاذة جديدة',command=self.new_lesson).pack(side='left',padx=15,pady=12)
        c=self.card(); tree=ttk.Treeview(c,columns=('title','level','year','updated'),show='headings');
        for col,txt,w in [('title','عنوان الدرس',360),('level','المستوى',150),('year','السنة الدراسية',150),('updated','آخر تعديل',180)]: tree.heading(col,text=txt); tree.column(col,width=w,anchor='e')
        tree.pack(fill='both',expand=True,padx=15,pady=15); self.refresh_lessons(tree)
        actions=tk.Frame(c,bg='white'); actions.pack(fill='x',padx=15,pady=(0,15)); ttk.Button(actions,text='فتح/تعديل',command=lambda:self.open_selected(tree)).pack(side='right',padx=4); ttk.Button(actions,text='نسخ',command=lambda:self.copy_selected(tree)).pack(side='right',padx=4); ttk.Button(actions,text='حذف',command=lambda:self.delete_selected(tree)).pack(side='right',padx=4); ttk.Button(actions,text='معاينة',command=lambda:self.preview_selected(tree)).pack(side='left',padx=4)
    def refresh_lessons(self,tree):
        for x in tree.get_children(): tree.delete(x)
        q=self.search_var.get().lower();
        for l in self.store.data['lessons']:
            text=' '.join(str(l.get(k,'')) for k in ('title','lesson_title','level','school_year','teacher')).lower()
            if q in text: tree.insert('', 'end', iid=l['id'], values=(l.get('lesson_title') or l.get('title'),l.get('level',''),l.get('school_year',''),l.get('updated_at','').replace('T',' ')))
    def selected(self,tree):
        s=tree.selection(); return s[0] if s else None
    def open_selected(self,t):
        if self.selected(t): self.edit_lesson(self.selected(t))
    def edit_lesson(self,lid): self.current=self.store.lesson(lid); self.current_stage=0; self.show_editor()
    def copy_selected(self,t):
        if self.selected(t):
            x=json.loads(json.dumps(self.store.lesson(self.selected(t)),ensure_ascii=False)); x['id']=uid(); x['title']=(x.get('lesson_title') or x.get('title'))+' – نسخة'; x['updated_at']=now(); self.store.data['lessons'].append(x); self.store.save(); self.show_lessons()
    def delete_selected(self,t):
        if self.selected(t) and messagebox.askyesno('تأكيد الحذف','هل تريد حذف الجذاذة نهائياً؟'):
            self.store.data['lessons']=[x for x in self.store.data['lessons'] if x['id']!=self.selected(t)]; self.store.save(); self.show_lessons()
    def preview_selected(self,t):
        if self.selected(t): self.current=self.store.lesson(self.selected(t)); self.show_preview()
    def show_editor(self):
        self.clear()
        self.header('محرر الجذاذة', 'تُحفظ التعديلات تلقائياً أثناء العمل')
        toolbar=self.card()
        ttk.Button(toolbar,text='حفظ',command=self.save_current).pack(side='right',padx=6,pady=10)
        ttk.Button(toolbar,text='معاينة كاملة',command=self.show_preview).pack(side='right',padx=6,pady=10)
        ttk.Button(toolbar,text='رجوع',command=self.show_lessons).pack(side='left',padx=6,pady=10)
        viewport=tk.Frame(self.main,bg='#f5f7fb'); viewport.pack(fill='both',expand=True,padx=35,pady=(0,12))
        canvas=tk.Canvas(viewport,bg='#f5f7fb',highlightthickness=0,bd=0); scrollbar=ttk.Scrollbar(viewport,orient='vertical',command=canvas.yview)
        content=tk.Frame(canvas,bg='#f5f7fb'); window_id=canvas.create_window((0,0),window=content,anchor='nw')
        content.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox('all'))); canvas.bind('<Configure>',lambda e:canvas.itemconfigure(window_id,width=e.width)); canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left',fill='both',expand=True); scrollbar.pack(side='right',fill='y'); self._editor_canvas=canvas; self._scroll_canvas=canvas; self._scroll_inner=content
        canvas.bind_all('<MouseWheel>',lambda e:canvas.yview_scroll(int(-e.delta/120),'units'),add='+'); canvas.bind_all('<Button-4>',lambda e:canvas.yview_scroll(-3,'units'),add='+'); canvas.bind_all('<Button-5>',lambda e:canvas.yview_scroll(3,'units'),add='+')
        canvas.bind_all('<Key-Up>',lambda e:canvas.yview_scroll(-3,'units'),add='+'); canvas.bind_all('<Key-Down>',lambda e:canvas.yview_scroll(3,'units'),add='+')
        basics=tk.Frame(content,bg='white',highlightbackground='#e2e8f0',highlightthickness=1); basics.pack(fill='x',pady=8)
        tk.Label(basics,text='المعلومات الأساسية',bg='white',fg='#183b56',font=('Segoe UI',13,'bold')).pack(anchor='e',padx=18,pady=(10,4))
        grid=tk.Frame(basics,bg='white'); grid.pack(fill='x',padx=18,pady=(0,10)); basic_fields=[('المؤسسة','institution'),('الأكاديمية','academy'),('المديرية','directorate'),('الأستاذ','teacher'),('المستوى','level'),('السنة الدراسية','school_year'),('المدخل','entry'),('المجال','domain'),('الوحدة','unit'),('عنوان الدرس','lesson_title'),('عدد الحصص','sessions'),('مدة الحصة','period'),('التاريخ','date')]
        for n,(lab,key) in enumerate(basic_fields):
            cell=tk.Frame(grid,bg='white'); cell.grid(row=n//4,column=n%4,padx=6,pady=4,sticky='ew'); grid.columnconfigure(n%4,weight=1); tk.Label(cell,text=lab,bg='white',font=('Segoe UI',9,'bold')).pack(anchor='e'); e=tk.Entry(cell,justify='right',font=('Segoe UI',10)); e.insert(0,str(self.current.get(key,''))); e.pack(fill='x'); e.bind('<FocusOut>',lambda _,k=key,w=e:(self.current.__setitem__(k,w.get()),self.save_silent()))
        extended=tk.Frame(basics,bg='white'); extended.pack(fill='x',padx=18,pady=(0,10))
        for lab,key in [('الكفاية','competency'),('الأهداف','objectives'),('الموارد','resources'),('المراجع','references')]:
            cell=tk.Frame(extended,bg='white'); cell.pack(side='right',fill='x',expand=True,padx=6); tk.Label(cell,text=lab,bg='white',font=('Segoe UI',9,'bold')).pack(anchor='e'); e=tk.Text(cell,height=2,wrap='word',font=('Segoe UI',10)); value=self.current.get(key,[]); e.insert('1.0','\\n'.join(value) if isinstance(value,list) else str(value)); e.pack(fill='x'); e.bind('<FocusOut>',lambda _,k=key,w=e:(self.current.__setitem__(k,[x for x in w.get('1.0','end-1c').splitlines() if x.strip()] if k in ('objectives','resources','references') else w.get('1.0','end-1c')),self.save_silent()))
        body=tk.Frame(content,bg='#f5f7fb'); body.pack(fill='both',expand=True,pady=8); left=tk.Frame(body,bg='white',width=260,highlightbackground='#e2e8f0',highlightthickness=1); left.pack(side='right',fill='y',padx=(0,10)); left.pack_propagate(False); stage_area=tk.Frame(body,bg='white',highlightbackground='#e2e8f0',highlightthickness=1); stage_area.pack(side='left',fill='both',expand=True)
        tk.Label(left,text='مراحل الجذاذة',font=('Segoe UI',13,'bold'),bg='white',fg='#183b56').pack(anchor='e',padx=18,pady=16); self.stage_list=tk.Listbox(left,justify='right',font=('Segoe UI',11),relief='flat',activestyle='none',selectbackground='#dbeafe'); self.stage_list.pack(fill='both',expand=True,padx=10,pady=(0,8))
        for i,st in enumerate(self.current['stages']): self.stage_list.insert('end',f'{i+1}. {st["name"]}')
        order=tk.Frame(left,bg='white'); order.pack(fill='x',padx=10,pady=(0,12)); ttk.Button(order,text='↑ الأعلى',command=lambda:self.move_stage(-1)).pack(side='right',padx=2); ttk.Button(order,text='↓ الأسفل',command=lambda:self.move_stage(1)).pack(side='right',padx=2)
        self.stage_list.bind('<<ListboxSelect>>',lambda _:self.render_stage(stage_area)); self.stage_list.selection_set(self.current_stage); self.render_stage(stage_area)

    def move_stage(self,delta):
        if not self.current or not self.current.get('stages'): return
        i=self.current_stage; j=i+delta
        if j<0 or j>=len(self.current['stages']): return
        self.current['stages'][i],self.current['stages'][j]=self.current['stages'][j],self.current['stages'][i]; self.current_stage=j; self.current['updated_at']=now(); self.store.save(); self.show_editor()

    def field(self,parent,label,key,multi=False):
        f=tk.Frame(parent,bg='white'); f.pack(fill='x',padx=25,pady=7); tk.Label(f,text=label,bg='white',fg='#334155',font=('Segoe UI',10,'bold')).pack(anchor='e');
        if multi:
            w=tk.Text(f,height=4,wrap='word',font=('Segoe UI',11)); w.insert('1.0','\n'.join(self.current.get(key,[]) if isinstance(self.current.get(key),list) else [self.current.get(key,'')])); w.pack(fill='x',pady=4); return w
        w=tk.Entry(f,justify='right',font=('Segoe UI',11)); w.insert(0,str(self.current.get(key,''))); w.pack(fill='x',pady=4); return w
    def render_stage(self,parent):
        for w in parent.winfo_children(): w.destroy()
        sel=self.stage_list.curselection() if hasattr(self,'stage_list') else (); i=sel[0] if sel else self.current_stage; self.current_stage=i; s=self.current['stages'][i]
        tk.Label(parent,text=s['name'],font=('Segoe UI',17,'bold'),bg='white',fg='#183b56').pack(anchor='e',padx=25,pady=(20,3)); tk.Label(parent,text=s.get('purpose',''),bg='white',fg='#64748b').pack(anchor='e',padx=25,pady=(0,15))
        canvas=tk.Canvas(parent,bg='white',highlightthickness=0,bd=0); scroll=ttk.Scrollbar(parent,orient='vertical',command=canvas.yview); inner=tk.Frame(canvas,bg='white'); window_id=canvas.create_window((0,0),window=inner,anchor='nw'); inner.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox('all'))); canvas.bind('<Configure>',lambda e:canvas.itemconfigure(window_id,width=e.width)); canvas.configure(yscrollcommand=scroll.set); canvas.pack(side='left',fill='both',expand=True); scroll.pack(side='right',fill='y'); self._scroll_canvas=canvas; self._scroll_canvas.bind('<Enter>',lambda e:canvas.focus_set()); self._scroll_canvas.bind('<MouseWheel>',lambda e:canvas.yview_scroll(int(-e.delta/120),'units')); self._scroll_canvas.bind('<Button-4>',lambda e:canvas.yview_scroll(-3,'units')); self._scroll_canvas.bind('<Button-5>',lambda e:canvas.yview_scroll(3,'units')); self._scroll_canvas.bind('<Key-Up>',lambda e:canvas.yview_scroll(-3,'units')); self._scroll_canvas.bind('<Key-Down>',lambda e:canvas.yview_scroll(3,'units'))
        if s['kind']=='problem':
            w=self.stage_text(inner,'الوضعية المشكلة',s,'problem'); self.stage_text(inner,'دراسة الوضعية / التفاعل مع المتعلمين',s,'study_text'); self.items_editor(inner,s,'hypotheses','الفرضيات',self.hypothesis_item)
        elif s['kind']=='task':
            for lab,k in [('عنوان المهمة','title'),('الهدف','goal'),('المدة','duration'),('أنشطة الأستاذ','teacher'),('أنشطة المتعلم','learner'),('الخلاصة','summary')]: self.stage_text(inner,lab,s,k)
            self.items_editor(inner,s,'evidences','السندات',self.simple_item); self.items_editor(inner,s,'questions','الأسئلة والأجوبة المتوقعة',self.question_item)
        elif s['kind'] in ('diagnostic','formative','summative'):
            self.items_editor(inner,s,'questions','الأسئلة والأجوبة المتوقعة',self.question_item)
        elif s['kind']=='scrutiny': self.scrutiny_view(inner,s)
        elif s['kind']=='values': self.items_editor(inner,s,'values','القيم المستنبطة',self.value_item)
        elif s['kind']=='self_learning':
            for lab,k in [('المهمة','task'),('التعليمات','instructions'),('المنتوج المنتظر','product'),('الموارد','resources'),('الأجل','deadline')]: self.stage_text(inner,lab,s,k)
        else: self.items_editor(inner,s,'activities','الأنشطة',self.simple_item)
        ttk.Button(inner,text='حفظ تلقائي',command=self.save_current).pack(anchor='e',padx=25,pady=18)
    def stage_text(self,p,label,obj,key):
        f=tk.Frame(p,bg='white'); f.pack(fill='x',padx=25,pady=7); tk.Label(f,text=label,bg='white',font=('Segoe UI',10,'bold')).pack(anchor='e'); w=tk.Text(f,height=4,wrap='word',font=('Segoe UI',11)); w.insert('1.0',obj.get(key,'')); w.pack(fill='x',pady=3); w.bind('<FocusOut>',lambda e:self.set_stage_value(obj,key,w.get('1.0','end-1c'))); return w
    def set_stage_value(self,obj,key,val): obj[key]=val; self.current['updated_at']=now(); self.store.save()
    def items_editor(self,p,obj,key,title,item_fn):
        box=tk.Frame(p,bg='white'); box.pack(fill='x',padx=25,pady=10); tk.Label(box,text=title,bg='white',font=('Segoe UI',12,'bold'),fg='#183b56').pack(anchor='e'); holder=tk.Frame(box,bg='white'); holder.pack(fill='x');
        def redraw():
            for w in holder.winfo_children(): w.destroy()
            for idx,item in enumerate(obj.get(key,[])):
                item_fn(holder,obj,key,idx,item,redraw)
            ttk.Button(box,text='+ إضافة',command=lambda:(obj.setdefault(key,[]).append({}),redraw(),self.store.save())).pack(anchor='e',pady=6)
        redraw()
    def item_text(self,p,label,item,key,redraw,height=3):
        f=tk.Frame(p,bg='#f8fafc',highlightbackground='#e2e8f0',highlightthickness=1); f.pack(fill='x',pady=4); tk.Label(f,text=label,bg='#f8fafc',font=('Segoe UI',10,'bold')).pack(anchor='e',padx=10,pady=(7,0)); w=tk.Text(f,height=height,wrap='word',font=('Segoe UI',10)); w.insert('1.0',item.get(key,'')); w.pack(fill='x',padx=10,pady=5); w.bind('<FocusOut>',lambda e:(item.__setitem__(key,w.get('1.0','end-1c')),self.store.save())); ttk.Button(f,text='حذف',command=lambda:(p.winfo_children(),self._remove(p,item,redraw))).pack(anchor='e',padx=10,pady=(0,7))
    def _remove(self,p,item,redraw):
        for s in self.current['stages']:
            for k in ('questions','evidences','hypotheses','values','activities'):
                if item in s.get(k,[]): s[k].remove(item)
        redraw(); self.store.save()
    def simple_item(self,p,obj,key,idx,item,redraw): self.item_text(p,f'العنصر {idx+1}',item,'text',redraw)
    def question_item(self,p,obj,key,idx,item,redraw):
        self.item_text(p,f'السؤال {idx+1}',item,'question',redraw); self.item_text(p,'الإجابة المتوقعة',item,'expected',redraw)
    def hypothesis_item(self,p,obj,key,idx,item,redraw):
        for lab,k in [('الفرضية الأصلية','text'),('التعليل الأصلي','original_reason')]: self.item_text(p,lab,item,k,redraw)
    def value_item(self,p,obj,key,idx,item,redraw):
        for lab,k in [('اسم القيمة','name'),('الدليل','evidence'),('الشرح','explanation'),('مظاهرها السلوكية','behaviors')]: self.item_text(p,lab,item,k,redraw,2)
    def scrutiny_view(self,p,s):
        tk.Label(p,text='تظهر الفرضيات المسجلة في مرحلة تقديم الوضعية المشكلة تلقائياً.',bg='white',fg='#64748b').pack(anchor='e',padx=25,pady=8)
        source=next((x for x in self.current['stages'] if x['kind']=='problem'),{}); s['results']=s.get('results',[])
        while len(s['results'])<len(source.get('hypotheses',[])): s['results'].append({})
        for idx,h in enumerate(source.get('hypotheses',[])):
            r=s['results'][idx]; box=tk.Frame(p,bg='#f8fafc',highlightbackground='#cbd5e1',highlightthickness=1); box.pack(fill='x',padx=25,pady=7); tk.Label(box,text=f'الفرضية {idx+1}: {h.get("text","")}',bg='#f8fafc',font=('Segoe UI',11,'bold'),wraplength=700,justify='right').pack(anchor='e',padx=12,pady=8); tk.Label(box,text=f'التعليل الأصلي: {h.get("original_reason","")}',bg='#f8fafc',justify='right',wraplength=700).pack(anchor='e',padx=12,pady=3); ttk.Label(box,text='الحكم').pack(anchor='e',padx=12); v=tk.StringVar(value=r.get('judgment','')); ttk.Combobox(box,textvariable=v,values=['صحيحة','غير صحيحة','تحتاج إلى تعديل'],state='readonly',justify='right').pack(anchor='e',padx=12,pady=3); v.trace_add('write',lambda *_ ,rr=r,vv=v:(rr.__setitem__('judgment',vv.get()),self.store.save())); self.item_text(box,'الدليل',r,'evidence',lambda:None,2); self.item_text(box,'التعليل النهائي',r,'final_reason',lambda:None,3)
    def save_current(self):
        self.current['updated_at']=now(); old=self.store.lesson(self.current['id']);
        if old: self.store.data['lessons']=[self.current if x['id']==self.current['id'] else x for x in self.store.data['lessons']]
        else: self.store.data['lessons'].append(self.current)
        self.store.save(); messagebox.showinfo('تم الحفظ','تم حفظ الجذاذة محلياً بنجاح.')
    def show_preview(self):
        self.save_silent(); self.clear(); self.header('معاينة الجذاذة','معاينة جدولية قريبة من شكل الجذاذة النهائي'); meta=self.card(); tk.Label(meta,text=f"{self.current.get('lesson_title') or self.current.get('title','')}  |  {self.current.get('level','')}  |  {self.current.get('school_year','')}",bg='white',font=('Segoe UI',12,'bold'),fg='#183b56').pack(anchor='e',padx=18,pady=12)
        c=self.card(); cols=('stage','activities','abilities','aids','indicators'); table=ttk.Treeview(c,columns=cols,show='headings'); heads={'stage':'مراحل الدرس','activities':'الأنشطة الديداكتيكية التعلمية','abilities':'القدرات المستهدفة','aids':'المعينات الديداكتيكية','indicators':'مؤشرات التقويم'}
        for col in cols: table.heading(col,text=heads[col]); table.column(col,width=190 if col!='activities' else 430,anchor='e')
        for s in self.current.get('stages',[]):
            activities=[]
            for k in ('problem','study_text','title','goal','teacher','learner','summary','task','instructions'):
                if s.get(k): activities.append(str(s[k]))
            for k in ('questions','evidences','hypotheses','values'):
                for x in s.get(k,[]): activities.append(' | '.join(str(v) for v in x.values() if v))
            table.insert('', 'end', values=(s.get('name',''),'\n'.join(activities),', '.join(s.get('abilities',[])),'، '.join(s.get('aids',[])), '، '.join(s.get('indicators',[]))))
        table.pack(fill='both',expand=True,padx=10,pady=10); b=self.card(); ttk.Button(b,text='تصدير Word',command=lambda:self.export('docx')).pack(side='right',padx=5,pady=10); ttk.Button(b,text='طباعة',command=lambda:self.export('html',print_it=True)).pack(side='right',padx=5,pady=10); ttk.Button(b,text='العودة للمحرر',command=self.show_editor).pack(side='left',padx=5,pady=10)
    def save_silent(self):
        old=self.store.lesson(self.current['id']); self.current['updated_at']=now(); self.store.data['lessons']=[self.current if x['id']==self.current['id'] else x for x in self.store.data['lessons']] if old else self.store.data['lessons']+[self.current]; self.store.save()
    def export(self,kind,print_it=False):
        self.save_silent(); title=(self.current.get('lesson_title') or self.current.get('title') or 'جذاذة').replace('/','-')
        if kind=='docx':
            target=filedialog.asksaveasfilename(title='حفظ ملف Word',initialfile=f'جذاذة - {title}.docx',defaultextension='.docx',filetypes=[('ملف Word','*.docx')])
            if not target: return
            try:
                write_docx(Path(target),render_text(self.current),self.current)
                if messagebox.askyesno('تم التصدير','تم تصدير ملف Word بنجاح. هل تريد فتحه الآن؟'): os.startfile(target) if os.name=='nt' else webbrowser.open(Path(target).as_uri())
            except Exception as e: messagebox.showerror('تعذر تصدير Word',str(e))
        else:
            target=filedialog.asksaveasfilename(title='حفظ نسخة المعاينة',initialfile=f'جذاذة - {title}.html',defaultextension='.html',filetypes=[('صفحة معاينة','*.html')])
            if not target: return
            Path(target).write_text(html_doc(self.current),encoding='utf-8'); webbrowser.open(Path(target).as_uri())

    def show_templates(self):
        self.clear(); self.header('القوالب','إدارة المراحل الثابتة وقوالب الجذاذات'); c=self.card();
        for t in self.store.data['templates']:
            r=tk.Frame(c,bg='white'); r.pack(fill='x',padx=25,pady=8); tk.Label(r,text=t['name'],bg='white',font=('Segoe UI',12,'bold')).pack(side='right'); tk.Label(r,text=f'{len(t.get("stages",[]))} مرحلة',bg='white',fg='#64748b').pack(side='right',padx=20); ttk.Button(r,text='استخدام',command=lambda x=t['id']:self.use_template(x)).pack(side='left')
        ttk.Button(c,text='+ قالب جديد من القالب الأساسي',command=self.duplicate_template).pack(anchor='e',padx=25,pady=18)
    def use_template(self,tid): self.current=blank_lesson(tid); self.current['stages']=json.loads(json.dumps(self.store.template(tid)['stages'],ensure_ascii=False)); self.show_editor()
    def duplicate_template(self):
        t=json.loads(json.dumps(self.store.data['templates'][0],ensure_ascii=False)); t['id']=uid(); t['name']=t['name']+' – نسخة قابلة للتعديل'; self.store.data['templates'].append(t); self.store.save(); self.show_templates()
    def show_settings(self):
        self.clear(); self.header('الإعدادات','إعدادات محلية لا تحتاج إلى اتصال بالإنترنت'); c=self.card();
        self.setting_entry(c,'اسم الأستاذ','teacher'); self.setting_entry(c,'المؤسسة','institution'); ttk.Button(c,text='حفظ الإعدادات',command=lambda:(self.store.save(),messagebox.showinfo('تم الحفظ','تم حفظ الإعدادات.'))).pack(anchor='e',padx=25,pady=18)
        b=self.card(); ttk.Button(b,text='نسخ احتياطي',command=self.backup).pack(side='right',padx=8,pady=15); ttk.Button(b,text='استرجاع نسخة',command=self.restore).pack(side='right',padx=8,pady=15)
    def setting_entry(self,p,label,key):
        f=tk.Frame(p,bg='white'); f.pack(fill='x',padx=25,pady=8); tk.Label(f,text=label,bg='white').pack(anchor='e'); e=tk.Entry(f,justify='right',font=('Segoe UI',11)); e.insert(0,self.store.data['settings'].get(key,'')); e.pack(fill='x'); e.bind('<FocusOut>',lambda _:self.store.data['settings'].__setitem__(key,e.get()))
    def backup(self):
        f=filedialog.asksaveasfilename(defaultextension='.json',filetypes=[('نسخة بيانات','*.json')]);
        if f: Path(f).write_text(json.dumps(self.store.data,ensure_ascii=False,indent=2),encoding='utf-8'); messagebox.showinfo('تم','تم إنشاء النسخة الاحتياطية.')
    def restore(self):
        f=filedialog.askopenfilename(filetypes=[('نسخة بيانات','*.json')]);
        if f:
            try: self.store.data=json.loads(Path(f).read_text(encoding='utf-8')); self.store.save(); messagebox.showinfo('تم','تم الاسترجاع بنجاح.'); self.show_home()
            except Exception as e: messagebox.showerror('خطأ',str(e))
    def close(self):
        if self.current: self.save_silent()
        self.destroy()

def render_text(l):
    out=[APP_NAME,'='*70,f'عنوان الدرس: {l.get("lesson_title") or l.get("title","")}',f'المستوى: {l.get("level","")} | السنة الدراسية: {l.get("school_year","")}',f'المجال: {l.get("domain","")} | عدد الحصص: {l.get("sessions","")}',f'الأستاذ: {l.get("teacher","")} | المؤسسة: {l.get("institution","")}', '']
    for i,s in enumerate(l.get('stages',[]),1):
        out += [f'{i}. {s.get("name","")}',s.get('purpose','')]
        for k in ('problem','study_text','title','goal','teacher','learner','summary','task','instructions','product','resources','deadline'):
            if s.get(k): out += [f'{k}: {s[k]}']
        for k in ('questions','evidences','hypotheses','values','results'):
            for x in s.get(k,[]): out += [json.dumps(x,ensure_ascii=False)]
        out.append('')
    return '\n'.join(out)

def _lines(value):
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    return [x.strip() for x in str(value or '').splitlines() if x.strip()]


def stage_activity(l):
    normalize_lesson(l)
    rows=[]
    for s in l.get('stages',[]):
        parts=[]
        for k in ('problem','study_text','title','goal','teacher','learner','summary','task','instructions','product','resources','deadline'):
            if s.get(k): parts.append(str(s[k]))
        for k in ('questions','evidences','hypotheses','values','results','activities'):
            for x in s.get(k,[]):
                if isinstance(x, dict):
                    parts.append(' | '.join(str(v) for v in x.values() if v))
                elif x: parts.append(str(x))
        rows.append((s.get('name',''), '\n'.join(parts), '\n'.join(_lines(s.get('abilities'))), '\n'.join(_lines(s.get('aids'))), '\n'.join(_lines(s.get('indicators')))))
    return rows


def html_doc(l):
    import html
    normalize_lesson(l)
    title=html.escape(l.get('lesson_title') or l.get('title','جذاذة'))
    headers=['مراحل الدرس','الأنشطة الديداكتيكية التعلمية','القدرات المستهدفة','المعينات الديداكتيكية','مؤشرات التقويم']
    head=''.join('<th>'+html.escape(x)+'</th>' for x in headers)
    body=''.join('<tr>'+''.join('<td>'+html.escape(str(v)).replace('\\n','<br>')+'</td>' for v in row)+'</tr>' for row in stage_activity(l))
    meta=[('المؤسسة',l.get('institution','')),('الأكاديمية',l.get('academy','')),('المديرية',l.get('directorate','')),('الأستاذ',l.get('teacher','')),('المستوى',l.get('level','')),('السنة الدراسية',l.get('school_year','')),('المادة',l.get('subject','التربية الإسلامية')),('المدخل',l.get('entry','')),('المجال',l.get('domain','')),('الوحدة',l.get('unit','')),('عدد الحصص',l.get('sessions','')),('التاريخ',l.get('date',''))]
    meta_html=''.join('<div><b>'+html.escape(k)+'</b><span>'+html.escape(str(v or ''))+'</span></div>' for k,v in meta)
    return f'''<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8"><title>{title}</title><style>
@page{{size:A4 landscape;margin:8mm}}*{{box-sizing:border-box}}body{{font-family:"Tahoma","Arial",sans-serif;direction:rtl;color:#111;margin:0;font-size:9px;line-height:1.35}}h1{{text-align:center;margin:0 0 3mm;font-size:17px}}.meta{{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid #333;margin-bottom:3mm}}.meta div{{display:flex;border-left:1px solid #333;border-bottom:1px solid #333;min-height:7mm}}.meta div:nth-child(4n){{border-left:0}}.meta div:nth-last-child(-n+4){{border-bottom:0}}.meta b{{background:#eef1f3;padding:2mm 1.5mm;width:38%;font-weight:bold}}.meta span{{padding:2mm 1.5mm;flex:1}}table{{width:100%;border-collapse:collapse;table-layout:fixed;direction:rtl}}th,td{{border:1px solid #222;padding:2.2mm 1.7mm;vertical-align:top;white-space:pre-wrap;overflow-wrap:anywhere}}thead{{display:table-header-group}}tr{{page-break-inside:avoid}}th{{background:#e5eaee;text-align:center;font-weight:bold}}th:nth-child(1),td:nth-child(1){{width:13%}}th:nth-child(2),td:nth-child(2){{width:48%}}th:nth-child(3),td:nth-child(3){{width:14%}}th:nth-child(4),td:nth-child(4){{width:12%}}th:nth-child(5),td:nth-child(5){{width:13%}}</style><h1>جذاذة مادة التربية الإسلامية: {title}</h1><section class="meta">{meta_html}</section><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></html>'''


def _pdf_rtl(value):
    """Shape Arabic text for ReportLab while preserving readable mixed text."""
    from arabic_reshaper import reshape
    from bidi.algorithm import get_display
    return get_display(reshape(str(value or '')))


def write_pdf(path, lesson):
    """إنشاء PDF عربي RTL محلياً عبر ReportLab بلا GTK أو Pango أو WeasyPrint."""
    normalize_lesson(lesson)
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_RIGHT, TA_CENTER
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    except ImportError as exc:
        raise RuntimeError('محرك PDF غير مثبت داخل التطبيق.') from exc

    app_root = Path(__file__).resolve().parent
    font_regular = app_root / 'assets' / 'Amiri-Regular.ttf'
    font_bold = app_root / 'assets' / 'Amiri-Bold.ttf'
    if not font_regular.exists():
        raise RuntimeError('ملف الخط العربي المضمّن غير موجود داخل التطبيق.')
    pdfmetrics.registerFont(TTFont('Amiri', str(font_regular)))
    if font_bold.exists():
        pdfmetrics.registerFont(TTFont('Amiri-Bold', str(font_bold)))
    bold_font = 'Amiri-Bold' if font_bold.exists() else 'Amiri'

    page = landscape(A4)
    doc = SimpleDocTemplate(str(path), pagesize=page, rightMargin=8*mm, leftMargin=8*mm, topMargin=8*mm, bottomMargin=8*mm, title=str(lesson.get('lesson_title') or lesson.get('title') or 'جذاذة'))
    normal = ParagraphStyle('ArabicNormal', fontName='Amiri', fontSize=8.2, leading=11, alignment=TA_RIGHT, wordWrap='CJK', spaceAfter=0)
    small = ParagraphStyle('ArabicSmall', parent=normal, fontSize=7.4, leading=9.5)
    head = ParagraphStyle('ArabicHead', parent=normal, fontName=bold_font, fontSize=8.3, leading=10.5, alignment=TA_CENTER)
    title_style = ParagraphStyle('ArabicTitle', parent=normal, fontName=bold_font, fontSize=14, leading=18, alignment=TA_CENTER)

    def P(value, style=normal):
        return Paragraph(_pdf_rtl(value).replace('\n', '<br/>'), style)

    title = lesson.get('lesson_title') or lesson.get('title') or 'جذاذة'
    story = [P(f'جذاذة مادة التربية الإسلامية: {title}', title_style), Spacer(1, 2*mm)]
    meta = [('المؤسسة', lesson.get('institution','')), ('الأكاديمية', lesson.get('academy','')), ('المديرية', lesson.get('directorate','')), ('الأستاذ', lesson.get('teacher','')), ('المستوى', lesson.get('level','')), ('السنة الدراسية', lesson.get('school_year','')), ('المادة', lesson.get('subject','التربية الإسلامية')), ('المدخل', lesson.get('entry','')), ('المجال', lesson.get('domain','')), ('الوحدة', lesson.get('unit','')), ('عدد الحصص', lesson.get('sessions','')), ('التاريخ', lesson.get('date',''))]
    meta_rows = []
    for i in range(0, len(meta), 4):
        row = []
        for label, value in meta[i:i+4]:
            row.extend([P(label, head), P(value, small)])
        meta_rows.append(row)
    meta_widths = []
    for _ in range(4): meta_widths.extend([24*mm, 38*mm])
    meta_table = Table(meta_rows, colWidths=meta_widths, repeatRows=0, hAlign='RIGHT')
    meta_table.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#333333')),('BACKGROUND',(0,0),(-1,-1),colors.white),('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#f5f7f9')),('VALIGN',(0,0),(-1,-1),'TOP'),('RIGHTPADDING',(0,0),(-1,-1),3),('LEFTPADDING',(0,0),(-1,-1),3),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
    story += [meta_table, Spacer(1, 3*mm)]

    headers = ['مراحل الدرس','الأنشطة الديداكتيكية التعلمية','القدرات المستهدفة','المعينات الديداكتيكية','مؤشرات التقويم']
    rows = [headers] + [[str(v) for v in row] for row in stage_activity(lesson)]
    rows = [[P(v, head) if r == 0 else P(v) for v in reversed(row)] for r, row in enumerate(rows)]
    table = Table(rows, colWidths=[25*mm, 24*mm, 29*mm, 96*mm, 84*mm], repeatRows=1, splitByRow=1, splitInRow=1, hAlign='RIGHT')
    table.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.65,colors.HexColor('#222222')),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5eaee')),('VALIGN',(0,0),(-1,-1),'TOP'),('ALIGN',(0,0),(-1,0),'CENTER'),('RIGHTPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LINEBELOW',(0,0),(-1,0),1,colors.HexColor('#222222'))]))
    story.append(table)
    doc.build(story)


def _wtext(text):
    import html
    return html.escape(str(text or '')).replace('\n', '<w:br/>')


def write_docx(path,text,lesson=None):
    import html
    if lesson is None:
        content=''.join(f'<w:p><w:pPr><w:bidi/></w:pPr><w:r><w:t xml:space="preserve">{_wtext(line)}</w:t></w:r></w:p>' for line in text.splitlines())
    else:
        normalize_lesson(lesson)
        rows=stage_activity(lesson)
        def tc(value, width, header=False):
            shade='<w:shd w:fill="E5EAEE"/>' if header else ''
            return f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/><w:vAlign w:val="top"/></w:tcPr><w:p><w:pPr><w:bidi/><w:jc w:val="right"/></w:pPr><w:r>{shade}<w:t xml:space="preserve">{_wtext(value)}</w:t></w:r></w:p></w:tc>'
        widths=[1900,7000,2050,1750,1900]
        headers=['مراحل الدرس','الأنشطة الديداكتيكية التعلمية','القدرات المستهدفة','المعينات الديداكتيكية','مؤشرات التقويم']
        header='<w:tr><w:trPr><w:tblHeader/></w:trPr>'+''.join(tc(h,w,True) for h,w in zip(headers,widths))+'</w:tr>'
        table_rows=[header]+['<w:tr>'+''.join(tc(v,w) for v,w in zip(row,widths))+'</w:tr>' for row in rows]
        title=lesson.get('lesson_title') or lesson.get('title','جذاذة')
        meta=f'المؤسسة: {lesson.get("institution","")} | الأستاذ: {lesson.get("teacher","")} | المستوى: {lesson.get("level","")} | السنة الدراسية: {lesson.get("school_year","")} | المجال: {lesson.get("domain","")} | الوحدة: {lesson.get("unit","")}'
        table='<w:tbl><w:tblPr><w:tblW w:w="14600" w:type="dxa"/><w:tblLayout w:type="fixed"/><w:bidiVisual/><w:tblBorders><w:top w:val="single" w:sz="8"/><w:left w:val="single" w:sz="8"/><w:bottom w:val="single" w:sz="8"/><w:right w:val="single" w:sz="8"/><w:insideH w:val="single" w:sz="6"/><w:insideV w:val="single" w:sz="6"/></w:tblBorders></w:tblPr>'+''.join(table_rows)+'</w:tbl>'
        content=f'<w:p><w:pPr><w:bidi/><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="28"/></w:rPr><w:t>{_wtext("جذاذة مادة التربية الإسلامية: "+title)}</w:t></w:r></w:p><w:p><w:pPr><w:bidi/><w:jc w:val="right"/></w:pPr><w:r><w:t>{_wtext(meta)}</w:t></w:r></w:p>'+table
    files={'[Content_Types].xml':'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>','_rels/.rels':'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>','word/document.xml':f'<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>{content}<w:sectPr><w:pgSz w:w="16838" w:h="11906"/><w:pgMar w:top="510" w:right="510" w:bottom="510" w:left="510"/></w:sectPr></w:body></w:document>'}
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for n,c in files.items(): z.writestr(n,c)

if __name__=='__main__': App().mainloop()
