# -*- coding: utf-8 -*-
"""واجهة HTML محلية لتطبيق مولّد الجذاذة، تعمل داخل EXE دون إنترنت."""
import json, os, shutil, sys, webbrowser
from pathlib import Path
import webview
from tkinter import Tk, filedialog
from main import Store, blank_lesson, uid, now, html_doc, write_docx, normalize_lesson

BASE = Path(__file__).parent
WEB = BASE / 'web'

class Api:
    def __init__(self):
        self.store = Store()

    def state(self):
        for lesson in self.store.data.get('lessons', []): normalize_lesson(lesson)
        return self.store.data

    def save_lesson(self, lesson):
        lesson = normalize_lesson(json.loads(json.dumps(lesson, ensure_ascii=False)))
        lesson['updated_at'] = now()
        old = self.store.lesson(lesson['id'])
        if old:
            self.store.data['lessons'] = [lesson if x['id'] == lesson['id'] else x for x in self.store.data['lessons']]
        else:
            self.store.data['lessons'].append(lesson)
        self.store.save()
        return {'ok': True, 'lesson': lesson}

    def new_lesson(self):
        return blank_lesson()

    def delete_lesson(self, lid):
        self.store.data['lessons'] = [x for x in self.store.data['lessons'] if x['id'] != lid]
        self.store.save()
        return {'ok': True}

    def copy_lesson(self, lid):
        item = self.store.lesson(lid)
        if not item: return {'ok': False}
        copied = json.loads(json.dumps(item, ensure_ascii=False))
        copied['id'] = uid(); copied['title'] = (copied.get('lesson_title') or copied.get('title','جذاذة')) + ' – نسخة'; copied['updated_at'] = now()
        self.store.data['lessons'].append(copied); self.store.save()
        return {'ok': True, 'lesson': copied}

    def export(self, kind, lesson):
        lesson = normalize_lesson(json.loads(json.dumps(lesson, ensure_ascii=False)))
        root = Tk(); root.withdraw(); root.attributes('-topmost', True)
        title = (lesson.get('lesson_title') or lesson.get('title') or 'جذاذة').replace('/', '-')
        if kind == 'docx':
            target = filedialog.asksaveasfilename(title='حفظ ملف Word', initialfile=f'جذاذة - {title}.docx', defaultextension='.docx', filetypes=[('ملف Word','*.docx')])
        else:
            target = filedialog.asksaveasfilename(title='حفظ المعاينة', initialfile=f'جذاذة - {title}.html', defaultextension='.html', filetypes=[('صفحة HTML','*.html')])
        root.destroy()
        if not target: return {'ok': False, 'cancelled': True}
        try:
            if kind == 'docx':
                write_docx(Path(target), '', lesson)
            else:
                Path(target).write_text(html_doc(lesson), encoding='utf-8')
            return {'ok': True, 'path': target}
        except Exception as exc:
            return {'ok': False, 'error': str(exc)}

    def backup(self):
        root = Tk(); root.withdraw(); root.attributes('-topmost', True)
        target = filedialog.asksaveasfilename(title='حفظ النسخة الاحتياطية', initialfile='نسخة احتياطية للجذاذات.json', defaultextension='.json', filetypes=[('بيانات JSON','*.json')])
        root.destroy()
        if not target: return {'ok': False, 'cancelled': True}
        Path(target).write_text(json.dumps(self.store.data, ensure_ascii=False, indent=2), encoding='utf-8')
        return {'ok': True, 'path': target}

    def restore(self):
        root = Tk(); root.withdraw(); root.attributes('-topmost', True)
        source = filedialog.askopenfilename(title='استرجاع نسخة احتياطية', filetypes=[('بيانات JSON','*.json')])
        root.destroy()
        if not source: return {'ok': False, 'cancelled': True}
        self.store.data = json.loads(Path(source).read_text(encoding='utf-8'))
        for lesson in self.store.data.get('lessons', []): normalize_lesson(lesson)
        self.store.save()
        return {'ok': True, 'state': self.store.data}

if __name__ == '__main__':
    api = Api()
    webview.create_window('مولّد الجذاذة – التربية الإسلامية', str(WEB / 'index.html'), js_api=api, width=1380, height=900, min_size=(1100, 700), text_select=True)
    webview.start(debug=False)
