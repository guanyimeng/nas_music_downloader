from music_downloader.model import Base


def test_model_package_exports_base_with_registered_tables() -> None:
    assert Base is not None
    assert "users" in Base.metadata.tables
    assert "download_history" in Base.metadata.tables
