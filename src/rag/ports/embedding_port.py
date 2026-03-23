class EmbeddingPort:
    def __init__(self, VectorProcessorAdapter):
        self.VectorProcessor = VectorProcessorAdapter

    def convert_query(self, query: str):
        return self.VectorProcessor.embedding_model.embed_query(query)
