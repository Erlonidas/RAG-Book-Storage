Noname manuscript No. (will be inserted by the editor)

# Beyond Black-Box Mutation: Grounding GPT-4.1 Mutant Generation in Historical Bug-Fix Patterns

Erlon Pereira Almeida · Daniel Lucreio · Rohit Ghey · Pierre-Yves Guilherme Jorge Ferreira · Paulo Arnelho da Manteleira Neto · Eduardo Santana de Almeida

Received: date / Accepted: date

Abstract Mutation testing is often constrained by the generation of unrealistic mutants, as existing approaches struggle to create faults that are both semantically meaningful and syntactically varied. Traditional and learningbased approaches alike struggle to create artificial faults that are both semantically meaningful and syntactically varied, often yielding simplistic or unstable results. This paper investigates using GPT-4.1 within a novel, two-stage workflow to generate mutants grounded in real fault patterns. We first systematically analyze multiple variations of prompt templates, combining five popular prompt templates together to address code modification patches. The Abstract Syntax Tree node layers, subsequently we deploy the optimization pipeline within a model-augmented framework that combines and applies historical mutation operators to 8,322 real-world code snippets. Our findings reveal that different prompt strategies induce distinct "error profiles," effectively creating "specialists" in misusing specific Java notes. Furthermore, compared to a specialized machine learning baseline, GPT-4.1 produces am-

Erlon P. Almeida Federal University of Bahia (UFBA), E-mail: erlon.almeida@ufba.br Daniel Lucrecio Universidade de São Carlos (UFSCar), E-mail: d.lucreio@gmail.com Rohit Gheyi Federal University of Campina Grande (UFCG), E-mail: rohitgheyi@gmail.com Pierre-Yves Schobbens University of Namur, E-mail: pierre-yves.schobbens@unamur.be Gilles Perrouin University of Namur, E-mail: gilles.perrouin@unamur.be Paulo Silveira Federal University of Pernambuco (UFPE), E-mail: paulosadmn96@gmail.com Edwards A. Almeida Federal University of Bahia (UFBA), E-mail: eduardo.almeida@ufba.br

---

2

Erlon Pereira Almeida et al.

tants with higher and more stable semantic resemblance to real faults, whereas the baseline excises its lexical fidelity but lacks stability. This work serves as a foundational investigation into the capabilities of LLMs for structured mutation testing.

Keywords GPT-4.1 · Mutation Testing · Prompt Engineering · Software Testing · LLM

## 1 Introduction

Mutation testing is a widely used technique for evaluating the fault-detection capability of test suites by introducing small, systematic changes called mutants to source code and measuring whether existing tests can detect them. These mutants are generated using mutation operators, such as Delete Invocation or Update Binary Operator , which simulate real faults and help assess the robustness of the test suite (Jucai et al., 2014; Papadakis et al., 2019b) .

Despite its utility, mutation testing suffers from two well-known challenges. First, the selection and manual curation of mutation operators are time-consuming and often fail to capture the semantic behavior of real-world faults (Papadakis et al., 2018; Ojdanic et al., 2023a) . The technique produces mutants in quantities several orders of magnitude greater than the number of lines in the program, thus necessitating multiple test executions (Gopinath et al., 2016, 2017b) . For systems with millions of lines of code, this becomes computationally expensive (Gopinath et al., 2015) . Beyond the issue of cost, a noteworthy example is the case of the GPT-2 large model, which generates excessive redundant or equivalent mutants (Zhang et al., 2019; Wang et al., 2017, 2024a) . Equivalent mutants are syntactically different but semantically identical to the original program, making them undetectable by any test case. Redundant mutants, while killable, are either (1) trivially detected by the same tests as other mutants or (2) subsumed by other mutants' behavior, offering no unique insight into test-suite effectiveness (Guimarães et al., 2020; Gheyie et al., 2021) . The research community has pursued a wide array of strategies to mitigate these challenges, which can be broadly categorized into cost reduction and the management of equivalent mutants. Regarding cost, techniques range from selecting a minimal set of mutation operators (Mathur, 1991; Wong, 1993; Gopinath et al., 2017b) to randomly sampling from the full mutant set (Gopinath et al., 2017b; Papadakis et al., 2019a) . For the issue of equivalence, solutions span from formal and heuristic detection methods (Offutt and Pan, 1996; 1997; 1998; 1999; 2014) . Kintla et al. (2013) employed a common-sense and analysis (Golchin, 2010; Schulzer and Zehl, 2010; Papadakis et al., 2014; Wright et al., 2014; Yao et al., 2014) . However, these approaches face inherent trade-offs: cost-reduction may compromise mutant representativeness, detection methods struggle with scalability, and prevention strategies introduce their own complexities.

These trade-offs reveal a fundamental tension within traditional mutation testing: the inherent limitations of syntactic, operator-driven approaches when tested for large-scale genomic variation.

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

3

applied to the equivalent mutant problem (Kintis et al., 2016) . Widely-used tools, such as MAJOR (Just, 2014) , muJava (Ma et al., 2006) , and PIT (Colls et al., 2016a) exemplify this paradigm, implementing selective sets of mutation operators to balance practical feasibility with fault-detection capability (Madeysky et al., 2014; Kintis et al., 2016; Gopinath et al., 2017a) . While their design choices result in modest equivalent mutant rates (6.5 % for PIT) compared to the 14 % -31 % found by MAJOR, mutation operators are expected to ate sacrifices in comprehensiveness rather than through intelligent reasoning about code semantics. Notably, only 4.1 % of equivalent mutants are common across all three tools, underscoring that each tool's approach to operator selection produces fundamentally different mutant sets, with limited consensus on what constitutes an equivalent mutant (Just et al., 2012; Kintis et al., 2016) . Higher-Order Mutation (HOM) strategies, which combine multiple first-order mutations to increase semantic diversity, offer a promising alternative that demonstrates significant reductions in equivalent mutants (Kurtz et al., 2016) . Empirical evidence from implementations using the July tool (Madeysky and Kurtz, unpublished) further supports these findings (Kurtz et al., 2016) . In 88 % and 75-82 % reductions in equivalent mutants, respectively, while maintaining test effectiveness with only 1.7%-4.2 % loss in fault-detection capability (Madeysky et al., 2014) . However, despite these advances, HOM strategies remain absent from the core of mainstream tools like muJava (Ma et al., 2006) and MAJOR (Just, 2014) . Researchers (Laurent and Ventresque, 2019) have even attempted to extend the PIT framework for higher-order mutation in small-scale experiments (PIT-HOM), however, they explicitly concluded that without a sophisticated selection process, the resulting mutants are “ largely redundant ” (Laurent and Ventresque, 2019) . Consequently, the core problem with PIT-based approaches is not entirely clear, and determining how to main fundamentally limited by their dependence on predefined syntactic rules and operator-based transformations, unable to reason about program context and semantics to prevent the generation of equivalent mutants in the first place.

Therefore, we posit that these persistent limitations stem from the absence of a cognitive component capable of intelligently selecting and combining amutation operators in a context-aware manner, tailored to the specific code under analysis. Strategies such as HOM attempted to address equivalence, but they are hindered by combinatorial explosion and often impair fault-detection capacity (Nguyen and Madeyski, 2014; Wong et al., 2020) . Similarly, tools that randomly select from a predefined operator set lack the semantic understanding to avoid nonsensical or equivalent changes.

On the other hand, the rapid evolution of Large Language Models (LLMs) such as GPT-4.1 has created new opportunities for leveraging these models across a wide range of software engineering activities. Recent studies demonstrate that LLMs can effectively support tasks such as code generation, embedding into computer systems, and bringing novel capabilities to C++ (Wei et al., 2024b) . While studies have applied LLMs to mutation testing, these efforts typically rely on the model's ability to generate plausible code variants

---

4

Erlon Pereira Almeida et al.

in a black-box fashion (Degiovani and Papadakis, 2022; Deng et al., 2023, 2024a) . Such approaches often lack insights into whether the generated nutents meaningfully reflect real-world faults, or whether the underlying model indeed learned any interpretable patterns about how bugs are introduced and fixed.

In this paper, we present an exploratory study and proof of concern for a more transparent and structured use of LLMs in mutation analysis. We investigate a two-stage workflow that first prompts an LLM to identify complex modification patterns at the AST-node level from a dataset of real Java bugfix commits, where code transformations naturally involve 1-to-6 concurrent modifications, effectively capturing historically-grounded higher-order mutations. These patterns are then reused for semantically-aware mutation operators to observe and repair any harmful approaches between mutation and regular prompting by grounding the mutation process in the multi-operator change patterns characteristic of real fault fixes. A core component of our investigation involves a deep analysis of the error profiles, specifically, the node-level errors and their distribution, generated by different prompt templates. By systematically examining how the LLM behaves in this specific task, we aim to structure a reliable and interpretable method for mutation generation. Our work is motivated by the potential of appropriately prompted LLMs to generalize from noisy examples and recognize recurring, human-like code transformations (Brown et al., 2020; Wei et al., 2022; 2023; Hou et al., 2024; Wang et al., 2023) . To address these issues, we model human-like coding as a cognitive component for generating higher-order mutants, with the longterm goal of reducing the generation of redundant and equivalent mutants, improving alignment with real-world defects, and enhancing the overall utility of mutation testing.

While recent work has begun to explore LLMs for generating mutants, such as intent-based mutation (Hamidi et al., 2025) , these approaches focus on different generation strategies, such as mutating the natural language specifications (or “ itents ” ) of the code (Hamidi et al., 2023) . In contrast, to the best of our knowledge, the first system that supports and works out these pare multiple prompt strategies to guide a state-of-the-art LLM (GPT-4.1) in extracting code modification patterns from real food-bags commits at the AST-level node, and (2) reuse these historically-grounded patterns to guide a transparent mutant generation process. A core contribution of our work is the LLM, a phenomenon not investigated in prior work. To evaluate our method, we address two major research questions:

RQ1: What is the most effective way to instruct an LLM model in identifying modifications to Java code?

To answer RQ1, we conducted a quantitative analysis focused specially on detective evolution (bug-fixes). We used an LLM on the main dataset of 8.8G Jaccard Index to obtain each pattern. It was useful to examine patterns to identify the ASTE-only detection patterns that transform files to only exist in the buggy version. Since LLM outputs are highly sensitive to prompt

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

5

formulation, we systematically evaluated four prompt templates, with different combinations of 5 popular prompt techniques (Few-Shot and Zero-shot Learning, Retrieval-Augmented Generation, Persona, Chain-of-Thoughts). We measured the correctness of the extracted AST node-level modifications and analyzed common biases and errors introduced by each prompt in each Java node.

The most effective prompting strategy from RQ1 was then adapted to guide the generation of tasks, which were then used in RQ2 shifting its core task from operator identification to code generation.

RQ2: How effectively does LLM generate mutant code aligned with real faults? The projects under the prompt strategies tested compared to existing techniques.

Leveraging the best-performing prompt template from RQ1, we implement a mutant generation workflow that draws on a secondary dataset of 71,003 bug-fix examples to derive mutation operators. We then used these operators as a reference to generate mutant versions for the same main dataset, used in RQ1. Our results demonstrate that the mutants generated by GPT-4.1 achieve structural characteristics with a level of semantic similarity comparable to those produced by state-of-the-art methods based on tabulated translators of 2019 and 2020. However, RQ1 is limited to 2019 and 2020. Thus, the advantage of our approach is particularly related to mutations involving modifications to deeply nested Java nodes, as measured by both semantic and lexical similarity metrics.

In summary, this study makes the following contributions:

- – An automated workflow that leverages GPT-4.1 to generate mutants
aligned with real-world Java faults, establishing the feasibility of using
LLMs for this task.
– The construction and empirical characterization of a novel set of
72 mutation operators directly mined from 8,322 real bug-fix pairs using
fine-grained AST analysis. These operators, encompassing 18 Java code
types and 4 change operations, provide a structured, historically-grounded
foundation for mutant generation that reflects the diversity of real fault
patterns.
– A comprehensive comparative analysis of prompt engineering strat-
egies, demonstrating that prompt choice does not lead to uniform improve-
ment but instead induces distinct error profiles. This analysis reveals that
our approach systematically biases the model's performance, concentrating
specific types of failure modes in a predictable manner.
– Identification and categorization of the specific Java node types where
the LLM struggles the most. This reveals both chronically difficult nodes
(e.g., TypeReference) and a fundamental confusion when key nodes (e.g.,
FieldRoad) are frequently both omitted (False Negatives) and hallucinated
(False Positives).
---

6

Erlon Pereira Almeida et al.

- • A publicly available replication package $^1$ , including all datasets, prompts,
and figures, to enable users to ensure the reproducibility of our find-
ings and facilitate future research.
## 2 Related Work

Mutation testing is a well-established technique for evaluating test utility by deliberately introducing faults (mutants) into source code (Jia and Hamann, 2011a; Papadakis et al., 2019a) . Its effectiveness relies on the coupling hypothesis, which posits that mutants simulate real faults. This approach not only works but also reveals new technical challenges in automated program repair (Weimer et al., 2013; Yi et al., 2018; Xiao et al., 2023) .

While large-scale studies confirm a strong correlation between mutant detection and real bug discovery (Just et al., 2014; Laurent et al., 2022; Giri and Sahalahad, 2023) , a significant challenge persists. Traditional mutation often generates a high volume of redundant or invalid mutants, making the process difficult. The majority of computational methods rely on extracting features for generating mutants that are both representative of real faults and efficient to produce remains a crucial research objective.

### 2.1 Prior Mutation Testing Tools

Traditional mutation testing tools apply predefined operators to generate mutants, with implementations varying by programming language and the level of code representation (e.g., source code, AST, or bytecode) (Jia and Harman, 2011b) . Well-known tools include Jumble (Irvine et al., 2007) and Pit (Coles et al., 2016b) for Java bytecode, MAJOR Just et al. (2011) for the Java AST, and AccMut (Wang et al., 2017) for LLVM IR in C programs.

A critical study by Gopinath et al. (2017a) compared tools like Major (Just et al., 2011) and Pit (Coles et al., 2016b) , revealing that mutation score are highly dependent and rarely agree for the same project. This highlights a significant need for improved test case generation, which will be needed more by the specific tool used than by a consistent measure of test suite quality.

We based on these traditional methods by avoiding the random selection of predefined rules that apply mutant operators uniformly across all code. Instead, our study investigates an LLM's capability to dynamically select context-aware mutant operators—validated against real developer-committed faults—by performing a semantic-based search on the secondary dataset to identify the most suitable mutations for each code scenario.

Shifting from predicted rules, Brown et al. (2017) empirically derived true rules based on positive and negative experiences for special categories of code comments on GitHub. Their approach, implemented in the mutgen tool,

1 https://github.com/nutgen-gpt4-based/MutGen-LLM-Based-Research

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

7

uses lexical analysis and pattern matching — not machine learning — to algorithmized methods, like those of extracting skills, creating a large set of fault patterns grounded in actual developer behavior.

We fundamentally differ from the lexical, pattern-matching, technique of Brown et al. ( 2017 ) by using GPT-1's semantic reasoning. Instead of manipulating tokens, our method employs a prompt template to guide an LLM in generating or reordering a more sophisticated alternative to purely syntactic operator application.

Machine learning (ML) has also been used to generate realistic mutants, Beller et al. (2021) built upon empirical principles with Mutation Monkey, a tool that learns mutation patterns from curated fault datasets (e.g., Dectofect4J) using a ML system called GMeta . Similarly, Tufano et al. (2019; 2020) embedding mutation models in a ML system to generate and demonstrate the ability to generate mutants with high stochastic validity and a significant rate of exact matches to original bugs from software repositories.

In contrast to prior ML approaches that depend on a persistent operator catalog, our research proposes using prompt engineering with an LLM (without fine-tuning) to generate mutants competitively with state-of-the-art methods. Our key innovation is a dynamic workflow where mutation logic is generated on-the-fly in response to specific code inputs, rather than being statically retrieved from a pre-trained model.

### 2.2 LLM used in Mutation Testing

Recent studies have begun leveraging LLMs to address specific challenges in mutation testing, though not for the core task of mutant generation. Dakhil et al. (2024) used LLMs like Llama-2 and Codex to augment test generation for surviving mutants produced by a traditional tool (MutPy). Similarly, Tian et al. (2024) applied LLMs with optimized prompting to the difficult problem of acquiring the mutant detection, showing significant improvement over traditional methods. Because these tools are LLMs as complementing tools, we study positions the LLM as the core component for the direct generation of mutants.

Foster et al. (2025) developed a thematically similar multi-agent system using LlamaA 70B. However, their work differs from ours in its fundamental objective and approach. Their system is concern-driven: it starts with a highlevel issue (e.g., privacy) and uses intent generation as an intermediate step. In contrast, we address a single challenge in our research: we are not agentdriven, focusing on using the LLM as the core engine for direct and generalpurpose mutant generation, rather than for generating tests.

In contrast, even though both studies use agentic workflows, ours leverages mutation operators from historical bug-fix commits, grounding mutations in real-world faults. While Foster et al. (2023) focus on test synthesis, we extend their work to test the generability of mutation and insert mutation-geneting combinations affect GPT-1's ability to generate fault-representative mu-

---

8

Erlon Pereira Almeida et al

tants—thereby shifting the optimization target from the tests to the mutatio source itself.

Others studies have applied language models to mutant generation. Degiovanni and Papadakis (2022) used μBERT for masked token replacement in Java, achieving a high fault detection rate. Expanding on this, Tip et al. (2025) compared multiple LLMs for generating JavaScript mutants, using AST node-based placeholders to enable more complex mutations than traditional replacement methods. Our results diverge from prior approaches to leveraging GPT-4-L to directly generate mutations from bug-fixes. Specifically, we rigorously analyze carefully designed prompts that explicitly instructs the LLM to select and apply mutation operators based on bug-fix history.

Li and Shin (2024) utilized mutation testing to evaluate LLM code understanding, specifically by mutating code descriptions to test for inconsistency detection. Our study diverges fundamentally from this approach in objective, methodology, and the LLM's role. While we extend the underlying principle of using mutation to probe model understanding, we apply it directly to the source code rather than natural language descriptions. Instead of positioning the model as a passive consistency checker, our systematic evaluation framework—grounded in 18 Java AST node types and 4 fundamental change operations—tasks the LLM as an active core generator and analyzer. Specifically, we assess GPT-4's ability to identify and replicate precise code modification patterns from bug-fix pairs, effectively reversing real-world fixes to recreate bugs.

Most closely related to our work, Wang et al. (2024a) conducted a largescale benchmark of six LLMs against traditional (including mJaa (Ma et al., 2006) and PIT (Coles et al., 2016a) ) and learning-based mutation tools. Their evaluation uses an extensive array of metrics, including compilability rate and similarity to 851 real lungs, to assess the mutants. The LLMs are prompted using a direct, fine-tuning approach with general few-shot examples from up to 1000 runs. In contrast to the SFT-LLM approach, we generate diverse code snippets, producing 45 distinct AAAI code types compared to only 20 rule-based tools (Wang et al., 2024a) .

Our proposed research uses a “ one-to-one ” targeted replication method. For a given code snippet, our automated workflow searches in dataset (the secondary) to find a single, highly similar historical fault. The LLM's task is then to understand the specific transformation in that single example and replicate it on the target code. This historical grounding yields 72 empirically derived mutation operators, providing a middle ground between rule-based approaches (2 AST node types) and pure LLM-based methods (45 types). In addition, our study explores how to architect an LLM-based system for a specific mutation task, whereas Wang et al. (2024a) focus on what the performance of different LLMs is on a more general mutation task.

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

9

## 3 Experiment Design

This study is grounded in the hypothesis that LLMs can serve as the primary component for generating significant mutants that accurately represent realworld faults. To validate this hypothesis, we conduct a deep, methodological investigation focused on a single, state-of-the-art model: GPT-4.1. This focused design choice is intentional and stems from our primary goal to perform a foundational characterization of the behavior and failure modes of a powerful LLM in the specific task of structured code mutation, rather than providing a superficial benchmark across multiple models.

The methodology proposed herein, grounding mutant generation in historical patterns, is implemented using the LangChain framework, ensuring a modular architecture that is easily adaptable to virtually any LLM. While this technical design facilitates the seamless substitution of the underlying model, rigorously characterizing the generation phenomena requires an in-depth, controlled analysis of a single model's behavior across thousands of data points. Using a top-tier model serves a crucial methodological purpose: it ensures that any observed limitations are attributable to the inherent challenges of the task and our methodological flaws, rather than to the inherent failure of intrinsic capacity. Consequently, if the proposed approach fails with a model of itself, it's it must indicate a fundamental limitation of the methodology of this By establishing a detailed analytical framework with a high-performance baseline (GPT-4.1), we provide the essential groundwork for future research, allowing subsequent studies to systematically evaluate other LLMs (e.g., Code Llama or Codex) against a well-understood standard.

To operationalize this investigation, we developed an automated workflow that combines GPT-4.1 with historical bug-fix data to determine the optimal conditions for mutant generation while investigating the model's cognitive limits. The study is organized into two sequential steps:

Step 1 (Operator Identification): We tested the LLM's ability to identify unique modification patterns from defective evolution (bug-fixes) in Jaccard code at the Abstract Syntax Tree (AST) node level. This was accomplished by systematically evaluating various prompting techniques, ranging from simple instructions to complex instructions, generated by Artificial Neural Networks (RAG) (Soudani et al., 2024) . To provide a granular analysis of the model's performance in this task, we addressed two specific sub-questions:

- – RQ1.1 : To what extent does our prompt engineering strategy dictate the
model's error profile?
– RQ1.2 : Which Java node types are difficult for GPT-4.1 to identify accu-
rately, given the prompt strategies applied in this study?
This initial evaluation was a crucial prerequisite for the generation task. Given the high-availability of LLMs to prompt construction, the approach of 3.2.3 will be considered.

3 https://codellama.dev/about

Downloaded by: [ University of California, San Diego]

• https://openai.com/pt-BR/index/codex-now-generally-available

---

10

Erlon Pereira Almeida et al.

fectiveness can vary drastically based on the chosen strategy. Since the specific impact of different prompt techniques on this structured task was unknown, by answering these sub-questions provided the essential insights needed to select an optimal prompt. This selection, in turn, enabled the creation of an effective workflow for Step 2, aimed at maximizing the model's reasoning capabilities through the high fidelity and semantic representativeness of the generated mutants.

Step 2 (Mutant Generation): We applied the optimal prompt template from Step 1, adapting its core instruction to shift the task from operator identification to code generation, to generate mutants for the entire main dataset. We then compared them with those produced by a validated baseline tool based on Recurrent Neural Network (RNN) translation models (Tufano et al., 2019) . This baseline score was deliberate, enabling a direct comparison between two distinct machine learning paradigms. Notably, this design contrasts a general-purpose LLM (GPT-4 $\dagger$ ), guided only by prompts, against specialist RNN models specific to NER tasks (Han et al., 2021; Liu et al., 2020; et al., 2019) . This comparison is methodologically the most appropriate, as the extracted, non-complausible nature of the dataset makes a direct evaluation against traditional tools (like PIT (Coles et al., 2016b) or MAJOR (Just et al., 2011) ) infeasible. The comparison utilized two metrics: the BLEU score for lexical realism and semantic similarity (via embedding vectors) to assess conceptual equivalence. This process revealed the strengths and limitations of our approach in using GPT-4 $\dagger$ for mutation testing. We detail the specific methodology for each step below.

### 3.1 Dataset

The dataset chosen for our study is in Java language and is unconventional. This dataset underwent a generalization process for each node, which forces the LLM to understand the code's structure, as its presentation prevents confusion with internal data that was incessantly used for training or fine-tuning. This makes it perfect for our experiment of exploring the limits of a language model's ability to comprehend and manipulate Java code.

This dataset, developed by Tufo et al. (2019) , was created from 78,178, Java bug-fix commits mined from public GitHub repositories between 2011 and 2017. The central idea of their work was to automatically learn how to generate realistic mutants by training Recurrent Neural Network (RNN) models to reverse the transformations present in the bug fixes (i.e., learning how to transform fixed into buggy code). The bug-fix commits were initially identified from the GitHub Archive using keyword-based filters (e.g., “ fix ” and “ bug ” ) and the Google BigQuery APIs. From this set, method-level code changes were extracted using the GitHub Compare API 3 and an AST based differentiation tool, GumTree (Falleri et al., 2014) . Several filters were applied to ensure that

5 https://docs.github.com/pt/rest/commits/commits?apiVersion=2022-11-28

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

11

quality. First, the scope of the analysis was restricted exclusively to commits from Java-centric repositories. From this initial set, we further excluded commits that modify more than five Java files — these likely represent tangled code websites. Additionally, we excluded code written in C and C++ languages (TPs), each containing a buggy method and its corresponding fixed version.

To reduce vocabulary complexity and focus the models' learning on structural transformations, Tufano et al. (2019) applied a preprocessing pipeline that abstracts Java source code. In this process, project-specific identifiers are generalized to preserve structural patterns while removing contextual details. For instance, as shown in Figure 1 , type names such as Integer and ListManager were replaced with generic placeholders such as TYPE1 and TYPE2 , while method names like getH1Element were abstracted to METHOD1 . As common data warehousing (e.g., maps and records) are preserved to preserve the meaning of structural syntax features and semantic context of the code constructs. A fundamental step in their process was the preservation of 272 highly frequent terms, or “ idioms ” (such as eques or the literal 0), which were identified through statistical analysis and manual curation to retain important semantic context (Tufano et al., 2019) .

This process, originally designed to train RNN mutation models, resulted in a dataset partitioned into a training set of 82,515 TPs and a test set of 10,313 TPs. To allow for a more granular analysis, Tufano et al. (2019) organized the dataset using an unsupervised clustering algorithm. This method resulted in five distinct clusters, grouping Transformation Pairs that share similar scientific characteristics, based on their common origins and modifications. For each cluster, we used the established tree of Tufano et al. (2019) , drawing upon the data from all five clusters underpin our LLM-based analysis.

```bash
public integer getMinElement(List myList) {
    if(myList.size() >= 1) {
        return ListManager.min(myList);
    }
    return null;
} public TYPE_1 METHOD_1 (List VAR_1 ) { if (
VAR_1.size() >= 1 ) { return TYPE_2 .min ( 
VAR_1 ); } return null ; }
```

Fig. 1 Code abstraction example from Tufano et al. (2020)

Many Java nodes occur with extremely low frequency, presenting two challenges for our GPT-1 analysis. First, it is difficult to draw meaningful conclusions about the model's performance on these infrequent nodes. Second, these nodes are often spurious and their low frequency suggests a different interpretation of the model. Finally, we are interested in how the selected few nodes contribute to our findings, which will be discussed in the following section.

---

12

Erlon Pereira Almeida et al.

fications, which appear 3,945 times. Conversely, nodes such as while, assert, ArayTypeReference, and break appear only 6, 6, 5, and 2 times, respectively.

To address this challenge, we determined that a data pruning step was necessary. Based on an analysis of the node distribution within each cluster, using a static code diff tool, we established a minimum threshold of 100 occurrences for a given Java node type to be included in our experiment. Consequently, any Transformation Fair composed exclusively of node types that fell below this threshold were pruned. This way, when analyzing and pruning approaches served the dual purpose of eliminating statistically insignificant data points, it was clear that the computational costs associated with the LLM's API, while still retaining a sufficient data volume for a robust analysis.

A key characteristic of the dataset is that each Transformation Pair is typically composed of multiple, fine-grained modification in each Java nodes. This compositional nature has a direct implication on the filtering process: removing a TP to filter out one low-frequency Java node inherently removes all other nodes bundled within that same TP, thus altering the overall frequency distribution.

Consequently, our filtering process did not eliminate every instance of noise components, as some were preserved when they co-occurred in a TP with high-frequency Java nodes that met the threshold. Nevertheless, the pruning algorithm only resulted in minimal changes to the overall representation of Java nodes modified and noise in the data for a more focused analysis.

Our final curated dataset (the main dataset) is a subset of test data from Tifano et al. (2019) . This subset contains 8,322 TFs covered by modifications in a testing or validation components. The final distribution of these nodes across the five distinct clusters is presented in Table 1 and analyzed in the discussion that follows.

Table 1 Absolute and Relative Frequency ( % ) of Components by Cluster.

<table><tr><td>Component</td><td>Cluster 1</td><td>Cluster 2</td><td>Cluster 3</td><td>Cluster 4</td><td>Cluster 5</td></tr><tr><td>Assignment</td><td>-</td><td>-</td><td>-</td><td>115 (1.4%)</td><td>928 (10.6%)</td></tr><tr><td>Subcluster</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td></tr><tr><td>If</td><td>236 (2.5%)</td><td>73 (2.1%)</td><td>72 (1.9%)</td><td>837 (9.9%)</td><td>113 (2.6%)</td></tr><tr><td>Owner-user</td><td>299 (3.5%)</td><td>106 (3.1%)</td><td>106 (2.8%)</td><td>106 (1.2%)</td><td>106 (2.6%)</td></tr><tr><td>Innovation</td><td>3434 (42.8%)</td><td>735 (21.7%)</td><td>754 (19.0%)</td><td>3115 (39.2%)</td><td>680 (16.2%)</td></tr><tr><td>Type-Action</td><td>3490 (33.37%)</td><td>426 (12.67%)</td><td>636 (11.43%)</td><td>951 (9.42%)</td><td>348 (8.8%)</td></tr><tr><td>Variable-Action</td><td>651 (7.47%)</td><td>164 (4.76%)</td><td>127 (2.97%)</td><td>414 (4.5%)</td><td>154 (3.5%)</td></tr><tr><td>Technical-Action</td><td>367 (4.2%)</td><td>-</td><td>-</td><td>101 (1.1%)</td><td>207 (5.1%)</td></tr><tr><td>Time</td><td>531 (5.7%)</td><td>142 (4.27%)</td><td>132 (3.09%)</td><td>108 (1.1%)</td><td>112 (2.7%)</td></tr><tr><td>Construct-Call</td><td>-</td><td>128 (3.4%)</td><td>198 (5.2%)</td><td>59 (0.6%)</td><td>130 (3.0%)</td></tr><tr><td>Parameter</td><td>-</td><td>-</td><td>-</td><td>10 (0.1%)</td><td>-</td></tr><tr><td>Software</td><td>54 (0.55%)</td><td>450 (13.39%)</td><td>451 (8.08%)</td><td>63 (0.62%)</td><td>-</td></tr><tr><td>W</td><td>-</td><td>-</td><td>305 (5.98%)</td><td>59 (0.6%)</td><td>16 (0.4%)</td></tr><tr><td>User-Operator</td><td>-</td><td>-</td><td>-</td><td>21 (0.19%)</td><td>-</td></tr><tr><td>Return</td><td>135 (1.29%)</td><td>59 (1.76%)</td><td>145 (2.61%)</td><td>420 (4.6%)</td><td>-</td></tr><tr><td>Block</td><td>29 (0.28%)</td><td>85 (2.36%)</td><td>51 (0.92%)</td><td>59 (0.6%)</td><td>118 (3.0%)</td></tr><tr><td>Total</td><td>10,285</td><td>3,361</td><td>3,562</td><td>10,285</td><td>4,305</td></tr><tr><td>Number of terms per TP</td><td>0.25</td><td>0.25</td><td>0.25</td><td>0.25</td><td>0.25</td></tr><tr><td>Amount TP per cluster</td><td>0.002</td><td>0.002</td><td>0.002</td><td>0.002</td><td>0.002</td></tr><tr><td rowspan="2">Primary Role</td><td>Dance</td><td>0.002</td><td>0.002</td><td>0.002</td><td>0.002</td></tr><tr><td>Open-text</td><td>Intimidation</td><td>And-Construction</td><td>Flow-Log</td><td>Management</td></tr></table>


---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

13

Cluster 1, the largest cluster with 10,458 modifications, exhibits a profile specialized in domain operations. It is characterized by the dominance of modifications to Invocation (32.83 % ) and TypeAccess (33.37 % ) nodes, indicating a primary focus on executing business logic through method and class construction, followed by code rewriting (FieldTotal: 6.61 % , Var: able-Read: 6.44 % ). The absence of control-flow node modifications suggests predominantly sequential, linear execution logic.

Cluster 2 (3,361 modifications) exhibits a profile that aligns with object initialization and configuration. This is suggested by a high concentration of nodes involved in invoking functions and handling types. The most prominent activity is method invocation ( Inevocation , 21.87 % ), supported by operations involving types ( TypeAccess , 12.67 % and TypeReference , 13.39 % ). The process appears to rely on reading data from variables ( VariableRead , 16.78 % ) and using local variables ( LocalVariable , 11.84 % ), which likely supply the necessary parameters and temporal information for an application. The fact that these variables are captured on nodes like If ( 21.71 % ) and WrongOperator ( 9.33 % ) indicates these modifications are likely focused on the linear setup and assembly of objects rather than on implementing complex conditional logic. The collective evidence points to a cluster specialized in the preparatory stages of creating and configuring objects.

Cluster 3 (5,602 modifications) is characterized by the definition and modification of methods and constructors. This is indicated by a significant presence of Parameter nodes (8.09 % ), which are exclusive to signatures. The internal logic of these units involves VariableRead (14.87 % ), Invocation (12.69 % ), and Literal (12.69 % ) nodes, suggesting operations that read data and call other constructors, even with constraints. The modifications are granular, averaging 2 to 4 node languages. However, it is possible that this shorter version is predominantly represents modifications to reusable code units like methods and constructors.

Cluster 4 (10,090 modifications) is characterized by modifications that strongly suggest a focus on altering a program's control flow and decisionmaking logic. This is primarily evidenced by the high co-occurrence of If (8.29 % ) and BinaryOperator (13.87 % ) nodes, which are the core components of conditional statements. The conditions within these structures appear to be based on reading object state, as indicated by Fieldpad (10.44 % ), and compared against a global entity value field (10.36 % ). The significance of the presence of Block (9.72 % ) nodes confirms that this cluster involves a nodes of code executed by these control flow structures. While method calls are involved (Invocation with 23.92 % ), the overall profile of this cluster is dominated by the components that define and branch execution paths.

Cluster 5 (4,305 modifications) exhibits a profile that is highly suggestive of a specialization in object state management. This interpretation is primarily driven by the dominant co-occurrence of Assignment (21.51%) and FieldWrite (21.18%) nodes, a combination that typically represents operations that update field values. The notable prevalence of Literal (12.17%) and ThisAccess (4.76%) nodes further supports the notion that these modifications often in-

---

14

Erlon Pereira Almeida et al.

volve assigning constant values to an object's own fields. Therefore, the collec- tion contains values for which we would like to encode the foundational operations for defining and updating an object's internal data.

### 3.2 Step 1: Analyzing LLM's Capabilities for Detecting AST Nodes.

![Figure](figures/ESE_journal_Erlon_page_014_figure_004.png)

Fig. 2 Workflow done in the process of testing GPT-4.1 on identifying modifications in each TP.

Figure 2 depicts the workflow used to evaluate GPT-4's ability to identify code modification patterns that transform fixed versions into buggy ones. The process began with an analysis of a dataset containing 10,313 TPs. This analysis revealed a substantial imbalance in the frequency of approximately 48 types of Java code nodes. These nodes could be modified through four operations: Insert, Move, Update, and Delete. We define a mutation operator as one of these four operations applied to a specific Java node type. As a result of this analysis, we found that out of 110 times, 47 changed, and in the last 100 times were excluded, resulting in a refined dataset of 8,323 TPs spanning 18 Java nodes. Considering those four operators by each node, we got a total of 72 mutation operators.

To identify the mutation operators in the dataset, we generated AST-level directional constraints on each mutation site. This method is known as a algorithm that computes fine-grained and accurate source code differences

6 https://github.com/SpoonLabs/guttres-spoon-ast-diff

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

15

configured with the Spoon parser. This general approach of using GunTree for code-diffing has been previously validated in studies such as Tan et al. (Tufano) (2019) , which allowed us to use the generated outputs as a starting point and choose the most parsimonious tree. GPT-LL would identify the same transformations using GunTree's notation.

The evaluation was conducted over four iterative rounds (or “ Attempts ” ), each leveraging a distinct prompt template that incorporated the techniques outlined in Table 2 . In each attempt, GPT-4.1's raised-mutation operations were compared against the Gumble ( Balled et al. , 2014 ; Martinez et al. , 2023 ) .

Upon completing this analysis, we compiled: (1) mutant operators identified as true positives, false positives and false negatives, (2) the accurate rate for correctly assessed TPs within each cluster, and (3) the percentage of Java cases that generated accurate responses, (4) and the most repeated errors raised.

Table 2 Overview of All Prompting Techniques Used.

<table><tr><td>Technique</td><td>Description</td></tr><tr><td>Few-shot learning (FS)</td><td>Offering the model one or more input-output samples to guide text generation (Brown et al., 2020).</td></tr><tr><td>Retrieval-Augmented Generation (RAG)</td><td>Enhancing the model's responses by extracting additional information from external knowledge sources or documents, which are then used as context to generate more accurate and informed outputs (Soudan et al., 2024).</td></tr><tr><td>Zero-shot learning (ZS)</td><td>Providing the model with direct task instruction, without prior examples (Wei et al., 2022).</td></tr><tr><td>Chain of Thought (CoT)</td><td>Decomposing complex problems into a sequence of intermediate steps for more detailed and interpretable problem-solving (Wei et al., 2023).</td></tr><tr><td>Persona (SyS)</td><td>Assigning a specific person or persons to the language, using additional source style and content (White et al., 2023).</td></tr></table>


While absolute error counts (FPs and FNs) are useful for understanding the overall volume of errors, they can be biased by the frequency of node types in the dataset. To measure the model's inherent difficulty with each node type, independent of its frequency, we define a Normalized Failure Index (NFI). The NFI is obtained as the ratio of the total number of times that a node is detected as the ratio of the total number of TPs with an error (either FP or FN) to the total frequency of that node's modifications in the ground truth dataset:

$$\begin{array} { r } {  N F I  = \frac { (  T o t a l ~ T P s ~ w i t h ~ F P  ) + (  T o t a l ~ T P s ~ w i t h ~ F N  ) } {  T o t a l ~ F r e q u e n c y ~ o f ~ t h e ~ N o d e ~ M o d i f i c a t i o n  } \times 1 0 0 \% } \end{array}$$

---

16

Erlon Pereira Almeida et al.

This index provides a measure of the model's proportional unreliability, allowing for a fair comparison between common and rare node types.

Thus, the objectives of this evaluation are to:

- 1. Quantify the deviation of GPT-4.1's results from the baseline tool;
2. Identify the most effective approach for employing an LLM in mutation
operator identification, and hence, for mutation generation;
3. Discuss relevant findings and discuss implications with policy
4. Examine patterns and potential biases in its results.
It is important to note that while several prompt techniques are reused across the four templates, their specific content is not always identical. For example, the Persona technique (White et al., 2023) is used in all four templates with largely consistent content (act as an `expert in Abstract Syntax Tree (AST) analysis for the Java language'). Conversely, the Chain-of-Thought technique (Wei et al., 2023) , although employed in three of the four templates, is slightly adapted in each case to complement the other techniques present within the same prompt template.

Attempt 1: We employed three prompt techniques. The Persona (Hite et al., 2023) technique to configure GPT-4.1 as an 'expert in Abstract Syntax' Tree (AST) analysis for the Java language', the Chain-of-Thought (Wei et al., 2020) technique (Han et al., 2021) and the 2020-2021 transfer learning (Tian et al., 2021) learning (Brown et al., 2020) , where we provided six exemplar fixed-to-buggy transformations from the training dataset of Tufano et al. (Tufano et al., 2019) , following the number of few-shot examples proposed by Deng et al. (Deng et al., 2024b) (six examples), which they found to be a sufficient number of examples for an LLM to act in code task. To mitigate GPT-4.1's tendency for code generation, we provided 1000 randomly chosen code snippets from past while expecting the model to propose valid modifications to any input. Figure 3 shows the template's structure used in this Attempt 1.

The advantages of this approach lie in its ability to effectively guide the LLM's code analysis and standardize its output. The primary disadvantages are the extensive prompt size, which makes it the most costly strategy, and the fact that llmControl (control) will not make much contribution into noise and adversely affect the quality of the generated response.

Attempt 2: This attempt enhances the prompt by incorporating a RAG approach (Soudani et al., 2024) . We created a knowledge base containing the explanations for all 18 annotated Java nodes (the same across all Attempts). This text was converted into vector embeddings using OpenAI's Text-Embedding-3-Large model 7 and stored in a vector database to enable semantic retrieval. For each TP, relevant chunks from the knowledge base were tokenized and translated into GPT-2. Additionally, the Chain-of-Thought (CoT) technique (Wei et al., 2021) was employed to instruct the model to perform an -step-by-step analysis.

This RAG-based methodology is designed to ground the model's reasoning in the provided documentation, thereby preventing hallucinations or reliance-

7 https://platform.openai.com/docs/models/text-embedding-3-large

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

17

![Figure](figures/ESE_journal_Erlon_page_017_figure_002.png)

Fig. 3 The prompt structure from Attempt 1.

on potentially incorrect knowledge from its internal training. The prompt explicitly directs the model to prioritize the retrieved context, ensuring that its analysis is based on the specific operator definitions supplied. In next Attempt, we formulated a method that represents the most straightforward approach for formulating a mutation operator identification task. The advantage of next Attempt lies in its ability to evaluate whether GPT-4.1 can effectively apply the correct modification from a mutation operator, given that the correct answer is contained within a provided set of options.

Attempt 3: We simplified GPT-1's decision-making by reformulating the task as a sequence of tasks, where each task is a $1$ -tailed sequential mutation operators that always included the correct solution.

The multiple-choice format followed these rules.

- For single-operator transformations: 5 candidate operators; and
Four multiplex single-operator +2 candidate operators (e.g., 8 op-
tions for 2-operator transformer).
---

18

Erlon Pereira Almeida et al.

We used Zero-shot (Wei et al., 2022) learning to establish the task and discriminate between positive instances and negative instances while operating in Persona . (White et al., 2023) consistently outperforms previous attempts, and

This setup allows for an objective assessment of the model's capability to correlate the inputs with the potential correct answers. However, this approach is limit to identification task, as we had to provide the set of mutation operators that simulate the correct fault from buggy version. Next Attempt we designed a template to leverage the full reasoning potential of GPT-4.1. As initial, user-sourced responses were subsequently processed and aligned with the data. The wet and defective results are shown in Figure 2 .

Attempt 4: We employed a two-stage process per TP to identify the mutation operators. The first stage involved tasksing GPT-4.1 to independently evaluate the TP without contextual information from the vector database, thereby collecting suggestions based on its internal knowledge. In the second stage, we performed a semantic search on GPT-4.1's free-text response to identify which nodes in the vector database it referred to. That is, for each modification proposed by GPT-4.1, we subsequently standardized it by performing RAG, which enabled us to generate a score in the final ranking. This had the highest semantic similarity to the proposed modification. The Person (Wei et al., 2023) , Zero-Shot (Wei et al., 2022) , and Chain-of-Thought (Wei et al., 2023) prompting techniques remained the same as in previous attempts.

The advantage is the reduced size of the required prompt. The main disadvantage, however, lies in the difficulty of standardizing GPT-J's output, as it must be mapped to the structured data from the vector database. Performing an accurate semantic search for this mapping can be complex.

### 3.3 Step 2: Generating Mutant Code

The second Step of this study consists of a workflow to instruct an LLM (GPT4.1) to generate mutants that represent real software faults. The process aims to transform fixed versions from the main dataset into mutant versions that are similar to their original buggy counterparts.

To achieve this, the primary objective is to define the mutation operators that will guide GPT-4.1. These operators are extracted from TFs in the secondary dataset, which is a subset of the train dataset used by Tufano et al. (2019) for training RNN models.

As shown in Figure 4 , the workflow begins with data preparation (Figure 4 block A). The main dataset (Figure 4 -A2) contains 8,322 fixed roles for which mutant versions need to be generated. The mutation operators for each fixed code are extracted from TPs in the secondary dataset (Figure 4 -A1). This dataset is filtered using the GnnTree tool (Falleri et al., 2014; Martinez et al., 2016) . This process outputs a weighted distribution, with weights 3.1), to retain only TPs whose modifications involve the 18 most frequent Java node types shown in Table 1 , providing us with a search base comprising 71,603 TPs. The selection of these filtered TPs is based on the semantic similarity

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

19

![Figure](figures/ESE_journal_Erlon_page_019_figure_002.png)

Fig. 4 Multi-agent workflow built for Step 2

between the fixed code from the main dataset and the codes from the secondary dataset. To optimize this large-scale search, the secondary dataset was indexed into a vector database (Figure 4 -A), enabling efficient retrieval of similar images. According to our understanding, in order to achieve this goal, a 2018 Malkov and Yashin, 2018; Jafari et al., 2021) search algorithm.

After selecting similar TPs for each fixed code in the main dataset, the mutation operations contained within them were extracted and formatted (Figure 4 -B). This information was then consolidated into a DataFrame (Figure 4 -C), which served as input for a specialized LLM agent called MutGen (Figure 4 D). For this task, the GPT-4 1 input prompt was adapted from the template that achieved the best performance in RQI (operator identification) to suit the mutant generation task. Due to the L/O-bound nature of the task and to the limited memory of the LLM, the LLM did not compute all quantum operations, and the 8,322 mutants was not executed all at once. Instead, we adopted a batch processing strategy. The process was conducted on a machine equipped with a 13th-generation Intel core i7 processor, 32 GB of RAM, and a GPU with 16 GB of VRAM. For each batch, 15 concurrent requests were sent to the API to maximize throughput without exceeding the service limits.

At the conclusion of the Step 2 workflow, the mutant versions generated by the LLM and those from Tufano et al. (2019) (RNN models) (Figure 4 -E) were used to perform a lexical (Figure 4 -G) and semantic (Figure 4 -F) comparison against the buggy versions from the main dataset. The baseline models from Tufano et al. (2019) are based on an RNN Encoder-Decoder architecture. Crucially, this baseline is not a single, general model, but an ensemble of five specialized models ( $M_1$ ,..., $M_5$ ). As described in the original study, each of these models was trained and fine-tuned exclusively on the data from its

---

20

Erlon Pereira Almeida et al.

corresponding cluster. The training for each model was substantial, utilizing cluster sizes of $C_1 = 30, 385$ TFs, $C_2 = 7,016$, $C_3 = 29,625$, $C_4 = 25,320$, and $C_5 = 10,798$. This establishes a fundamental asymmetry in our comparative analysis: the performance of a single, general-purpose foundation model (GF-4/11, guided only by a prompt), is benchmarked against five specialist models that are evaluated on the specific data category on which it was exhibitorly trained.

To assess lexical similarity, we employed the BLEU (Bilingual Evaluation Understory) metric (Papineni et al., 2002) . BLEU is an automated score designed to quantify the lexical similarity between a machine-generated text and human-written reference texts. Its core mechanism involves comparing sequences of words (n-grams) to measure overlap, while also adjusting for word frequency and penetrating over short generated texts. The final BLEU score, which is based on the overlap matrix and the following rules for adjusted text, showing high correlation with human judgments of quality. In our study, the mutants (generated by both the LLM and the RNN) were compared against the buggy versions from the main dataset, which served as the reference.

To assess semantic resemblance, we employed Cosine Similarity, a metric that quantifies the similarity between two texts by measuring the cosine of the angle between their vector representations (embeddings). The process first transforms the text string into its associated vector representation using a buggy code, into a numerical vector using OpenAI's text-embedding-3-large model. Unlike metrics such as Euclidean distance that measure magnitude, cosine similarity focuses purely on the orientation of these vectors in a highdimensional space. The resulting score ranges from -1 to 1, where a value of 1 indicates identical orientation (maximum semantic similarity) and 0 indicates identical orientation (minimum semantic similarity). However, we ask whether a generated mutant preserved the functional purpose of the original fault.).

This study evaluates generated mutants against reference buggy code along two complementary dimensions: lexical fidelity and semantic resemblance. Lexical fidelity, measured using the BLEU score, quantifies the surface-level ngram overlap between the generated and reference code, assessing the correctuse of keywords, identifiers, and syntactic structure. Semantic resemblance, measured via Cosine Similarity of code embeddings, evaluates whether the mutant tries to preserve the functional purpose and logical intent of the original, even with differing syntax. Employing both metrics allows us to distinguish merely syntactic copies from conceptually equivalent mutants, providing a holistic evaluation of the models' generation capabilities.

## 4 Results

This section presents the findings obtained through the methodology used to answer the research questions.

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

1

RQ1: What is the most effective way to instruct an LLM model in identifying modifications to Java code?

Table 3 presents the results of all Attempts for each cluster in Step 1. These results consider the complete response, meaning we verified whether the initial operators provided by the LLM (specifying which modification was made) were correctly located in the list identified by GumTree (Pallett et al., 2014; Martinez et al., 2023) .

We observed that the examples from the Few-Shot technique influenced the accuracy results, showing that Attempt 1 achieved balanced results, ranging from 70.57 % to 74.08 % across all clusters. We also noted that the Recall results were the highest among all Attempts, reaching up to 61.367 % in Cluster 3.

In Attempt 2, although GPT-1.1 showed significant precision results in chusters 1 and 2, its performance dropped drastically in the remaining clusters, leading to $42.9\%$ in cluster 5. Furthermore, it presented the worst Recall result in all other clusters, with all values below $58\%$ , reaching as low as $12.2\%$ , also in cluster 5.

Attempt 3 produced the best precision results among all Attempts. This result is due to the fact that this prompt template provides the correct intent and options for most participants. Although it is not the best result yet, it is best in cluster 3, with 79.21 % and the highest was in cluster 5, with 90.53 % . The Recall results all remained below 50 % , which lowered the F1-Score level.

The results of Attempt 1 showed precision slightly lower than that of Attempt 3, notably in clusters 1, 2, and 5, in addition to being the Attempt with

Table 3 Classification metrics from GPT-4.1 Responses per each Attempt.

<table><tr><td></td><td>Cluster</td><td>Precision</td><td>Recall</td><td>F1-Score</td></tr><tr><td rowspan="5">Attempt 1</td><td>1</td><td>73.06</td><td>57.19</td><td>64.16</td></tr><tr><td>2</td><td>74.08</td><td>53.73</td><td>62.29</td></tr><tr><td>3</td><td>74.78</td><td>47.04</td><td>60.62</td></tr><tr><td>4</td><td>74.21</td><td>40.04</td><td>52.01</td></tr><tr><td>5</td><td>74.59</td><td>51.89</td><td>61.21</td></tr><tr><td rowspan="5">Attempt 2</td><td>1</td><td>84.22</td><td>27.52</td><td>41.51</td></tr><tr><td>2</td><td>84.90</td><td>24.45</td><td>41.74</td></tr><tr><td>3</td><td>48.94</td><td>29.79</td><td>37.04</td></tr><tr><td>4</td><td>54.11</td><td>16.37</td><td>25.13</td></tr><tr><td>5</td><td>56.42</td><td>12.28</td><td>19.04</td></tr><tr><td rowspan="5">Attempt 3</td><td>1</td><td>90.24</td><td>41.46</td><td>46.65</td></tr><tr><td>2</td><td>81.14</td><td>26.75</td><td>40.23</td></tr><tr><td>3</td><td>79.21</td><td>17.73</td><td>59.57</td></tr><tr><td>4</td><td>81.82</td><td>40.83</td><td>56.05</td></tr><tr><td>5</td><td>90.53</td><td>40.20</td><td>45.29</td></tr><tr><td rowspan="5">Attempt 4</td><td>1</td><td>86.24</td><td>27.98</td><td>42.25</td></tr><tr><td>2</td><td>75.02</td><td>22.79</td><td>34.96</td></tr><tr><td>3</td><td>69.07</td><td>43.47</td><td>53.36</td></tr><tr><td>4</td><td>74.77</td><td>44.12</td><td>54.33</td></tr><tr><td>5</td><td>89.68</td><td>24.41</td><td>38.38</td></tr></table>


---

22

Erlon Pereira Almeida et al.

the smallest prompt size. Furthermore, Attempt 4 presented slightly higher Recall results than Attempt 3, reaching 43.47 % in cluster 3.

Table 4 Aggregated Results of Precision, Recall, and F1-Score by Approach

<table><tr><td></td><td>Precision (%)</td><td>Recall (%)</td><td>F1 (%)</td></tr><tr><td>Attempt 1</td><td>73.302</td><td>52.842</td><td>61.062</td></tr><tr><td>Attempt 2</td><td>62.064</td><td>22.626</td><td>31.878</td></tr><tr><td>Attempt 3</td><td>88.910</td><td>29.642</td><td>42.242</td></tr><tr><td>Attempt 4</td><td>79.090</td><td>28.604</td><td>41.156</td></tr></table>


To determine the most effective prompt template for the mutant operator identification task, a comparative analysis of the aggregated results was conducted, as presented in Table 4 . Attempt 1, which combined techniques such as Chain-of-Thought (CoT) with 6-shot learning examples, demonstrated the best overall performance, achieving the highest F1-Score of 61.062 % . This result was primarily driven by its Recall of 52.842 % , the highest among all applications, indicating that it effectively identified the majority of cases correctly. In fact, although Attempt 3 achieved the highest Precision (84.830), its low Recall (26.462 % ) resulted in a considerable lower F1-Score. This suggests that, despite their accurate identifications, both Attempt 3 and Attempt 4 failed to detect a large portion of the necessary transformations.

Finding 1: The prompt template from Attempt 1 (Fig. 3 ) provides the main tool for the subsequent development. Although it attempts and is the most effective for the mutant operator identification task,

## RQ1.1: To what extent does our prompt engineering strategy dictate the model's error profile?

To answer RQ1.1, we conducted a quantitative analysis to evaluate whether GPT-4.1 adequately selected the node types to be modified within each TP. Our error analysis was therefore focused on the correctness of the node choice itself, rather than the frequency of its application within the code. The errors were categorized into two types. False Positives (FPs), where the model chose a node type that was not part of the ground truth transformation, and False Negatives (FNs), where the model failed to choose a node type that was wrong in its transformation. An error for as few as 10 was not counted as wrong per TP. To reach such an error count, we test the model's subdomain capability. This approach prevents complex TPs with multiple instances of the same node from disproportionately influencing the results. We then aggregated these TP-level error counts across all four prompting strategies (Attempts) to identify the nodes with the highest absolute error volumes.

Our analysis of False Positives revealed that a small subset of node types accounts for the majority of hallucinated content. As detailed in Table 5 , the five node types with the highest volume of FPs were VariableRoad (1968 instances), Invocation (1301), Return (1280), Literal (1006), and FieldRoad

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

1

Table 5 Percentage Contribution of Each Prompting Strategy to FP Errors per Node Type.

<table><tr><td>Node Type</td><td>Attempt 1</td><td>Attempt 2</td><td>Attempt 3</td><td>Attempt 4</td><td>Total Errors</td></tr><tr><td>Global</td><td>5.60%</td><td>7.78%</td><td>9.50%</td><td>10.93%</td><td>3.13</td></tr><tr><td>Innovation</td><td>3.87%</td><td>48.81%</td><td>4.92%</td><td>41.13%</td><td>1.301</td></tr><tr><td>Return</td><td>6.41%</td><td>10.39%</td><td>10.16%</td><td>73.05%</td><td>1.280</td></tr><tr><td>Field</td><td>8.67%</td><td>2.00%</td><td>6.15%</td><td>2.58%</td><td>1.993</td></tr><tr><td>FieldRead</td><td>94.62%</td><td>0.00%</td><td>5.38%</td><td>0.00%</td><td>0.00</td></tr><tr><td>LocalVariable</td><td>12.33%</td><td>0.00%</td><td>2.83%</td><td>0.00%</td><td>0.00</td></tr><tr><td>Time</td><td>1.16%</td><td>29.62%</td><td>9.83%</td><td>58.00%</td><td>5.19</td></tr><tr><td>Parameter</td><td>12.16%</td><td>23.08%</td><td>11.66%</td><td>53.10%</td><td>0.00</td></tr><tr><td>TypeAccess</td><td>12.33%</td><td>0.00%</td><td>1.16%</td><td>77.77%</td><td>0.00</td></tr><tr><td>If</td><td>5.76%</td><td>15.45%</td><td>5.50%</td><td>73.30%</td><td>3.82</td></tr><tr><td>TypeReference</td><td>49.60%</td><td>25.47%</td><td>10.72%</td><td>14.21%</td><td>0.00</td></tr><tr><td>Constructor</td><td>12.33%</td><td>0.00%</td><td>31.16%</td><td>1.16%</td><td>0.00</td></tr><tr><td>ConstructorCall</td><td>12.88%</td><td>0.61%</td><td>15.45%</td><td>71.17%</td><td>0.00</td></tr><tr><td>UnaryOperator</td><td>3.39%</td><td>2.34%</td><td>6.78%</td><td>2.29%</td><td>1.18</td></tr><tr><td>UnaryExpression</td><td>7.4%</td><td>77.61%</td><td>1.16%</td><td>13.43%</td><td>0.00</td></tr><tr><td>BinaryOperator</td><td>23.88%</td><td>22.39%</td><td>28.30%</td><td>25.37%</td><td>67</td></tr><tr><td>MathOperator</td><td>29.33%</td><td>21.16%</td><td>18.28%</td><td>28.30%</td><td>38</td></tr><tr><td>FieldWriter</td><td>61.29%</td><td>9.68%</td><td>22.58%</td><td>6.45%</td><td>0.00</td></tr></table>


(893). However, a deeper analysis of the error distribution, shown in Table 5 , demonstrates that these high volumes are not uniform but are instead concentrated in specific failure modes for each prompt strategy. For instance, 68.09 % of Variable Read errors and 94.62 % of Field Read errors originated from Attempt 1, whereas 73.05 % of Return errors were attributed to Attempt 4. On the other hand, errors for BinaryOperator were almost evenly distributed across all four attempts (ranging from 22.39 % to 28.36 % ), suggesting a more fundamental, strategy-agnostic difficulty for this task. It indicates that the choice of prompt technique often induces a specific error profile, effectively creating specialists in raising certain types of incorrect modes.

Table 6 Percentage Contribution of Each Prompting Strategy to FN Errors per Node Type.

<table><tr><td>Node Type</td><td>Attempt 1</td><td>Attempt 2</td><td>Attempt 3</td><td>Attempt 4</td><td>Attempt 5</td></tr><tr><td>Block</td><td>18.22%</td><td>28.10%</td><td>25.56%</td><td>28.12%</td><td>76.22</td></tr><tr><td>FieldRead</td><td>18.22%</td><td>28.10%</td><td>25.56%</td><td>28.12%</td><td>76.22</td></tr><tr><td>Literal</td><td>8.03%</td><td>36.28%</td><td>23.62%</td><td>31.87%</td><td>83.04</td></tr><tr><td>BlockRead</td><td>18.22%</td><td>28.10%</td><td>25.56%</td><td>28.12%</td><td>76.22</td></tr><tr><td>Innovation</td><td>16.21%</td><td>11.54%</td><td>26.79%</td><td>45.45%</td><td>49.72</td></tr><tr><td>Block</td><td>26.79%</td><td>26.79%</td><td>26.79%</td><td>26.79%</td><td>26.79</td></tr><tr><td>BlockOperator</td><td>12.95%</td><td>34.69%</td><td>29.81%</td><td>31.87%</td><td>42.58</td></tr><tr><td>TypeReference</td><td>16.65%</td><td>27.81%</td><td>24.29%</td><td>31.24%</td><td>40.58</td></tr><tr><td>Block</td><td>18.22%</td><td>28.10%</td><td>25.56%</td><td>28.12%</td><td>76.22</td></tr><tr><td>FieldWrite</td><td>11.94%</td><td>0.00%</td><td>0.00%</td><td>55.96%</td><td>1.401</td></tr><tr><td>Assignment</td><td>20.05%</td><td>48.34%</td><td>14.44%</td><td>17.27%</td><td>1.401</td></tr><tr><td>Constructor</td><td>0.81%</td><td>0.00%</td><td>0.00%</td><td>0.41%</td><td>0.00</td></tr><tr><td>ConstructorCall</td><td>9.70%</td><td>44.17%</td><td>15.77%</td><td>30.36%</td><td>1021</td></tr><tr><td>Return</td><td>19.76%</td><td>22.71%</td><td>23.88%</td><td>33.65%</td><td>365</td></tr><tr><td>BlockOperator</td><td>0.00%</td><td>27.79%</td><td>25.56%</td><td>28.12%</td><td>76.22</td></tr><tr><td>Variable</td><td>1.15%</td><td>87.96%</td><td>1.15%</td><td>10.34%</td><td>87</td></tr><tr><td>Variable</td><td>0.00%</td><td>0.00%</td><td>0.00%</td><td>6.27%</td><td>1.401</td></tr><tr><td>Wia</td><td>0.00%</td><td>0.00%</td><td>100.00%</td><td>0.00%</td><td>0.00</td></tr></table>


---

24

Erlon Pereira Almeida et al.

Subsequently, we applied the same analytical process to the False Negatives (FNs), which represent modifications the model failed to identify. The analysis revealed that the volume of FN errors was substantially higher than that of FPs, a finding consistent with the model's overall low Recall (Table 4 ). The five most frequently omitted node types, as detailed in Table 6 , were Type _ Access (1713 instances), Path _ Foldset (7022), Literal (538), Variable Read (6256), and Invocation (4972).

Following the same analysis from the FP Table 5 , two primary patterns emerged. First, a set of nodes exhibited a consistent error pattern, with omissions being relatively distributed across all four attempts. Nodes such as TypeAccess , FieldRead , and Block fail into this category. For TypeAccess , for example, out of 100 nodes only 29 out of 100 have less than 88.8 % of the total errors. This indicates a persistent challenge for the model in identifying those types of modifications, regardless of the prompt design.

The second pattern revealed highly concentrated, strategy-specific failing modes. The most striking example is the If node, where a single strategy, Attempt 2, was responsible for an overwhelming 98.1 % of all omissions. A similar pattern was observed for Parameter , where Attempt 2 also accounted for 77.4 % of the errors. This demonstrates that certain prompts create critical blind spots for the model, making it a specialist in omitting specific node types.

Finding 2: The prompt engineering strategy is a dominant factor in dictating the model's error profile. Different strategies were found to induce higher distinct and specialized failures modes, often leading to opposing responses from specialists and producing server negatives and effectively creating error specialists for specific node types.

RQ1.2: Which Java node types are difficult for GPT-4.1 to identify accurately, given the prompt strategies applied in this study?

While the previous analysis demonstrated that each prompt strategy induces a distinct error profile, a direct comparison of error volumes can be influenced by the frequency with which each node type appears in the dataset. To definitively answer RQ1.1 — “ To what extent does our prompt engineering strategy dictate the model's error profile? ” and to determine the model's inherent difficulty with each node, a normalized analysis is required.

To this end, we calculated a Normalized Failure Index (NFI) for each node across all four attempts. This index, as defined in the methodology section, represents the ratio of total errors (FFs + FNs) generated by an attempt for each node type to the total frequency of that node in the ground truth

Table 7 presents the results of this analysis, enabling a fair comparison of the model's proportional struggle across different node types. The analysis of this table reveals two primary categories of difficulty: (1) nodes that pose a challenge, exhibiting high error rates across all strategies; and (2) nodes that suffer from catastrophic failures, with extremely high error rates under specific prompt strategies.

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

25

Table 7 Normalized Failure Index (NFI) per Node Type and Prompting Strategy (Corrected).




Finding 3: The most problematic nodes are those with high proportional error rates across all prompt strategies, such as TypeReference, FieldRead, and VariableRead. This indicates a fundamental difficulty in processing these node types, which is distinct from high-volume errors (like Invocation) that are primarily a function of their frequency in the dataset.

RQ2: How effectively does GPT-4.1 generate mutant code aligned with what we know about students? Under the prompt strategies tested, compared to existing techniques?

Figures 5 and 6 present a comparative analysis between two fundamentally different approaches: a single, general-purpose LLM (GPT-4.1), guided only by a prompt across all five bug-chusters, and the five specialized LLMs mentioned in Section 2.1 . The LLMs perform competitively on the 2000 single, corresponding cluster. Figure 5 shows semantic similarity scores, where GPT-4.1 demonstrates a remarkably stable and consistent performance. This stability indicates that the model is less susceptible to the particular nature of the modifications within each cluster, suggesting a strong generalization effect. On the other hand, for the 1500 samples in the validation set of SST-2018, measuring the token-level overlap between the generated and reference code,

Our workflow generated mutants for all 8,322 TPs at a rate of 0.41% mutation calls per trivalent computational cost of approximately $0.001$ . This is compared to mutating 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

The analysis of semantic similarity scores, presented in Figure 5 , reveals that GPT-4.1 consistently generates code with higher and more stable semantic alignments to the buggy reference code. In contrast, the RNNs-based model obtained significantly lower variability and a higher propensity for low-scoring outliers across most classes.

This pattern of superior stability from GPT-4.1 is evident across the different code patterns represented by the clusters. In Clusters 1 and 2, for ex-

---

26

Erlon Pereira Almeida et al.

![Figure](figures/ESE_journal_Erlon_page_026_figure_002.png)

Fig. 5 Workflow done in the process of testing GPT-4.1 on identifying modifications in each TP.

ample, while both models achieved high median scores, the RNNs' performance showed a much wider dispersion. Even in Cluster 3, where the median scores were comparable, GPT-4.1 demonstrated greater robustness by juxtaining higher error maps. However, all methods produced better results when the RNN models achieved slightly higher peak scores, yet this came at the cost of greater instability, producing several outputs with substantial semantic deviation (below 0.82). GPT-4.1, by contrast, maintained its characteristic high consistency. A notable exception is Cluster 5, representing simpler bugfix structures, where both models performed exceptionally well, suggesting both bugfixes and semantics were shared. This common phenomenon also directly indicate that while both models are capable of generating semantically similar code, GPT-4.1 does so with a much lower outliers range.

The analysis of lexical similarity, measured via the BLEU score, is presented in Figure 6 . The results reveal a clear trade-off between the two models. The RNN-based models generally achieve higher median BLEU scores across the four languages, with the VFT-LLM-Ctrl being the stronger literal replacement of token sequences from the original buggy code.

However, this higher lexical alignment from the RNN came at the cost of significantly lower consistency, a pattern particularly evident in the first three clusters. In Clusters 1, 2, and 3, the RNN's performance was marked by a wider score dispersion and a substantial number of severe low-score outliers. In contrast, in Clusters 4 and 5, the RNN's results were much more stable and compared similar to GPT-LTs. Across the board, GPT-4.0 demonstrated several promising results in stability, with a more compact distribution of scores and a near-total absence of the catastrophic low-score outliers that affected the RNN.

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

27

![Figure](figures/ESE_journal_Erlon_page_027_figure_002.png)

Fig. 6 Workflow done in the process of testing GPT-4.1 on identifying modifications in each TP.

Finding 4: GPT-4.1 and the specialized RNN models baseline exhibit can a clear trade-off in mutant generation. GPT-4.1 produces mutants with higher Semantic Similarity and, crucially, demonstrates a performance that is less susceptible to the specific nature of the modifications within each cluster. The RNN model achieves better Lexical similarity (BLEU score) but with higher output variability and more frequent semantically divergent mutants. GPT-4.1 emerges as the more robust and generalizable approach for generating meaningful, fault-aligned mutants.

## 5 Discussion

In this section, we interpret the findings presented in the previous sections and discuss their broader implications. Our results revealed two central themes: (1) the profound impact of prompt engineering on the model's error behavior in the mode identification task, leading to the creation of distinct "error profiles"; (2) the dramatic performance trade-off between GPT-4.1 and the RNN baseline in the mutant generation task, highlighting a dichotomy between semantic and lexical similarity.

### 5.1 Prompt Strategy as an Error Profile Director

The finding that prompt engineering strategies induce distinct and predictable error profiles offers a significant contribution beyond simply ranking prominent performance. It reiterates the challenge of prompt optimization, transforming engineering into a design opportunity for both academic research and industrial applications.

---

28

Erlon Pereira Almeida et al.

For Academic Research, this discovery challenges the conventional methodology of evaluating prompts based on single, aggregated performance metrics, like F1-score. We demonstrate that a deeper analysis of error profiles is crucial for a complete understanding of a prompt's behavior. Our results suggest that future research should focus not on finding a single “ perfect prompt ”— our own findings suggest this may be unattainable—but rather on exploring prompt performance. The single, perfect prompt approach, as we have demonstrated, has the outputs of multiple, complementary prompts — each strong where others are weak — could lead to a far more robust and comprehensive result than any individual prompt could achieve. This opens a new avenue for research in creating more reliable LLM-based code analysis tools.

For Industrial Applications, this insight provides a direct path toward building more reliable and predictable AI systems. Instead of relying on a single prompt, a production system could implement a “ committee of experts ” architectural. Multiple LLM instances, each guided by a specialized prompt (e.g., one tailored for control flow, another for data access), could analyze code in parallel. A voting or merging mechanism could then consolidate the outputs, effectively mitigating the individual “ blind spots ” of each prompt and increasing the system's overall accuracy and robustness. Furthermore, understanding a prompt's specific error profile allows for intelligent risk management. In a context where errors in control flow (if they are) are more critical than errors in code execution (control nodes) development can be resolved in a different way that minimizes these costly type of errors. Even if it is not the best-performing prompt overall. Additionally, the detailed error analysis provides a crucial roadmap for future model specialization through fine-tuning. By identifying the specific node types where the general-purpose model struggles, a targeted dataset of these challenging examples can be created to fine-tune smaller, more efficient models, producing highly specialized and cost-effective tools optimized to avoid the specific failure modes identified in this study.

### 5.2 The Trade-off Between Lexical and Semantic Similarity

The comparative analysis of lexical and semantic similarity between single, general-purpose LLM (GPT-4.1) against five specialized RNN models, provides significant contributions to both academic research and industrial practice.

For Academic Research, our findings highlight the limitations of relying solely on surface-level metrics like the BLEU score for evaluating model LLMs in mutant generation tasks. The specialized RNN models, while achieving higher median BLEU scores, proved to be both more sensitive to the specific modification patterns of each cluster and more prone to instability, as evidenced by their frequent generation of severe low-score outliers. This demonstrates that academic benchmarks must increasingly incorporate semantic evaluation metrics to capture a model's true capability for generat-

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

29

ing functionally correct and meaningful code, rather than its ability for mere pattern replication. Furthermore, this study provides a clear characterization of the different operational philosophies of these models: the RNN acts as a high-fidelity pattern reproducer, which excels at literal imitation but is brittle when past context is used. In contrast, GPT-LL operates as a semantic generator, which paraphrases and creates new content, leading to lower lexical error but centrally coherent semantic and robustness.

This distinction is critically contextualized by recent research that directly investigates the link between lexical and semantic similarity in mention testing. The study by Odamic et al. (2023b) empirically demonstrated that synonymy, which is a type of lexical similarity, was critical to selecting participants with high BLEU scores often failed to replicate the semantic behavior of real faults. Crucially, their work evaluated four fault-seeding tools against the Defects4L v2.0 benchmark, and the tool with the worst performance was DeepMutation — which is based on the same RNN translation model architecture (Tufano et al., 2019) in our baseline. Despite being optimized for syntactic comprehension, it still does not consistently rank top-1 or top-5 % of the real data, a result significantly lower than the other three evaluated techniques (Table 1 , scored between 61.39 % and 76.41 % ).

For industrial applications, this distinction offers a practical framework for model selection. Regarding tasks requiring high reliability, predictability, and maintainability — where the process or code must be easily understood and trained to be deployed in a GPT-4's trained system — it is crucial to address. Its high semantic similarity and its robustness against producing less outliers make it a more suitable model for production environments. Our results quantify this risk associated with models such as the RNN, which, despite achieving performance peaks, can introduce unpredictable and nonsensical outputs into production environments. By addressing these issues, we hope that our work hence its limitations are minimal, not to the detriment of GPT-4's performance, but to the benefit of our own design.

Finally, our comparative analysis provides a framework for evaluating generative models based on the critical trade-off between lexical and semantic similarity. This guide is both future research and enables a more strategic selection of techniques for producing practitioners to choose the model that best fits their specific project needs.

## 6 Threats to Validity

We identify a few threats to the validity of our study, which are categorized next. For each threat, we also discuss the mitigation strategies employed.

Internal Validity: The findings of our study are closely tied to the specific instructions and prompting strategies employed with the LLM. During the initial exploratory phase, we systematically experimented with combinations of prompting techniques, contextualization strategies, and RAG (Soudani et al., 2024) to assess the LLM's ability to identify code modification patterns. We also investigated how many prompt variations were needed to capture each

---

30

Erlon Pereira Almeida et al.

TP adequately. Furthermore, we explored multiple ways to translate these identified patterns into mutant operators to generate meaningful mutant code. We selected and reported the four most promising approaches highlighting the rationale behind each attempt.

Furthermore, we acknowledge that the stochastic nature of LLMs can introduce random effects. To mitigate this, we deliberately configured the model's temperature parameter to 0, effectively disabling stochastic nucleus sampling (top-p) and ensuring the most deterministic outputs possible. Regarding experiment results, the figures 12 and 13 show that LLMs with different models experimute multiple runs to establish statistical robustness, replicating for the full generation process for 8,322 TPs multiple times was infeasible due to the substantial computational costs and strict API rate limits associated with the commercial GPT-4.1 model. However, we argue that the sheer scale of our dataset (over 8,000 samples) provides sufficient statistical power to stabilize aggregate metrics (such as F1-score and Semantic Similarity) and identify semantic patterns that would be unlikely to emerge from random fluctuations along the lines of Gaussian posteriors.

External Validity: The generalizability of our findings is primarily limited by the scope of our dataset and methodology. First, this study focuses solely on Java projects. Although the proposed methodology is adaptable to other programming languages, the performance of the LLM and the specific error patterns observed may not directly translate to languages with different syntactic and semantic structures. Second, our analysis is based on a cut-off set of 18 mutant operators. While these operators were selected to be replicable into the Java language, other methods, e.g., tabuaries or heuristic constitute an exhaustive set of all possible mutation patterns found in prior work (Tufo et al., 2019) .

Third, the generalizability of our results is bounded by the use of a single LLM (GPT-4.1). While the proposed two-stage workflow is a model-agnostic methodology, the quantitative performance, the relative effectiveness of the prompt templates, and the specific "error profiles" we identified are intrinsically linked to the capabilities and architectural biases of this particular model. These behaviors might differ significantly in other LLMs (e.g., open-source models), and in different settings (e.g., out-of-the-box). To establish a foundational baseline with a suited-the-at model rather than a universal benchmark.

Furthermore, a significant threat to external validity arises from the unconventional nature of our dataset. While the dataset is large, which supports the generalizability of our findings, the Transformation Pairs were intentionally abstracted and generalized. This design forces the LLM to perform a purely structural analysis, identifying modification patterns without the rich semantic context of a full project (e.g., variable meanings, method purposes, or overall architecture). We hypothesize that this represents a more challenging “ worstcase” scenario for the LLM. Consequently, the performance metrics reported in this study should be interpreted as a conservative lower bound; it is plausible that in a real-world industrial application, when the LLM would leverage

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

31

access to the full semantic context of the code, its performance in identifying and generating modifications would be substantially higher.

Construction validity: A threat to construct validity concerns the mis- interpretation of the model's low recall, particularly in the context of False Negatives. Our methodology correctly and objectively measures the model's output against the exhaustive, fine-grained syntactic modifications identified in the evaluation. The objective of the interpretation of these results must account for the inherent operational philosophy of LLMs like GPT-11, which often prioritize semantic compression.

Rather than generating a complete list of all syntactically affected nodes, the model may provide a single, high-level description of a change, implicitly considering lower-level nodes as inferrable. This behavior inevitably leads to a higher number of measured FNs when compared to our systematic, exhaustive baseline. Consequently, the low Recall reported in our study should not be interpreted solely as a lack of capability, but rather as evidence of a fundamental mismatch between the LLM's semantically-driven, summary-oriented approach and the exhaustive, syntactically-driven nature of our ground truth. Acknowledging this difference is crucial for a fair interpretation of the model's performance.

A significant threat to construct validity is the lack of operational validation for the generated mutants. Due to the abstract nature of the dataset Transformation Pairs (which use generic phoscholiers like TYPE_1 or even METHOD_1 ), the mutants generated by both GPT-4.1 and the RNN baseline model were validated, but the methods did not produce comparable results. Perform dynamic analysis to calculate a traditional mutation score (i.e., determine if the mutants are killed by a test suite) or compare LLM's results with other tool such as Pit (Coles et al., 2016b) or LEAM (Tam et al., 2023) . Our evaluation of effectiveness is therefore necessarily limited to the lexical and semantic alignment of the generated code with the reference fault, not its concrete operational behavior when executed. A critical direction for future work is therefore to bridge this gap by adapting the developed workflow to operate on a benchmark of real Java code, such as defects4J. This would enable us directly to assess the model's performance against other state-of-the-art tools on a standard benchmark and validate its practical effectiveness in an end-to-end scenario.

## 7 Conclusion

This paper presents a foundational investigation into the operational characteristics of GPT-4.1 on the key tasks of identifying and generating inutants. The goal was not to propose a production-ready tool, but to establish a comprehensive benchmark against a specialized, RNN-based approach. By exploiting a collection of in-text, in-code, and in-air samples with a variety of temporal characteristics, its limitations, and the fundamental trade-offs involved, Our findings therefore reveal a complex and nuanced performance landscape.

---

32

Erlon Pereira Almeida et al.

moving beyond simple metrics of success or failure to provide a clearer understanding of how to effectively leverage these models in practice.

The primary conclusion of this work is that the efficacy of LLMs in code analysis is not monolithic but is characterized by a series of significant tradeoffs. First, in the node identification task, we found that prompt engineering acts as a bias director, inducing specialized and often contradictory error profiles rather than providing uniform improvement. This suggests that the search for a single, universally optimal prompt is likely futile. Our analysis of the Normalized Failure Index (NFI) further pinpointed the model's deepest struggles, distinguishing between nodes that pose a chronic, strategy-agnostic challenge (e.g., TypeReference ) and those that suffer from catastrophic failures under specific prompts (e.g., I1 ).

Second, in the mutant generation task, we identified a clear trade-off between GPT-4.1 and an RNN baseline. GPT-4.1 excels in generating mutants with superior semantic similarity, consistently producing meaningful and predictable code. The RNN, conversely, is better at achieving high lexical similarity through literal reproduction but at the cost of significant instability and a propensity for generating low-quality, nonsensical outliers.

The findings of this study open several critical directions for future research. The most pressing question arising from our work is whether the error profile phenomenon — where prompt strategies induce distinct and specialized failure modes — is a behavior unique to GPT-4.1 or a general characteristic of large language models. Therefore, our primary future work will be to replicate this methodology with other state-of-the-art LLMs (such as models from Anthropic, Llama, Deepseek, Gemini families) to investigate if prompt engineering consistently acts as a bias director across different model architectures.

Subsequently, building on our error specialist finding, we plan to develop and evaluate a prompt ensemble system. By combining the outputs of multiple, complementary prompts, we hypothesize that we can create a more robust and comprehensive result than any single prompt could achieve. Furthermore, we intend to bridge our generative framework with traditional mutation testing tools. This will allow us to evaluate the efficacy of existing test suites against our approach by assessing the efficiency of our methodological pipeline. To do so, simpler, synthetic mutants generated by conventional tools. Finally, to validate our approach in a full-scale industrial setting, we will apply our methodology to an end-to-end real-world project, allowing us to assess performance with full semantic context.

Author Contributions: Élen Persona Almeida. Conceptualization, Methodology, Code, Data Visualization, Validation, Formal analysis, Investigation, Data Curation, Writing, original draft, Visualisation

Daniel Lucrediro: Conceptualization, Methodology, Formal analysis, Resources, Writing review & editing, Supervision, Project administration.

Rohit Gheyi: Conceptualization, Methodology, Formal analysis, Writing - review & editing, Supervision.

Pierre-Yves Schobbens: Methodology, Formal analysis, Validation, Writing - review & editing.

Gilles Perrouin: Methodology, Formal analysis, Validation, Writing - review & editing

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

33

Paulo Anônio da Mota Silva Neto: Methodology, Formal analysis, Validation, Investigation, Writing - review & editing.

Eduardo Santana de Almeida, Conceptualization, Methodology, Formal analysis, Resources, Writing, review & editing, Supervision, Funding acquisition.

Data Availability The datasets generated during and/or analysed during the current study are available from GitHub repository: https://github.com/natgas-gg45-bio/ NatGas-LLR-Based-Research

Funding The authors did not receive support from any organization for the submitted work.

## Declarations

Ethical approval Not applicable.

Informed consent Not applicable.

Conflict of Interest The authors have no relevant financial or non-financial interests to disclose. The authors declare that they have no conflict of interest.

Clinical Trial Number Clinical trial number: not applicable.

## References

Andoni A, Indyk P, Razensteyn I (2018) Approximate nearest neighbor searching in high dimensions. https://arxiv.org/abs/1806.09823 , 1806.09823

Beller M, Wong CP, Bader J, Scott A, Machalica M, Chandra S, Mejer E (2021) What it would take to use mutation testing in industry: a study at facebook. In: Proceedings of the 43rd International Conference on Software Engineering: Software Engineering in Practice. IEEE Press, ICSE-SEI ¯21, p 268–277. DOI:10.1109/ICSE-SEI.PE52600.2021.00036. URL https://doi. org/10.1109/ICSE-SEI.PE52600.2021.00036

Brown DB, Vaughn M, Libitt B, Reps T (2017) The care and feeding of wildcaught mutants. In: Proceedings of the 2017 11th Joint Meeting on Foundations of Software Engineering Workshop on Machine Learning, MachineNeu AI, USA. ESEC/FSE 2017, p. 511–522. DOI: 10.3891/2017. 3106280. URL https://doi.org/10.1145/3106237.3106280

Brown TB, Mann B, Ryder N, Subbiah M, Kaplan J, Harihawat P, Neckantan A, Shyam P, Sastry G, Askell A, Agarwal S, Herbert-Voss A, Kruegat G, Henighan T, Child R, Ramesh A, Ziegler DM, Wu J, Winter C, Hesse C, Chen M, Sigler E, Litwin M, Gray S, Chess B, Clark J, Berner MC, CCandlish S, Radford A, Sutskever I, Amodei D (2020) Language models are few-shot learners. URL https://arxiv.org/abs/2005.14165 , 2020, 15:4185.

---

34

Erlon Pereira Almeida et al.

Coles H, Laurent T, Henard C, Papadakis M, Ventres V (2016) Pfit: a pandora toolkit for probabilistic inference. In: Fourth International Conternational symposium on software testing and analysis, pp 449–452

Coles H, Laurent T, Henard C, Papadakis M, V rentueuse A (2016b) Pit: a practical mutation testing tool for java (demo). In: Proceedings of the 25th International Symposium on Software Testing and Analysis, Association for Computing Machinery, New York, NY, USA, 2018, pp. 2, 449–452. DOI 11.1145/2931037.2948707, URL https://doi.org/10.1145/ 2931037.2948707

Dakhel AM, Nikanjam A, Majdinasab V, Khomfi F, Desmaris MC (2024) Effective test generation using pre-trained large language models and mutation testing. Information &30(16):107468. DOI https://doi. org/10.1016/j.ijiso.2024.107468. URL https://www.sciencedirect.com/ science/article/pii/S0950589424000739

Deogiovani R, Papadakis M (2022) pbert: Mutation testing using pre-trained language models. In: 2022 IEEE International Conference on Software Testing, Verification and Validation Workshops (ICSTW), pp 160–169. DOI: 10.1109/ICSTW55396.2022.00039

Deng Y, Xia CS, Peng H, Yang C, Zhang L (2023) Large language models are zero-shot fuzzers: Fuzzing deep-learning libraries via large language models. In: Proceedings of the 32nd ACM SIGSOFT International Symposium on Software Testing and Analysis, Association for Computing Machinery, New York, NY, USA, ISSTA 2023, p 423–435. DOI 10.1145/3597926.3598067. URL https://doi.org/10.1145/3597926.3598067

Deng Y, Xia CS, Yang C, Zhang SD, Yang S, Zhang L (2024a) Large language models are edge-case generators: Crafting unusual programs for fuzzing deep learning libraries. In: Proceedings of the IEEE/ACM 46th International Conference on Software Engineering, Association for Computing Machinery, New York, NY, USA, ICSE ’24. DOI: 10.1145/3597503.3623343, URL: https://doi.org/10.1145/3595703.3623343

Deng Y, Xia CS, Yang C, Zhang SD, Yang S, Zhang L (2024b) Large language models are edge-case generators: Crafting unusual programs for fuzzing deep learning libraries. In: Proceedings of the 46th IEEE/ACM international conference on software engineering, pp 1–13

Du B, Han B, Liu H, Chang Z, Liu Y, Chen X (2024) Neural-mid: Improving mutation-based fault localization by neural mutation. In: 2024 IEEE, 48th Annual Computers, Software, and Applications Conference (COMPSAC), pp 1274–1283. DOI 10.1109/COMPASCB1065.2024.100168

Falleri JR, Morandat F, Blanc X, Martínez M, Monperrous M (2014) Finegrained and accurate source code differencing. In: Proceedings of the 29th ACM/IEEE International Conference on Automated Software Engineering, Association for Computing Machinery, New York, NY, USA, ASE ’14, p. 313–324. DOI:10.1145/2642937.2642982. URL https://doi.org/10.1145/ 2642937.2642982

Foster C, Gulati A, Harman M, Harper I, Mao K, Ritchie J, Robert H, Sengupta S (2025) Mutation-guided llm-based test generation at meta. URL

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

1

https://arxiv.org/abs/2501.12862 , 2501.12862

Gay G, Salahatad A (2023) How closely are common mutation operators coupled to real faults? In: 2023 IEEE Conference on Software Testing, Verification and Validation (ICST), pp 129–140. DOI 10.1109/ICST57152.2023. 00021

Ghevi, R., Ribeiro M., Souza B., Guimarães M., Fernandes L., d'Amorim M., Alves V., Teixeira L., Fonseca B. (2021) Identifying method-level mutations in an unclassified mutation. Mutation and Evolution of Life, https: 32:106496, DOI: https://doi.org/10.1016/j.mevol.2016.06.096, URL: https: //www.sciencedirect.com/science/article/pii/S095058492030228X

Gong P, Zhao R, Li Z (2015) Faster mutation-based fault localization with a novel mutation execution strategy. In: 2015 IEEE Eighth International Conference on Software Testing, Verification and Validation Workshops (ICSTW), pp 1–10. DOI 10.1109/ICSTW.2015.7107448

Gopinath R, Alipour A, Ahmed I, Jensen C, Groce A (2015) How hard does mutation analysis have to be, anyway? In: 2015 IEEE 26th International Symposium on Software Reliability Engineering (ISSRE), pp 216–227. DOI: 10.1109/ISSRE.2015.7381815

Gopinath E, Alipour MA, Ahmed I, Jesse C, Groce A (2016) On the limits of prediction accuracy for special categories of attacks. In: 2016 IEEE International Conference on Software Engineering (ICSE), pp 511–522

Gopinath R, Ahmed I, Alipour MA, Jensen C, Groce A (2017a) Does choice of mutation tool matter? Software Quality Journal 25:871–920

Gopinath R, Ahmed I, Alipour MA, Jensen C, Groce A (2017b) Mutation locations of human missense variants in MEDLINE Transactions on Reliability 6(3):854–874. DOI 10.1109/TRL.2017.2705566

Grün JB, Schaler D, Zeiler A (2009) The impact of equivalent mutants. In: Gr u¨ n JB, Schaler D, Zeiler A (eds.) Molecular Signature Testing: Verification, and Validation Workshop. IEEE, pp 192–199

Gumárias MA, Fernandes L, Ribeiro M, d'Amorim M, Gheyri R (2020) Optimizing mutation testing by discovering dynamic mutant subsumption relations. In: 2020 IEEE 13th International Conference on Software Testing, Validation, and Verification (ICST), pp 198–208. DOI 10.1109/ICST46399. 2020.00029

Hamadi A, Khaufir A, Papailakis M (2023) Intent-based mutation testing: From naturally written programming intents to mutants. In: 2023 IEEE International Conference on Software Testing, Verification and Visual化 workshops (ICSTW), pp 347–357. DOI 10.1109/ICSTW64638.2023. 10962508

Hou X, Zhao Y, Liu Y, Yang Z, Wang K, Li L, Luo X, Lo D, Grundy J, Wang H (2024) Large language models for software engineering: A systematic literature review. ACM Trans Softw Eng Methodol 33(8), DOI 10.1145/3695988. URL https://doi.org/10.1145/3695988

Irvine SA, Pavlinic T, Trigg L, Cleary JG, Ingle S, Uttin M (2007) Junning: Academic and Industrial Conference Practice and Research Tech-

---

36

Erlon Pereira Almeida et al.

niques - MUTATION (TALC/PART-MUTATION 2007), pp 169-175, DOI: 10.1109/TAG.PART.2007.38

Jafari O, Maura P, Nagarkar P, Islam KM, Crushev C (2021) A survey on mobile learning and e-learning applications. Internet of Things //arxiv.org/abs/2102.08942. 2102.08942

Jia Y., Harman M (2011a) An analysis and survey of the development of mulephant models. In: Proceedings on Software Engineering 37(5):649-678. DOI:10.1109/TSSE.2010.62

Jia Y., Harman M. (2011b) An analysis and survey of the development of mobile networks. IEEE Transactions on Software Engineering 37(5):1649-60. doi: 10.1109/TSE.2010.62

June R (2014) The major mutation framework: Efficient and scalable mutation testing. In: Proceedings of the 2014 international symposium on software testing and analysis, pp 433–436

Just R, Schwiggert F, Kaphmarer GM (2011) Major: An efficient and extensible tool for mutation analysis in a java compiler. In: 2011 26th IEEE/ACM International Conference on Automated Software Engineering (ASE 2011), pp 612–615. DOI 10.1109/ASE.2011.610038

Just R, Kaphhammer GM, Schweiggerf F (2012) Do redundant mutants affect the effectiveness and efficiency of mutation analysis? In: 2012 IEEE Fifth International Conference on Software Testing, Verification and Validation, pp 720–725. DOI 10.1109/ICST.2012.162

Just R, Jalali D, Ingozsema L, Ernst MD, Holmes R, Fraser G (2014) Are mutants a valid substitute for real faults in software testing? In: Proceedings of the 22nd ACM SIGSOFT International Symposium on Foundations of Software Engineering. Association for Computing Machinery, New York, NY, USA, FSE 2014, p. 654–665. http:10.1145/2635688.2635929, URL https://doi.org/10.1145/2635688.2635929

Kintia M, Papadakis M, Papadopoulos A, Valvis E, Malevina N (2016) Analysing and comparing the effectiveness of mutation testing tools: A manual study. In: 2016 IEEE 16th International Working Conference on Search Engineering and Manipulation (SEAM), pp. 147–156. DOI: 10.1109/SEAM.2016.28

Kintis M, Papadakis M, Jia Y, Malewnis N, Le Traon Y, Harman M (2018) Detecting trivial mutant equivalences via compiler optimisations. IEEE Transactions on Software Engineering 44(4):308–333. DOI 10.1109/TSE.2017. 2684805

Kurtz B, Ammann P, Ofulte J, Kurtz M (2016) Are we then yet? how redundant and equivalent mutants affect determination of test completeness. In: 2016 IEEE Ninth International Conference on Software Test Development and Validation Workshops (ICSTW), pp 142–151. DOI: 10.1109/ICSTW.2016.41

Laurent T, Ventresque A (2019) Pit-horn: an extension of pitest for higher order mutation analysis. In: 2019 IEEE International Conference on Software Testing, Verification and Validation Workshops (ICSTW), pp 83–89. DOI: 10.1109/ICSTW.2019.00036

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

37

Laurent T, Galfney S, Ventresque A (2022) Re-visiting the coupling between mutants and real faults with defects4] 2.0. In: 2022 IEEE International Conference on Software Testing, Verification and Validation Workshops (ICSTW), pp 189–198. DOI 10.1109/ICSTW53395.2022.00042

Li Z, Shin D (2024) Mutation-based consistency testing for evaluating the code understanding capability of llms. In: Proceedings of the IEEE/ACM 3rd International Conference on AI Engineering - Software Engineering for AI, Association for Computing Machinery, New York, NY, USA. CAIN ’24, p. 150–159. DOI:10.1145/3644815.3644946. URL https://doi.org/10.1145/ 3644815.3644946

Lin D, Koppel J, Chen A, Solar-Lezama A (2017) Quixbugs: a multi-lingual program repair benchmark set based on the quixkey challenge. In: Proceedings Companion of the 2017 ACM SIGPLAN International Conference on Systems, Programming, Languages, and Applications: Software for Intermediate Networks, Virtual and On-line, New York, NY, USA. SPLASH Companion 2017, p. 55–56. DOI: 10.1145/3155932.3155941. https: https://doi.org/10.1145/3155932.3155941

Ma YS, Olfurt J, Kwon YR (2006) MuJava: a mutation system for java. In: Proceedings of the 28th international conference on Software engineering, pp 827–834

Madeysi L, Radyk N (2010) Judy-a mutation testing tool for java. IET software 4(1):32-42

Madełycki L, Orszynska W, Torkar R, Józala M (2014) Overcoming the equivalent mutant problem: A systematic literature review and a comparative experiment of second order mutation. IEEE Transactions on Software Engineering 40(1):23–42. DOI:10.1109/TSE.2013.44

Malkov YA, Yashmin DA (2018) Efficient and robust approximate neural networks for large-scale image recognition. arXiv:abs/1603.09320 , www.world-aiq. https://arxiv.org/abs/1603.09320 , 1603.09320

Martinez M, Falleri JR, Mongrenna M (2023) Hyperparameter optimization for machine learning. In: Lecture Notes in Machine Learning, Software Engineering, 49(10):481482. doi: 10.1016/j.TCF.2023.3315935

Mathur A (1991) Performance, effectiveness, and reliability issues in software testing. In: [1991] Proceedings The Fifteenth Annual International Computer Software & Applications Conference, pp 604–605. DOI:10.1109/ CMPSAC.1991.170248

Nguyen QV, Madesyi L (2014) Problems of mutation testing and higher order mutation testing. In: Advanced Computational Methods for Knowledge Engineering: Proceedings of the 2nd International Conference on Computer Science, Applied Mathematics and Applications (ICCSAMA 2014), Springer, pp 157–172

Offutt AJ, Pan J (1996) Detecting equivalent mutants and the feasible particle. In: Proceedings of the 2nd Annual Conference on Computer Computance, COMP'S'96, IEEE, pp 224-230

Ofutt Alt, Pan J (1997) Automatically detecting equivalent mutants and infeasible paths. Software testing, verification and reliability 7(3):165-192

---

38

Erlon Pereira Almeida et al.

Ojamie M, Garg A, Khanir A, Degiovanni R, Papadakis M, Le Traon Y (2023a) Syntactic versus semantic similarity of artificial and real faults in mutation testing studies. IEEE Transactions on Software Engineering 49(7):3922–3938. DOI:10.1109/TSE.2023.3277564

Ojmanic M, Garg A, Khaufar A, Degiovani R, Papadakis M, Le Tron Y (2023b) Syntactic versus semantic similarity of artificial and real faults in mutation testing studies. IEEE Transactions on Software Engineering 49(7):3922–3938. DOI:10.1109/TSE.2023.3277564

Papadakis M, Delamante M, Le Tureau Y (2014) Mitigating the effects of equivocal word order on sentence classification. In: Conference in Artificial Intelligence Programming 95:298–310

Papadakis M, Jia Y, Harman M, Le Tron Y (2015) Trivial complex equivalence: A large scale empirical study of a simple, fast and effective equivalent nautic detection technique. In: 2015 IEEE/ACM 37th IEEE International Conference on Software Engineering, vol 1, pp 836–848. DOI: 10.1109/ICSE.2015.103

Papadakis M, Shin D, Yoo S, Ban DH (2018) Are mutation scores correlated with real fault detection? a large scale empirical study on the relationship between mutants and real faults. In: Proceedings of the 40th International Conference on Software Engineering, Association for Computing Machinery, New York, NY, USA. ICSE ’18, p. 537–548. DOI 10.1145/3180155.3180183. URL https://doi.org/10.1145/3180155.3180183

Papadakis M, Kiutis M, Zhang J, Jia Y, Tron Y, Harman M (2019a) Data gathering advances: An analysis and survey. Nature 549:118 advances in computers

Papadakis M, Kintis M, Zhang J, Jia Y, Trous YL, Harman M (2019) Chilter six - mutation testing advances: An analysis and survey. Advances in Computing and Education, Elsevier, pp 275–378. DOI https://doi.org/10.1016/j. arce.2018.03.001 . www. arce.com/ . www.sciencedirect.com/science/ article/pii/S0065248518300305

Papineni K, Roukos S, Ward T, Zhu WJ (2002) Bleu: a method for automatic evaluation of machine translation. In: Proceedings of the 40th Annual Meeting on Association for Computational Linguistics. Association for Computational Linguistics, pp 623–631. https://doi.org/10.18653/v1/2002.VLG URL https://doi.org/10.3115/1073085.1073135

Schüder D, Zeiler A (2010) (un-) covering equivalent mutants. In: 2010 Third International Conference on Software Testing, Verification and Validation. IEEE, pp 45-54

Sondä H, Kanouhais E, Hashi F (2024) Fine tuning vs. retrieval augmented generation for less popular knowledge. In: Proceedings of the 2024 Annual International ACM SIGIR Conference on Research and Development in Information Retrieval in the Asia Pacific Region, Association for Computing Machinery, New York, NY, USA. SIGIR-AP 2024, p 12–22. DOI: 10.1145/ 3673791.3698415. URL https://doi.org/10.1145/3673791.3698415

Tian Z, Chen J, Zhu Q, Yang J, Zhang L (2023) Learning to construct better mutation faults. In: Proceedings of the 37th IEEE/ACM International

---

Grouding GPT-4.1 Mutant Generation in Bug-Fixes Patterns

39

Conference on Automated Software Engineering. Association for Computing Science, 2005. http://dx.doi.org/10.1145/3519439.3556494 URL https://doi.org/10.1145/3519439.3556494

Tian Z, Shi H, Wang D, Cao X, Kamei Y, Chen J (2024) Large language models for equivalent mutant detection: How far are we? In: Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis, Association for Computing Machinery, New York, NY, USA, ISSTA 2024, p 1733–1745. DOI 10.1145/3650212.3680395. URL https:// doi.org/10.1145/3650212.3680395

Tip F, Bell J, Schaefer M (2023) Lmnoophus: Mutation testing using large language models. https://arxiv.org/abs/2404.09952 , 2405 , 09952

Tufano M, Watson C, Bavota G, Di Penta M, White M, Pooysaenyaik D (2019) Learning how to mutate source code from bug-fixes. In: 2019 IEEE International Conference on Software Maintenance and Evolution (ICSME), pp 301–312. DOI 10.1109/ICSME.2019.00046

Tufano M, Kimko J, Wang S, Watson C, Bavota G, Di Penta M, Pomyhavan D (2020) Depeuneration: a neural mutation tool. Association for Computing Machinery, New York, NY, USA, ICSE 20, p 29–32. DOI:10.1145/3377812. 3382146. URL https://doi.org/10.1145/3377812.3382146

Wang B, Xiong Y, Shi Y, Zhang L, Hao D (2017) Faster mutation analysis via equivalence modulo states. In: Proceedings of the 26th ACM SIGSOFT International Symposium on Software Testing and Analysis, Association for Computing Machinery, New York, NY, USA, 2017, p. 295–306. DOI 1145/3092703.3092714, URL https://doi.org/10.1145/ 3092703.3092714

Wang B, Chen M, Lin Y, Papadakis M, Zhang JM (2024a) An exploratory study on acidification and base excess in soil testing. URL https: //arxiv.org/abs/2406.09843 , 2405: 09843

Wang J, Huang Y, Chen C, Liu Z, Wang S, Wang Q (2024b) Software testing with large language models: Survey, landscape, and vision. IEEE Trans Softw 50(4):911–936. DOI 10.1109/TSE.2024.3368208, URL https: //doi.org/10.1109/TSE.2024.3368208

Wei J, Joanna M, Zhao YY, Guo K, Yu AW, Lester B, Du N, Dai AM, Levine D. 2017. Open large language models are few-shot learners. URL https: //arxiv.org/abs/1709.01652 , 2109.01652

Wei, J., Wang X, Schuurman, D, Bosma, I., Ichter, B, Xia, F, Chi, E, Le, Q.: Zhong W, Li, Liu, H., Li, B., Li, J., Li, Z., Li, Y., Li, S., Li, T., Li, W.-T.: Fossil modes. URL https://arxiv.org/abs/2201.11903 , 2201, 11903

Weimer W, Fry ZP, Forrest S (2013) Leveraging program equivalence for adaptive program repair: Models and first results. In: 2013 28th IEEE/ACM International Conference on Automated Software Engineering (ASE), pp 356–366. DOI 10.1109/ASE.2013.6693094

White J, Fu Q, Hays S, Sandborn M, Olea C, Gilbert H, Elnashar A, Spencer-Smith J, Schmidt DC (2023) A prompt pattern catalog to enhance prompt engineering with chatgpt. URL https://arxiv.org/abs/ 2302.11382 , 2302.11382

---

40

Erlon Pereira Almeida et al.

Wong CP, Meincke J, Chen L, Dinija JAp, Kastner C, Figueiredo E (2020) Efficiently finding higher-order mutants. In: Proceedings of the 28th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering, Association for Computing Machinery, New York, NY, USA, ESEC/FSE 2020, p 1165–1177. DOI: 10.1145/ 3368089.3490713. https://doi.org/10.1145/3365089.3490713

Wong WE (1993) On mutation and data flow. Purdue University

Wright CJ, Kapfhammer GM, McMinn P (2014) The impact of equivalent language technologies on student learning: an overview. In: Proceedings of the 14th International Conference on Quality Software

Xia YA, Yang C, Wang B, Xiong Y (2023) Expressapp: Efficient patch validation for java automated program repair systems. In: 2023 38th IEEE/ACM International Conference on Automated Software Engineering (ASE), pp. 2038–2041. DOI 10.1109/ASE56229.2023.00012

Yao X, Harman M, Jia Y (2014) A study of equivalent and stubborn mutation operators using human analysis of equivalence. In: Proceedings of the 36th International Conference on Software Engineering. Association for Computer Science, http://www.cs.cuhk.hk/~min-qi/ISL.speech.lvcsr.html? 2568225,2568265, URL https://doi.org/10.1145/2568225, 2568265

Yi J, Tan SH, Mechaert S, Böhme M, Roychoudhury A (2018) [journal first] correlation study between automated program repair and test-suite metrics. In: 2018 IEEE/ACM 40th International Conference on Software Engineering (ICSE), pp 24–24. DOI: 10.1145/3180155.3182517

Zhang, J., Zhang, L., Harman, M., Hao, D., Jia, Y., Zhang, L. (2019). Predictive multivariate data analysis problems on Software Engineering . IEEE Software R&D, DOI: 10.1109/TSE.2018.2809496.

