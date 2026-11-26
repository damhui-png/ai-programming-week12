# ai-programming-week12
AI 협업 프로그래밍 12주차 테스트 코드 작성 및 GitHub 문서화

# 성적 관리 프로그램

## ① 무엇을 하나요 (What)

성적 CSV 파일을 읽어 정상적인 학생 이름과 점수를 반환하고, 잘못된 데이터는 제외 사유와 함께 기록하는 프로그램이다.

## ② 왜 만들었나요 (Why)

성적 데이터에 빈칸이나 잘못된 점수가 포함되어 있을 경우 이를 구분하여 처리할 필요가 있다. 또한 프로그램이 정상적으로 실행되는 것만으로는 정확성을 보장하기 어렵기 때문에 테스트 코드를 통해 다양한 입력 상황에서 올바르게 동작하는지 확인하고자 하였다.

## ③ 어떻게 쓰나요 (How)

Python 3.9.6 환경에서 실행 및 검증하였다.

### 설치

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest==8.4.2 pytest-cov==7.1.0
```

### 실행

```bash
python load_scores.py scores.csv
```

## ④ 어떻게 테스트하나요

```bash
python -m pytest
```

커버리지 측정:

```bash
python -m pytest --cov=load_scores --cov-report=term-missing
```

### 실제 테스트 결과

| 구분 | 통과한 테스트 | 커버리지 |
|---|---:|---:|
| 설계표 기반 테스트 | 13개 | 100% |
| 프롬프트 A | 18개 | 80% |
| 프롬프트 B | 21개 | 80% |
| 전체 테스트 | 52개 | 100% |

```text
load_scores.py    45    0    100%
TOTAL             45    0    100%
52 passed in 0.16s
```

함정 실험에서는 고장난 함수의 논리 오류를 확인하기 위해 별도로 테스트를 실행하였다. 18개 중 11개가 통과하고 7개가 실패하였다.

함정 실험 파일은 experiments 폴더에 보관하며 일반적인 pytest 실행에서는 제외한다. 원본 AI 테스트의 잘못된 모듈 이름을 실행 시 연결하여 검증하였다.

## ⑤ 파일 구성

| 파일 | 역할 |
|---|---|
| load_scores.py | 성적 CSV 처리 함수 |
| scores.csv | 기본 성적 데이터 |
| empty.csv | 헤더만 있는 테스트 데이터 |
| weird.csv | 비정상 데이터 검증용 파일 |
| test_load_scores.py | 설계표 기반 및 커버리지 보완 테스트 |
| test_ai_A.py | 코드를 제공하여 생성한 AI 테스트 |
| test_ai_B.py | 명세를 제공하여 생성한 AI 테스트 |
| experiments/ | 고장난 코드 및 함정 실험 |
| pytest.ini | 테스트 실행 범위 설정 |
| README.md | 프로그램 사용 및 테스트 안내 |
| LICENSE | MIT 라이선스 |

## ⑥ 만든 사람 · AI를 어디에 썼는지

- 만든 사람: 노담희
- AI를 쓴 곳: 테스트 코드 작성 지원, 프롬프트 A/B 실험, 오류 원인 분석 및 문서 작성 지원
- 내가 직접 수행한 것: 테스트 실행, 커버리지 측정, 기대값과 실제 결과 비교, GitHub 커밋 및 업로드

Assisted-by: ChatGPT

## 라이선스

MIT License (LICENSE 파일 참고)
