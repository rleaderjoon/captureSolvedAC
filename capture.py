"""
Playwright-based DOM capture for solved.ac profile sections.

Strategy: Use JavaScript evaluate_handle to find card containers
by text content (stable), not CSS class names (unstable/hashed).
"""
import asyncio
from typing import Callable, Optional, Tuple
from playwright.async_api import async_playwright, ElementHandle, Page

from config import (
    VIEWPORT_WIDTH, VIEWPORT_HEIGHT,
    PAGE_TIMEOUT, HYDRATION_WAIT_MS, STREAK_RENDER_TIMEOUT_MS
)

# JS to find a card section by the text of its heading.
# Walks up from the leaf text node until it finds a wide, tall container
# whose parent is significantly taller (meaning this is one section among many).
_FIND_CARD_JS = """
(text) => {
    // Find the leaf element whose text content exactly matches
    const all = Array.from(document.querySelectorAll('*'));
    let leaf = null;
    for (const el of all) {
        if (el.textContent.trim() === text && el.childElementCount === 0) {
            leaf = el;
            break;
        }
    }
    if (!leaf) {
        // Fallback: looser match (element may have icon as child)
        for (const el of all) {
            const t = el.textContent.trim();
            if (t === text && el.childElementCount <= 1) {
                leaf = el;
                break;
            }
        }
    }
    if (!leaf) return null;

    // Walk up to find the card container
    let el = leaf.parentElement;
    while (el && el !== document.body) {
        const rect = el.getBoundingClientRect();
        if (rect.width >= 600 && rect.height >= 100) {
            const parent = el.parentElement;
            if (parent) {
                const parentRect = parent.getBoundingClientRect();
                // Parent is > 100px taller: this element is a section, not the whole page
                if (parentRect.height > rect.height + 100) {
                    return el;
                }
            }
        }
        el = el.parentElement;
    }
    return null;
}
"""

# JS to wait until the streak heatmap calendar has rendered (has rect cells)
_STREAK_RENDERED_JS = """
() => {
    const all = Array.from(document.querySelectorAll('*'));
    const leaf = all.find(el =>
        el.textContent.trim() === '스트릭' && el.childElementCount <= 1
    );
    if (!leaf) return false;
    let el = leaf.parentElement;
    for (let i = 0; i < 10; i++) {
        if (!el) break;
        if (el.querySelectorAll('rect').length > 30) return true;
        el = el.parentElement;
    }
    return false;
}
"""


async def capture_sections(
    handle: str,
    on_status: Optional[Callable[[str], None]] = None
) -> Tuple[bytes, bytes]:
    """
    Navigate to solved.ac/profile/{handle} and capture:
      - AC RATING section as PNG bytes
      - 스트릭 (Streak) section as PNG bytes

    Raises ValueError if profile not found.
    Raises RuntimeError if sections cannot be located.
    """
    def status(msg: str):
        if on_status:
            on_status(msg)

    async with async_playwright() as p:
        status("브라우저 시작 중...")
        try:
            browser = await p.chromium.launch(channel="chrome", headless=True)
        except Exception:
            browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
            color_scheme="dark",
        )
        page = await context.new_page()

        url = f"https://solved.ac/profile/{handle}"
        status(f"프로필 로딩 중... ({handle})")
        await page.goto(url, wait_until="networkidle", timeout=PAGE_TIMEOUT)

        # Extra wait for React hydration and data fetching
        await page.wait_for_timeout(HYDRATION_WAIT_MS)

        # Sanity check: profile exists
        not_found_count = await page.get_by_text("존재하지 않는 사용자").count()
        if not_found_count > 0:
            await browser.close()
            raise ValueError(f"사용자를 찾을 수 없습니다: {handle}")

        # --- Capture AC RATING section ---
        status("AC RATING 섹션 캡처 중...")
        rating_el = await _find_section(page, "AC RATING")
        rating_png: bytes = await rating_el.screenshot(type="png")

        # --- Wait for streak heatmap to render, then capture ---
        status("스트릭 히트맵 렌더링 대기 중...")
        await _wait_for_streak_render(page)

        status("스트릭 섹션 캡처 중...")
        streak_el = await _find_section(page, "스트릭")
        streak_png: bytes = await streak_el.screenshot(type="png")

        await browser.close()
        return rating_png, streak_png


async def _find_section(page: Page, heading_text: str) -> ElementHandle:
    """Find a card section's ElementHandle by its heading text."""
    handle = await page.evaluate_handle(_FIND_CARD_JS, heading_text)
    el = handle.as_element()

    if el is not None:
        # Verify the element has a reasonable size
        box = await el.bounding_box()
        if box and box["width"] >= 200 and box["height"] >= 50:
            return el

    # Fallback: use Playwright locator + ancestor xpath walk
    return await _fallback_find_section(page, heading_text)


async def _fallback_find_section(page: Page, heading_text: str) -> ElementHandle:
    """Fallback section finder using Playwright locators."""
    locator = page.get_by_text(heading_text, exact=True).first

    # Walk up ancestors using xpath
    for depth in range(2, 15):
        ancestor = locator.locator(f"xpath=ancestor::*[{depth}]")
        try:
            box = await ancestor.bounding_box()
            if box and box["width"] >= 600 and box["height"] >= 100:
                parent_box = await locator.locator(f"xpath=ancestor::*[{depth + 1}]").bounding_box()
                if parent_box and parent_box["height"] > box["height"] + 100:
                    # Get ElementHandle from locator
                    el = await ancestor.element_handle()
                    if el:
                        return el
        except Exception:
            continue

    # Last resort: use ancestor at depth 5
    el = await locator.locator("xpath=ancestor::*[5]").element_handle()
    if el:
        return el
    raise RuntimeError(f"'{heading_text}' 섹션을 찾을 수 없습니다. DOM 구조가 변경되었을 수 있습니다.")


async def _wait_for_streak_render(page: Page) -> None:
    """Wait until the streak heatmap has rendered (contains rect cells)."""
    try:
        await page.wait_for_function(_STREAK_RENDERED_JS, timeout=STREAK_RENDER_TIMEOUT_MS)
    except Exception:
        # Proceed even if timeout — maybe rects use different elements
        pass
