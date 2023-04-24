"""
This is test file for bibtex functionality.
"""
from s23openalex import Works


BIBTEX = """@article{kitchin-2015-examples,
 authors = {John R. Kitchin, },
 doi = {10.1021/acscatal.5b00538},
 journal = {ACS Catalysis},
 number = {6},
 pages = {3894-3899},
 title = {Examples of Effective Data Sharing in Scientific Publishing},
 url = {https://doi.org/10.1021/acscatal.5b00538},
 volume = {5},
 year = {2015}
}
"""


def test_bibtex():
    """Test getting bibtex."""
    mywork = Works("https://doi.org/10.1021/acscatal.5b00538")
    assert BIBTEX == mywork.bibtex
