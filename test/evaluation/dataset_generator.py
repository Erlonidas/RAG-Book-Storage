from langchain_core.messages import HumanMessage, SystemMessage
from src.services.opensearch import OpenSearchClient
from src.services.llm_factory import create_llm
from src.config import JSON_EXTRACTED_CONTENT, CONTENT_INDEX, EVAL_DATA_DIR, setup_logger
from test.evaluation.prompts_eval import *
from test.evaluation.output_strutured import EvalOutputStructured
from pathlib import Path
import pandas as pd
import json
import random
from typing import List, Dict, Union

logger = setup_logger(__name__)
opensearch_client = OpenSearchClient()


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


def feed_dataset(
    batch_responses: List[Union[EvalOutputStructured, Exception]],
    target_chunks: List[List[dict]],
    destiny_directory) -> None:
    """
    Appends new data to the final evaluation dataset.
    This dataset is a .csv file, generated using pandas dataframe.
    
    <args>
        batch_responses = All responses from LLM about generated questions followed by ground truth answers
        target_chunks = List of chunk lists used for each question generation (must parallel batch_responses)
        destiny_directory = The folder where the dataset should be saved (Path or str)
    """
    records = []
    
    for response, chunks in zip(batch_responses, target_chunks):
        
        # 1. DEFESA: Ignora se o LangChain retornou erro de rede/API neste item específico do batch
        if isinstance(response, Exception):
            logger.warning(f"LLM call could not resolve this question in generation process of data: {response}")
            continue
            
        # 2. EXTRAÇÃO: Pega os dados do Pydantic (com fallback para dict caso mude no futuro)
        try:
            question = response.question if hasattr(response, 'question') else response.get("question")
            ground_truth = response.ground_truth_answer if hasattr(response, 'ground_truth_answer') else response.get("ground_truth_answer")
        except AttributeError:
            logger.error("Unexpected attribute in output structure of the LLM (question/ground_truth_answer).")
            continue

        # 3. CONTEXTO E METADADOS: Extrai o texto limpo e rastreabilidade
        contexts_list = []
        metadata_list = []
        
        for chunk in chunks:
            source = chunk.get("_source", {})
            content = source.get("content")
            
            if content:
                contexts_list.append(content)
                # Salva de onde esse chunk veio para debug futuro
                metadata_list.append({
                    "chunk_id": chunk.get("_id", ""),
                    "page_number": source.get("page_number"),
                    "reading_order": source.get("reading_order")
                })
        
        # 4. MONTAGEM: O schema universal que o RAGAS/Phoenix ama + Debug
        records.append({
            "question": question,
            "ground_truth": ground_truth,
            "contexts": contexts_list,
            "metadata": metadata_list  # <--- SEU SALVA-VIDAS AQUI
        })
        
    # Se todos os itens falharam, não faz nada
    if not records:
        logger.warning("There is no batch data to register")
        return

    # Converte para DataFrame
    df = pd.DataFrame(records)
    
    # Garante que o diretório de destino existe (cria se não existir)
    dest_path = Path(destiny_directory)
    dest_path.mkdir(parents=True, exist_ok=True)
    
    file_path = dest_path / "ground_truth_dataset.csv"
    
    # 5. APPEND INTELIGENTE NO CSV
    if file_path.exists():
        # Se já existe, anexa no final (mode='a') e não repete o cabeçalho (header=False)
        df.to_csv(file_path, mode='a', header=False, index=False, encoding='utf-8')
        logger.info(f"Adicionados {len(df)} novos registros ao dataset existente.")
    else:
        # Se é a primeira vez, cria o arquivo e coloca o cabeçalho (header=True)
        df.to_csv(file_path, mode='w', header=True, index=False, encoding='utf-8')
        logger.info(f"Novo dataset criado com {len(df)} registros.")


def main(file_json: str, batch_size: int = 5):
    chat = create_llm(model="gpt-4o-mini")
    structured_chat = chat.with_structured_output(EvalOutputStructured)
    chunks, max_pages = get_all_chunks_from_pdf(json_file=file_json)

    logger.info("Generating question-answer data...")
    pages_to_group_by = 3

    # Itera sobre as páginas (não sobre chunks)
    for start_page in range(1, max_pages + 1, pages_to_group_by):
        batch_input_prompts_list = list()
        list_set_chunks_used = list()

        # Seleciona chunks das páginas do intervalo atual
        target_chunks = select_chunks_by_pages(
            start_page=start_page,
            groupby=pages_to_group_by,
            last_page=max_pages,
            chunks=chunks
        )

        # Gera batch_size perguntas para este intervalo de páginas
        system_prompt = [SystemMessage(EVAL_DATA_GEN_SYS)]
        for index in range(batch_size):
            # Seleciona chunks aleatórios do intervalo
            chunks_set = select_random_context(window_chunks=target_chunks)
            list_set_chunks_used.append(chunks_set)

            # Extrai o conteúdo dos chunks
            window_list = [chunk["_source"]["content"] for chunk in chunks_set]
            formatted_user_prompt = [HumanMessage(USER_QA_TASK.format(chunk_list=window_list))]
            user_request_prompt = system_prompt + formatted_user_prompt
            batch_input_prompts_list.append(user_request_prompt)
        
        # Processa o batch de perguntas
        batch_responses = structured_chat.batch(
            batch_input_prompts_list, 
            config={"max_concurrency": 5},
            return_exceptions=True)
        
        # Salva os resultados no dataset
        feed_dataset(batch_responses, list_set_chunks_used, EVAL_DATA_DIR)
