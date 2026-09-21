# Changelog Maker

A small, deterministic CLI that turns Git history into a clean Markdown changelog. It understands Conventional Commits, groups changes by purpose, highlights breaking changes, and can link entries to GitHub commits.

## English

### Why it exists
Release notes are easy to postpone and hard to reconstruct. Changelog Maker generates a useful draft directly from commit history without sending repository data to a service or requiring an API key.

### Features
- Parses `type(scope)!: subject` Conventional Commit messages.
- Groups `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`, and `revert` commits.
- Highlights breaking changes and optionally keeps ordinary/non-Conventional commits.
- Supports Git revision ranges with `--since` / `--until`.
- Generates version/date headings and optional GitHub commit links.
- Writes UTF-8 Markdown atomically and refuses accidental overwrite unless `--force` is supplied.
- Has no runtime Python dependencies; only Git is required to read history.

### Requirements & installation
- Python 3.10+
- Git

```bash
git clone https://github.com/rad03i2/changelog-maker.git
cd changelog-maker
python -m pip install .
```

For development/testing:
```bash
python -m pip install pytest
python -m pip install -e .
pytest
```

### Usage
Generate unreleased notes from the current repository:
```bash
changelog-maker .
```

Generate release notes since a tag:
```bash
changelog-maker . --since v1.2.0 --version 1.3.0 --date 2026-09-21 -o CHANGELOG-1.3.0.md
```

Add commit links:
```bash
changelog-maker . --since v1.2.0 --repo-url https://github.com/rad03i2/changelog-maker
```

Use `--exclude-other` to omit non-Conventional commits, `--max-count N` to cap history (default 500), and `--force` only when replacing an output file intentionally. Run `changelog-maker --help` for all options.

### Configuration
There is deliberately no config file and no environment-variable requirement. All behavior is explicit through CLI flags, which keeps CI usage reproducible.

### Project structure
```text
src/changelog_maker/core.py   parser + Markdown renderer
src/changelog_maker/cli.py    Git integration + CLI
src/changelog_maker/__init__.py
 tests/                        unit/CLI tests
.github/workflows/ci.yml       cross-platform CI
```

### Preview / screenshots
This is a terminal tool, so a screenshot is optional. For a project-page preview, capture `changelog-maker . --since <tag>` beside the generated Markdown rendered by GitHub. Do not use fabricated output.

### Testing
`pytest` exercises Conventional Commit parsing, grouping, breaking changes, commit links, empty history, path/output behavior, overwrite protection, and CLI validation. CI runs on Linux, Windows, and macOS with supported Python versions.

### Security & privacy
The tool runs locally, makes no network requests, executes Git with an argument list (not a shell), and never evaluates commit messages as code. Treat commit text as untrusted when publishing generated notes. `--repo-url` only formats links; it is not contacted.

### Limitations
- Classification depends on commit-message quality; it does not infer intent from diffs.
- Breaking-change footers in commit bodies are not parsed; `!` in the subject header is supported.
- It does not query GitHub releases/PRs or resolve contributor names.
- Output is a release section, not an automatic merge into an existing changelog.

### Optional roadmap
Body/footer parsing, contributor summaries, and safe insertion into an existing `CHANGELOG.md` may be added later; they are not required for current functionality.

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Security guidance is in [SECURITY.md](SECURITY.md).

### License
MIT — see [LICENSE](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

## العربية

### نظرة عامة
**Changelog Maker** أداة سطر أوامر محلية تحول سجل Git إلى ملاحظات إصدار Markdown مرتبة. تفهم صيغة Conventional Commits، وتجمع التغييرات حسب نوعها، وتبرز التغييرات الكاسرة، ويمكنها إنشاء روابط إلى الـ commits على GitHub.

### لماذا هذا المشروع؟
كتابة سجل التغييرات يدويًا تُنسى بسهولة. تستخرج الأداة مسودة مفيدة مباشرة من سجل Git من دون رفع بيانات المستودع إلى خدمة خارجية ومن دون API key.

### المميزات
- تحليل الصيغة `type(scope)!: subject`.
- تصنيف الميزات والإصلاحات والأداء وإعادة الهيكلة والتوثيق والاختبارات والبناء وCI والصيانة والتراجعات.
- إبراز Breaking Changes وإمكانية الاحتفاظ بالرسائل العادية أو استبعادها.
- تحديد مجال Git عبر `--since` و`--until`.
- عنوان إصدار وتاريخ وروابط commits اختيارية.
- كتابة UTF-8 بطريقة آمنة ورفض استبدال ملف موجود دون `--force`.
- لا توجد مكتبات Python مطلوبة أثناء التشغيل؛ يلزم Git فقط لقراءة السجل.

### المتطلبات والتثبيت
Python 3.10 أو أحدث وGit، ثم:
```bash
git clone https://github.com/rad03i2/changelog-maker.git
cd changelog-maker
python -m pip install .
```
للتطوير: ثبّت `pytest` والحزمة بوضع editable ثم شغّل `pytest` كما في القسم الإنجليزي.

### الاستخدام
```bash
changelog-maker .
changelog-maker . --since v1.2.0 --version 1.3.0 --date 2026-09-21 -o CHANGELOG-1.3.0.md
```
استخدم `--repo-url` لإضافة روابط commits، و`--exclude-other` لاستبعاد الرسائل غير التقليدية، و`--max-count` لتحديد عدد السجلات، و`--force` فقط عند قصد استبدال ملف.

### الإعداد والبنية
لا تحتاج الأداة ملف إعداد أو متغيرات بيئة. المنطق في `src/changelog_maker/core.py`، وواجهة CLI وتكامل Git في `cli.py`، والاختبارات في `tests/`، وCI في `.github/workflows/ci.yml`.

### الاختبارات والمعاينة
تغطي الاختبارات التحليل والتصنيف والتغييرات الكاسرة والروابط والسجل الفارغ وحماية الاستبدال والتحقق من CLI. ولأن المشروع طرفي، يمكن أخذ لقطة حقيقية للأمر وMarkdown الناتج عند الحاجة، ولا توجد صورة مزيفة ضمن المستودع.

### الخصوصية والأمان
العمل محلي بالكامل ولا توجد طلبات شبكة. يُشغّل Git بقائمة معاملات من دون shell، ولا تُنفذ رسائل commits ككود. رابط المستودع يستخدم للتنسيق فقط.

### القيود
الأداة تعتمد على جودة رسائل commits، ولا تحلل الـdiffs أو تذييل `BREAKING CHANGE` داخل body، ولا تستعلم عن Releases/PRs أو أسماء المساهمين، ولا تدمج الناتج تلقائيًا داخل changelog موجود.

### تطوير اختياري
يمكن مستقبلًا دعم body/footer وملخص المساهمين والإدراج الآمن في `CHANGELOG.md`؛ هذه ليست وظائف مدعاة حاليًا.

### المساهمة والترخيص
راجع [CONTRIBUTING.md](CONTRIBUTING.md) و[SECURITY.md](SECURITY.md). المشروع مرخص وفق MIT في [LICENSE](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
