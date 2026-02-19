# Guia: Executando Dolphin no Google Colab para Extração de PDFs

Este guia mostra como usar o Dolphin no Google Colab para extrair conteúdo estruturado de PDFs e gerar arquivos Markdown.

## Visão Geral

O Dolphin é uma ferramenta de análise de documentos que:
- Processa PDFs página por página
- Detecta layout e ordem de leitura
- Extrai texto, tabelas, fórmulas, código e figuras
- Gera saídas em JSON e Markdown

## Pré-requisitos

- Conta Google (para acessar o Colab)
- PDF(s) que você deseja processar
- Conexão com internet estável

## Configuração do Ambiente

### Passo 1: Criar Notebook no Colab

1. Acesse [Google Colab](https://colab.research.google.com/)
2. Crie um novo notebook
3. Configure para usar GPU:
   - Menu: `Runtime` > `Change runtime type`
   - Selecione: `Hardware accelerator: GPU` (T4 ou melhor)
   - Clique em `Save`

## Execução Passo a Passo

### Célula 1: Clonar Repositório e Instalar Dependências

```python
# Clonar o repositório Dolphin
!git clone https://github.com/bytedance/Dolphin.git
%cd Dolphin

# Instalar dependências do requirements.txt
!pip install -q -r requirements.txt

print("✅ Repositório clonado e dependências instaladas!")
```

**O que acontece:**
- Clona o repositório oficial do Dolphin do GitHub
- Instala todas as dependências necessárias (PyTorch, Transformers, PyMuPDF, etc.)
- Tempo estimado: 2-3 minutos

---

### Célula 2: Baixar o Modelo

```python
from huggingface_hub import snapshot_download

# Baixar o modelo Dolphin-v2
print("⏳ Baixando modelo Dolphin-v2 (pode levar alguns minutos)...")
snapshot_download(
    repo_id="ByteDance/Dolphin-v2",
    local_dir="./hf_model",
    local_dir_use_symlinks=False
)

print("✅ Modelo baixado!")
```

**O que acontece:**
- Baixa o modelo Dolphin-v2 (3B parâmetros) do Hugging Face
- Tamanho: ~6GB
- Tempo estimado: 5-10 minutos (dependendo da conexão)
- O modelo fica salvo em `./hf_model/`

---

### Célula 3: Upload do PDF

```python
from google.colab import files

# Upload do PDF
print("📤 Faça upload do seu PDF:")
uploaded = files.upload()

# Pegar o nome do arquivo
pdf_filename = list(uploaded.keys())[0]
print(f"✅ Arquivo recebido: {pdf_filename}")
```

**O que acontece:**
- Abre uma janela para você fazer upload do PDF
- Clique em "Choose Files" e selecione seu PDF
- O arquivo é carregado para o ambiente Colab
- Tempo: depende do tamanho do PDF

**Dica:** Para PDFs grandes (>50MB), considere usar Google Drive ao invés de upload direto.

---

### Célula 4: Processar o PDF

```python
# Processar usando o script demo_page.py do repositório
!python demo_page.py \
    --model_path ./hf_model \
    --input_path {pdf_filename} \
    --save_dir ./results \
    --max_batch_size 4

print("\n✅ Processamento concluído!")
print("📁 Resultados salvos em: ./results")
```

**O que acontece:**
- Executa o script `demo_page.py` com seus parâmetros
- Converte cada página do PDF em imagem
- **Estágio 1:** Analisa o layout de cada página
- **Estágio 2:** Extrai conteúdo de cada elemento detectado
- Gera arquivos JSON, Markdown e visualizações

**Parâmetros:**
- `--model_path`: Caminho do modelo baixado
- `--input_path`: Arquivo PDF a processar
- `--save_dir`: Diretório para salvar resultados
- `--max_batch_size`: Número de elementos processados em paralelo (4 é ideal para Colab gratuito)

**Tempo estimado:**
- ~30-60 segundos por página (dependendo da complexidade)
- PDF de 10 páginas: ~5-10 minutos

---

### Célula 5: Visualizar Resultados

```python
import json
import os

# Encontrar o arquivo JSON gerado
pdf_base = pdf_filename.replace('.pdf', '')
json_file = f"./results/recognition_json/{pdf_base}.json"

# Ler e mostrar o JSON
if os.path.exists(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("📋 Resumo do Processamento:")
    print(f"Arquivo: {data.get('source_file', 'N/A')}")
    print(f"Total de páginas: {data.get('total_pages', 0)}")
    
    for page in data.get('pages', []):
        print(f"\n📄 Página {page['page_number']}: {len(page['elements'])} elementos")
        
        # Mostrar primeiros 3 elementos
        for i, elem in enumerate(page['elements'][:3]):
            text_preview = elem['text'][:100] + "..." if len(elem['text']) > 100 else elem['text']
            print(f"  [{elem['label']}] {text_preview}")
    
    # Mostrar JSON completo (primeiros 2000 caracteres)
    print("\n📄 JSON completo (preview):")
    print(json.dumps(data, indent=2, ensure_ascii=False)[:2000] + "...")
else:
    print(f"❌ Arquivo JSON não encontrado: {json_file}")

# Mostrar o Markdown
md_file = f"./results/markdown/{pdf_base}.md"
if os.path.exists(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    print("\n📝 Conteúdo Markdown (primeiros 1500 caracteres):")
    print(markdown_content[:1500])
    if len(markdown_content) > 1500:
        print("...")
else:
    print(f"❌ Arquivo Markdown não encontrado: {md_file}")
```

**O que acontece:**
- Lê o arquivo JSON gerado com todos os dados estruturados
- Mostra um resumo: número de páginas, elementos por página
- Exibe preview dos primeiros elementos de cada página
- Mostra o conteúdo Markdown gerado

**Informações exibidas:**
- Total de páginas processadas
- Número de elementos por página
- Preview do texto extraído
- Estrutura do JSON
- Conteúdo Markdown

---

### Célula 6: Listar Todos os Arquivos Gerados

```python
import os

print("📁 Estrutura de arquivos gerados:\n")

for root, dirs, files in os.walk('./results'):
    level = root.replace('./results', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        print(f'{subindent}{file}')
```

**O que acontece:**
- Lista todos os arquivos e pastas criados em `./results/`
- Mostra a estrutura de diretórios de forma organizada

**Estrutura esperada:**
```
results/
  markdown/
    seu_pdf.md
    figures/
      seu_pdf_figure_001.png
      seu_pdf_figure_002.png
  recognition_json/
    seu_pdf.json
  output_json/
  layout_visualization/
    seu_pdf_page_001_layout.png
    seu_pdf_page_002_layout.png
```

---

### Célula 7: Download dos Resultados

```python
from google.colab import files
import shutil

# Criar ZIP com os resultados
shutil.make_archive('dolphin_results', 'zip', './results')

# Download
print("⬇️ Baixando resultados...")
files.download('dolphin_results.zip')
print("✅ Download concluído!")
```

**O que acontece:**
- Compacta toda a pasta `./results/` em um arquivo ZIP
- Inicia o download automático do arquivo
- O arquivo `dolphin_results.zip` será baixado para seu computador

**Conteúdo do ZIP:**
- Arquivos Markdown (`.md`) com o conteúdo extraído
- Arquivos JSON com dados estruturados
- Figuras extraídas (`.png`)
- Visualizações do layout (`.png`)

---

## Estrutura dos Arquivos Gerados

### 1. Arquivo Markdown (`markdown/seu_pdf.md`)

Contém o conteúdo extraído formatado em Markdown:
- Títulos e seções (com níveis hierárquicos)
- Parágrafos de texto
- Tabelas em HTML
- Fórmulas matemáticas em LaTeX
- Blocos de código
- Links para figuras extraídas

**Exemplo:**
```markdown
# Título Principal

Este é um parágrafo extraído do PDF.

## Seção 1

Mais texto aqui.

<table>
<tr><td>Célula 1</td><td>Célula 2</td></tr>
</table>

$E = mc^2$

![Figure](figures/seu_pdf_figure_001.png)
```

### 2. Arquivo JSON (`recognition_json/seu_pdf.json`)

Contém dados estruturados de todo o documento:

```json
{
  "source_file": "seu_pdf.pdf",
  "total_pages": 3,
  "pages": [
    {
      "page_number": 1,
      "elements": [
        {
          "label": "sec_0",
          "bbox": [210, 136, 910, 172],
          "text": "Título Principal",
          "reading_order": 0,
          "tags": []
        },
        {
          "label": "para",
          "bbox": [202, 217, 921, 325],
          "text": "Este é um parágrafo...",
          "reading_order": 1,
          "tags": ["author"]
        }
      ]
    }
  ]
}
```

**Campos importantes:**
- `label`: Tipo do elemento (para, tab, equ, fig, sec_0, etc.)
- `bbox`: Coordenadas [x1, y1, x2, y2] do elemento na página
- `text`: Conteúdo extraído
- `reading_order`: Ordem de leitura natural
- `tags`: Metadados adicionais

### 3. Figuras (`markdown/figures/`)

Imagens extraídas do PDF salvas como PNG.

### 4. Visualizações de Layout (`layout_visualization/`)

Imagens mostrando os bounding boxes coloridos de cada elemento detectado, útil para debug.

---

## Tipos de Elementos Detectados

| Label | Descrição | Exemplo de Saída |
|-------|-----------|------------------|
| `sec_0` | Título principal | `# Título` |
| `sec_1` | Subtítulo nível 1 | `## Subtítulo` |
| `sec_2` | Subtítulo nível 2 | `### Subtítulo` |
| `para` | Parágrafo de texto | Texto plano |
| `tab` | Tabela | HTML `<table>` |
| `equ` | Fórmula matemática | LaTeX `$...$` |
| `code` | Bloco de código | Markdown code block |
| `fig` | Figura/imagem | Link para PNG |
| `list` | Item de lista | `- Item` |
| `fnote` | Nota de rodapé | Texto plano |

---

## Dicas e Otimizações

### Para PDFs Grandes

Se você tem um PDF muito grande (>50 páginas ou >100MB):

1. **Use Google Drive:**
```python
from google.colab import drive
drive.mount('/content/drive')

# Processar PDF do Drive
!python demo_page.py \
    --model_path ./hf_model \
    --input_path "/content/drive/MyDrive/seu_pdf.pdf" \
    --save_dir ./results \
    --max_batch_size 4
```

2. **Processe em lotes:**
   - Divida o PDF em partes menores
   - Processe cada parte separadamente

3. **Ajuste o batch_size:**
   - Colab gratuito: `--max_batch_size 2` ou `4`
   - Colab Pro: `--max_batch_size 8` ou `16`

### Para Melhor Performance

- Use GPU (T4 ou melhor)
- Feche outras abas do navegador
- Evite processar durante horários de pico
- Mantenha a aba do Colab ativa (não minimize)

### Processamento em Lote

Para processar múltiplos PDFs:

```python
# Upload múltiplos PDFs
uploaded = files.upload()

# Processar todos
for pdf_file in uploaded.keys():
    print(f"\n📄 Processando: {pdf_file}")
    !python demo_page.py \
        --model_path ./hf_model \
        --input_path {pdf_file} \
        --save_dir ./results \
        --max_batch_size 4
```

---

## Solução de Problemas

### Erro: "CUDA out of memory"

**Solução:**
- Reduza `--max_batch_size` para 2 ou 1
- Reinicie o runtime: `Runtime` > `Restart runtime`
- Use Colab Pro para mais memória

### Erro: "Model download failed"

**Solução:**
- Verifique sua conexão com internet
- Tente novamente após alguns minutos
- Use VPN se estiver em região com restrições

### PDF não processa corretamente

**Possíveis causas:**
- PDF protegido por senha (remova a senha primeiro)
- PDF corrompido (tente abrir em outro leitor)
- PDF com imagens de baixa qualidade (use PDF de melhor qualidade)

### Markdown com caracteres estranhos

**Solução:**
- Problema de encoding, geralmente com PDFs em idiomas não-latinos
- O JSON terá os dados corretos, use-o como fonte

---

## Limitações

- **Tempo de sessão:** Colab gratuito desconecta após 12h ou 90min de inatividade
- **Memória:** Limitada no Colab gratuito (~12GB RAM, ~15GB GPU)
- **PDFs escaneados:** Funciona melhor com PDFs digitais; PDFs escaneados podem ter qualidade inferior
- **Tabelas complexas:** Tabelas muito complexas podem não ser extraídas perfeitamente
- **Idiomas:** Otimizado para inglês e chinês; outros idiomas podem ter resultados variados

---

## Próximos Passos

Após extrair o conteúdo:

1. **Editar o Markdown:** Use qualquer editor de Markdown para refinar o conteúdo
2. **Processar o JSON:** Use Python/JavaScript para análise adicional dos dados estruturados
3. **Integrar em pipeline:** Use o Dolphin como parte de um pipeline maior de processamento de documentos
4. **Fine-tuning:** Se necessário, faça fine-tuning do modelo para seu domínio específico

---

## Recursos Adicionais

- **Repositório GitHub:** https://github.com/bytedance/Dolphin
- **Modelo Hugging Face:** https://huggingface.co/ByteDance/Dolphin-v2
- **Paper:** https://arxiv.org/abs/2505.14059
- **Issues:** Reporte problemas no GitHub

---

## Conclusão

Este guia fornece um fluxo completo para usar o Dolphin no Google Colab. O processo é dividido em 7 células simples que:

1. ✅ Configuram o ambiente
2. ✅ Baixam o modelo
3. ✅ Fazem upload do PDF
4. ✅ Processam o documento
5. ✅ Visualizam resultados
6. ✅ Listam arquivos gerados
7. ✅ Fazem download dos resultados

O resultado final são arquivos Markdown prontos para uso, com todo o conteúdo estruturado extraído do PDF!
