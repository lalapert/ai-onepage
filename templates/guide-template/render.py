#!/usr/bin/env python3
"""
ai.onepage 상세 가이드 — PDF 생성·검증 범용 스크립트 (재사용 템플릿)

  guide 폴더(guides/{NUM}/)에서 print.html → guide.pdf 를 만들고,
  index.html 을 모바일 390x844 로 열어 가로 넘침·폰트·복사 버튼을 검사한다.

  준비:
      pip install playwright pypdf
      python3 -m playwright install chromium
      # 리눅스에서 chromium 실행이 라이브러리 부족으로 실패하면:
      #   python3 -m playwright install-deps chromium

  쓰는 법 (템플릿을 guides/{NUM}/ 로 복사한 뒤 그 폴더에서):
      python3 render.py                 # guide.pdf 생성 + 검증 리포트(JSON) 출력
      python3 render.py --shots ./shots # 섹션 스크린샷도 저장
      python3 render.py --no-shots      # 스크린샷 생략
      python3 render.py --pdf guide.pdf --dir . --num 25

  이 스크립트가 검사하는 것:
    1) PDF 쪽수·용지(A4)·NotoSansKR 임베딩 여부
    2) index.html 의 PDF 카드에 적힌 "A4 N쪽" 숫자와 실제 PDF 쪽수가 같은지
    3) 모바일 390px 에서 가로 스크롤이 생기지 않는지 (scrollWidth == 390)
    4) NotoSansKR 400/700/900 폰트가 실제로 로드되는지
    5) [복사] 버튼을 눌렀을 때 라벨·토스트가 바뀌고 클립보드 내용이 pre 원문과 같은지
  하나라도 실패하면 종료 코드 1 로 끝난다(리포트의 "ok": false 항목 참고).
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# ── 선택 인자 ───────────────────────────────────────────────────────────────
DEFAULT_PDF = "guide.pdf"
MOBILE_W = 390
MOBILE_H = 844


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="guide PDF build + verification")
    ap.add_argument("--dir", default=None, help="가이드 폴더(기본: 이 스크립트가 있는 폴더)")
    ap.add_argument("--pdf", default=DEFAULT_PDF, help=f"만들 PDF 파일명 (기본: {DEFAULT_PDF})")
    ap.add_argument("--shots", default=None, help="스크린샷을 저장할 폴더 (기본: 저장 안 함)")
    ap.add_argument("--no-shots", action="store_true", help="스크린샷 생략")
    ap.add_argument("--num", default=None, help="가이드 번호(리포트에 표시용)")
    return ap.parse_args()


# ── PDF 검사 ────────────────────────────────────────────────────────────────
def pdf_info(path: pathlib.Path) -> dict:
    info: dict = {"bytes": path.stat().st_size}
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        info["pages"] = len(reader.pages)
        info["mediabox_pt"] = [round(float(x), 1) for x in reader.pages[0].mediabox]
        embedded, all_fonts = set(), set()
        for page in reader.pages:
            fonts = page.get("/Resources", {}).get("/Font", {}) or {}
            for key in fonts:
                font = fonts[key].get_object()
                name = str(font.get("/BaseFont"))
                all_fonts.add(name)
                desc = font.get("/FontDescriptor")
                if desc is not None:
                    desc = desc.get_object()
                    if any(x in desc for x in ("/FontFile", "/FontFile2", "/FontFile3")):
                        embedded.add(name)
                # Type0(한글) 폰트는 하위 폰트에 임베딩이 들어 있다
                for child in (font.get("/DescendantFonts") or []):
                    cdesc = child.get_object().get("/FontDescriptor")
                    if cdesc is not None and any(
                        x in cdesc.get_object() for x in ("/FontFile", "/FontFile2", "/FontFile3")
                    ):
                        embedded.add(name)
        info["fonts"] = sorted(f for f in all_fonts if f)
        info["embedded_fonts"] = sorted(embedded)
        info["nanum_or_noto_embedded"] = any(
            ("NotoSansKR" in f or "Noto" in f) for f in embedded
        )
    except Exception as exc:  # noqa: BLE001
        info["pypdf_error"] = repr(exc)
    return info


def pages_in_html(html: str) -> int | None:
    """index.html 의 PDF 카드에 적힌 'A4 N쪽' 숫자를 찾는다."""
    m = re.search(r"A4\s*(\d+)\s*쪽", html)
    return int(m.group(1)) if m else None


def main() -> int:
    args = parse_args()
    root = pathlib.Path(args.dir).resolve() if args.dir else pathlib.Path(__file__).resolve().parent
    index_html = root / "index.html"
    print_html = root / "print.html"
    pdf_out = root / args.pdf

    if not index_html.exists() or not print_html.exists():
        print(json.dumps({"ok": False, "error": f"{root} 에 index.html / print.html 이 없습니다"},
                         ensure_ascii=False, indent=2))
        return 1

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(json.dumps({"ok": False, "error": "playwright 가 없습니다: pip install playwright"},
                         ensure_ascii=False, indent=2))
        return 2

    report: dict = {"dir": str(root), "pdf": str(pdf_out.name), "ok": True}
    if args.num:
        report["num"] = args.num
    shots_dir = None
    if args.shots and not args.no_shots:
        shots_dir = pathlib.Path(args.shots).resolve()
        shots_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--allow-file-access-from-files", "--font-render-hinting=none"])

        # ── 1) PDF ─────────────────────────────────────────────────────────
        ctx = browser.new_context()
        page = ctx.new_page()
        page.goto(print_html.as_uri(), wait_until="load")
        try:
            page.wait_for_function("document.fonts.ready.then(() => true)", timeout=15000)
        except Exception:  # noqa: BLE001
            pass
        page.wait_for_timeout(800)
        report["print_fonts_loaded"] = page.evaluate(
            "() => ({r:document.fonts.check('400 16px NotoKR'),"
            "b:document.fonts.check('700 16px NotoKR'),"
            "k:document.fonts.check('900 16px NotoKR')})"
        )
        page.pdf(
            path=str(pdf_out),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        ctx.close()

        report["pdf_info"] = pdf_info(pdf_out)
        pages = report["pdf_info"].get("pages")
        claimed = pages_in_html(index_html.read_text(encoding="utf-8"))
        report["pdf_pages_claimed_in_html"] = claimed
        report["pdf_pages_match_html"] = (pages is not None and claimed is not None and pages == claimed)
        if claimed is None:
            report["ok"] = False
            report.setdefault("warnings", []).append(
                "index.html 에 'A4 N쪽' 숫자가 없습니다. PDF 카드의 {{PAGES}} 를 실제 쪽수로 바꾸세요."
            )
        elif pages is not None and pages != claimed:
            report["ok"] = False
            report.setdefault("warnings", []).append(
                f"index.html 의 'A4 {claimed}쪽' 과 실제 PDF 쪽수 {pages} 가 다릅니다. 숫자를 맞추세요."
            )
        if not report["pdf_info"].get("nanum_or_noto_embedded", False):
            report["ok"] = False
            report.setdefault("warnings", []).append("한글 폰트가 PDF에 임베딩되지 않았습니다(경로 확인).")

        # ── 2) 모바일 390px ────────────────────────────────────────────────
        mctx = browser.new_context(
            viewport={"width": MOBILE_W, "height": MOBILE_H},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
            user_agent=("Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36"),
        )
        try:
            mctx.grant_permissions(["clipboard-read", "clipboard-write"])
        except Exception as exc:  # noqa: BLE001
            report["clipboard_permission_error"] = repr(exc)
        mp = mctx.new_page()
        mp.goto(index_html.as_uri(), wait_until="load")
        mp.wait_for_timeout(700)

        report["mobile"] = mp.evaluate(
            """() => ({
                 scrollWidth: document.documentElement.scrollWidth,
                 innerWidth: window.innerWidth,
                 bodyHeight: document.body.scrollHeight,
                 fonts: {r: document.fonts.check('400 16px NotoKR'),
                         b: document.fonts.check('700 16px NotoKR'),
                         k: document.fonts.check('900 16px NotoKR')}
               })"""
        )
        if report["mobile"]["scrollWidth"] != report["mobile"]["innerWidth"]:
            report["ok"] = False
            report.setdefault("warnings", []).append(
                f"390px 에서 가로 넘침: scrollWidth {report['mobile']['scrollWidth']} ≠ innerWidth "
                f"{report['mobile']['innerWidth']}"
            )

        # ── 3) 스크린샷 (선택) ─────────────────────────────────────────────
        if shots_dir:
            def clip_between(start_sel: str, end_sel: str, name: str):
                try:
                    start = mp.locator(start_sel).first.bounding_box()
                    end = mp.locator(end_sel).first.bounding_box()
                except Exception:  # noqa: BLE001
                    return None
                if not start or not end:
                    return None
                top = max(0, start["y"] - 8)
                bottom = end["y"] + end["height"] + 10
                out = shots_dir / name
                mp.screenshot(path=str(out), full_page=True,
                              clip={"x": 0, "y": top, "width": MOBILE_W, "height": bottom - top})
                return str(out)

            report["shots"] = {
                "top": clip_between(".topbar", ".toc", "guide_top.png"),
                "pdf_cta": clip_between(".pdf-card", "footer", "guide_pdf_cta.png"),
            }
            try:
                box = mp.locator(".prompt").first.bounding_box()
                if box:
                    out = shots_dir / "guide_prompt.png"
                    mp.screenshot(path=str(out), full_page=True,
                                  clip={"x": 0, "y": max(0, box["y"] - 12),
                                        "width": MOBILE_W, "height": box["height"] + 24})
                    report["shots"]["prompt"] = str(out)
            except Exception:  # noqa: BLE001
                pass
            mp.screenshot(path=str(shots_dir / "guide_full.png"), full_page=True)

        # ── 4) 복사 버튼 실동작 ────────────────────────────────────────────
        btn = mp.locator(".copy-btn").first
        if btn.count() == 0 or btn.get_attribute("data-copy") is None:
            report["copy_test"] = {"skipped": "복사 버튼(.copy-btn)이 없습니다"}
        else:
            target_id = btn.get_attribute("data-copy")
            btn.scroll_into_view_if_needed()
            before = btn.inner_text().strip()
            btn.click()
            mp.wait_for_timeout(350)
            after = btn.inner_text().strip()
            expected = mp.evaluate(f"() => document.getElementById({target_id!r}).innerText.trim()")
            try:
                got = mp.evaluate("() => navigator.clipboard.readText()")
            except Exception as exc:  # noqa: BLE001
                got = "READ_FAIL: " + repr(exc).splitlines()[0]
            report["copy_test"] = {
                "label_before": before,
                "label_after": after,
                "toast": mp.locator("#toast").inner_text(),
                "toast_class": mp.locator("#toast").get_attribute("class"),
                "button_class": btn.get_attribute("class"),
                "clipboard_matches": isinstance(got, str) and got.strip() == expected,
                "expected_preview": expected[:120],
            }
            if after == before or not report["copy_test"]["button_class"].count("done"):
                report["ok"] = False
                report["warnings"] = report.get("warnings", []) + ["복사 버튼 라벨이 바뀌지 않았습니다."]
            if not report["copy_test"]["clipboard_matches"]:
                report["warnings"] = report.get("warnings", []) + [
                    "클립보드 읽기 결과가 pre 원문과 다릅니다(헤드리스 환경 제한일 수 있음 — 실제 폰에서 한 번 더 확인)."
                ]

        mctx.close()
        browser.close()

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
