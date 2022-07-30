# -*- coding: utf-8 -*

from official_sponsors.models import OfficialSponsorNames
from identified_sponsors.models import IdentifiedSponsors
from article_sponsors.models import ArticleSponsors

from scielo_scholarly_data import standardizer
import kshingle as ks
from sentence_transformers import SentenceTransformer, util
from operator import itemgetter


model = SentenceTransformer('scms-sponsors-1/stmodels/paraphrase-multilingual-MiniLM-L12-v2')


def make_standard_sponsor(name, acron):
    """
    Função para montar uma lista de dicionários a partir de uma string que descreve o nome de um financiador e seu acrônimo.

    Parameters
    ----------
    sponsor : str
        Nome e acrônimo padronizados de um financiador.
        Exemplo:
            "Conselho Nacional de Desenvolvimento Científico e Tecnológico,CNPq"

    Returns
    -------
    list
        Uma lista de dicionários nos quais a chave "text" descreve as possíveis combinações de nome e acrônimo.
        [{
            "text": "Conselho Nacional de Desenvolvimento Científico e Tecnológico CNPq",
            "name": "Conselho Nacional de Desenvolvimento Científico",
            "acronym": "CNPq"
        },
        {
            "text": "Conselho Nacional de Desenvolvimento Científico e Tecnológico",
            "name": "Conselho Nacional de Desenvolvimento Científico",
            "acronym": "CNPq"
        },
        {
            "text": "CNPq",
            "name": "Conselho Nacional de Desenvolvimento Científico",
            "acronym": "CNPq"
        }]
    """
    result = [
        {
            "text": name + " " + acron,
            "name": name,
            "acronym": acron
        },
        {
            "text": name,
            "name": name,
            "acronym": acron
        },
        {
            "text": acron,
            "name": name,
            "acronym": acron
        }
    ]
    return result


def search_sponsors_by_jaccard_similarity(name, sponsors):
    """
    Procedimento para obter o nome completo e o acrônimo do financiador de uma pesquisa,
    considerando o coeficiente de similaridade de Jaccard

    Parameters
    ----------
    name : str
        Nome da instituição financiadora, da forma que foi declarada, para padronização.
    sponsors : list
        Uma lista de dicionários nos quais a chave "text" descreve as possíveis combinações de nome e acrônimo.

    Returns
    -------
    list
        Uma lista ordenada de dicionários nos quais os nomes e acrônimos são associados a uma medida de similaridade.
        [{
            "standard_name": "Conselho Nacional de Desenvolvimento Científico e Tecnológico",
            "standard_acronym": "CNPq",
            "score": 1.0
        },
        {
            "standard_name": "Coordenação de Aperfeiçoamento de Pessoal de Nível Superior",
            "standard_acronym": "CAPES",
            "score": 0.01
        },
        {
            "standard_name": "Fundação de Amparo à Pesquisa do Estado de São Paulo",
            "standard_acronym": "FAPESP",
            "score": 0.05
        }]
    """
    name = standardizer.document_sponsors(name)
    if len(name) > 0:
        result = []
        for sponsor in sponsors:
            jaccard_index = ks.jaccard_strings(standardizer.document_sponsors(sponsor["text"]), name, k=2)
            d = {
                "standard_name": sponsor["name"],
                "standard_acronym": sponsor["acronym"],
                "score": jaccard_index
            }
            result.append(d)
        return sorted(result, key=itemgetter('score'), reverse=True)


def search_sponsors_by_semantic_similarity(name, sponsors):
    """
    Procedimento para obter o nome completo e o acrônimo do financiador de uma pesquisa,
    considerando a similaridade baseada em semântica textual.
    (https://www.sbert.net/examples/training/sts/README.html)

    Parameters
    ----------
    name : str
        Nome da instituição financiadora, da forma que foi declarada, para padronização.
    sponsors : list
        Uma lista de dicionários nos quais a chave "text" descreve as possíveis combinações de nome e acrônimo.

    Returns
    -------
    list
        Uma lista ordenada de dicionários nos quais os nomes e acrônimos são associados a uma medida de similaridade.
        [{
            "standard_name": "Conselho Nacional de Desenvolvimento Científico e Tecnológico",
            "standard_acronym": "CNPq",
            "score": 1.0
        },
        {
            "standard_name": "Coordenação de Aperfeiçoamento de Pessoal de Nível Superior",
            "standard_acronym": "CAPES",
            "score": 0.01
        },
        {
            "standard_name": "Fundação de Amparo à Pesquisa do Estado de São Paulo",
            "standard_acronym": "FAPESP",
            "score": 0.05
        }]
    """
    query_embedding = model.encode(name, convert_to_tensor=True)
    texts = [item["text"] for item in sponsors]
    corpus_embeddings = model.encode(texts, convert_to_tensor=True)
    search_hits = util.semantic_search(query_embedding, corpus_embeddings)
    search_hits = search_hits[0]  # Get the hits for the first query

    result = []

    for hit in search_hits:
        related_sponsor = sponsors[hit['corpus_id']]
        d = {
            "standard_name": related_sponsor['name'],
            "standard_acronym": related_sponsor['acronym'],
            "score": hit['score']
        }
        result.append(d)

    return result


def get_sponsor_names_with_score(name, sponsors):
    """
    Procedimento para obter o nome completo e o acrônimo do financiador de uma pesquisa,
    a partir da escolha de um método específico (jaccard ou semantic).

    Parameters
    ----------
    name : str
        Nome da instituição financiadora, da forma que foi declarada, para padronização.
    sponsors : list
        Uma lista de dicionários nos quais a chave "text" descreve as possíveis combinações de nome e acrônimo.
    method : str
        "jaccard" - similaridade de Jaccard
        "semantic" - similaridade semântica textual

    Returns
    -------
    list
        Uma lista ordenada de dicionários nos quais os nomes e acrônimos são associados a uma medida de similaridade.
        [{
            "standard_name": "Conselho Nacional de Desenvolvimento Científico e Tecnológico",
            "standard_acronym": "CNPq",
            "score": 1.0
        },
        {
            "standard_name": "Coordenação de Aperfeiçoamento de Pessoal de Nível Superior",
            "standard_acronym": "CAPES",
            "score": 0.01
        },
        {
            "standard_name": "Fundação de Amparo à Pesquisa do Estado de São Paulo",
            "standard_acronym": "FAPESP",
            "score": 0.05
        }]
    """
    jaccard = search_sponsors_by_jaccard_similarity(name, sponsors)
    semantic = search_sponsors_by_semantic_similarity(name, sponsors)
    if float(jaccard[0]['score']) >= float(semantic[0]['score']):
        return jaccard[0], 'jaccard'
    else:
        return semantic[0], 'semantic'


def get_official_sponsors():
    officials = []
    for item in OfficialSponsorNames.objects.all():
        name = item.official_sponsor_name
        acron = item.official_sponsor_acron
        officials.extend(make_standard_sponsor(name, acron))
    return officials


def check_for_sponsor_identified(name):
    sponsor_identified = IdentifiedSponsors.objects.filter(declared_name=name)
    try:
        sponsor_identified = sponsor_identified[0]
    except IndexError:
        sponsors_official = OfficialSponsorNames.objects.all()
        sponsor_standard = get_sponsor_names_with_score(name, sponsors_official)
        sponsor_identified = IdentifiedSponsors()
        sponsor_identified.declared_name = name
        sponsor_identified.official_name = sponsor_standard[0]['standard_name']
        sponsor_identified.official_acron = sponsor_standard[0]['standard_acronym']
        sponsor_identified.method = sponsor_standard[1]
        sponsor_identified.score = sponsor_standard[0]['score']
        sponsor_identified.save()
    return sponsor_identified


def load_sponsor(pid, name, proj=None):
    article_sponsor = ArticleSponsors.objects.filter(pid=pid)
    try:
        article_sponsor = article_sponsor[0]
    except IndexError:
        article_sponsor = ArticleSponsors()
        article_sponsor.pid = pid
        article_sponsor.project_id = proj
    article_sponsor.sponsor_name = check_for_sponsor_identified(name)
    article_sponsor.save()


def run():
    with open('identified_sponsors/scripts/examples.csv', 'r') as csvfile:
        data = csv.DictReader(csvfile)

        for row in data:
            load_sponsor(row.get('pid'), row.get('name'), row.get('proj'))


if __name__ == '__main__':
    run()
