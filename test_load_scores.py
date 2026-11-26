# 노담희 2024180122

import pytest
from load_scores import load_scores


# 정상 ①
def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5


# 정상 ②
def test_빈_줄은_건너뛴다(tmp_path):
    path = tmp_path / "blank.csv"
    path.write_text(
        "name,score\n김민수,85\n\n이서연,90\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(path)

    assert kept == [("김민수", 85), ("이서연", 90)]
    assert skipped == []


# 정상 ③
def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    path = tmp_path / "comma.csv"
    path.write_text(
        'name,score\n"김,민수",85\n',
        encoding="utf-8"
    )

    kept, skipped = load_scores(path)

    assert kept == [("김,민수", 85)]
    assert skipped == []


# 예외 ①
def test_없는_파일이면_오류가_난다(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


# 예외 ②
def test_헤더만_있으면_빈_결과이다():
    kept, skipped = load_scores("empty.csv")

    assert kept == []
    assert skipped == []


# 경계값 테스트
@pytest.mark.parametrize("score, valid", [
    (-1, False),
    (0, True),
    (1, True),
    (99, True),
    (100, True),
    (101, False),
])
def test_점수_경계값(tmp_path, score, valid):
    path = tmp_path / "boundary.csv"
    path.write_text(
        f"name,score\n김민수,{score}\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(path)

    if valid:
        assert kept == [("김민수", score)]
        assert skipped == []
    else:
        assert kept == []
        assert len(skipped) == 1

def test_이름이_비어_있는_경우(tmp_path):
    path = tmp_path / "no_name.csv"
    path.write_text(
        "name,score\n,85\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [(2, ",85", "이름이 비어 있음")]


def test_프로그램_직접_실행(tmp_path, monkeypatch, capsys):
    import runpy

    path = tmp_path / "sample.csv"
    path.write_text(
        "name,score\n김민수,85\n,90\n",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        "sys.argv", ["load_scores.py", str(path)]
    )

    runpy.run_path("load_scores.py", run_name="__main__")

    output = capsys.readouterr().out

    assert "읽은 줄 : 1개" in output
    assert "건너뛴 줄 : 1개" in output
    assert "김민수 85" in output
    assert "이름이 비어 있음" in output