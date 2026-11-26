
import pytest
from load_scores import load_scores


# 테스트용 CSV 파일 생성 함수
def make_csv(tmp_path, content):
    path = tmp_path / "scores.csv"
    path.write_text(content, encoding="utf-8-sig")
    return path


# 1. 정상적인 데이터 처리
def test_normal_scores(tmp_path):
    path = make_csv(tmp_path, "이름,점수\n김철수,80\n이영희,95\n")

    kept, skipped = load_scores(path)

    assert kept == [("김철수", 80), ("이영희", 95)]
    assert skipped == []


# 2. 파일이 존재하지 않는 경우
def test_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


# 3. 헤더만 존재하는 경우
def test_header_only(tmp_path):
    path = make_csv(tmp_path, "이름,점수\n")

    assert load_scores(path) == ([], [])


# 4. 열 개수가 2개가 아닌 경우
def test_invalid_columns(tmp_path):
    path = make_csv(tmp_path, "이름,점수\n김철수\n이영희,90,100\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [
        (2, "김철수", "열 개수가 2가 아님"),
        (3, "이영희,90,100", "열 개수가 2가 아님")
    ]


# 5. 점수가 비어 있는 경우
def test_empty_score(tmp_path):
    path = make_csv(tmp_path, "이름,점수\n김철수,\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [(2, "김철수,", "점수가 비어 있음")]


# 6. 점수가 정수가 아닌 경우
@pytest.mark.parametrize("score", ["abc", "85.5"])
def test_invalid_score(tmp_path, score):
    path = make_csv(tmp_path, f"이름,점수\n김철수,{score}\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [
        (2, f"김철수,{score}", "점수가 정수가 아님")
    ]


# 7. 점수의 정상 경계값 검사
@pytest.mark.parametrize("score", [0, 1, 99, 100])
def test_valid_boundary(tmp_path, score):
    path = make_csv(tmp_path, f"이름,점수\n김철수,{score}\n")

    kept, skipped = load_scores(path)

    assert kept == [("김철수", score)]
    assert skipped == []


# 8. 점수의 범위를 벗어나는 경계값 검사
@pytest.mark.parametrize("score", [-1, 101])
def test_invalid_boundary(tmp_path, score):
    path = make_csv(tmp_path, f"이름,점수\n김철수,{score}\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [
        (2, f"김철수,{score}", "점수가 0~100 밖")
    ]


# 9. 이름이 비어 있는 경우
def test_empty_name(tmp_path):
    path = make_csv(tmp_path, "이름,점수\n,80\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [(2, ",80", "이름이 비어 있음")]


# 10. 동일한 이름이 중복되는 경우
def test_duplicate_names(tmp_path):
    path = make_csv(tmp_path, "이름,점수\n김철수,80\n김철수,90\n")

    kept, skipped = load_scores(path)

    assert kept == [("김철수", 80), ("김철수", 90)]
    assert skipped == []


# 11. 빈 줄이 포함된 경우
def test_blank_lines(tmp_path):
    path = make_csv(tmp_path, "이름,점수\n\n김철수,80\n\n")

    kept, skipped = load_scores(path)

    assert kept == [("김철수", 80)]
    assert skipped == []


# 12. 이름과 점수에 공백이 포함된 경우
def test_whitespace(tmp_path):
    path = make_csv(tmp_path, "이름,점수\n 김철수 , 80 \n")

    kept, skipped = load_scores(path)

    assert kept == [("김철수", 80)]
    assert skipped == []


# 13. 정상 데이터와 잘못된 데이터가 섞인 경우
def test_mixed_data(tmp_path):
    path = make_csv(
        tmp_path,
        "이름,점수\n김철수,80\n\n이영희,101\n박민수,90\n최지수,abc\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [("김철수", 80), ("박민수", 90)]
    assert skipped == [
        (4, "이영희,101", "점수가 0~100 밖"),
        (6, "최지수,abc", "점수가 정수가 아님")
    ]
