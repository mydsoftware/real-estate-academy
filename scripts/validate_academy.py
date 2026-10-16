import re
from pathlib import Path

source = Path("src/main.jsx").read_text(encoding="utf-8")
styles = Path("src/styles.css").read_text(encoding="utf-8")

modules_start = source.index("const modules = [")
details_start = source.index("const lessonDetails = {")
modules_text = source[modules_start:details_start]
details_end = source.index("\n};\n\nconst allLessons", details_start)
details_text = source[details_start:details_end]

lesson_titles = re.findall(r"^\s*\['([^']+)','[^']*'\],?$", modules_text, re.MULTILINE)
detail_keys = re.findall(r"""^  .([^'"]+).:\s*\{$""", details_text, re.MULTILINE)

errors = []
if len(lesson_titles) != 50:
    errors.append(f"Expected 50 lessons, found {len(lesson_titles)}")
if len(set(lesson_titles)) != len(lesson_titles):
    errors.append("Duplicate lesson titles found in modules")
if len(detail_keys) != 50:
    errors.append(f"Expected 50 lesson detail entries, found {len(detail_keys)}")
if len(set(detail_keys)) != len(detail_keys):
    duplicates = sorted({title for title in detail_keys if detail_keys.count(title) > 1})
    errors.append("Duplicate lesson detail entries: " + ", ".join(duplicates))
missing = sorted(set(lesson_titles) - set(detail_keys))
extra = sorted(set(detail_keys) - set(lesson_titles))
if missing:
    errors.append("Lessons without detailed content: " + ", ".join(missing))
if extra:
    errors.append("Detail entries without lessons: " + ", ".join(extra))
if "function QuizPanel" not in source or "make(10," not in source:
    errors.append("Ten-question lesson quiz implementation is missing or incomplete")
if ".quizOptions{display:flex!important;flex-direction:column!important;" not in styles:
    errors.append("Quiz answer choices are not configured as a vertical list")
if "localStorage.setItem(storageKey" not in source:
    errors.append("Quiz score persistence is missing")

if errors:
    print("ACADEMY VALIDATION FAILED")
    for error in errors:
        print(" - " + error)
    raise SystemExit(1)

print(f"ACADEMY VALIDATION PASSED: {len(lesson_titles)} lessons, {len(detail_keys)} unique lesson guides, 10-question quiz, vertical answers, saved scores.")
