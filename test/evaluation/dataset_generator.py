from langchain_core.messages import HumanMessage, SystemMessage
from src.services.opensearch import OpenSearchClient
from src.services.llm_factory import create_llm
from src.config import JSON_EXTRACTED_CONTENT, CONTENT_INDEX, setup_logger
from test.evaluation.prompts_eval import *
from test.evaluation.output_structured import EvalOutputStructured
import pandas
import json
import random
from typing import List, Dict

logger = setup_logger(__name__)


def get_all_chunks_from_pdf(json_file: str):
    file_path = JSON_EXTRACTED_CONTENT / json_file
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return None
        
    logger.info(f"File Json detected: {file_path.name}")
    with open(file_path, 'r', encoding='utf-8') as f:
        dolphin_json = json.load(f)

    book_id = dolphin_json.get("source_file")
    all_chunks_indexed = opensearch_client.collect_all(CONTENT_INDEX, book_id)
    
    total_pages = 0
    if all_chunks_indexed:
        total_pages = max(
            chunk["_source"].get("page_number", 0) 
            for chunk in all_chunks_indexed
        )
        
    logger.info(f"Recuperados {len(all_chunks_indexed)} chunks. Total de páginas: {total_pages}")
    return all_chunks_indexed, total_pages


def select_chunks_by_pages(start_page: int, groupby: int, last_page: int, chunks: List[Dict]) -> List[Dict]:
    """
    Select chunks from referred pages.
    <args>
        start_page = Initial search page
        groupby = how many pages you want extract chunks
        last_page = Limit pages in the pdf
        chunks = list of all chunks in pdf
    
    return = sub set list of chunks
    """
    end_page = min(start_page + groupby - 1, last_page)

    selected_chunks = [
        chunk for chunk in chunks
        if chunk.get("_source", {}).get("page_number") is not None 
        and start_page <= chunk["_source"]["page_number"] <= end_page
    ]

    selected_chunks.sort(
        key=lambda x: (
            x.get("_source", {}).get("page_number", 0),
            x.get("_source", {}).get("reading_order", 0)
        )
    )
    return selected_chunks


def select_random_context(window_chunks: List[Dict], max_chunks: int = 7) -> List[Dict]:
    """
    Given a list of chunks (e.g., snippets from a 3-page window), it randomly samples 'max_chunks'.
    If there are fewer chunks than the desired amount, it safely returns all available chunks.
    Finally, it sorts the result chronologically to maintain reading coherence for the LLM.
    """
    total_available = len(window_chunks)
    if total_available == 0:
        return []

    num_to_sample = min(max_chunks, total_available)
    
    sampled_chunks = random.sample(window_chunks, num_to_sample)
    
    sampled_chunks.sort(
        key=lambda x: (
            x.get("_source", {}).get("page_number", 0), 
            x.get("_source", {}).get("reading_order", 0)
        )
    )
    return sampled_chunks


def main(file_json: str, batch_size: int = 5):
    opensearch_client = OpenSearchClient()
    chat = create_llm(model="got-4o-mini")
    structured_chat = chat.with_structured_output(EvalOutputStructured)
    chunks, max_pages = get_all_chunks_from_pdf(json_file=file_json)

    logger.info("Generating question-answer data...")
    total_chunks = len(chunks)
    pages_to_group_by = 3

    for sliced_set in range(0, total_chunks, pages_to_group_by):
        batch_package_chunks = list()
        target_chunks = select_chunks_by_pages(
            start_page=sliced_set,
            groupby=pages_to_group_by,
            last_page=total_chunks,
            chunks=chunks
        )

        system_prompt = [SystemMessage(EVAL_DATA_GEN_SYS)]
        for index in range(batch_size):
            chunks_set = select_random_context(window_chunks=target_chunks)
            window_list = [content["content"] for content in chunks_set]
            formatted_user_prompt = USER_QA_TASK.format(chunk_list=window_list)
            user_request_prompt =  [HumanMessage()]
            batch_package_chunks.append()
            

        pass
