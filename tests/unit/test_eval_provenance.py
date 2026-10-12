from eval.provenance import repository_state


def test_zip_without_git_metadata_has_unknown_provenance(tmp_path):
    assert repository_state(tmp_path) == ("unknown", "unknown")
