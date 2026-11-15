# ai.onepage — AI 툴 가이드 허브

`@ai.onepage` 인스타그램에서 소개한 **AI 툴·클로드 가이드 링크를 한 페이지에 모아 둔 정적 사이트**입니다.
번호(`1번` ~ 최신 번호)로 가이드를 가리키고, 카드를 누르면 해당 가이드가 새 탭에서 열립니다.

- **라이브 주소**: <https://lalapert.github.io/ai-onepage/>
- **저장소**: <https://github.com/lalapert/ai-onepage> (public)
- **배포 방식**: `main` 브랜치 루트를 GitHub Pages 가 그대로 서빙합니다. `main` 에 푸시하면 1~2분 안에 자동 반영됩니다. (빌드 도구·프레임워크 없음)

이 문서는 **인수인계용**입니다. 링크를 고치거나 디자인을 바꾸고 싶을 때 이 문서와 `CLAUDE.md` 만 읽으면 작업할 수 있게 적어 두었습니다.

> **2026-11-15 역할 변경:** 이제 `@ai.onepage` 의 허브 갱신과 **상세 가이드(HTML + A4 PDF) 제작·배포를 Claude 단독**으로 합니다. 1~23번도 2026-11-15에 이 저장소 안의 정적 HTML + PDF 로 옮겼고, 새 편도 같은 방식으로 만듭니다. 역할·이유·레퍼런스 분석·제작 절차는 **[`GUIDE_HANDOFF.md`](GUIDE_HANDOFF.md)**, 실제 템플릿은 **[`templates/guide-template/`](templates/guide-template/)** 에 있습니다.

**공식 프로필 링크는 이 허브입니다: <https://lalapert.github.io/ai-onepage/>**

---

## 1. 파일 구조

```
/
├─ index.html      # 화면 전체 (HTML + CSS + JS 한 파일)
├─ guides.json     # 가이드 목록 데이터 (23건, 최신 번호가 맨 앞)
├─ thumbs/         # 카드 썸네일 이미지 (예: 23_impeccable.jpg)
├─ guides/{num}/   # 상세 가이드 한 편: index.html + print.html + guide.pdf
├─ templates/guide-template/  # 상세 가이드를 찍어내는 범용 템플릿
├─ avatar.jpg      # 프로필 사진 (원형 68px)
├─ fonts/          # NotoSansKR 웹폰트 (Regular / Bold / Black .woff2)
├─ .nojekyll       # GitHub Pages 가 Jekyll 처리 없이 정적 파일을 그대로 서빙
├─ README.md       # 이 문서
├─ CLAUDE.md       # Claude Code 작업용 안내 (허브 규칙)
└─ GUIDE_HANDOFF.md # 상세 가이드 HTML·PDF 인수인계
```

### `index.html` 안에서 어디를 보면 되는지

| 위치 | 내용 |
|---|---|
| `<head>` 의 `<style>` 맨 위 `:root { … }` | **디자인 토큰**(색상 변수). 색을 바꾸려면 여기만 고치면 됩니다. |
| `:root` 아래 `@font-face` | 웹폰트 등록 (NotoKR 400 / 700 / 900) |
| `<section class="filters">` | 필터 알약(`#pills`)과 검색창(`#q`)이 들어가는 자리 |
| `.pills` / `.search` / `.card` CSS | 알약·검색창·카드 모양 |
| `<script>` 의 `CATS` | 필터 알약 목록(순서·이름). `key` 는 `guides.json` 의 `category` 값과 같아야 합니다. |
| `<script>` 의 `buildPills()` | 알약을 그리고 클릭 시 `state.cat` 을 바꿔 목록을 다시 그립니다. |
| `<script>` 의 `exactNumber()` / `matches()` | **번호 정확 검색 + 키워드 검색 로직** |
| `<script>` 의 `cardHTML()` | 카드 한 장의 HTML(`N번 | 제목` 형태) |
| `<script>` 의 `render()` | 필터·검색 결과를 목록에 그림 |
| `<script>` 맨 아래 `fetch("./guides.json")` | 데이터 로드 후 첫 렌더 |

---

## 2. `guides.json` 스키마

배열이며, **최신 번호가 맨 앞**에 옵니다. 각 항목은 아래 9개 필드를 가집니다.

```json
{
  "num": 23,
  "title": "AI 티 나는 디자인 빼기: impeccable 설치와 쓰는 법",
  "summary": "클로드가 만든 화면에서 AI 티를 빼는 디자인 스킬. 말로 고치는 명령 24개와 AI 티 검사 규칙 62개",
  "category": "클로드 코드",
  "date": "2026-11-14",
  "url": "https://smooth-agreement-bd7.notion.site/AI-impeccable-4176c80331b781598835f71939ea5855",
  "thumb": "thumbs/23_impeccable.jpg",
  "badge": "NEW",
  "tags": "클로드 코드 디자인 UI impeccable 홈페이지 랜딩"
}
```

| 필드 | 타입 | 설명 |
|---|---|---|
| `num` | 숫자 | 가이드 번호. 화면에 `23번` 처럼 표시되고, 인스타 캡션의 번호와 일치합니다. |
| `title` | 문자열 | 카드 제목. 카드에서는 `23번 | 제목` 으로 보입니다. |
| `summary` | 문자열 | 한 줄 요약(카드에서 최대 2줄). |
| `category` | 문자열 | `클로드 코드` / `로컬·무료 AI` / `영상·이미지` / `수익·마케팅` 중 하나 (아래 3-4 참고). |
| `date` | 문자열 | 발행일 `YYYY-MM-DD`. 카드에 `11월 14일 가이드` 로 표시. |
| `url` | 문자열 | 카드를 눌렀을 때 열릴 주소(`./guides/{num}/`). 새 탭으로 열립니다. |
| `thumb` | 문자열 | 썸네일 경로 `thumbs/{num}_{slug}.jpg`. 비우면(`""`) 썸네일 없이 표시됩니다. |
| `badge` | 문자열 또는 `null` | `"NEW"`, `"지금 인기"`, `null`(=배지 없음) |
| `tags` | 문자열 | 띄어쓰기로 구분한 검색용 키워드. 화면에는 보이지 않습니다. |

---

## 3. 번호·검색·분류 규칙

### 3-1. 번호 규칙 (가장 중요)

- 번호는 **영구**입니다. 가장 오래된 가이드 `OpenFilm` 이 `1번`, 가장 최근 가이드가 `23번`.
- 새 릴스/가이드가 나오면 **`기존 최대 num + 1`** 을 부여하고 `guides.json` **배열 맨 앞**에 추가합니다.
  - 예: 지금 최대가 `23` 이므로 다음 가이드는 `"num": 24`.
- **기존 번호는 절대 밀어내거나 다시 매기지 마세요.** 번호는 인스타 캡션에서 이미 쓰였기 때문에, 한 번 정해진 번호는 계속 같은 가이드를 가리켜야 합니다.
- 화면 정렬은 `num` 내림차순(최신이 위)으로 자동 처리됩니다. 배열 순서와 무관하게 안전합니다.

### 3-2. 검색 규칙

- 입력이 **숫자만** (`1`, `2`, `23`) 또는 **숫자+`번`** (`1번`, `23번`, `23 번`) 이면 → **번호 정확 검색**. `num` 이 그 숫자와 **정확히 같은 1건만** 나옵니다.
  - `1` 을 검색해도 `11번`, `21번` 은 나오지 않습니다. (부분 일치 아님)
  - 번호 검색은 카테고리 필터보다 우선합니다. (다른 알약이 눌려 있어도 그 번호를 보여 줌)
- 그 외 글자는 **키워드 검색**: `title`, `summary`, `category`, `tags`, `num`, `date` 를 대상으로 하고, 공백으로 나눈 단어를 **모두** 포함하는 항목을 보여 줍니다. (예: `올라마 pdf`)
- 검색창 안내 문구: `번호나 키워드 검색 (예: 23번, 올라마, 클로드)`

### 3-3. 표시 규칙

- 카드 제목은 `<span class="num">23번</span><span class="bar">|</span>제목` 형태로, **번호가 제목 맨 앞에 포인트 색으로** 보입니다.
- 썸네일 파일명은 `{num}_{slug}.jpg` — 파일 이름의 숫자와 화면의 번호가 같습니다.
- 필터 알약의 개수 배지는 데이터에서 자동 계산됩니다. (`countFor()`)
- 하단 문구의 `가이드 N편` 도 데이터 개수로 자동 갱신됩니다.

### 3-4. 카테고리 규칙

`guides.json` 의 `category` 값과 `index.html` 의 `CATS` 필터 알약은 **한 글자도 다르면 안 됩니다.**

| `category` 값 | 포함 주제 | 개수(자동) |
|---|---|---|
| (전체) | 전체 보기 | 자동 계산 |
| `클로드 코드` | Claude Code, 스킬·플러그인, MCP, 코딩·업무 에이전트 | 자동 계산 |
| `로컬·무료 AI` | Ollama, 오픈소스 모델, PC 설치형·무료 유틸리티 | 자동 계산 |
| `영상·이미지` | AI 영상·이미지·효과음 제작, 릴스·쇼츠·유튜브 도구 | 자동 계산 |
| `수익·마케팅` | 마케팅·브랜딩, 홈페이지, 취업/이직, 수익화 툴 | 자동 계산 |

- **새 카테고리 추가 기준**:
  - 기존 4개 안에 들어가면 새로 만들지 않습니다.
  - 기존 4개로 묶기 어려운 새 주제가 **2~3편 이상** 모이거나 본격 연재가 시작될 때만 추가합니다. (1편만으로는 카테고리를 늘리지 않음)
  - 모바일 화면에서 알약이 너무 길어지지 않게 **짧은 한글(2~7자)**로 짓고, 전체 카테고리는 **6~7개 이하**를 권장합니다.
  - 추가할 때는 `guides.json` 의 `category` 값과 `index.html` 의 `CATS` 배열 **양쪽**에 같은 문자열을 넣어야 합니다.

### 3-5. 배지

| `badge` 값 | 카드 표시 |
|---|---|
| `"NEW"` | 빨간 `NEW` 칩 |
| `"지금 인기"` | 청록 `지금 인기` 칩 |
| `null` | 배지 없음 |

`"NEW"` 는 보통 가장 최근 1~2건에만 붙입니다. 순수 표시용이라 언제든 바꿔도 번호에는 영향이 없습니다.

---

## 4. 디자인 수정 가이드

색은 `index.html` 상단 `:root` 변수만 바꾸면 전체에 반영됩니다.

| 변수 | 기본값 | 쓰임 |
|---|---|---|
| `--bg` | `#FAF7F1` | 페이지 배경(아이보리) |
| `--card` | `#FFFFFF` | 카드·검색창·알약·프로필 테두리 배경 |
| `--ink` | `#211E1A` | 본문 텍스트(거의 검정) |
| `--muted` | `#7C756B` | 보조 텍스트 |
| `--line` | `#EDE7DB` | 카드 구분선·테두리 |
| `--teal` | `#0F8A72` | 포인트 색: 번호, `지금 인기` 칩 |
| `--teal-dark` | `#0B6B59` | 진한 포인트: 결과 개수 |
| `--teal-soft` | `#DBF2E9` | 역할 배지 배경 |
| `--red` | `#E0452E` | `NEW` 칩 |
| `--red-soft` | `#FBE3DE` | (여유분) |

수정할 때 지켜야 할 것:

1. **모바일 우선**. `.page` 는 `max-width:430px` 이고, **390px 폭에서 가로 스크롤이 생기면 안 됩니다.** (`overflow-X:hidden` 은 안전장치일 뿐, 넘치는 요소를 숨겨 두는 용도로 쓰지 마세요.)
2. **레이아웃 골격 유지**: `header.profile` → `section.filters` → `#resultbar` → `main#list` 순서와 `id`(`pills`, `q`, `resultbar`, `list`, `footnote`)는 JS 가 잡고 있으므로 바꾸지 마세요.
3. **검색 로직 유지**: `exactNumber()`, `matches()`, `CATS` 는 번호 정확 검색과 필터의 핵심입니다. 디자인만 바꿀 때는 건드리지 마세요.
4. **폰트**: `fonts/` 의 `NotoSansKR-{Regular,Bold,Black}.woff2` 를 쓰고 있습니다. 폰트를 바꾸려면 `@font-face` 3줄과 `body` 의 `font-family` 를 함께 고치고, 용량이 커지지 않게 한글 서브셋을 유지하세요.
5. **카드 썸네일**: `.thumb` 은 58×58 정사각 크롭(`object-fit:cover`)입니다. 세로형(1080×1920) 원본을 그대로 넣어도 중앙 기준으로 잘려 보입니다.

---

## 5. 상세 가이드(HTML + PDF) 만들기

카드를 눌렀을 때 열리는 **상세 페이지**는 노션이 아니라 이 저장소의 정적 HTML 이고, 같은 내용을 A4 PDF 로 미리 뽑아 두어 바로 내려받게 합니다(인스타 인앱 웹뷰에서는 인쇄가 막히는 기기가 많기 때문).

```bash
cp -r templates/guide-template guides/25      # 25 대신 "기존 최대 번호 + 1"
cd guides/25
# index.html 과 print.html 의 {{...}} 를 실제 내용으로 바꾼다
python3 render.py --shots ./shots              # guide.pdf 생성 + 검증(쪽수·390px·복사 버튼)
```

- `guides.json` 의 `url` 을 `./guides/25/` 로 바꾸면 카드가 이 페이지로 연결됩니다.
- PDF 카드의 `A4 N쪽` 숫자는 실제 PDF 쪽수와 같아야 합니다(`render.py` 가 대조).
- 자리표시자 전체 목록·블록 복사 규칙: [`templates/guide-template/README.md`](templates/guide-template/README.md)
- 역할·레퍼런스 분석·검증 체크리스트: [`GUIDE_HANDOFF.md`](GUIDE_HANDOFF.md)

---

## 6. 로컬에서 미리 보기

`index.html` 은 `guides.json` 을 `fetch` 로 읽기 때문에 **`file://` 로 바로 열면 목록이 비어 보입니다.** 반드시 로컬 서버로 확인하세요.

```bash
# 이 폴더에서
python3 -m http.server 8080
# 브라우저에서 http://localhost:8080
```

---

## 7. 배포

```bash
git add -A
git commit -m "가이드 24번 추가"
git push origin main
```

푸시 후 1~2분 뒤 <https://lalapert.github.io/ai-onepage/> 를 열어 확인하세요. (Pages 빌드 기록은 저장소 **Actions** 탭, 또는 `gh api repos/lalapert/ai-onepage/pages` 로 확인)

배포 후 체크리스트:

- [ ] `24번` 이 맨 위에 보이고, 기존 번호가 그대로인가
- [ ] 검색창에 `1번` → `1번 | …` 1건만 나오는가
- [ ] 필터 알약 개수와 목록이 새 데이터와 맞는가
- [ ] 카드를 눌러 링크가 정상적으로 열리는가
- [ ] 개발자도구 Network 에 404(썸네일·폰트·`guides.json`)가 없는가

---

## 8. 주의 (공개 저장소)

이 저장소는 **누구나 볼 수 있는 public 저장소**입니다. 아래는 절대 커밋하지 마세요.

- 비밀번호·API 키·토큰·쿠키
- 개인정보(전화번호, 주소, 주민번호, 계좌·카드 정보, 개인 이메일)
- 내부 메모, 작업 스크립트, 비공개 통계·매출 자료, 초안 문서
- 비공개 노션 페이지 주소나 초대 링크
- **발행 전 편의 본문·HTML·PDF·수치·제목** (발행일에 `guides/{num}/` 로 커밋)
