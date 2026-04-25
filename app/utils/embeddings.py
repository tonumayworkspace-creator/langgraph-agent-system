def get_embeddings():
    class DummyEmbedding:
        def embed_query(self, text):
            return [0.0] * 384  # fixed vector
    return DummyEmbedding()