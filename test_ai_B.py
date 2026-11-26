
import pytest
from load_scores import load_scores


# 테스트용 CSV 파일 생성 함수
def make_csv(tmp_path, content):
    path = tmp_path / "scores.csv"
    path.write_text(content, encoding="utf-8")
    return path


# 제외된 데이터의 기록 검증 함수
def check_skipped(record, line_number, original):
    number, raw, reason = record

    assert number == line_number
    assert raw.rstrip("\r\n") == original
    assert isinstance(reason, str)
    assert reason.strip() != ""


# 1. 정상적인 데이터 처리
def test_normal_scores(tmp_path):
    path = make_csv(
        tmp_path,
        "name,score\nKim,80\nLee,95\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [("Kim", 80), ("Lee", 95)]
    assert skipped == []
    assert all(type(score) is int for _, score in kept)


# 2. 파일이 존재하지 않는 경우
def test_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


# 3. 헤더만 존재하는 경우
def test_header_only(tmp_path):
    path = make_csv(tmp_path, "name,score\n")

    assert load_scores(path) == ([], [])


# 4. 빈 줄이 존재하는 경우
def test_empty_lines(tmp_path):
    path = make_csv(
        tmp_path,
        "name,score\n\nKim,80\n\nLee,90\n\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [("Kim", 80), ("Lee", 90)]
    assert skipped == []


# 5. 열 개수가 2개가 아닌 경우
@pytest.mark.parametrize("row", [
    "Kim",
    "Kim,80,90",
])
def test_invalid_columns(tmp_path, row):
    path = make_csv(tmp_path, f"name,score\n{row}\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1
    check_skipped(skipped[0], 2, row)


# 6. 이름 또는 점수가 비어 있는 경우
@pytest.mark.parametrize("row", [
    ",80",
    "Kim,",
    ",",
])
def test_missing_values(tmp_path, row):
    path = make_csv(tmp_path, f"name,score\n{row}\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1
    check_skipped(skipped[0], 2, row)


# 7. 점수가 정수가 아닌 경우
@pytest.mark.parametrize("score", [
    "abc",
    "80.5",
    "90.0",
])
def test_non_integer_score(tmp_path, score):
    row = f"Kim,{score}"
    path = make_csv(tmp_path, f"name,score\n{row}\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1
    check_skipped(skipped[0], 2, row)


# 8. 정상 범위의 경계값
@pytest.mark.parametrize("score", [0, 1, 99, 100])
def test_valid_boundary_scores(tmp_path, score):
    path = make_csv(
        tmp_path,
        f"name,score\nKim,{score}\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [("Kim", score)]
    assert skipped == []
    assert type(kept[0][1]) is int


# 9. 점수가 허용 범위를 벗어나는 경우
@pytest.mark.parametrize("score", [-1, 101])
def test_out_of_range(tmp_path, score):
    row = f"Kim,{score}"
    path = make_csv(tmp_path, f"name,score\n{row}\n")

    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 1
    check_skipped(skipped[0], 2, row)


# 10. 동일한 이름이 여러 번 등장하는 경우
def test_duplicate_names(tmp_path):
    path = make_csv(
        tmp_path,
        "name,score\nKim,80\nKim,90\nKim,80\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [
        ("Kim", 80),
        ("Kim", 90),
        ("Kim", 80),
    ]
    assert skipped == []


# 11. 따옴표로 감싼 이름에 쉼표가 있는 경우
def test_quoted_name_with_comma(tmp_path):
    path = make_csv(
        tmp_path,
        'name,score\n"Kim, Min",85\n'
    )

    kept, skipped = load_scores(path)

    assert kept == [("Kim, Min", 85)]
    assert skipped == []


# 12. 정상 데이터와 잘못된 데이터가 섞인 경우
def test_mixed_data(tmp_path):
    path = make_csv(
        tmp_path,
        "name,score\n"
        "Kim,80\n"
        "Lee,abc\n"
        "\n"
        "Park,100\n"
        "Choi,101\n"
        ",90\n"
        "Han,0\n"
    )

    kept, skipped = load_scores(path)

    assert kept == [
        ("Kim", 80),
        ("Park", 100),
        ("Han", 0),
    ]

    assert len(skipped) == 3

    check_skipped(skipped[0], 3, "Lee,abc")
    check_skipped(skipped[1], 6, "Choi,101")
    check_skipped(skipped[2], 7, ",90")
