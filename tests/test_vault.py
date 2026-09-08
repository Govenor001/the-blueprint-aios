from scripts.index_vault import index_vault
from scripts.ingest_documents import ingest
from scripts.search_vault import search


def test_ingest_never_overwrites_and_searches_without_model(tmp_path, monkeypatch):
    incoming = tmp_path / "vault" / "documents"
    incoming.mkdir(parents=True)
    (incoming / "business.txt").write_text("Refunds are available within thirty days.", encoding="utf-8")
    result = ingest(tmp_path)
    assert result["processed"] == 1
    assert (incoming / "processed" / "business.txt").exists()
    (tmp_path / "vault" / "context" / "existing.md").write_text("Owner content", encoding="utf-8")
    monkeypatch.delenv("AIOS_LOCAL_MODEL_URL", raising=False)
    assert index_vault(tmp_path) == 2
    hits = search(tmp_path, "refunds")
    assert hits and "thirty days" in hits[0]["passage"]
