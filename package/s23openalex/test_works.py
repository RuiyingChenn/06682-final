"""
File to test work class.
"""
from .works import Works


def test_works_init():
    """Test initialization of work class."""
    oaid = "https://doi.org/10.1021/acscatal.5b00538"
    work = Works(oaid)

    assert work.oaid == oaid
    assert work.req is not None
    assert work.data is not None


def test_works_repr():
    """Test repr function of work class."""
    oaid = "https://doi.org/10.1021/acscatal.5b00538"
    work = Works(oaid)

    repr_str = repr(work)
    string = (
        "John R. Kitchin, Examples of Effective Data Sharing in Scientific Publishing, "
        "5, 6, 3894-3899, (2015), https://doi.org/10.1021/acscatal.5b00538. "
        "cited by: 18. https://openalex.org/W2288114809"
    )

    assert repr_str == string
    assert isinstance(repr_str, str)
    assert work.oaid in repr_str
