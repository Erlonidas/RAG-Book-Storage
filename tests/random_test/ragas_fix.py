# CORREÇÃO PARA O RAGAS - Cole este código em novas células do seu notebook

# ============================================
# CÉLULA 1: Importações e configuração do Ragas
# ============================================
from ragas import evaluate
from ragas.metrics import (
    faithfulness, 
    answer_relevancy,
    context_precision,
    context_recall,
    answer_correctness
)
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from datasets import Dataset

# Configurar LLM e Embeddings para o Ragas com timeout maior
evaluator_llm = LangchainLLMWrapper(
    ChatOpenAI(
        model="gpt-4o",
        timeout=120,  # 2 minutos de timeout
        max_retries=3  # Tentar 3 vezes antes de falhar
    )
)
evaluator_embeddings = LangchainEmbeddingsWrapper(
    OpenAIEmbeddings(
        timeout=60,  # 1 minuto de timeout para embeddings
        max_retries=3
    )
)

print("✓ Ragas configurado com sucesso!")


# ============================================
# CÉLULA 2: Preparar DataFrame
# ============================================
# Preparar DataFrame com as colunas corretas que o Ragas espera
eval_df = df[["question", "answer", "contexts", "reference"]].copy()
eval_df = eval_df.rename(columns={"reference": "ground_truth"})

# Verificar estrutura dos dados
print(f"Colunas do DataFrame: {eval_df.columns.tolist()}")
print(f"\nTipo de contexts[0]: {type(eval_df['contexts'].iloc[0])}")
print(f"Número de contextos no primeiro exemplo: {len(eval_df['contexts'].iloc[0])}")
print(f"\nPrimeiras 2 linhas:")
print(eval_df.head(2))


# ============================================
# CÉLULA 3: Executar avaliação
# ============================================
# Converter para Dataset do Ragas
dataset = Dataset.from_pandas(eval_df)


result = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
        answer_correctness
    ],
    llm=evaluator_llm,
    embeddings=evaluator_embeddings,
    batch_size=5,  
    raise_exceptions=False  
)

print("\n" + "="*50)
print("RESULTADOS DA AVALIAÇÃO")
print("="*50)
print(result)


# ============================================
# CÉLULA 4: Visualizar resultados detalhados
# ============================================
import numpy as np

# Extrair valores das métricas
# result é um dict com médias e listas de valores
print("\n" + "="*50)
print("MÉDIAS DAS MÉTRICAS")
print("="*50)
print(result)

# Acessar valores individuais de cada métrica
faithfulness_values = result["faithfulness"]
context_precision_values = result["context_precision"]
context_recall_values = result["context_recall"]
answer_correctness_values = result["answer_correctness"]

# answer_relevancy pode vir como np.float64 (média) ou lista
answer_relevancy_values = result["answer_relevancy"]
if isinstance(answer_relevancy_values, (float, np.floating)):
    print(f"\n⚠️ answer_relevancy retornou apenas a média: {answer_relevancy_values:.4f}")
    answer_relevancy_values = None
else:
    print(f"\n✓ answer_relevancy tem {len(answer_relevancy_values)} valores")

# Estatísticas detalhadas
print("\n" + "="*50)
print("ESTATÍSTICAS DETALHADAS")
print("="*50)

metrics_data = {
    "faithfulness": faithfulness_values,
    "context_precision": context_precision_values,
    "context_recall": context_recall_values,
    "answer_correctness": answer_correctness_values,
}

if answer_relevancy_values is not None:
    metrics_data["answer_relevancy"] = answer_relevancy_values

for metric_name, values in metrics_data.items():
    if isinstance(values, list):
        valid_values = [v for v in values if not np.isnan(v)]
        print(f"\n{metric_name}:")
        print(f"  Média: {np.mean(valid_values):.4f}")
        print(f"  Mediana: {np.median(valid_values):.4f}")
        print(f"  Min: {np.min(valid_values):.4f} | Max: {np.max(valid_values):.4f}")
        print(f"  Valores válidos: {len(valid_values)}/{len(values)}")


# ============================================
# CÉLULA 5: Visualizar com Boxplots
# ============================================
import matplotlib.pyplot as plt

# Preparar dados para visualização
plot_data = []
plot_labels = []

for metric_name, values in metrics_data.items():
    if isinstance(values, list):
        # Remover NaN para visualização
        valid_values = [v for v in values if not np.isnan(v)]
        if valid_values:
            plot_data.append(valid_values)
            plot_labels.append(metric_name.replace("_", " ").title())

# Criar figura com boxplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Boxplot
bp = ax1.boxplot(plot_data, labels=plot_labels, patch_artist=True)
ax1.set_ylabel('Score', fontsize=12)
ax1.set_title('Distribuição das Métricas RAG', fontsize=14, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)
ax1.set_ylim(0, 1)

# Colorir os boxes
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
for patch, color in zip(bp['boxes'], colors[:len(plot_data)]):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# Rotacionar labels se necessário
ax1.tick_params(axis='x', rotation=45)

# Gráfico de barras com médias
means = [np.mean(data) for data in plot_data]
bars = ax2.bar(plot_labels, means, color=colors[:len(plot_data)], alpha=0.7, edgecolor='black')
ax2.set_ylabel('Score Médio', fontsize=12)
ax2.set_title('Média das Métricas RAG', fontsize=14, fontweight='bold')
ax2.set_ylim(0, 1)
ax2.grid(axis='y', alpha=0.3)
ax2.tick_params(axis='x', rotation=45)

# Adicionar valores nas barras
for bar, mean in zip(bars, means):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{mean:.3f}',
             ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.show()

# Estatísticas resumidas
print("\n" + "="*50)
print("RESUMO FINAL")
print("="*50)
for label, data in zip(plot_labels, plot_data):
    print(f"{label}: {np.mean(data):.4f} (±{np.std(data):.4f})")
