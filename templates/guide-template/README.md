# templates/guide-template — 상세 가이드 재사용 템플릿

`@ai.onepage` 릴스 한 편에 붙는 **상세 가이드 페이지(모바일 HTML) + A4 PDF** 를 매번 같은 모양으로 찍어내기 위한 템플릿입니다.
`preview/` 에서 검증한 첫 샘플(4쪽 A4, 390px 가로 넘침 없음, 복사 버튼 동작 확인)의 **구조·CSS·JS·인쇄 스타일을 그대로** 옮기고, 특정 편의 내용만 `{{...}}` 자리표시자로 바꾼 것입니다.

| 파일 | 무엇 |
|---|---|
| `index.html` | 모바일 상세 가이드(허브에서 카드로 들어오는 화면). CSS·복사 스크립트 포함 |
| `print.html` | A4 인쇄 전용 레이아웃. 이 파일을 인쇄해 `guide.pdf` 를 만든다 |
| `render.py` | `print.html` → `guide.pdf` 생성 + 390px 검증·복사 버튼 테스트 + 쪽수/폰트 확인 |
| `README.md` | 이 문서 |

---

## 1. 쓰는 순서 (새 가이드 한 편)

```bash
# 1) 폴더 만들기 (번호는 guides.json 의 최대 num + 1)
cp -r templates/guide-template guides/25

# 2) 내용 채우기 — index.html 과 print.html 의 {{...}} 를 모두 실제 내용으로 바꾼다
#    (두 파일의 문장이 어긋나면 안 된다. print.html 은 화면용 버튼이 없는 같은 내용이다)

# 3) PDF 만들기 + 검증
cd guides/25
pip install playwright pypdf
python3 -m playwright install chromium
python3 render.py --shots ./shots
#  → guide.pdf 생성, JSON 리포트 출력. "ok": true 가 될 때까지 고친다.

# 4) 허브에 연결 — guides.json 맨 앞에 항목 추가
#    "url": "./guides/25/"   (또는 https://lalapert.github.io/ai-onepage/guides/25/)
#    "thumb": "thumbs/25_{slug}.jpg"

# 5) 커밋·푸시 → 라이브 URL 확인
git add -A && git commit -m "가이드 25번 추가 (slug)" && git push origin main
```

`render.py` 는 **A4 {{PAGES}}쪽** 숫자와 실제 PDF 쪽수를 대조합니다. 쪽수가 다르면 실패로 표시되니, PDF를 만든 뒤 `index.html` 의 숫자를 실제 값으로 바꾸고 다시 돌리세요.

---

## 2. 자리표시자(`{{...}}`) 목록

### 공통 · 히어로

| 자리표시자 | 값 |
|---|---|
| `{{NUM}}` | 가이드 번호 (`guides.json` 의 `num`). 배지·PDF·푸터에 쓰인다 |
| `{{DATE_KO}}` | 발행일 한국어 표기. 예: `12월 1일` |
| `{{CATEGORY}}` | 카테고리. `guides.json` 의 `category` 와 **한 글자도 다르면 안 된다** |
| `{{TITLE_LINE_1}}` / `{{TITLE_LINE_2}}` | 히어로 제목 두 줄(HTML). 한 줄이면 2번째 줄을 지운다 |
| `{{TITLE_INLINE}}` | 한 줄 제목(`<title>`, PDF 머리글, 푸터용) |
| `{{SUBTITLE}}` | 제목 아래 부제(틸색 굵은 한 줄) |
| `{{LEDE}}` | 한 줄 요약 문단. `<code>` 태그를 섞어도 된다 |
| `{{SUMMARY}}` | `meta description` 용 (검색·공유 미리보기) |
| `{{PILL_1_KEY}}`·`{{PILL_1_TEXT}}` | 히어로 알약 3개. KEY는 굵게(틸) 나온다. 예: `무료` + `설치 1분` |
| `{{CHECKED_KO}}` | 사실 확인한 날. 예: `2026년 11월 15일` |
| `{{REQUIREMENT}}` | 필요한 조건. 예: `Claude Pro 이상` |
| `{{TOOL_NOTE}}` | 도구·비용 한 줄. 예: `무료 오픈소스` |
| `{{FOOT_SOURCE}}` | 푸터 마지막 줄(무엇을 보고 썼는지) |

### 한눈에 비교 (선택)

비교할 실제 숫자가 있을 때만 쓴다. 없으면 `index.html` 의 `<section class="cmp">` 와 `print.html` 의 `<div class="cmp">` 를 통째로 지운다.

| 자리표시자 | 값 |
|---|---|
| `{{CMP_BASIS}}` | 비교 기준 캡션. 예: `제 실제 기록 기준` |
| `{{CMP_1_LABEL}}` | 첫 번째 비교 항목 이름 |
| `{{CMP_1_A_NAME}}` / `{{CMP_1_A_VALUE}}` / `{{CMP_1_UNIT}}` | 기준 값(막대 100%) |
| `{{CMP_1_B_NAME}}` / `{{CMP_1_B_VALUE}}` / `{{CMP_1_B_WIDTH}}` | 비교 값 + 막대 너비 %(A 대비 상대값) |
| `{{CMP_1_FOOT}}` / `{{CMP_1_TAG}}` | 아래 설명 / 빨간 태그(예: `A vs B`) |
| `{{CMP_2_**}}` | 두 번째 항목. 같은 규칙 |

### 목차

`{{TOC_0}}`~`{{TOC_4}}` = 항목 이름, `{{TOC_0_NOTE}}`~`{{TOC_4_NOTE}}` = 오른쪽 작은 꼬리표(`개요`, `3개`, `주의` …).
항목 수를 늘리거나 줄이면 **`index.html` 의 `<li>` 와 `print.html` 의 `<li>` 를 함께** 고친다. 단계 카드의 `id="s0"`…`id="s4"` 와 번호가 맞아야 점프가 된다.

### 단계 카드

| 자리표시자 | 값 |
|---|---|
| `{{STEP_0_TITLE}}` / `{{STEP_0_BODY_1}}` / `{{STEP_0_BODY_2}}` / `{{STEP_0_OK}}` | 0단계(개요) 카드. `ok` 박스는 "핵심" 한 줄 |
| `{{PREP_1_NAME}}` / `{{PREP_1_WHY}}` / `{{PREP_1_WHERE}}` (1~3) | 준비물 표. 모바일에서는 3칸이 세로로 쌓인다 |
| `{{STEP_2_KICKER}}` | `block-title` 뒤에 붙는 짧은 설명. 예: `가장 효과가 커요` |
| `{{STEP_2_TITLE}}` / `{{STEP_2_ITEM_1}}` / `{{STEP_2_ITEM_2}}` / `{{STEP_2_SUCCESS}}` | 단계 카드 |
| `{{PROMPT_1_LABEL}}` / `{{PROMPT_1_BODY}}` | 프롬프트 박스 제목 / 복사될 본문(`<pre>` 안, 줄바꿈 그대로) |
| `{{STEP_2_NOTE}}` | 카드 아래 회색 노트 |
| `{{STEP_3_KICKER}}` / `{{STEP_3_TITLE}}` / `{{STEP_3_BODY}}` | 측정·결과 카드 |
| `{{MEASURE_TITLE}}` / `{{MEASURE_CAPTION}}` / `{{MEASURE_NOTE}}` | 측정값 캡션(도구·날짜·기준)과 아래 노트 |
| `{{GAIN_1_CMD}}` / `{{GAIN_1_BEFORE}}` / `{{GAIN_1_AFTER}}` / `{{GAIN_1_CUT}}` (1~2) | 결과 막대 항목. `CUT` 은 줄어든 %(막대 너비로도 쓰임) |
| `{{CHECK_1}}`~`{{CHECK_3}}` | `꼭 알아 둘 점` 체크리스트 |

### 출처 · PDF · 요약

| 자리표시자 | 값 |
|---|---|
| `{{SOURCE_1_URL}}` / `{{SOURCE_1_NAME}}` / `{{SOURCE_1_META}}` (1~2) | 출처 링크와 확인일 메모 |
| `{{SOURCE_NOTE}}` | 출처 카드 아래 노트(무엇을 언제 확인했고 무엇은 직접 잰 값인지) |
| `{{PAGES}}` | **실제 PDF 쪽수**(`render.py` 가 대조) |
| `{{SUM_1_NO}}` / `{{SUM_1_TODO}}` / `{{SUM_1_HOW}}` / `{{SUM_1_RESULT}}` (1~4) | `print.html` 마지막 장 `한 장 요약` 표. 본문에 있는 내용만 다시 적는다 |
| `{{SUMMARY_NOTE}}` | 요약 표 아래 한 줄 주의 |

---

## 3. 블록 복사 규칙

- **단계 카드 늘리기**: `index.html` 은 `<div class="block-title">…</div>` + `<article class="card" id="sN">…</article>` 한 세트를 통째로 복사하고, `print.html` 도 `<section class="sec">` 한 덩어리를 복사한다. 번호(`id`, `.n`, `STEP 0N`, 목차)를 **한꺼번에** 고친다.
- **프롬프트 박스 추가**: `.prompt` 블록을 복사하고 `<pre id="p-1">` → `p-2`, 버튼의 `data-copy="p-1"` → `p-2` 로 **두 값을 같이** 바꾼다. id가 어긋나면 복사 버튼이 조용히 동작하지 않는다.
- **CSS·JS는 손대지 않는다.** 색은 `:root` 토큰만 바꾼다(허브와 같은 팔레트).
- **모바일 390px**: `render.py` 가 `scrollWidth == 390` 을 확인한다. 넘치면 `overflow-x:hidden` 으로 숨기지 말고 원인(긴 코드·표·긴 단어)을 고친다. 긴 코드는 `class="brk"` 를 준다.
- **표는 모바일에서 스택형**(`.tbl`)을 쓴다. `td[data-l="…"]` 의 값이 라벨이 된다.

---

## 4. `render.py` 옵션

```bash
python3 render.py                       # guide.pdf 생성 + 검증 리포트
python3 render.py --shots ./shots       # 섹션 스크린샷도 저장 (guide_top.png, guide_prompt.png, guide_pdf_cta.png, guide_full.png)
python3 render.py --no-shots            # 스크린샷 생략
python3 render.py --pdf guide.pdf --dir . --num 25
```

검사 항목: PDF 쪽수·A4 크기·NotoSansKR 임베딩 / `A4 N쪽` 숫자 일치 / 390px 가로 넘침 / 폰트 400·700·900 로드 / 복사 버튼 라벨·토스트·클립보드 내용.
하나라도 실패하면 **종료 코드 1** 과 함께 `warnings` 에 이유가 나온다.

> 이 환경의 화면 없는 리눅스에서 Chromium 실행이 라이브러리 부족으로 실패하면 `python3 -m playwright install-deps chromium` 로 의존성을 설치한다. 폰트·PDF가 깨져 보이면 `print_fonts_loaded` 가 모두 `true` 인지 먼저 확인한다.

---

## 5. 공개 저장소 주의

이 저장소는 **public** 입니다.

- **발행 전 편의 본문·수치·제목을 여기에 올리지 않는다.** 새 가이드는 발행일에 `guides/{NUM}/` 로 커밋한다.
- 전화번호·개인 이메일·집 주소·API 키·내부 계정은 어떤 파일에도 넣지 않는다.
- 스크린샷·임시 PDF·작업 로그는 커밋 전에 지운다(`git status` 로 확인).
