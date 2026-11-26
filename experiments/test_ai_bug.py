
import pytest
from scores import find_max, count_pass


# ==========================================
# 1. find_max() 테스트
# ==========================================

# 정상 테스트: 일반적인 점수 목록
def test_find_max_normal():
    assert find_max([70, 85, 60, 95]) == 95


# 정상 테스트: 첫 번째 값이 최댓값
def test_find_max_first():
    assert find_max([95, 80, 70, 60]) == 95


# 정상 테스트: 중간 값이 최댓값
def test_find_max_middle():
    assert find_max([70, 95, 80, 60]) == 95


# 경계값 테스트: 원소가 한 개
def test_find_max_single():
    assert find_max([80]) == 80


# 경계값 테스트: 원소가 두 개
def test_find_max_two():
    assert find_max([60, 90]) == 90


# 경계값 테스트: 모든 점수가 동일
def test_find_max_same():
    assert find_max([70, 70, 70]) == 70


# 경계값 테스트: 최저점과 최고점
def test_find_max_boundary():
    assert find_max([0, 50, 100]) == 100


# 예외 테스트: 빈 리스트
def test_find_max_empty():
    with pytest.raises(IndexError):
        find_max([])


# 예외 테스트: 잘못된 입력 자료형
def test_find_max_invalid_type():
    with pytest.raises(TypeError):
        find_max(None)


# ==========================================
# 2. count_pass() 테스트
# ==========================================

# 정상 테스트: 기본 합격 기준 적용
def test_count_pass_normal():
    assert count_pass([70, 85, 60, 95]) == 4


# 정상 테스트: 사용자 지정 합격 기준
def test_count_pass_custom_cutoff():
    assert count_pass([70, 80, 90], cutoff=80) == 2


# 정상 테스트: 전원 합격
def test_count_pass_all():
    assert count_pass([70, 80, 90]) == 3


# 정상 테스트: 전원 불합격
def test_count_pass_none():
    assert count_pass([30, 40, 50]) == 0


# 경계값 테스트: 합격 기준 직전, 일치, 직후
def test_count_pass_boundary():
    assert count_pass([59, 60, 61]) == 2


# 경계값 테스트: 합격 기준과 동일한 점수
def test_count_pass_exact_cutoff():
    assert count_pass([60]) == 1


# 경계값 테스트: 빈 리스트
def test_count_pass_empty():
    assert count_pass([]) == 0


# 경계값 테스트: 최저점과 최고점
def test_count_pass_min_max():
    assert count_pass([0, 100]) == 1


# 예외 테스트: 잘못된 점수 자료형
def test_count_pass_invalid_type():
    with pytest.raises(TypeError):
        count_pass([70, "80", 90])
