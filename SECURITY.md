# Security Policy / سياسة الأمان

## Supported version
The latest release/main branch receives security fixes.

## Reporting
Please report suspected vulnerabilities privately through GitHub's available private security-reporting mechanism when enabled. Do not include secrets or private repository history in a public issue.

## Security model
Changelog Maker reads local Git history and writes Markdown. It does not make network requests or evaluate commit text. Repository paths and revision names are passed to Git as argument-list values rather than through a shell. Review generated text before publishing because commit messages are untrusted content.

## العربية
يتلقى الفرع الرئيسي/أحدث إصدار إصلاحات الأمان. أبلغ عن الثغرات عبر قناة GitHub الخاصة المتاحة عند تفعيلها، ولا تنشر أسرارًا أو سجل مستودع خاص في Issue عامة. الأداة تقرأ سجل Git محليًا ولا تنفذ نص رسائل commits، ويجب مراجعة Markdown الناتج قبل نشره.
