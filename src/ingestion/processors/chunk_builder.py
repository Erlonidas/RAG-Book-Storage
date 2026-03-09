"""
Construtor de chunks a partir do JSON do Dolphin.
Anteriormente: FilterChunkGeneration.py
"""
from typing import Dict, Any, List, Optional
from markdownify import markdownify as md
from src.config import TAGS_IGNORADAS, setup_logger

logger = setup_logger(__name__)


def criar_doc(book_id: str, sec_0: str, sec_1: str, sec_2: str, texto: str, page_number: int, reading_order: int, doc_type: str = "text") -> dict:
    """
    Monta o documento final para ingestão no OpenSearch.
    """
    partes_contexto = [p for p in [sec_1, sec_2] if p]
    contexto = " > ".join(partes_contexto) if partes_contexto else "Initial Session"

    return {
        "book_id": book_id,
        "sec_0": sec_0,
        "sec_1": sec_1,
        "sec_2": sec_2,
        "section_context": contexto,
        "doc_type": doc_type,
        "page_number": page_number,
        "reading_order": reading_order,
        "content": f"{contexto}\n\n{texto}"
    }


def get_section_content(chunks: list[dict], sec_1: str, sec_2: str = None, 
                       include_context: bool = False, doc_types: list[str] = None) -> str:
    """
    Recupera todo o conteúdo de uma seção/subseção.
    """
    filtered = [c for c in chunks if c["sec_1"] == sec_1]
    if sec_2:
        filtered = [c for c in filtered if c["sec_2"] == sec_2]
    if doc_types:
        filtered = [c for c in filtered if c.get("doc_type", "text") in doc_types]
    
    if include_context:
        return "\n\n".join([c["content"] for c in filtered])
    else:
        contents = []
        for c in filtered:
            text = c["content"]
            if text.startswith("Context:"):
                text = "\n".join(text.split("\n")[2:])
            contents.append(text)
        return "\n\n".join(contents)


def get_section_hierarchy(chunks: list[dict]) -> dict[str, list[str]]:
    """
    Extrai a hierarquia de seções e subseções dos chunks.
    
    Args:
        chunks: Lista de chunks processados
    
    Returns:
        Dicionário onde a chave é sec_1 e o valor é uma lista de sec_2 (subseções)
        Exemplo: {
            "Introduction": ["", "Background", "Motivation"],
            "Methods": ["Data Collection", "Analysis"],
            "Results": [""]
        }
        Nota: "" indica que há conteúdo diretamente na seção sem subseção
    """
    hierarchy = {}
    
    for chunk in chunks:
        sec_1 = chunk.get("sec_1", "")
        sec_2 = chunk.get("sec_2", "")
        
        if sec_1 not in hierarchy:
            hierarchy[sec_1] = set()
        
        hierarchy[sec_1].add(sec_2)
    
    result = {}
    for sec_1, sec_2_set in hierarchy.items():
        sec_2_list = sorted(sec_2_set, key=lambda x: (x != "", x))
        result[sec_1] = sec_2_list
    
    return result


def _flush_buffer(buffer: str | None, book_id: str, sec_0: str, sec_1: str, sec_2: str, 
                  docs: list, page_number: int, reading_order: int, doc_type: str = "text") -> None:
    """Salva o buffer no array de docs se ele não estiver vazio."""
    if buffer and buffer.strip():
        docs.append(criar_doc(book_id, sec_0, sec_1, sec_2, buffer, page_number, reading_order, doc_type))


def processar_json_dolphin(dolphin_json: dict, book_id: str) -> list[dict]:
    """
    Processa o JSON do Dolphin e monta os chunks prontos para ingestão no OpenSearch.

    Padrões de agrupamento suportados:
    - sec_1 > sec_2 > para (+ half_para, list, equ, code)
    - Tabelas: chunks separados com doc_type="table" (concatena tab+tab se quebrada)
    - Figuras: chunks separados com doc_type="figure"
    
    Tags ignoradas: foot, fnote, que, sec_0, header
    """
    docs_to_index = []

    # machine state
    current_sec_0 = ""
    current_sec_1 = "Initial Section"
    current_sec_2 = ""
    buffer_para: str | None = None
    buffer_table: str | None = None
    buffer_figure: str | None = None
    buffer_code: str = None

    pages = dolphin_json.get('pages', [])
    for page in pages:
        elements = page.get('elements', [])
        page_number = page.get("page_number")
        
        for item in elements:
            tipo = item.get('label', '')
            conteudo = item.get('text', '').strip()
            reading_order = item.get("reading_order")

            if not conteudo and tipo not in ('tab', 'fig'):
                logger.debug(f"Item sem conteúdo ignorado: tipo={tipo}")
                continue

            if tipo == 'sec_0':
                _flush_buffer(buffer_para, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order, "text")
                _flush_buffer(buffer_table, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "table")
                _flush_buffer(buffer_figure, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "figure")
                _flush_buffer(buffer_code, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "code")
                buffer_code = None
                buffer_para = None
                buffer_table = None
                buffer_figure = None  

                # new 
                current_sec_0 = conteudo

            elif tipo == 'sec_1':
                _flush_buffer(buffer_para, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "text")
                _flush_buffer(buffer_table, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "table")
                _flush_buffer(buffer_figure, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "figure")
                _flush_buffer(buffer_code, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "code")
                buffer_code = None
                buffer_para = None
                buffer_table = None
                buffer_figure = None

                #new
                current_sec_1 = conteudo
                current_sec_2 = ""

            elif tipo == 'sec_2':
                _flush_buffer(buffer_para, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "text")
                _flush_buffer(buffer_table, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "table")
                _flush_buffer(buffer_figure, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "figure")
                _flush_buffer(buffer_code, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "code")
                buffer_code = None
                buffer_para = None
                buffer_table = None
                buffer_figure = None

                #new
                current_sec_2 = conteudo

            elif tipo == 'para':
                _flush_buffer(buffer_table, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "table")
                _flush_buffer(buffer_figure, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "figure")
                _flush_buffer(buffer_para, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "text")
                _flush_buffer(buffer_code, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "code")
                buffer_code = None
                buffer_table = None
                buffer_figure = None

                #new
                buffer_para = conteudo

            elif tipo == 'tab':
                tabela_md = md(conteudo) 
                if buffer_table is not None:
                    buffer_table += f"\n{tabela_md}"
                else:
                    buffer_table = tabela_md
                buffer_code = None

            elif tipo == 'fig':
                _flush_buffer(buffer_para, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "text")
                _flush_buffer(buffer_table, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "table")
                _flush_buffer(buffer_code, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "code")
                buffer_code = None
                buffer_para = None
                buffer_table = None

                # new
                buffer_figure = conteudo
                
            elif tipo == 'cap':    
                if buffer_figure: # se tem fig antes en
                    buffer_figure += f"\n{conteudo}"
                    _flush_buffer(buffer_figure, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "figure")
                    buffer_figure = None

                else:
                    _flush_buffer(buffer_para, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "text")
                    buffer_para = None

                    #new
                    if buffer_code:
                        buffer_code += f"\n{conteudo}"
                        _flush_buffer(buffer_code, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "code")
                        continue

                    buffer_table = conteudo
                    buffer_code = conteudo
                    
            elif tipo == 'code':
                buffer_table = None
                
                _flush_buffer(buffer_figure, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "figure")
                buffer_figure = None
                _flush_buffer(buffer_para, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "text")
                buffer_para = None
                
                codigo = f"```\n{conteudo}\n```"
                if buffer_code is not None:
                    buffer_code += f"\n{codigo}"
                else:
                    buffer_code = f"{codigo}"

            elif tipo == 'half_para':              
                if buffer_para is not None:
                    buffer_para += f" {conteudo}"
                else:
                    buffer_para = conteudo

            elif tipo == 'list':
                _flush_buffer(buffer_table, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "table")
                _flush_buffer(buffer_figure, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "figure")
                buffer_table = None
                buffer_figure = None
                
                if buffer_para:
                    buffer_para += f"\n{conteudo}"
                else:
                    buffer_para = f"{conteudo}"

            elif tipo == 'equ':
                _flush_buffer(buffer_table, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "table")
                _flush_buffer(buffer_figure, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "figure")
                buffer_table = None
                buffer_figure = None
                
                if buffer_para is not None:
                    buffer_para += f"\n{conteudo}"
                else:
                    buffer_para = conteudo

            elif tipo in TAGS_IGNORADAS:
                logger.debug(f"Tag ignorada: tipo={tipo}")
            else:
                logger.warning(f"Tag desconhecida: tipo='{tipo}' em book_id={book_id}")

    # Saves final buffers
    _flush_buffer(buffer_para, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "text")
    _flush_buffer(buffer_table, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "table")
    _flush_buffer(buffer_figure, book_id, current_sec_0, current_sec_1, current_sec_2, docs_to_index, page_number, reading_order,  "figure")

    logger.info(f"book_id='{book_id}' → {len(docs_to_index)} chunks gerados.")
    return docs_to_index