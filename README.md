# captureSolvedAC

solved.ac 프로필의 **AC RATING**과 **스트릭** 섹션을 자동으로 캡처해 트위터에 올릴 수 있는 이미지를 만들어주는 Windows 앱입니다.

매일 수동으로 캡처할 때 생기는 위치 불일치 문제를 해결하고, 버튼 하나로 일관된 이미지를 생성합니다.

---

## 다운로드 & 실행 (비개발자용)

> Python 없이 바로 실행 가능합니다.

### 1단계 — 앱 다운로드

👉 **[최신 버전 다운로드 (Releases)](../../releases/latest)**

`captureSolvedAC.exe` 파일을 다운로드합니다.

### 2단계 — 첫 실행 (Chromium 자동 설치)

`captureSolvedAC.exe`를 더블클릭합니다.

**처음 실행 시** 브라우저(Chromium) 자동 설치 안내가 뜹니다. **"설치"** 를 눌러주세요. (~150MB, 한 번만 필요합니다.)

### 3단계 — 캡처 & 트위터 공유

1. solved.ac 핸들 입력 (예: `intars`)
2. **캡처하기** 클릭
3. 이미지가 생성되면 **트위터 올리기** 클릭
4. 브라우저에서 트위터 창이 열리면 `Ctrl+V`로 이미지 붙여넣기 후 게시

---

## 출력 예시

| 생성 이미지 |
|---|
| ![예시](docs/example.png?raw=true) |

---

## 개발자용 — 소스에서 실행

### 요구사항
- Python 3.10+
- Windows

### 설치 및 실행

```bash
git clone https://github.com/YOUR_USERNAME/captureSolvedAC.git
cd captureSolvedAC

# 의존성 설치 + Chromium 다운로드 (최초 1회)
setup.bat

# 앱 실행
start.bat
```

### .exe 직접 빌드

```bash
pip install pyinstaller
build.bat
# dist/captureSolvedAC.exe 생성됨
```

---

## 기술 스택

- **Playwright** — headless Chromium으로 DOM 요소 직접 캡처 (CSS 클래스가 아닌 텍스트 기반 선택)
- **Pillow** — 두 섹션 이미지 합성
- **CustomTkinter** — Windows 네이티브 스타일 GUI
- **PowerShell** — 클립보드 복사

---

## 문제 해결

**Q: 캡처 중 오류가 발생해요**
- 인터넷 연결을 확인하세요
- solved.ac 핸들이 정확한지 확인하세요

**Q: 트위터에 붙여넣기가 안 돼요**
- "이미지 복사" 버튼을 다시 누른 뒤 트위터 입력창 클릭 후 `Ctrl+V`

**Q: 처음 실행 시 설치가 너무 오래 걸려요**
- Chromium (~150MB) 다운로드 중입니다. 인터넷 속도에 따라 1~5분 소요됩니다.
