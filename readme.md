## 📌 풀스택 개발 초기 컨셉 요약표

| 항목 | 내용 |
|------|------|
| 🏗️ 프로젝트명 | 개인 풀스택 웹 서비스 (게시판 + 자동매매 + 메신저 연동) |
| 🧩 아키텍처 구성 | FastAPI (백엔드) + Vue3 or React (프론트엔드) + PostgreSQL (DB) |
| 🖥️ 개발 환경 | 로컬 PC (VSCode + PostgreSQL) → 이후 Docker로 서버 배포 |
| 🗂️ 디렉토리 구조 | `backend/`, `frontend/`, `docker-compose.yml` 구성 예정 |
| 📦 핵심 기능 | 1. 게시판 CRUD<br>2. 한국투자증권 모의계좌 자동매매<br>3. 카카오톡/텔레그램 알림 연동 |
| 🔒 로그인 처리 | 로컬 DB 기반 로그인 (SSO 구조와 유사한 흐름으로 설계) |
| 📡 API 연동 | `mojito2` 라이브러리로 한국투자증권 API 호출 |
| 📬 메신저 알림 | 조건별 알림 전송 (체결 알림, 오류 등) – `notifier.py`로 모듈화 |
| 🧹 코드 구조 | 기능 기반 분리 (예: `features/board/`, `features/trade/`)<br>UI는 탭별 파일로 구성하되, 기능 폴더 안에 둠 |
| ⚙️ 배포 계획 | 초기에는 로컬 테스트, 완성 후 `docker-compose`로 서버 전환 |
| 📁 확장성 대비 | 클린 아키텍처 기반: `domain / usecase / interface / infra` 구조 적용 가능 |
| 🧪 테스트 전략 | 기능별 로컬 테스트 우선, 추후 유닛테스트 + e2e 테스트 도입 고려 |
| 📌 기타 유의사항 | - DB는 PostgreSQL 기준<br>- 공통 로직은 `utils/`에 정리<br>- 초기 개발은 한 파일로 작성 후 분리 리팩토링 |
### Backend structure
- domain: SQLAlchemy models
- usecases: business logic
- interfaces: FastAPI routers and entrypoint
- infrastructure: DB and external API
- 환경 변수 파일(`.env`)에 DB 및 API 키 정보를 저장합니다. 샘플은 `.env.example`을 참고하세요.
