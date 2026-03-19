def list_content(chunks):
    all_content = []
    for chunk in chunks:
        source = chunk["_source"]['content']
        all_content.append(source)
    return all_content


def rag_search(adapter_search_client):
    def search(
        index_name: str, query_vector: List[float],
        book_id: str, query_text: str = None):
        """
        <Args>:
            index_name: index should perform the search (required)
            book_id: id of the pdf (required)
            query_vector: vector of the input question (required)
            query_text: Optional text for hybrid search (BM25 + vector) (optional)
        """
        chunk_list = adapter_search_client.semantic_search(
            index_name=index_name,
            query_vector=query_vector,
            book_id=book_id,
            query_text=query_text
        )
        all_content = list_content(chunk_list)
        return all_content
    return search


