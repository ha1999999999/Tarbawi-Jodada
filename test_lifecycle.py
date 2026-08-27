# -*- coding: utf-8 -*-
import json, tempfile, shutil
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / 'app'))
import main

def run():
    with tempfile.TemporaryDirectory() as d:
        root=Path(d); main.DATA_DIR=root; main.DATA_FILE=root/'data.json'; main.EXPORT_DIR=root/'exports'
        store=main.Store(); lesson=main.blank_lesson(); lesson['lesson_title']='درس اختبار حقيقي'; lesson['level']='الأولى باكالوريا'; lesson['stages'][1]['problem']='وضعية مشكلة'; lesson['stages'][1]['hypotheses']=[{'text':'فرضية 1','original_reason':'تعليل 1'},{'text':'فرضية 2','original_reason':'تعليل 2'},{'text':'فرضية 3','original_reason':'تعليل 3'}]; lesson['stages'][2]['title']='المهمة الأولى'; lesson['stages'][2]['questions']=[{'question':'سؤال','answer':'جواب'}]; lesson['stages'][5]['title']='المهمة الثانية'; lesson['stages'][7]['hypotheses']=lesson['stages'][1]['hypotheses']; lesson['stages'][7]['judgements']=[{'judgement':'صحيحة','evidence':'دليل','final_reason':'تعليل نهائي'} for _ in range(3)]; lesson['stages'][8]['values']=[{'name':'الأمانة','evidence':'دليل','explanation':'شرح','behaviors':'تطبيق'}]; store.data['lessons'].append(lesson); store.save()
        reopened=main.Store(); assert reopened.lesson(lesson['id'])['lesson_title']=='درس اختبار حقيقي'; assert len(reopened.lesson(lesson['id'])['stages'][7]['hypotheses'])==3
        copied=json.loads(json.dumps(lesson,ensure_ascii=False)); copied['id']=main.uid(); copied['lesson_title']='نسخة درس اختبار'; reopened.data['lessons'].append(copied); reopened.save(); assert len(reopened.data['lessons'])==2
        reopened.data['lessons']=[x for x in reopened.data['lessons'] if x['id']!=lesson['id']]; reopened.save(); assert reopened.lesson(lesson['id']) is None
        backup=root/'backup.json'; backup.write_text(json.dumps(reopened.data,ensure_ascii=False),encoding='utf-8'); valid=json.loads(backup.read_text(encoding='utf-8')); assert 'lessons' in valid and 'templates' in valid and 'settings' in valid
    print('PASS full_lifecycle_data')

if __name__=='__main__': run(); print('ALL LIFECYCLE TESTS PASSED')
