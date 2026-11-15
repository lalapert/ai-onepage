# CLAUDE.md — ai.onepage 가이드 허브 작업 안내

이 저장소는 `@ai.onepage` 인스타그램의 **AI 툴·클로드 가이드 링크 허브**입니다. 빌드 도구 없는 순수 정적 사이트(HTML/CSS/JS 한 파일 + JSON 데이터)이고, `main` 브랜치 루트가 GitHub Pages 로 그대로 배포됩니다.

- 라이브: <https://lalapert.github.io/ai-onepage/>
- 저장소: <https://github.com/lalapert/ai-onepage> (**public**)
- 배포: `main` 에 푸시 → GitHub Pages 자동 빌드(1~2분). 프레임워크·번들러·의존성 없음, `package.json` 없음.

`README.md` 는 사람용 설명서, 이 문서는 **Claude Code 가 이 저장소에서 바로 작업하기 위한 규칙**입니다. 둘 내용이 어긋나면 실제 파일이 기준입니다.

---

## 1. 작업 시작 전에

1. `guides.json` 을 먼저 읽어 현재 최대 `num` 과 마지막 항목을 확인한다.
2. 어떤 요청인지 구분한다: **① 가이드 추가/수정** → `guides.json` 만 고친다. **② 디자인·문구 변경** → `index.html` 의 `<style>` 또는 마크업만 고친다. ③ 둘 다면 둘 다.
3. 로컬 확인은 반드시 HTTP 서버로 한다 (`fetch` 때문에 `file://` 은 빈 목록):
   ```bash
   python3 -m http.server 8080   # → http://localhost:8080
   ```
4. 푸시 후 라이브 URL에서 실제로 확인한 뒤 끝낸다.

---

## 2. 파일 구조

```
index.html   화면 전체: <style> 안 CSS, 마크업, <script> 안 로직
guides.json  가이드 목록 데이터(배열, 최신 번호가 맨 앞)
thumbs/      카드 썸네일 {num}_{slug}.jpg (예: 23_impeccable.jpg)
avatar.jpg   프로필 사진(원형)
fonts/       NotoSansKR Regular/Bold/Black .woff2 (한글 서브셋)
.nojekyll    GitHub Pages 가 정적 파일을 그대로 서빙하도록 하는 빈 파일 — 지우지 말 것
README.md    사람용 문서
CLAUDE.md    이 문서
```

---

## 3. `guides.json` 스키마

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

| 필드 | 타입 | 규칙 |
|---|---|---|
| `num` | number | 가이드 번호. **영구**. 화면에 `23번` 으로 표시. |
| `title` | string | 카드 제목. 화면에서 `23번 \| 제목` 으로 렌더링됨. |
| `summary` | string | 한 줄 요약. 카드에서 최대 2줄. |
| `category` | string | `클로드 코드` / `로컬·무료 AI` / `영상·이미지` / `수익·마케팅` 중 **정확히 하나** (띄어쓰기·가운뎃점 포함 그대로) |
| `date` | string | `YYYY-MM-DD` 발행일 |
| `url` | string | 카드 클릭 시 새 탭으로 열릴 주소 |
| `thumb` | string | `thumbs/{num}_{slug}.jpg`. 없으면 `""` |
| `badge` | `"NEW"` \| `"지금 인기"` \| `null` | 표시용 칩 |
| `tags` | string | 띄어쓰기 구분 검색 키워드(화면 비노출) |

JSON 은 UTF-8 + 한글 그대로(이스케이프 없이), 2칸 들여쓰기. 최상위는 **배열**이다.

---

## 4. 번호 규칙 — 절대 지킬 것

- 가장 오래된 `OpenFilm` 이 **`1`번**, 가장 최근 가이드가 **`23`번**.
- 새 가이드를 추가할 때: **`num = 기존 최대 num + 1`** (지금이면 `24`) 을 주고 `guides.json` **배열 맨 앞**에 넣는다.
- **기존 번호를 다시 매기거나 밀어내지 않는다.** 번호는 인스타그램 캡션에 이미 노출된 값이라 영구 식별자다. 중간에 빈 번호가 생겨도 그대로 둔다.
- 화면 정렬은 `num` 내림차순으로 JS 가 처리하므로 배열 순서가 틀려도 깨지지 않지만, 배열도 최신순으로 유지한다.
- 번호 중복·건너뜀은 버그로 취급한다. 추가 후 `num` 목록이 1..최대값인지 확인:
  ```bash
  python3 -c "import json;d=json.load(open('guides.json'));print(sorted(g['num'] for g in d))"
  ```

---

## 5. 검색·표시 규칙

- `index.html` 의 `CATS` 는 필터 알약 정의. `key` 는 `guides.json` 의 `category` 와 **문자열이 완전히 같아야** 한다. 새 카테고리는 양쪽에 함께 추가.
- `exactNumber(q)`: `^(\d{1,3})\s*번?$` 에 맞으면 **번호 정확 검색** → `num === N` 인 1건만. (`1` 검색 시 `11`, `21` 제외)
- 번호 검색은 **카테고리 필터보다 우선**한다. (다른 알약이 눌려 있어도 해당 번호를 보여 줌)
- 그 외 입력은 키워드 검색: `title`, `summary`, `category`, `tags`, `num+"번"`, `date`, `badge` 에 대해 공백 분리 토큰 AND 매칭.
- 검색창 `placeholder` 는 `번호나 키워드 검색 (예: 23번, 올라마, 클로드)` — 바꾸지 말 것.
- 카드 제목 마크업: `<h2><span class="num">N번</span><span class="bar">|</span>제목</h2>`
- 배지 칩: `"NEW"` → `.chip.new`(빨강), `"지금 인기"` → `.chip.hot`(청록), `null` → 없음
- 필터 알약 개수, 하단 `가이드 N편` 은 데이터에서 자동 계산된다. 하드코딩 금지.
- 텍스트는 `esc()` 로 이스케이프해서 넣는다. `innerHTML` 에 날것으로 넣지 말 것.

---

## 6. 디자인 수정

색은 `index.html` 의 `<style>` 맨 위 `:root` 변수로만 바꾼다.

| 변수 | 기본값 | 쓰임 |
|---|---|---|
| `--bg` | `#FAF7F1` | 페이지 배경 |
| `--card` | `#FFFFFF` | 카드·검색창·알약·프로필 링 배경 |
| `--ink` | `#211E1A` | 본문 텍스트 |
| `--muted` | `#7C756B` | 보조 텍스트 |
| `--line` | `#EDE7DB` | 구분선·테두리 |
| `--teal` | `#0F8A72` | 포인트(번호, 인기 칩) |
| `--teal-dark` | `#0B6B59` | 진한 포인트(결과 개수, 링크) |
| `--teal-soft` | `#DBF2E9` | 역할 배지 배경 |
| `--red` | `#E0452E` | NEW 칩 |
| `--red-soft` | `#FBE3DE` | (여유분) |

지킬 것:

1. **모바일 390px 기준.** `.page` 는 `max-width:430px`. 390px 에서 **가로 스크롤·요소 잘림이 없어야** 한다. `overflow-x:hidden` 으로 넘침을 숨기는 식의 처리는 금지(원인을 고친다).
2. **JS 가 잡는 훅 유지**: `#pills`, `#q`, `#resultbar`, `#list`, `#footnote` 의 `id` 와 `header.profile` → `section.filters` → `#resultbar` → `main#list` 순서.
3. **검색 로직 유지**: 디자인만 바꿀 때 `exactNumber()`, `matches()`, `CATS`, `cardHTML()` 의 번호 표기 부분을 건드리지 않는다.
4. **폰트**: `@font-face` 3개(NotoKR 400/700/900)와 `body` 의 `font-family`. 폰트 교체 시 한글 서브셋 woff2 를 유지해 용량(현재 전체 2.2MB 수준)을 크게 늘리지 않는다.
5. **썸네일**: `.thumb` 은 58×58 정사각, `object-fit:cover`. 세로형 원본(1080×1920) 그대로 넣어도 된다.
6. **데이터 로딩 상태 유지**: `fetch("./guides.json")` 실패 시 안내 문구를 보여 주는 `.catch` 를 없애지 않는다.
7. `<meta name="viewport">`, `lang="ko"`, `theme-color` 유지.

---

## 7. 가이드 추가 절차 (체크리스트)

1. `guides.json` 맨 앞에 새 항목 추가, `num` = 기존 최대 + 1.
2. 썸네일을 `thumbs/{num}_{slug}.jpg` 로 저장. (없으면 `"thumb": ""`)
3. `badge`: 새 항목 `"NEW"`, 직전 항목은 `null` 로 내리는 것이 기본.
4. 로컬 서버로 확인: 목록 맨 위에 새 번호, 알약 개수 +1, `N번` 검색 시 1건.
5. 커밋 메시지는 짧게: `가이드 24번 추가 (slug)` / `디자인: 카드 간격 조정`.
6. `git push origin main` → 라이브 URL 확인 (새 번호 노출, 404 없음, 카드 링크 정상).

---

## 8. 보안 — public 저장소

이 저장소는 **전 세계에 공개**된다. 아래는 이 저장소에 **절대 커밋하지 않는다**.

- 비밀번호, API 키, 토큰, 쿠키, `.env`
- 개인정보: 전화번호, 집·사무실 주소, 개인 이메일, 계좌·카드 정보, 주민번호
- 내부 메모, 작업 스크립트, 초안·매출·통계 같은 비공개 자료
- 비공개 노션 페이지 주소·초대 링크, 비공개 저장소 링크

작업 중 생긴 임시 파일(스크린샷, 로그, 백업)은 커밋 전에 지우고, `git status` 로 무엇이 올라가는지 확인한 뒤 커밋한다.
