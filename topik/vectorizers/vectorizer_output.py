import itertools

def _accumulate_terms(tokenized_corpus):
    global_terms=set()
    document_term_counts = {}
    for doc_id, doc in tokenized_corpus:
        doc_terms = set(doc)
        global_terms.update(doc_terms)
        document_term_counts[doc_id] = len(doc_terms)
    id_term_map = {term_id: term for term_id, term in enumerate(global_terms)}
    return id_term_map, document_term_counts


class VectorizerOutput(object):
    def __init__(self, tokenized_corpus=None, vectorizer_func=None, id_term_map=None,
                 document_term_counts=None, vectors=None):
        if tokenized_corpus and vectorizer_func and not vectors:
            iter1, iter2 = itertools.tee(tokenized_corpus)
            self.id_term_map, self._document_term_counts = _accumulate_terms(iter1)
            self.term_id_map = {term: term_id for term_id, term in self.id_term_map.items()}
            self._vectors = vectorizer_func(iter2, self)
        elif id_term_map and document_term_counts and vectors:
            self.id_term_map = id_term_map
            self.term_id_map = {term: term_id for term_id, term in self.id_term_map.items()}
            self._global_terms = set(id_term_map.values())
            self._document_term_counts = document_term_counts
            self._vectors = vectors
        else:
            raise ValueError("Must provide either tokenized corpora and vectorizer func, "
                             "or global term collection, document term counts, and vectors.")
            self._global_terms = []

    def __iter__(self):
        for doc_id, vector in self._vectors.items():
            yield doc_id, vector

    def __len__(self):
        return len(self._vectors)

    @property
    def global_term_count(self):
        return len(self.id_term_map)

    @property
    def document_term_counts(self):
        return self._document_term_counts

    @property
    def vectors(self):
        return self._vectors
