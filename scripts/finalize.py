from pathlib import Path

main = Path('src/main.jsx')
css = Path('src/styles.css')
s = main.read_text(encoding='utf-8')

if 'FINAL_ACADEMY_QUIZ_V1' not in s:
    marker = 'function App(){'
    component = r'''/* FINAL_ACADEMY_QUIZ_V1 */
function QuizPanel({ lessonTitle, detail }) {
  const storageKey = `reAcademyQuiz:${lessonTitle}`;
  const [answers, setAnswers] = React.useState({});
  const [submitted, setSubmitted] = React.useState(false);
  const [score, setScore] = React.useState(null);
  const questions = React.useMemo(() => {
    if (!detail) return [];
    const steps = detail.steps || [];
    const checklist = detail.checklist || [];
    const mistakes = detail.mistakes || [];
    const qs = [];
    const pool = steps.length ? steps : [['اصل درس', detail.goal || 'هدف اصلی درس را در عمل رعایت کن.']];
    const make = (id, q, correct, distractors, explanation) => {
      const opts = [correct, ...distractors].filter((x,i,a)=>x && a.indexOf(x)===i).slice(0,4);
      while (opts.length < 4) opts.push('این گزینه در محتوای درس به‌عنوان رویکرد اصلی معرفی نشده است.');
      const shift = (id * 3) % 4;
      const rotated = opts.slice(shift).concat(opts.slice(0,shift));
      return {id, q, o:rotated, c:rotated.indexOf(correct), explanation};
    };
    for (let i=0;i<Math.min(6,pool.length);i++) {
      const step=pool[i];
      qs.push(make(i+1,`در درس «${lessonTitle}»، در بخش «${step[0]}» کدام اقدام درست‌تر است؟`,step[1],pool.filter((_,j)=>j!==i).map(x=>x[1]),step[1]));
    }
    while(qs.length<6){const i=qs.length%pool.length,step=pool[i];qs.push(make(qs.length+1,`کدام گزینه با روش حرفه‌ای مطرح‌شده در درس «${lessonTitle}» هماهنگ‌تر است؟`,step[1],pool.filter((_,j)=>j!==i).map(x=>x[1]),step[1]));}
    const good=checklist[0]||pool[0][1], bad=mistakes[0]||'نتیجه‌گیری بدون بررسی کافی', c2=checklist[1]||good;
    qs.push(make(7,`کدام مورد باید در اجرای «${lessonTitle}» کنترل شود؟`,good,[bad,'نادیده گرفتن ابهام‌های مهم','دادن وعده قطعی بدون داده'],good));
    qs.push(make(8,`کدام رفتار در «${lessonTitle}» یک اشتباه رایج محسوب می‌شود؟`,bad,[good,'ثبت دقیق اطلاعات','ارجاع موضوع تخصصی به متخصص'],bad));
    qs.push(make(9,`برای اجرای حرفه‌ای درس «${lessonTitle}» کدام گزینه مناسب‌تر است؟`,c2,[bad,'پنهان کردن ایرادها','استفاده از اطلاعات حدسی'],c2));
    qs.push(make(10,`اگر در اجرای «${lessonTitle}» با ابهام مهمی روبه‌رو شدی، بهترین رویکرد چیست؟`,'ابهام را ثبت کن و پیش از تصمیم قطعی، بررسی لازم را انجام بده.',['آن را نادیده بگیر تا معامله سریع‌تر پیش برود.','برای اطمینان مشتری، پاسخ قطعی بدون بررسی بده.','اطلاعات را حدس بزن و بعداً اصلاح کن.'],'ابهام مهم باید ثبت و بررسی شود؛ سرعت نباید جای دقت را بگیرد.'));
    return qs;
  },[lessonTitle,detail]);
  React.useEffect(()=>{try{const x=JSON.parse(localStorage.getItem(storageKey)||'null');if(x&&typeof x.score==='number')setScore(x.score)}catch{}},[storageKey]);
  const submit=()=>{if(Object.keys(answers).length!==10)return;const n=questions.reduce((a,q)=>a+(answers[q.id]===q.c?1:0),0),r=n*10;setScore(r);setSubmitted(true);try{localStorage.setItem(storageKey,JSON.stringify({score:r,answers,date:new Date().toISOString()}))}catch{}};
  return <section className="quizPanel"><div className="quizHeader"><div><span className="quizEyebrow">آزمون درس</span><h3>آزمون ۱۰ سؤالی «{lessonTitle}»</h3></div>{score!==null&&<strong className="quizScore">آخرین نمره: {score}%</strong>}</div><p className="quizHint">۱۰ سؤال از محتوای همین درس. حداقل نمره پیشنهادی قبولی ۷۰٪ است.</p><div className="quizQuestions">{questions.map((q,i)=><div className="quizQuestion" key={q.id}><b>{i+1}. {q.q}</b><div className="quizOptions">{q.o.map((o,j)=><label key={j} className={submitted?(j===q.c?'quizCorrect':answers[q.id]===j?'quizWrong':''):''}><input type="radio" name={`${storageKey}-${q.id}`} checked={answers[q.id]===j} disabled={submitted} onChange={()=>setAnswers(a=>({...a,[q.id]:j}))}/><span>{o}</span></label>)}</div>{submitted&&<div className="quizFeedback">{answers[q.id]===q.c?'✓ پاسخ درست':'✗ پاسخ صحیح: '+q.o[q.c]} — {q.explanation}</div>}</div>)}</div>{!submitted?<button className="quizSubmit" disabled={Object.keys(answers).length!==10} onClick={submit}>ثبت آزمون و مشاهده نتیجه</button>:<div className="quizResult"><strong>{score>=70?'قبول شدی':'نیاز به مرور دوباره داری'}</strong><span>نمره: {score}%</span><button onClick={()=>{setAnswers({});setSubmitted(false)}}>آزمون مجدد</button></div>}</section>;
}

'''
    if marker not in s: raise SystemExit('App marker not found')
    s=s.replace(marker,component+marker,1)
    hook="{open.key&&<button className=\"complete\" onClick={()=>toggle(open.key)}>{done.includes(open.key)?'✓ درس تکمیل شده':'علامت‌گذاری به‌عنوان تکمیل‌شده'}</button>}"
    quiz="{open.key&&lessonDetails[open.title]&&<QuizPanel lessonTitle={open.title} detail={lessonDetails[open.title]}/> }"
    if hook not in s: raise SystemExit('completion marker not found')
    s=s.replace(hook,quiz+hook,1)

if 'FINAL_ACADEMY_EXTRAS_V1' not in s:
    marker='function App(){'
    component=r'''/* FINAL_ACADEMY_EXTRAS_V1 */
function AcademyExtras(){
  const [done,setDone]=React.useState(()=>{try{return JSON.parse(localStorage.getItem('reAcademyDone')||'[]')}catch{return []}});
  const [exam,setExam]=React.useState(null),[answers,setAnswers]=React.useState({}),[submitted,setSubmitted]=React.useState(false),[scenario,setScenario]=React.useState(0);
  const moduleLessons=m=>m.lessons.map((l,i)=>({title:l[0],text:l[1],key:`${m.id}-${i}`}));
  const makeExam=(title,lessons,final=false)=>{const pool=lessons.flatMap(l=>[{q:`کدام گزینه به‌طور مستقیم با «${l.title}» مرتبط است؟`,a:l.text},{q:`در اجرای حرفه‌ای درس «${l.title}» کدام اصل باید رعایت شود؟`,a:l.text}]);const qs=[];for(let i=0;i<(final?20:10);i++){const item=pool[i%pool.length],others=pool.filter((_,j)=>j!==i).slice(0,3).map(x=>x.a),opts=[item.a,...others],shift=(i*2)%4,ro=opts.slice(shift).concat(opts.slice(0,shift));qs.push({q:item.q,o:ro,c:ro.indexOf(item.a)})}return{title,qs}};
  const start=(title,lessons,final=false)=>{setExam(makeExam(title,lessons,final));setAnswers({});setSubmitted(false)};
  const score=exam?Math.round(exam.qs.reduce((n,q,i)=>n+(answers[i]===q.c?1:0),0)/exam.qs.length*100):0;
  const reset=()=>{if(window.confirm('پیشرفت و نمرات محلی پاک شوند؟')){localStorage.removeItem('reAcademyDone');Object.keys(localStorage).filter(k=>k.startsWith('reAcademyQuiz:')).forEach(k=>localStorage.removeItem(k));setDone([])}};
  const scenarios=[['مالک می‌گوید: «قیمت من قطعی است.»','مبنای قیمت، شرایط و نمونه‌های قابل مقایسه را بررسی و مستند کن.'],['خریدار فقط می‌گوید: «ارزان‌ترین را می‌خواهم.»','نیازسنجی کن و بودجه، محدوده و معیارهای حذف‌کننده را مشخص کن.'],['در بازدید ترک و نم مشکوک می‌بینی.','مشاهده را دقیق ثبت و برای علت فنی، بررسی متخصص را پیشنهاد کن؛ تشخیص قطعی نده.'],['نماینده آمده اما حدود اختیارش روشن نیست.','پیش از تعهد جدی، هویت، سمت و حدود اختیار را از مسیر معتبر بررسی کن.']];
  return <section className="academyExtras"><div className="extraHead"><div><span className="eyebrow">مرکز ارزیابی</span><h2>داشبورد و آزمون‌های آکادمی</h2><p>پیشرفت، آزمون‌های ماژولی، آزمون نهایی و تمرین سناریویی.</p></div><button onClick={reset}>بازنشانی پیشرفت</button></div><div className="extraStats"><div><b>{done.length}</b><span>درس تکمیل‌شده</span></div><div><b>{allLessons.length}</b><span>درس کل</span></div><div><b>{Math.round(done.length/allLessons.length*100)}%</b><span>پیشرفت</span></div><div><b>{modules.length}</b><span>ماژول</span></div></div><div className="examGrid">{modules.map(m=><article className="examCard" key={m.id}><span>{m.title}</span><strong>{m.lessons.length} درس</strong><button onClick={()=>start(`آزمون ماژول: ${m.title}`,moduleLessons(m))}>آزمون ۱۰ سؤالی</button></article>)}<article className="examCard finalExam"><span>آزمون نهایی آکادمی</span><strong>۲۰ سؤال ترکیبی</strong><button onClick={()=>start('آزمون نهایی آکادمی',allLessons,true)}>شروع آزمون نهایی</button></article></div><div className="scenarioCard"><div><span className="quizEyebrow">شبیه‌ساز تصمیم‌گیری</span><h3>اگر جای مشاور بودی چه می‌کردی؟</h3><p>{scenarios[scenario][0]}</p></div><div className="scenarioAnswer"><button onClick={()=>setScenario((scenario+1)%scenarios.length)}>نمایش رویکرد حرفه‌ای</button><p>{scenarios[scenario][1]}</p></div></div>{exam&&<div className="examOverlay"><div className="examModal"><button className="close" onClick={()=>setExam(null)}>×</button><span className="eyebrow">{exam.title}</span><h2>{exam.title}</h2><p>برای ثبت نتیجه، به همه سؤال‌ها پاسخ بده.</p>{exam.qs.map((q,i)=><div className="finalQuestion" key={i}><b>{i+1}. {q.q}</b>{q.o.map((o,j)=><label key={j} className={submitted?(j===q.c?'quizCorrect':answers[i]===j?'quizWrong':''):''}><input type="radio" name={`final-${i}`} disabled={submitted} checked={answers[i]===j} onChange={()=>setAnswers(a=>({...a,[i]:j}))}/><span>{o}</span></label>)}{submitted&&<small>{answers[i]===q.c?'✓ درست':'✗ پاسخ صحیح: '+q.o[q.c]}</small>}</div>)}{!submitted?<button className="quizSubmit" disabled={Object.keys(answers).length!==exam.qs.length} onClick={()=>setSubmitted(true)}>ثبت آزمون</button>:<div className="quizResult"><strong>نمره: {score}%</strong><span>{score>=70?'قبول شدی':'نیاز به مرور دوباره داری'}</span><button onClick={()=>{setAnswers({});setSubmitted(false)}}>آزمون مجدد</button></div>}</div></div>}</section>;
}

'''
    s=s.replace(marker,component+marker,1)
    s=s.replace('<section className="field">','<AcademyExtras/>\n        <section className="field">',1)

main.write_text(s,encoding='utf-8')

extra_css='''\n/* FINAL_ACADEMY_V1 */\n.quizPanel{margin-top:22px;border:1px solid #dfe6df;border-radius:16px;background:#f8faf7;padding:18px}.quizHeader{display:flex;justify-content:space-between;gap:15px;align-items:flex-start}.quizEyebrow{font-size:9px;color:#9a742e;font-weight:800}.quizHeader h3{margin:5px 0 0;font-size:16px;color:#173f36}.quizScore{font-size:11px;background:#edf4f0;color:#173f36;padding:7px 10px;border-radius:9px;white-space:nowrap}.quizHint{font-size:10px;line-height:1.8;color:#707a74;margin:10px 0 15px}.quizQuestions{display:grid;gap:12px}.quizQuestion{background:#fff;border:1px solid #e5eae4;border-radius:12px;padding:13px}.quizQuestion>b{display:block;font-size:11px;line-height:1.9;color:#28352f}.quizOptions{display:grid;gap:7px;margin-top:10px}.quizOptions label,.finalQuestion label{display:flex;gap:8px;align-items:flex-start;padding:8px 9px;border:1px solid #e6eae5;border-radius:9px;font-size:10px;line-height:1.8;color:#56615b;cursor:pointer}.quizOptions input,.finalQuestion input{margin-top:4px;accent-color:#173f36}.quizOptions .quizCorrect,.finalQuestion .quizCorrect{border-color:#8ebaa4;background:#eef7f1}.quizOptions .quizWrong,.finalQuestion .quizWrong{border-color:#d9a6a6;background:#fff3f3}.quizFeedback{margin-top:9px;padding:8px 10px;border-radius:8px;background:#f2f5f1;font-size:10px;line-height:1.9;color:#59635d}.quizSubmit{margin-top:14px;background:#143f36;color:#fff;border-radius:10px;padding:11px 16px;font-size:11px}.quizSubmit:disabled{opacity:.45;cursor:not-allowed}.quizResult{display:flex;align-items:center;gap:12px;margin-top:14px;padding:12px;background:#edf4f0;border-radius:10px;font-size:11px;color:#173f36}.quizResult button{margin-right:auto;background:#fff;color:#173f36;border:1px solid #cddbd3;border-radius:8px;padding:7px 11px;font-size:10px}.academyExtras{margin-top:28px}.extraHead{display:flex;justify-content:space-between;align-items:center;gap:20px;margin-bottom:15px}.extraHead h2{margin:6px 0;font-size:21px;color:#173f36}.extraHead p{margin:0;font-size:11px;color:#707a74}.extraHead button{background:#fff;border:1px solid #d9dfda;border-radius:9px;padding:9px 12px;font-size:10px;color:#6a4f25}.extraStats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:15px}.extraStats div{background:#fff;border:1px solid #e2e7e1;border-radius:13px;padding:14px}.extraStats b{display:block;font-size:20px;color:#173f36}.extraStats span{font-size:9px;color:#7c8580}.examGrid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.examCard{background:#fff;border:1px solid #e2e7e1;border-radius:13px;padding:14px;display:grid;gap:8px}.examCard span{font-size:11px;color:#36443d;line-height:1.8}.examCard strong{font-size:9px;color:#8b948f}.examCard button,.scenarioCard button{background:#143f36;color:#fff;border-radius:9px;padding:9px 11px;font-size:10px}.finalExam{border-color:#cdb77e;background:#fcfaf3}.scenarioCard{margin-top:15px;background:#143f36;color:#fff;border-radius:16px;padding:18px;display:grid;grid-template-columns:1fr 1fr;gap:18px}.scenarioCard h3{margin:7px 0;font-size:16px}.scenarioCard p{font-size:11px;line-height:1.9;color:#d5e0da}.scenarioAnswer{background:#ffffff12;border:1px solid #ffffff18;border-radius:11px;padding:13px}.examOverlay{position:fixed;inset:0;background:#0e211dcc;z-index:60;padding:18px;overflow:auto}.examModal{background:#fff;width:min(760px,100%);margin:0 auto;border-radius:18px;padding:25px;position:relative}.examModal h2{margin:7px 0}.finalQuestion{padding:13px 0;border-bottom:1px solid #e8ece7}.finalQuestion>b{display:block;font-size:11px;line-height:1.9}.finalQuestion small{display:block;margin-top:7px;color:#68736c;font-size:9px;line-height:1.8}@media(max-width:760px){.quizHeader,.extraHead{display:block}.quizScore{display:inline-block;margin-top:10px}.extraHead button{margin-top:10px}.extraStats{grid-template-columns:repeat(2,1fr)}.examGrid{grid-template-columns:1fr}.scenarioCard{grid-template-columns:1fr}.examModal{padding:18px}.quizResult{flex-wrap:wrap}.quizResult button{margin-right:0;width:100%}}\n'''
if 'FINAL_ACADEMY_V1' not in css.read_text(encoding='utf-8'):
    css.write_text(css.read_text(encoding='utf-8')+extra_css,encoding='utf-8')
