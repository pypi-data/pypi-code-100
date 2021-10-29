import json
from math import isclose
from pathlib import Path

import pytest as pytest
from pyformatters_summarizer.summarizer import SummarizerFormatter, \
    SummarizerParameters, TrfModel
from pymultirole_plugins.v1.schema import Document, DocumentList
from starlette.responses import Response


# @pytest.mark.skip(reason="Not a test")
def test_summarizer_french():
    parameters = SummarizerParameters(model=TrfModel.camembert2camembert_shared_finetuned_french_summarization)
    formatter = SummarizerFormatter()
    doc = Document(text="""Un nuage de fumée juste après l’explosion, le 1er juin 2019.
        Une déflagration dans une importante usine d’explosifs du centre de la Russie a fait au moins 79 blessés samedi 1er juin.
        L’explosion a eu lieu dans l’usine Kristall à Dzerzhinsk, une ville située à environ 400 kilomètres à l’est de Moscou, dans la région de Nijni-Novgorod.
        « Il y a eu une explosion technique dans l’un des ateliers, suivie d’un incendie qui s’est propagé sur une centaine de mètres carrés », a expliqué un porte-parole des services d’urgence.
        Des images circulant sur les réseaux sociaux montraient un énorme nuage de fumée après l’explosion.
        Cinq bâtiments de l’usine et près de 180 bâtiments résidentiels ont été endommagés par l’explosion, selon les autorités municipales. Une enquête pour de potentielles violations des normes de sécurité a été ouverte.
        Fragments de shrapnel Les blessés ont été soignés après avoir été atteints par des fragments issus de l’explosion, a précisé une porte-parole des autorités sanitaires citée par Interfax.
        « Nous parlons de blessures par shrapnel d’une gravité moyenne et modérée », a-t-elle précisé.
        Selon des représentants de Kristall, cinq personnes travaillaient dans la zone où s’est produite l’explosion. Elles ont pu être évacuées en sécurité.
        Les pompiers locaux ont rapporté n’avoir aucune information sur des personnes qui se trouveraient encore dans l’usine.
        """)
    resp: Response = formatter.format(doc, parameters)
    assert resp.status_code == 200
    assert resp.media_type == "text/plain"
    summary = resp.body.decode(resp.charset)
    assert len(summary) > 0
    # assert len(summary) >= parameters.min_length*len(doc.text)
    # assert isclose(len(summary), parameters.max_length*len(doc.text), rel_tol=3e-01)


# @pytest.mark.skip(reason="Not a test")
def test_summarizer_english():
    parameters = SummarizerParameters()
    formatter = SummarizerFormatter()
    doc = Document(text="""The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris.
    Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930.
    It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft).
    Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct.
        """)
    resp: Response = formatter.format(doc, parameters)
    assert resp.status_code == 200
    assert resp.media_type == "text/plain"
    summary = resp.body.decode(resp.charset)
    assert len(summary) >= parameters.min_length * len(doc.text)
    assert isclose(len(summary), parameters.max_length * len(doc.text), rel_tol=3e-01)

    docs = formatter.process([doc], parameters)
    summary = docs[0].metadata["summary"]
    assert len(summary) >= parameters.min_length * len(doc.text)
    assert isclose(len(summary), parameters.max_length * len(doc.text), rel_tol=3e-01)


@pytest.mark.skip(reason="Not a test")
def test_summarizer_kantar():
    testdir = Path(__file__).parent / 'data'
    json_file = testdir / "thermogenesistxt-documents.json"
    with json_file.open("r") as fin:
        docs = json.load(fin)
    docs = [Document(**doc) for doc in docs]
    parameters = SummarizerParameters(model=TrfModel.distilbart_xsum_12_6)
    formatter = SummarizerFormatter()
    # rows = []
    for doc in docs:
        resp: Response = formatter.format(doc, parameters)
        assert resp.status_code == 200
        summary = resp.body.decode(resp.charset)
        doc.metadata['summary'] = summary
        # rows.append({
        #     'Title': doc.title,
        #     'Content': doc.text,
        #     'Summary': summary
        # })
    # row_file = testdir / f"{json_file.stem}_{parameters.model.value.replace('/', '_')}.xlsx"
    # df = pd.DataFrame.from_records(rows)
    # df.to_excel(row_file)
    sum_file = testdir / f"{json_file.stem}_{parameters.model.value.replace('/', '_')}.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


# @pytest.mark.skip(reason="Not a test")
def test_summarizer_pubmed():
    parameters = SummarizerParameters(model=TrfModel.pegasus_pubmed)
    formatter = SummarizerFormatter()
    doc = Document(text="""Gene duplications and gene losses have been frequent events in
    the evolution of animal genomes, with the balance between these two dynamic processes contributing to major
    differences in gene number between species. After gene duplication, it is common for both daughter genes to
    accumulate sequence change at approximately equal rates. In some cases, however, the accumulation of sequence
    change is highly uneven with one copy radically diverging from its paralogue. Such 'asymmetric evolution' seems
    commoner after tandem gene duplication than after whole-genome duplication, and can generate substantially novel
    genes. We describe examples of asymmetric evolution in duplicated homeobox genes of moths, molluscs and mammals,
    in each case generating new homeobox genes that were recruited to novel developmental roles. The prevalence of
    asymmetric divergence of gene duplicates has been underappreciated, in part, because the origin of highly
    divergent genes can be difficult to resolve using standard phylogenetic methods.This article is part of the
    themed issue 'Evo-devo in the genomics era, and the origins of morphological diversity'.""")
    resp: Response = formatter.format(doc, parameters)
    assert resp.status_code == 200
    assert resp.media_type == "text/plain"
    summary = resp.body.decode(resp.charset)
    assert len(summary) >= parameters.min_length * len(doc.text)
    assert isclose(len(summary), parameters.max_length * len(doc.text), rel_tol=3e-01)
