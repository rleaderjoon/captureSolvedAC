# captureSolvedAC

solved.ac 프로필의 **AC RATING**과 **스트릭** 섹션을 자동으로 캡처해 트위터에 올릴 수 있는 이미지를 만들어주는 앱입니다.

매일 수동으로 캡처할 때 생기는 위치 불일치 문제를 해결하고, 버튼 하나로 일관된 이미지를 생성합니다.

---

## 다운로드 & 실행 (비개발자용)

> Python 없이 바로 실행 가능합니다.

### 1단계 — 앱 다운로드

<p>
  <a href="../../releases/latest">
    <img src="https://img.shields.io/badge/Windows-다운로드-0078D6?logo=windows&logoColor=white&style=for-the-badge" alt="Windows 다운로드" />
  </a>
  &nbsp;
  <a href="../../releases/latest">
    <img src="https://img.shields.io/badge/macOS-다운로드-000000?logo=apple&logoColor=white&style=for-the-badge" alt="macOS 다운로드" />
  </a>
</p>

- **Windows**: `captureSolvedAC.exe` 다운로드
- **macOS**: `captureSolvedAC.dmg` 다운로드 후 앱을 Applications 폴더로 드래그

### 2단계 — 첫 실행

크롬이 설치되어 있으면 바로 실행됩니다.

크롬이 없을 경우 **처음 실행 시** 브라우저(Chromium) 자동 설치 안내가 뜹니다. **"설치"** 를 눌러주세요. (~150MB, 한 번만 필요합니다.)

> **macOS 주의**: 처음 실행 시 "확인되지 않은 개발자" 경고가 뜰 수 있습니다.
> Finder에서 앱을 우클릭 → **열기** → **열기** 를 선택하면 실행됩니다.

### 3단계 — 캡처 & 트위터 공유

1. solved.ac 핸들 입력 (예: `intars`)
2. **캡처하기** 클릭
3. 이미지가 생성되면 **트위터 올리기** 클릭
4. 브라우저에서 트위터 창이 열리면 `Ctrl+V` (macOS: `Cmd+V`)로 이미지 붙여넣기 후 게시

---

## 출력 예시

| 생성 이미지 |
|---|
| ![예시](docs/example.png?raw=true) |

---

## 개발자용 — 소스에서 실행

### 요구사항
- Python 3.10+
- Windows 또는 macOS

### 설치 및 실행

**Windows:**
```bash
git clone https://github.com/YOUR_USERNAME/captureSolvedAC.git
cd captureSolvedAC

# 의존성 설치 + Chromium 다운로드 (최초 1회)
setup.bat

# 앱 실행
start.bat
```

**macOS:**
```bash
git clone https://github.com/YOUR_USERNAME/captureSolvedAC.git
cd captureSolvedAC

# 의존성 설치 + Chromium 다운로드 (최초 1회, 크롬이 있으면 생략 가능)
pip install -r requirements.txt
python -m playwright install chromium

# 앱 실행
python main.py
```

### 빌드

**Windows (.exe):**
```bash
pip install pyinstaller
build.bat
# dist/captureSolvedAC.exe 생성됨
```

**macOS (.dmg):**
```bash
pip install pyinstaller
pyinstaller captureSolvedAC_mac.spec --clean --noconfirm
hdiutil create -volname captureSolvedAC -srcfolder dist/captureSolvedAC.app -ov -format UDZO dist/captureSolvedAC.dmg
# dist/captureSolvedAC.dmg 생성됨
```

---

## 기술 스택

- **Playwright** — headless Chromium으로 DOM 요소 직접 캡처 (CSS 클래스가 아닌 텍스트 기반 선택)
- **Pillow** — 두 섹션 이미지 합성
- **CustomTkinter** — 다크모드 GUI
- **PowerShell / osascript** — 클립보드 복사 (Windows / macOS)

---

## 문제 해결

**Q: 캡처 중 오류가 발생해요**
- 인터넷 연결을 확인하세요
- solved.ac 핸들이 정확한지 확인하세요

**Q: 트위터에 붙여넣기가 안 돼요**
- "이미지 복사" 버튼을 다시 누른 뒤 트위터 입력창 클릭 후 `Ctrl+V` (macOS: `Cmd+V`)

**Q: 처음 실행 시 설치가 너무 오래 걸려요**
- Chromium (~150MB) 다운로드 중입니다. 인터넷 속도에 따라 1~5분 소요됩니다.
- 크롬이 설치되어 있으면 이 과정이 생략됩니다.

**Q: macOS에서 "확인되지 않은 개발자" 경고가 떠요**
- Finder에서 앱을 우클릭 → **열기** → **열기** 를 선택하세요.
