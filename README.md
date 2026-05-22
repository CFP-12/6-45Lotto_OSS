# 🎫 6/45 Lotto 웹 서비스 (Multi-Container Web App)

Django와 Docker Multi-Container 환경을 활용하여 개발한 **6/45 로또 복권 시뮬레이터 및 당첨 확인 웹 서비스**
일반 사용자는 수동/자동 복권 구매 및 실시간 당첨 확인 가능, 관리자는 강력한 내장 Admin 인터페이스를 통해 판매 내역 확인, 회차별 당첨 번호 추첨 및 자동 당첨 정산 시스템 제어 가능.

---

## 🚀 1. 프로젝트 개요 및 주요 기능

### 👤 일반 사용자 (User)
- **복권 구매 (`/lotto/buy/`)**
  - **자동 발급**: `random.sample` 기능을 통해 1~45 중 중복 없는 6개 숫자를 자동으로 정렬하여 발급.
  - **수동 마킹**: HTML5 입력 폼을 통해 사용자가 직접 숫자를 입력, 범위(1~45) 및 중복 입력을 백엔드 단에서 Validation.
- **당첨 확인 (`/lotto/results/`)**
  - 본인이 구매한 모든 복권 리스트를 한눈에 볼 수 있는 대시보드 화면을 제공.
  - 관리자의 추첨 전에는 `추첨 대기중 ⏳` 배지가 표시, 추첨 후에는 정산된 등수(`1등~5등 🎉` 또는 `낙첨 😢`)와 발급된 번호 공이 시각적으로 출력.

### 👑 관리자 (Admin)
- **판매 내역 확인**: 전체 사용자가 구매한 모든 복권 티켓 데이터 및 선택 방식, 구매 일시를 모니터링.
- **추첨 기능 및 당첨 내역 확인**: 특정 회차에 당첨 번호 6개와 보너스 번호를 입력하고 저장하면, 해당 회차에 판매된 전재 티켓을 일괄 스캔하여 등수를 판정하는 백엔드 Batch 정산 로직이 자동 구동.

---

## 📂 2. 프로젝트 파일 구조 (Project Architecture)

Multi-Container 환경 및 Django App 패턴에 따라 유기적으로 설계된 파일 구조.

```text
645Lotto/
│
├── config/                  # Django 프로젝트 메인 설정 폴더
│   ├── __init__.py
│   ├── settings.py          # PostgreSQL 연동 및 환경 변수 설정
│   ├── urls.py              # 메인 라우팅 및 템플릿 URL include
│   └── wsgi.py
│
├── lotto/                   # 로또 핵심 비즈니스 로직 앱
│   ├── migrations/          # DB 테이블 설계도 스크립트 폴더
│   ├── templates/lotto/     # 프론트엔드 UI 화면
│   │   ├── buy.html         # 복권 구매 페이지 (수동/자동 폼 포함)
│   │   └── results.html     # 사용자 당첨 확인 내역 페이지
│   ├── __init__.py
│   ├── admin.py             # 관리자 추첨 및 save_model 오버라이딩 훅 설정
│   ├── apps.py
│   ├── models.py            # LottoRound, Ticket 관계형 데이터 모델 설계
│   ├── tests.py
│   ├── utils.py             # 교집합 연산 기반 로또 등수 판정 알고리즘
│   └── views.py             # 로그인 세션 검증 및 구매·결과 조회 처리 로직
│
├── manage.py                # Django CLI 진입 스크립트
├── Dockerfile               # Python 3.11-slim 기반의 웹 이미지 빌드 스펙
├── docker-compose.yml       # Web(Django) & DB(PostgreSQL) 멀티 컨테이너 정의서
└── requirements.txt         # 패키지 의존성 목록 (Django, psycopg2-binary)
```
## 🛠️ 3. 사전 준비 (Prerequisites)

본 프로젝트를 로컬 환경에서 실행하고 검증하기 위해서는 다음 프로그램의 설치가 필요.

- **Docker Desktop** (Windows / macOS / Linux)
- **Docker Compose v2** (최신 Docker Desktop 설치 시 기본 포함)

> 💡 **실행 전 체크**: 터미널 명령어를 입력하기 전에 반드시 Docker Desktop 앱이 PC 환경에서 구동 중이며, 시스템 트레이의 고래 아이콘이 **초록색(Engine Running)** 상태인지 확인.

---

## 🏃‍♂️ 4. 실행 방법 (Installation & Quick Start)

컨테이너 가상화 환경 구축부터 서버 구동, 데이터베이스 스키마 마이그레이션, 테스트용 최고 관리자 계정 생성까지의 인프라 구축 순서 가이드라인.

### 1) 저장소 복제 및 디렉토리 이동
원격 저장소에 등록된 로또 시스템 소스코드를 복제, 프로젝트의 Root Directory 내부로 이동.

### 2) Multi-Container 빌드 및 백그라운드 실행
웹 서버 역할을 담당하는 Django 애플리케이션 컨테이너와 데이터 스토리지를 담당하는 PostgreSQL 데이터베이스 인프라 컨테이너 유닛을 동시에 격리된 가상 네트워크 세트로 빌드하고 구동.

### 3) 데이터베이스 마이그레이션 (설계도 반영)
관계형 데이터베이스 인프라에 접속, Django 엔티티가 인식할 수 있는 로또 회차 엔티티 구조인 `LottoRound` 스키마 테이블 및 복권 구매 영수증 테이블인 `Ticket` 관계형 레코드 구조를 실시간 생성하기 위해 마이그레이션 엔진을 순차 실행.

### 4) 서비스 검증용 최고 관리자(Superuser) 계정 생성
과제 요구사항에 명시된 관리자 전용 제어 기능(회차별 추첨 실행, 전 회원 티켓 자동 당첨 정산 가동, 전체 판매 내역 모니터링) 검증용 계정을 확보하기 위해 장고 백엔드 커맨드 라인을 통해 관리자 마스터 아이디와 안전한 비밀번호를 세팅.

### 5) 브라우저 접속 주소 정보
- **일반 사용자 복권 구매 인터페이스**: http://localhost:8000/lotto/purchase/
- **일반 사용자 결과 대시보드**: http://localhost:8000/lotto/results/
- **관리자 전용 추첨 관리 컨트롤 타워**: http://localhost:8000/admin/

---

## 🧠 5. 핵심 알고리즘 샘플 코드 (Core Algorithms)

### ① 파이썬 집합(Set) 교집합 연산을 통한 당첨 등수 판정 알고리즘 (`lotto/utils.py`)
파이썬 언어가 자체 지원하는 핵심 해시 기반 자료구조인 `set` 객체를 매핑하여 당첨자 선별 대조 연산을 효율적이고 직관적으로 수행하는 백엔드 유틸리티 함수.

```python
def check_lotto_rank(ticket_numbers, winning_numbers, bonus_number):
    matched_count = len(set(ticket_numbers) & set(winning_numbers))
    has_bonus = bonus_number in ticket_numbers

    if matched_count == 6:
        return 1  # 1등
    elif matched_count == 5 and has_bonus:
        return 2  # 2등
    elif matched_count == 5:
        return 3  # 3등
    elif matched_count == 4:
        return 4  # 4등
    elif matched_count == 3:
        return 5  # 5등
    else:
        return None  # 낙첨
```

### ② 데이터 타입 불일치 방지 및 배치 정산 제어 로직 (`lotto/models.py`)
웹 브라우저 클라이언트의 폼(`POST`) 요청 파라미터 컨텍스트 데이터나 데이터베이스 적재 상태에 의해 불시에 발생할 수 있는 데이터 타입 혼선(String vs Integer 문자열-정수 충돌 예방) 버그를 완벽하게 차단하기 위해, 일괄 정산 직전 원시 데이터를 강제로 정수형 캐스팅(`int()`) 작업을 처리하는 견고한 데이터 방어 코드 스펙입니다.

```python
def settle_tickets(self):
        if not self.is_drawn:
            return  # 추첨이 완료되지 않은 경우 처리하지 않음

        from .utils import check_lotto_rank



        winning_numbers = [
            int(self.num1),
            int(self.num2),
            int(self.num3),
            int(self.num4),
            int(self.num5),
            int(self.num6)
        ]
        bonus_number = self.bonus_num
        tickets = self.tickets.all()

        for ticket in tickets:
            ticket_nums = [int(n) for n in ticket.get_numbers()]
            rank = check_lotto_rank(ticket_nums, winning_numbers, bonus_number)
            ticket.rank = rank
            ticket.save()
```

---

## ⚖️ 6. 라이센스 (License)

This project is licensed under the **MIT License**.  
자유로운 복제, 수정 및 배포가 가능하며 대학 오픈소스 소프트웨어 과제물 제출 및 개인 백엔드 개발 포트폴리오 아카이빙 목적으로 최적화되어 있습니다.
