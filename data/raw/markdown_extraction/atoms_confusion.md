![Figure](figures/atoms_confusion_page_001_figure_000.png)

![Figure](figures/atoms_confusion_page_001_figure_001.png)

![Figure](figures/atoms_confusion_page_001_figure_002.png)

![Figure](figures/atoms_confusion_page_001_figure_003.png)

![Figure](figures/atoms_confusion_page_001_figure_004.png)

Latest updates: https://dl.acm.org/doi/10.1145/3422392.3422437

![Figure](figures/atoms_confusion_page_001_figure_006.png)

PDF Download

23423922182437.pdf

01 March 2023

by IEEE Xplore

Total Download: 225.15

Published: 21 December 2014

RESEARCH-Article

Citation in BibTeX format

# Atoms of Confusion: The Eyes Do Not Lie

BENEDITO DE OLIVEIRA, Federal University of Alagoas, Maceio, AL, Brazil MÁRCIO RIBEIRO, Federal University of Alagoas, Maceio, AL, Brazil JOSÉ ALDO SILVA DA COSTA, Federal University of Campina Grande, Campina Grande, PB, Brazil ROHIT GHEYI, Federal University of Campina Grande, Campina Grande, PB, Brazil QUILHERME AMARAL, Federal University of Alagoas, Maceio, AL, Brazil RAFAEL DE MELLO, Federal Center for Technological Education Celso Suckow da Fonseca, Rio de Janeiro, RJ, Brazil

View all

Open Access Support provided by:

Federal University of Alagoas University of Brasília Pontifical Catholic University of Rio de Janeiro Federal University of Campina Grande Federal Center for Technological Education Celso Suckow da Fonseca

---

# Atoms of Confusion: The Eyes Do Not Lie

Benedito de Oliveira

Federal University of Alagoas

Maceio, Alagoas, Brazil

bfao@ic.ufr.br

Márcio Ribeiro

Federal University of Alagoas

Maceio, Alagoas, Brazil

marcio@cif.ufa.br

José Aldo Silva da Costa

Federal University of Campina Grande

Campina Grande, Paraíba, Brazil josealdo@copin.ufcg.edu.br

Rohit Gheyi Federal University of Campina Granda Campina Grande, Brazil rohit@disc.ufcg.edu.br

Guilherme Amaral

Federal University of Alagoas

Maceio, Alagoas, Brazil

gyma@ci.utaf.br

Rafael de Mello

Federal Center for Technological Education of Rio de Janeiro, Rio de Janeiro, Maracatuba, Brazil rafael.mello@cefet-rj.br

Anderson Oliveira

PUC-Rio

Rio de Janeiro, Rio de Janeiro, Brazil aoliveira@inf.puc-riro.br

Alessandro Garcia

PUC-Rio

De Janeiro, Rio de Janeiro, Brazil afgarcia@imf-puc-br.io

Rodrigo Bonifacio

University of Brasília

Brasília, Brazil ronbifacio@ubh.br

Baldoino Fonseca

Federal University of Alagoas

Maceio, Alagoas, Brazil

baldoino@i.ufral.br

## ABSTRACT

Code comprehension is crucial in software maintenance activities, though it can be hindered by misunderstandings and confusion patterns, namely, atoms of confusion. They are small pieces of code using specific programming language constructs, such as Condi- tional Operators and Comma Operators. A previous study showed that code comparison was an independent variable to assess coding time and accuracy, and increase code misunderstandings. However, empirical knowledge of the impact of such atoms on code compre- hension is still scarce, especially when it comes to analyzing that impact on developers' visual attention. The present study evalu- ates whether developers misunderstand the code in the presence of atoms of confusion with an eye tracker. For this purpose, we examined the effect of code on the screen and analyzed them, and analyze the distribution of visual attention. We conducted a controlled experiment with 30 students and software practitioners. We ask the subjects to specify the output of three tasks with atoms and three without atoms randomly assigned using a L400 Square design. We use an eye-tracking camera to detect the visual atten- tion of each atom and note the times of each atom's attention. In this perspective, we observed an increase of 43.02% in the time taken to gaze transcode in code snippets with atoms. For accuracy, no statistically significant difference was observed. We also confirm that the regions that receive most of the eye attention were the

regions with atoms. Our findings reinforce that actors hinder development of technical comprehension. So, developers should avoid writing code with ill-structured sentences.

## CCS CONCEPTS

• Software and its engineering → Maintaining software, Software verification and validation, Abstraction, modelling and modularity.

## KEYWORDS

Atoms of Confusion, Code Comprehension, Eye Tracking

### ACM Reference Format:

Benedito de Oliveira, Márcio Ribeiro, José Alvar Silva da Costa, Rohit Ghey, Ritshree Dinda, and Marcelo Cardemil. 19th IEEE International Conference on Rodrigo Benevides and Baldoino Fonos. 2024. Asymposium of Conference of The Eyes Do Not Lie. 4th Brazilian Symposium on Software Engineering (SES 2024) , 256–257, 258–262. IEEE, New York, NY, USA, 10 pages. http://doi.org/10.1145/3422923.3422427

## 1  INTRODUCTION

Code comprehension is a critical activity in software development, especially in the maintenance and evolution processes. Developers often have to deal with maintaining or improving code that they have not been written. Thus, when code changes, new opers have to understand it. Indeed, a previous study showed that most of their time is spent on code comprehension activities [13] . However, the comprehension process can be hindered by aspects of the code that cause misunderstandings. For instance, previous research has shown that 5-12% of the code written in a business term that contribute to the increase of the time and effort necessary

This article has been accepted for publication in a future issue of this journal, but has not been fully edited. Content may change prior to final publication. Citation information: DOI 10.1109/ACCESS.2020.3021068, IEEE Access

Please cite this article as: Zhang, H., Huang, X., Li, B., et al., A survey on resource allocation in public cloud for large-scale networks, IEEE Public云, https://doi.org/10.1016/j.ptal.2020.10.004

SBES '20, October 21-23, 2020, Natal, Bra

c 2020 Association for Computing Machinery 108(1):342-353. https://doi.org/10.1145/3422542.3433637

---

SBES '20, October 21-23, 2020, Natal, Brazil

Oliveira, et al.

to understand the code correctly. Examples of these small code patterns in imperative languages like C and C++, namely atoms of confusion, include Conditional Operators, Commu Operators, Logic Operators, and Place Pairs, among others, and are often found in source code bases [10].

In a previous study [4] , researchers conducted a controlled experiment to compare the performance, i.e., time and accuracy of participants when dealing with code with and without atoms of confusion. They have shown that the presence of atoms of confusion in the code increases misunderstandings and that, however, empirical knowledge on the impact of such atoms on code comprehension is still scarce, given the difficulties in measuring code comprehension [18] . On the other hand, the code comprehension task has been gaining new highlighting from researchers in terms of time and accuracy with eye-tracking devices [16] . For instance, known which parts of the code receive more or less attention given a given task, we have seen that different parts of each atom's visual effort, which is a dimension not considered before [4] or in any other study that we are aware. Although time and accuracy are good estimators of code confusion, knowing precisely the regions that participants paid attention, allows us to estimate their real effects.

Given this scenario, we use an eye tracker to evaluate whether developers misunderstand the code in the presence of atoms of confusion. For this purpose, we measure time, accuracy, and distinctly from other studies, we also analyze the visual effort given to satisfy the above criteria. The triangulation of these dimensions allows us to understand better the real effects of atoms of confusion in code comprehension.

In this controlled experiment, we selected six code snippets from real open-source C/C++ systems of different domains containing atoms of three different types ( Assignment as Value, Conditional Operator , and Logic as Control Flow ), being two snippets for each domain. These snippets are chosen because they were the most commonly found in industrial practice [10] . We then manually refactored the code to remove the atoms from the snippets and build our tasks. We also changed the function to remove several internal code dependencies so that the function can get more straightforward, but we keep its primary structure. We executed the experiment with 39 developers. The developers were asked to read, understand, and analyze the code, and we chose not to answer any question about three with no atoms. We used the Latin Square design to assign the tasks randomly and minimize learning effects. We then measure the completion time of tasks, as well as the number of incorrect answers. Besides, through the eye tracker, we captured the developers' eyes coordinates while looking at the screen. These eye coordinates allowed us to build heatmaps, measure the number of times participants could be seen on each screen, and observe the number of gaze transitions, which are the transitions of the eyes from one location of the code to another.

When analyzing all tasks together, we found that the presence of atoms of confusion statistically significantly increased the time required to understand the code by 43.02 % . We could not find a statistically significant difference for accuracy. When analyzing the _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

show that the regions that receive most of the attention are precisely the ones where the atoms are placed. The regions with atoms have an increase of 56.8 % gap transitions. These results confirm and add a new perspective to the previous study [4] .

In conclusion, our findings reinforce that atoms of confusion cause confusion by hindering developers' performance and code comprehension. They make the maintenance activity more timeconsuming and require more visual effort. We also show that the eye-tracking methodology seems promising, revealing a new perspective not seen in previous works.

In summary, this paper provides the following contribution: An empirical controlled experiment with the use of an eye tracker demonstrates that the presence of atoms of confusion leads to more time to understand code and more visual effort.

## 2   EXAMPLE

Atoms of confusion frequently appear in open source repositories. A previous study on their prevalence on 50 projects found more than 109 thousand occurrences of 11 out of 12 atoms types considered, including the ones we focus on this paper: Conditional Operator with 98 % of prevalence, Assignment as Value with 94 % of prevalence, and Logic as Control Flow with 50 % of prevalence [10] .

Figure 1 illustrates two code snippets from function printIf written in C programming language. The left-hand side snippet contains a function with an example of the atom of confusion called Conditional Operator . 1 Notice the two nested ternary operators. At the right-hand side, a developer refactored the function to remove the Conditional Operator atom by replacing it with a regular if-else statement. 2 For examples of Assignment as Value and Logic as Control flow see Figure 4 .

According to Gopstein et al. [5] , there is empirical evidence that atoms of confusion impact developers' performance, causing misunderstanding, and that their removal makes code easier to replace. However, just as that is true for new languages, the issue of such atoms on code comprehension, we need to assess other dimensions besides time and accuracy to draw more insights. In this scenario, eye-tracking devices come at home to allow us to locate where and for how long subjects are looking at the screen [17] . These devices have been used before in the code comprehension task. However, evaluation of such devices, like those that are designed for accuracy to provide additional information related to visual effort [7, 12] .

Thus, to gather more information on how atoms impact code comprehension, we use an eye-tracking camera to analyze how those atoms influence the focus of attention. By triangulating the time, accuracy, and focus of the developers, we can better understand the impact of the atoms. For instance, it helps us to confirm whether the regions of the code that receive most of the attention are the places where the atoms are positioned, how the focus of attention changes interacting with code elements, and whether removing those patterns alleviates developers' effort from a visual perspective not considered in previous works.

3 https://github.com/narnasr/printf/comm/s/b4f15e6ef454f1a2c820e88582844151dcb8e6c

2https://github.com/narnat/printf/commit/385233be85dd409c17be255b529e5b9ef14e29

---

Atoms of Confusion: The Eyes Do Not Lie

SBES '20, October 21-23, 2020, Natal, Brazil

![Figure](figures/atoms_confusion_page_004_figure_002.png)

Figure 1: A transformation removing an atom of confusion (Conditional Operator).

## 3   STUDY: CONTROLLED EXPERIMENT

We now present our controlled experiment. We present the settings, experimental units, execution, and data analysis procedures.

### 3.1 Study Settings

In this experiment, we analyze programs written in C with atoms of confusion and with no atoms of confusion using an eye-tracking camera to investigate the effects of the presence of the atoms concerning time, accuracy, and focus of attention in solving "specify correct output" tasks from the point of view of developers in the context of code comprehension.

We focus on the following research questions:

- : RQ1: To what extent do atoms of confusion affect task com-
pletion time? To answer this question, we measure the total
time developers need to solve each task. Thus, our first null
hypothesis (H0) is: there is no significant difference be-
tween the time required to understand code with no atoms
of confusion (the control treatment) and code with atoms of
confusion (the test-retest treatment). To answer this question,
: RQ2: To what extent do atoms of confusion affect task accu-
racy? To answer this question, we measure the number of
errors committed by developers while solving a task. Thus,
our second null hypothesis (H2a) is: there is no significant
difference in the number of errors committed by developers
when understanding code with no atoms of confusion (the
control treatment) and code with atoms of confusion (the
test-retest treatment). To answer this question, we measure
: RQ3: To what extent do atoms of confusion affect the focus of
attention? We measure the number of gaze points captured
using an eye-tracking system and generate heatmaps. The
heatmaps of the aggregated tasks solved by the developers
help us visualize possible differences in attention. Our third
null hypothesis (H3a) is: there is no significant difference
in the number of gaze points when analyzing code with no
atoms of confusion (the control treatment) and code with
no atoms of confusion (the test-retest treatment). Also,
we measure the number of gaze points inside the area of
the atom of confusion and compare it with the number of points
in the region modified to remove the atom.
We use a Latin Square design of order two with replicas [2] in our experiment, mainly because our goal is to compare two treatments and block two variables: (a) participant skill and engagement; and (b) two sets of comprehension tasks. Each Latin Square replica comprises two participants and two sets of comprehension tasks (representing the columns of each square, i.e., S1 and S2). Each set of comprehension tasks contains one condition and one condition, one, containing an Assignment as Value , and one containing a Condition . Operator . Figure 2 presents the design of our experiment.

![Figure](figures/atoms_confusion_page_004_figure_011.png)

Figure 2: Design of the experiment using Latin squares.

We also randomly set the treatments that each participant should use in $ST_1$ and $ST_2$ . Each treatment appears once in each row and column. This way, we block the two sources of variability: the participants and the two sets of tasks [9, 15] . The design also leads to one replica for each Latin Square (increasing the number of errors' degrees of freedom) [14] .

### 3.2 Experimental Units

In total, 30 subjects participated in the experiment. 9 undergraduates, 17 masters, and 4 Ph.D. at Pontifical Catholic University of Rio de Janeiro (PUC-Rio). Out of the 30 subjects, 25 were men, while 3 were women. Although we have used code structures common to most programming languages, prior knowledge in C, C++, or JavaScript were required to participate in the experiment. We recruited 33 students. However, we had to discard 3 of them. We discarded the 33rd subject because we could not run the experiment with the last Latin Square, lacking one subject. Then, we discarded

245

---

SBES '20, October 21-23, 2020, Natal, Brazil

Oliveira, et al.

another subject because he answered the cell phone while participating in soccer. He said, "I'm sorry, but I was also to discuss the other participant on his Latin Spanish test. I'm sorry."

For the experiment execution, we have prepared a laptop with a system developed to control the experiment's execution flow. The system is a web application written in Python using the Web Framework. All captured data was stored in a PostgreSQL database to posterior analysis. The system showed the functions to the participants automatically when they finish a task based on the previous Latin Squares randomization. Figure 3 illustrates our setup. To find the two possible responses, the system will ask the participants to choose one of three possible responses: (1) answer the set of tasks (ST) comprising code with atoms of confusion, and (2) solve the second set of tasks (ST2) comprising code with no atoms of confusion. Both sets contain three tasks: that is, ST1 contains the tasks T1, T2, and T3, while ST2 contains the tasks T4, T5, and T6. In the second configuration, we invert our treatments, according to the Latin Square design (Figure 3 ).

![Figure](figures/atoms_confusion_page_005_figure_004.png)

Figure 3: Structure of the experiment in terms of experimental units. We have two Sets of Tasks (ST1 and ST2) that comprehend Tasks 1 to 6 (T1, T2, ..., T4). Half of the tasks are with atoms (WA) and half with no atoms (NA).

To create the experiment's tasks, we mined the code of open source projects to find functions containing atoms of confusion. The selected functions were adapted and simplified to make them self-contained, fit them to our research scope, and reduce the time to analyze. We found that our coding approach was the most different types of atoms (see Figure 4 ): Assignment as Value, Conditional Operator, and Logic as Control Flow . Each task has one or more pr if statements; each participant's assignment is to specify the correct output to be printed on the standard output when the code snippet is executed. We have selected six functions in total, and for each selected snippet, we created a refactored version by using the atom of confusion and use it as a control treatment group. The tests have less than 30 LOC, so that small down could be avoided.

The applied transformations used for the tasks consisted of maintaining the same code except that the atom was replaced with a more clarified code fragment. There is not only one way to perform the transformation but also two ways to apply proposed transformations in [10] and proposed and evaluated in [4] .

### 3.3 Execution and Data Analysis Procedures

We first randomly assigned the treatments (With Atom × with No Atom) to the 15 Latin square replicas. When a new participant

starts the experiment execution, the system automatically assigns him to the next available row in the Latin Square's lat. Before starting the tasks, for each participant, the eye-tracking device is re-calibrated. This procedure is required because the calibration device (the joystick) will not be able to track the movements of other external characteristics such as the use of glasses positioning, and distance of the chair relative to the computer, participant's height, among others. We have plugged the device at the bottom of the laptop's screen to capture the points where the participant is looking. Then, we stored the captured eye gaze points in a database. Before executing the two sets of tasks, each participant completed a series of tasks. By performing tasks in sequence, the user obtains atoms of confusion to understand how the flow of the experiment works and gets acquainted with the eye tracker equipment setup.

![Figure](figures/atoms_confusion_page_005_figure_011.png)

Figure 4: Code snippets with the three types of atoms evaluated in this study. At the left-hand side, we have the atom of confusion (treatment group) and at the right-hand side we have the same code with no atoms (control group).

Once the Warm-Up is successfully done, the system allows the participant to execute the main tasks. When a participant believes to have the correct answer, he or she should click otherwise on the screen that will present the result and show you the screen that allows him or her to submit the answer.

If the participant's answer is wrong, the system increments the error count for this execution and allows the user to get back to the menu. Even if the user continues to enter an invalid command, correct answer, or is far to get, the next task the user asks is to task' execution, the participants are allowed to pause anytime by clicking anywhere on the screen. The system collects the user's end time for the execution of each task and the complete experiment. We monitor the amount of time the user takes to finish each task and thus during each provided answer. We considered that the execution completed only when all tasks are correctly solved. To

246

---

Atoms of Confusion: The Eyes Do Not Lie

SBES 20, October 21-23, 2020, Natal, Brazil

avoid any inter-subject contamination, we instructed participants to share answers or explain anything about the experiment to them.

We proceeded with an exploratory data assessment and tested the normality of the data. Following the approach of Harrell (2017) , we follow a normal distribution, we used the Kruskal-Wallis test.

We analyzed the eye gaze perspective using heatmaps, and we measured the number of gaze transitions, along with other metrics associated with how gaze points are located inside or move between regions of the code. Heatmaps are static graphical representations in colors, and the intensity of the color represents the concentration of gaze points over a particular field. We aggregated the heatmaps of gaze points per eye by 15 discrete steps. The duration of gaze transitions adds a more dynamic perspective of analysis, expressing how many transitions of the focus of attention occurred in the code. The eye tracker camera captures about 80 sample points per second, and tasks took from a few seconds to a few minutes to be answered. To ease the analysis, we computed the median of the coordinates x and y of these 80 points in one second. This coordinate is the focus of attention per second . The transition of the eyes from one focus to another is the gaze transition. We analyzed the average number of times a participant spent looking at the end of all participants in the same task. To simplify the analyses, we considered only transitions that occur at least 1/3 at times. At least 1/3 of the participants must have performed the same transition allowing us to observe a pattern.

## 4 RESULTS AND DISCUSSION

In this section, we present the results of our research questions along with a discussion. $^3$

### 4.1 RQ1: To what extent do atoms of confusion affect task completion time?

The boxplots of Figure 5 show some descriptive statistics related to the total time spent by the participants to conclude the different tasks.

The Aggregate boxplot represents an aggregation of the tasks, either with atoms or with no atoms. When aggregated, the total time median when analyzing code with atoms of confusion (294.5 seconds) is shown. This is the case for the test task from task 1, but with no atoms of confusion (178 seconds). The observations related to the total time to conclude all tasks, when analyzing code with no atoms of confusion, lie between 74 and 776 seconds; in contrast, the observations when analyzing code with atoms of confusion lie between 91 and 736 seconds. There is only a small overlapping of the results, where it appears that the average time for correctly understanding code with atoms of confusion is more time consuming than understanding code with no atoms of confusion.

We tested our first null hypothesis and found evidences for rejecting it (p-value = 0.001972 < 0.05 = α). This leads to the first conclusion of this study that atoms of confusion increases the time required to solve the tasks.

![Figure](figures/atoms_confusion_page_006_figure_011.png)

Figure 5: Time to conclude on tasks. Aggregate + aggregative (s) = Sequential Execution; Cyclic (c) = No-Data; CO = Conditional Operator; LAC = Logic as Control Flow.

Under an individual perspective, considering the hypothesis test for each type of atom of confusion separately, we found diverging results. Two atoms of confusion allowed us to reject the null-hypothesis $H_0$ ; particularly, the atoms Assignment as Value (p-value = 0.008) and Logics as Control Flow and (p-value = 0.0001). In both cases, they favored the code with no atoms.

Even though the size of the code can interfere with time, making it longer to look at more elements is not necessarily true. For instance, in Figure 4 , the number of elements added to remove the atom is considerably higher, especially in the Conditional Operator when compared to the regular case. This phenomenon suggests a higher productivity in terms of time in code with no atom rather than in code with atom. The slight increase in the time for the Conditional Operator with no atom can be explained by the relatively large amount of code added to remove such atom (see Figure 4 b). All the three evaluated atoms were present in the data set of Gopstein et al. [4] and are evaluated by them. The only bug that should be removed from our analysis is the typo of the OpenMP which in their work showed statistical differences, but we could not observe such effect. The discrepancy might be due to other factors involved, such as methodology. For instance, we have used code from real projects, we assigned fewer tasks to participants, and the participants were not exposed to the same code with atom and with no atom. Besides, in our case, it is also possible that both codes were generated from the same source code but are written in different ways that in the version with no atom, for Conditional Operator , we have many more lines of code, which can affect time.

Previous studies have investigated the prevalence of errors on real projects. Among the investigated atoms, Conditional Operator , Last vs Central Flow , and Assignment as Value were on the top seven of the most error-laden items. This is consistent with [10] and [5] . On Medeiros et al. [10] , Conditional Operator and Assignment as Value were found on the top three most commonly used. Given that Conditional Operator is commonly used on both evaluations, and we found conflicting results with Gopalan et al. [4] regarding its real effects, we need more studies on this topic. According to these findings, in addition to the present set of projects, we need three evaluated atoms in this study. However, at least a patch of each atom was also rejected.

$^{1}$ All results are available at the GitHub repository website: https://github.com/easysoftware-utah/Analysis-of-Confusion-Experiment-Data

247

---

SBES '20, October 21-23, 2020, Natal, Brazil

Oliveira, et al.

Finding 1. The presence of atoms of confusion increases 43.02% in time required to understand code correctly

### 4.2 RQ2: To what extent do atoms of confusion affect task accuracy?

We followed a similar approach to investigate the second hypothesis, which relates to answers correctness or accuracy when analyzing code with atoms of confusion. We first carry out an exploratory data analysis. Figure 6 shows boxplots that present some descriptive statistics related to the number of submitted answers to conclude all tasks under an aggregated and individual perspective. Under an aggregated perspective, the median number of answers when the items are answered correctly is 3. This indicates that the median number of answers in code with no atoms. This result means getting the task solved on the first try. They only differ in terms of discrepant values. The same applies to the atoms individually. Consequently, we cannot infer a sound conclusion about our second hypothesis $H_{2B}$ .

![Figure](figures/atoms_confusion_page_007_figure_005.png)

Figure 6: Number of trials to conclude all tasks. Aggregate scores for each task indicate the average rank of the trial; CO Conditioned Operator; LACF - Logic as Control Flow.

One main reason why conclusive results could not be obtained by analyzing accuracy alone may rely on the fact that we have used simple tasks, with small pieces of code with a few operations. Thus, the number of submitted answers did not vary so much. In Gopstein et al. [4] , for instance, even though the tasks were also small, the number of tasks answered by participants was higher.

Finding 2. We have not found evidence that the presence of atoms of confusion impacts the accuracy.

### 4.3 RQ: To what extent do atoms of confusion affect the focus of attention?

In the heatmaps, blue (col) areas are areas of the code that did not receive much attention, while red (hot) areas represent the areas that received most of the attention. By the developers' distribution of visual attention, and how the focus of attention changes over distinct code elements, we can infer whether a particular code element is confusing. The analysis of heatmaps can assess the distribution of attention.The colors in the heatmap represent the relative concentration of gaze points over an area, and the higher the amount

of points on it, the more intense the color gets. If the atom of confusion areas require more attention from the participants, they are likely to appear on more intense colors on the heatmaps, which is a phenomenon we are interested in investigating. Most importantly, we aim to find out how well our participants can focus on and attention. Heatmaps are exceptionally helpful and useful, giving the following reasons. First, they allow us to observe where the participants focused the most and with what intensity, and by doing so, we can see where most time and visual effort in task completion can be found. Second, we can observe how well our participants do not catch the attention of participants, which is also a relevant information. Third, they allow us to perform a sanity check so that we can verify whether gaze samples were properly captured. To get more insights on this matter, we separated the areas of interest to perform more specific analysis. We have defined these Areas Of Interest (AOI) as the lines of code where the atom of confusion is explicit. From this perspective, when the version with no sham InFigure 4 , we present the areas of interest in the code, which are the areas in which both code differs.

Table 1: Summarizing Metrics. Bold font denotes a significant statistical difference with a significance level of 5 % . Signal $\uparrow$ corresponds to an increase with atom while $\downarrow$ corresponds to a reduction.

<table><tr><td>Atoms</td><td>Time</td><td>Errors</td><td>Points in AO</td><td>Errors in AO</td><td>Gaze Trans.</td></tr><tr><td>AV</td><td>46.05%</td><td>16.7%</td><td>13.4%</td><td>17.9%</td><td>15.7%</td></tr><tr><td>EC</td><td>62.80%</td><td>15.60%</td><td>11.60%</td><td>16.10%</td><td>15.00%</td></tr><tr><td>LACF</td><td>91.7%</td><td>8.10%</td><td>28.2%</td><td>47.8%</td><td>22.7%</td></tr><tr><td>Aggregated</td><td>43.0%</td><td>16.2%</td><td>20.6%</td><td>49.3%</td><td>30.8%</td></tr></table>


In Figures 7 , 8 , and 9 , we see a comparison of three heatmaps, one of each evaluated atom, showing how the attention is disturbed over different parts of the program relative to time spent by the user. It can be seen that the majority of individual heatmaps of the participants who performed the same task,

In Figure 7 , we have a more clear distinction in the heatmaps for Logic as Control Flow alone. We observe that the attention is mainly focused on one main region where the atom is located while the rest of the image is missing. This is because the atom is located in two main regions, causing a higher distribution of attention over distinct parts. With atom, the total time was increased by 91.7 % , and, in it, participants focused on the area of the atom with 26.2 % more points. Participants also needed to enter the atom area 36.5 % to avoid this effect. The fact that the participants still can observe us and indication that code with atom is more confusing.

In Figure 8 , we could not observe so much difference in the heatmaps for the Assignment as a Value atom. The developers tend to focus their attention on the atom region. When the atom is located, the distance to the nearest atom is measured and it is extracted. However, we observe that the attention is more restricted and focused on a relatively smaller area at the right-hand side of the heatmap compared to a more sparse at the left-hand side. It is important to emphasize that the color intensity is relative to the amount of time to solve the code. However, according to Table 1 , in addition to the above observations, the results of the SIFT Gopfinen et al. [4] have shown that this atom causes confusion, and by intense color on the atom area, we conclude that the participants

248

---

Atoms of Confusion: The Eyes Do Not Lie

SBES '20, October 21-23, 2020, Natal, Brazil

![Figure](figures/atoms_confusion_page_008_figure_002.png)

Figure 7: Logic as Control Flow - With atom vs. No atom.

are focusing on it because they are confused. However, in our results, the number of points in this area is decreased by 34.5%, which means that other parts of the same code were also confuting. The remaining regions are all within the same cluster, with 9.1% more entries in the atom area and 15.7% more transitions in the core.

![Figure](figures/atoms_confusion_page_008_figure_005.png)

Figure 8: Assignment as Value - With atom vs. No atom.

In Figure 9 , at the top, we observe that the attention is distributed more horizontally while at the bottom, vertically. The visual difference is not so clear, however, in terms of the concentration of points and the area of the figure. As can be seen in Figure 9 , the at [4] showed that the atom causes confusion, but, in our results, time and accuracy did not support those results. However, the eye gaze metrics indeed support those results. There is a higher concentration of points on the atom region, 85 % more points, according to our results. On the contrary, the other metrics, like precision and f1, were significantly lower than our results.

in the atom area, which supports confusion associated with that transition. However, by inspecting more than 20% of parts of the code since we have 93.7% more transitions with atom

![Figure](figures/atoms_confusion_page_008_figure_009.png)

Figure 9: Conditional Operator - With atom (top) vs. No atom. (bottom)

The code with the Conditional Operator atom required, on average, less time to be solved but more visual effort due to some reasons. To discuss those reasons, we show an example of how two distinct participants solved the tasks. The first one solved the code with an atom, and the second one solved the code with no atom. For the participant who solved the task with an atom, we took the code of the atom and its correspondent graph of gait transition, which can be seen in Figure 10 . at the top and in the bottom. Similarly, for the participant who solved the code for this particular case, we examine the x-sine, representing how their eyes moved back and forth horizontally over the distinct elements in the function of time. The red color represents eyes looking inside the area of interest in the function of time. As we can see by the red colored line, this participant had to go back and forth several times at the time with the atom, going until the end and until the

249

---

SBES '20, October 21-23, 2020, Natal, Brazil

Oliveira, et al.

middle. The participant reached almost the end of the line 3 times, represented by the highest peak, 3 times about half of the line, and several smaller movements resembled by smaller peaks. The line was nearly completely filled with red dots. This is a hallmark of the atom, which indicates confusion. On the other hand, the second participant analyzed a code with no atom (illustrated in Figure 10, at the top, right-hand side). Here, the difference is that the code with no atom has more lines of code. We can see a small amount of variation in the number of times the participant spent in the area of interest (see the few red lines with respect to time).

We also analyze the y-axis representing the visual effort vertically in the code (see the bottom of Figure 10 ). With no atom, the participant makes more gazes on the x-axis, going up and down more often, with about 7 long peaks, and 5 of them touching the area of interest in about 30 seconds. However, the effort going amortization of the y-axis indicates that on average, each participant stays in the area of interest for about 45 seconds. The natural dispersion of the variations for x-axis and y-axis together shows a symptom of confusion introduced by the atom.

Finding 3. The presence of atoms of confusion increases the amount of ambiguity in the prompt. This is usually the case of entries in ACL and 20.6% the number of points is above 100.

## 5 THREATS TO VALIDITY

We now discuss potential threats to the validity of our controlled algorithm. We start with the threats using the classification of Woithlin et al. [21] .

Conclusion Validity: Since our data do not follow a normal distribution, our hypotheses tests are based on a nonparametric test named Kruskal-Wallis. This test can determine if there are statistically significant differences between two or more groups of an independent variable on a continuous or ordinal dependent variable. However, we believe that the test will only detect statistically significant eyes can gaze over areas out of the screen or out of the code, and the eye tracker can still capture those points. We observed, by analyzing the generated heatmaps, that some participants tend to look into emptiness sometimes when they are thinking. However, this situation is likely to occur in both treatments, i.e., with atoms and with no atoms. Regarding the points captured, techniques are commonly employed to reduce their number, which the literature refers to as removing artifacts. However, the majority of the time and points can also be used to generate the heatmaps once they show the density of concentration of such points over distinct areas.

Internal Validity. There were some other threats to validity in this study that we realized during the experiment execution, such as the rotating chair used by the participants. This rotating chair affected the eye tracking device so we contacted with the participant's eyes. Additionally, we determined that each participant only tested the eye tracker device for each participant right before executing the experiment. The different potential luminosity between the two room environments we used to execute the experiment can also be considered a threat since they can change the sensibility of the eyes of the participant. Since the experiment was not designed to minimize this threat, we closed all curtains to avoid the external luminosity. Also, the size of the font and style might influence the

participant's attention. To mitigate this threat, we have chosen a popular font style and a size that fits the screen. All tasks are displayed in the same font size, highlighted with a light theme, to mitigate possible effects. The time duration of the whole experiment can also influence visual effort if it is too long. We mitigated it by using simpler and only a few tasks to not let participants tired.

![Figure](figures/atoms_confusion_page_009_figure_010.png)

Figure 10: Conditional Operator transitions on $x$ -axis (two graphs at the top) and $x$ -axis (two graphs at the bottom).

Construct validity. Our controlled study can involve threats regarding mono-operation bias or possible effects of interaction between treatments. To deal with and control these threats, we employed in our experiment the Latin Square design.

External Viability: In our experiment, we have used programs which were originally written for use in laboratory laboratory capa- tion capacity to other languages. However, we used simple code

---

Atoms of Confusion: The Eyes Do Not Lie

SBES '20, October 21-23, 2020, Natal, Brazil

snippets with constructs incorporated in several programming languages, such as variable declarations and assignments and if-else statements. Additionally, we cannot generalize the results of our experiment to other code comprehension scenarios—although we explored different types of atoms of confusion: Assignment as Value , and Confirmation of Value . By repeating this experiment we generalizes our results to the professional developers' population since some of our experiment participants were graduate students. However, some students argue in favor of using students to conduct controlled experiments [19, 22] . Our strategy in this paper was to conduct an empirical experiment that initially consisted of a seek on open source repositories to find functions to the experiment. Then we created a complete environment to make it possible to execute the experiment with the least possible interaction, and by making it possible to test for cases that might better cause relationships of code comprehension of code engineers’ atten- tions of confusion. This work aims to validate preexisting works favoring internal validity.

## 6 IMPLICATION

Our results reveal and reinforce what a previous study has claimed regarding the impact of atoms on time [4] . From an additional perspective, which includes eye-tracking, the presence of atoms can confuse, affecting developers' productivity, making them spend more time and misjudge code behavior, and bringing effects to their attention, which makes them focus on the atom regions.

The catalogs of atoms of confusion created by previous works are not yet widespread among software developers. Thus, developers need to be aware of any possible atoms of confusion, which appear as bottlenecks in code comprehension. This way, we invite and suggest the community to give a greater diffusion of these atoms and the negative effects of their presence on the code.

These results also motivate the development of plugins and tools in IDEs and code editors that can make it easier for programmers to detect and refactor atoms of confusion. A good practice is also to make project managers and senior developers more concerned of their roles and more sensitive during code review and accepting contributions (e.g., merging pull requests in Diffku) from other developers.

The methodology we adopted by using an eye tracker to assess visual attention is a promising alternative to analyzing code comprehension in the presence of atoms of confusion. It reveals how a particular atom can change the amount or direction of the attention, and how this activity might be affected by a more realistic idea of the impact of atoms. Previous works do not explore the eye perspective in the context of atoms of confusion.

Last but not least, in this work, we have found empirical evidence that atoms of confusion increase time to comprehend the code and that some types of atoms are more prejudicial than others. Thus, we encourage researchers, the academic community, and practitioners to conduct more controlled experiments, especially considering the types of atoms of confusion not explored in this paper.

## 7 RELATED WORK

Code comprehension is often explored in computer science, particularly in the software engineering field, since a significant portion

of the maintenance effort is dedicated to understanding existing software. A considerable amount of effort to properly understand code can be a problem not only for the business environment but also for the development of software. In this work, we rely on in assessments, mainly in the first years of graduation [16] .

Some prior works [4, 5, 10] have studied some particular smallcode patterns which have a big potential to cause misunderstandings. These code patterns were named as forms of confusion [4, 5, 10] or misunderstanding patterns [10] . Such patterns can even lead to the generation of many errors. It is possible that the use of code as a case of bug introduction related to the atom of confusion Dangfong Ehe in a function used on a code library called OpenH264.

Gopstein et al. [4] have performed an experiment with 73 participants and showed empirically that these atoms of confusion could lead to a significantly increased rate of misunderstanding when compared with code without atoms of confusion. As they were expected, the results were consistent: 70 out of 100, 92.5 % about the behavior of a piece of code. These different conclusions can naturally lead to bugs. Still, according to Gopstein et al. [4] , atoms of confusion can also cause diminished productivity, faulty products, and higher costs. They have also cataloged 15 atoms of confusion and provided a methodology for empirically deriving these complex atoms. In their study [4] , they have conducted two experiments. One of them is similar to ours. However, we use an experiment with just 120 minutes of coding. In addition to the developers' attention, We observed an increase of 36.8 % of gaze transitions in code snippets with atoms. In then, experiment. Copstein et al. [4] instructed subjects to step through the program if they were the computer, execute each instruction in their mind, and record the standard output of the program. They also modified the experiment's protocols to include only meaningful instructions. How oftenly these are necessary? By repeating this experiment many times from the subject. Our experiment followed a very similar approach. This approach was mixed with an eyeTracker device to record the subjects' eye movements.

Other works [1, 3, 6, 8, 11] have studied the correlation and effectiveness of visual attention tracking on code and text understanding. They have shown that a longer fixation on any specific part of the code can indicate a higher cognitive workload trying to understand each line ofcode. In our study on our knowledge, no similar studies with eye tracking were performed to investigate the impact of atoms of confusion in code comprehension.

Gospstein et al. [5] showed a strong correlation between atoms of confusion and bug fix commits and a tendency for atoms of confusion to be commented. They also observed a higher rate of security vulnerabilities in projects with more atoms. They did it by selecting 14 of the most representative and popular open-source C and C++ repositories to measure the prevalence and significance of atoms of confusion. They correlate the occurrence of these atoms in the tested projects with the external ones. They find that the comment rate highly related to the prevalence with more atoms tend to have more CVEs (Common Vulnerabilities and Exposure) and bugs by domain. In this experiment, they did not analyze developers' performances or asked them about the code; they searched for atoms of confusion in existing code. They analyzed the correlation between the rate of atoms on these repositories with bugs' presence and whether these codes were refactored, and the atoms were removed.

---

SBES '20, October 21-23, 2020, Natal, Brazil

Oliveira, et al.

from the code, among other questions. In our study, we include the measurement of how long it takes to developers understand code extracted from real open-source projects and which part of code they understand correctly. Questions about the impact of the difference in code understanding with and without atoms

Another study conducted by Medeiros et al. [10] tried to better understand the occurrence and relevance of atoms of confusion by mining some repositories seeking for the occurrence of these atoms and also applied a survey with 93 developers. They found that the atoms studied (92 % ) are highly used in practice and that developers agreed that 6 of the studied atoms hinder code understanding, representing 50 % of the 12 atoms studied. They also showed that the atoms are not frequently cited on guidelines. Our experiment of the above methods allowed us to probe how well our code misunderstanding in practice. Moreover, it allows us to catalog which atoms cause confusion and propose a tool to indicate and refactor them. Besides, we followed a more objective approach by using an eye-tracker, which allowed us to compare the perception of programmers with quantitative data about real confusion generated by the atoms.

## 8 CONCLUDING REMARKS

In this paper, we presented a controlled experiment with an eye tracker with 30 participants to investigate the effects of atoms of confusion on code comprehension. In particular, we analyzed the atoms' effects on time, accuracy, and participants' attention while specifying the output of six code tasks adapted from real open-source systems. We found evidence that code with atoms of confusion is more time-consuming, unlike code with no atom of confusion. This study was the first effort to do such attention on particular areas of the atoms more often. We observed an increase by 36.8 % of gaze transitions in code snippets with atoms, thus more visual effort.

In previous work, Geppstein et al. [4] showed that the presence of these patterns in the code affects developers' performance, i.e., time and accuracy, and increase code misunderstandings. We showed that this bias, however, can be ameliorated by adding more accuracy, namely attention, should also be taken into consideration being affected by the presence of atoms. This was clear by the increase in the number of points in AOI entries in AOI, and the number of gaze transitions, indicating more effort when analyzing code with atoms of confusion. These nuances would not be possible to add more effort to the code, because it is generally considered sensitive to a perspective of analysis that contributes to more insights into the atoms' impact on the attention.

For the developer community, we recommend avoiding writing code with atoms of confusion since they can hamper code comprehension. For the research community, we encourage more empirical study around the code of reference. However, the analysis of confusion, since we have seen that some atoms can cause more negative effects than others. Other comprehension code scenarios and activities should also be explored, and other eye-tracking metrics should also be investigated. We believe that more empirical analysis of code conflict can help inform future directions of work of confusion among software developers. We also recommend them

to propose and implement refactorings in IDEs to remove atoms of confusion automatically.

## REFERENCES

[1] Roman Bedar and Markkin Tikkanen. 2009. An Eye-tracking Methodology for Characterizing Process Performance. IEEE Transactions on User Interface Evaluation and Design, vol. 6, no. 3, pp. 152-167. IEEE, 2009.

[2] George E. P. Box, J. Stuart Hunter, and William G. Hunter. 2005. Statistics for Experiments: Design, innovation, and之道 . Wiley-Interscience.

10. Terasjuni, Roman, Andrew Arnold, Andrew Berg, Matschus, Jens, James Earl, and Michael C. Morin. 1997 Hub-5e Eval System Design. http://isl.speech.lv.uka. in Code Reading. Relating the Linear Order In Proceedings of the International Systems Engineering Conference, 1997, 23-26 June, 1997, St. Louis, Missouri.

41. Dan Gupta, Jake Iacinski, Yu Yan, Lori Allen Deloit, Yiyan Zhang, Martin Westphal, "Professional Quality of Life (PQQ) Measurement Scales." In Proceedings of the Foundations of Software Engineering (FSE) 13(2):119-128, 1997.

14 Dan Gupta, Hongwei Henry Zhou, Phyllia Frank and Justin Cuttone. 2018 The AI Ethical Society: Ethical AI for the Rest of Us. Cambridge University Press, Online. Proceedings of the Mining Software Reunion (SSR 2018) 281-291.

[7] Peter Green, Randall Hendrick, Markus Johnson, and Yoohyoung Lee. "Learning psychology through play." 2019 International Journal of Tracking and Gaming, Journal of Experimental Psychology: Learning, Memory, and Cognition, pp. 1-15.

[7] Ahmad Ihsan and Dr. G Feris Fettweis. 2017 . How programmers read regular code effectively . http://www.microsoft.com/en-us/library/dotnetmvc . Accessed: February 2018. (IEEE17/23) 712-713, 1404–1407.

[8] Marcel Just and Patricia Carpenter. 1965. A theory of reading: From eye fixation to comprehension. Psychological Review. Psychological Review, 329-354.

[9] Romero Maluquira, Mario Alberto, Rodrigo Benoit, Eduardo Monteiro, Flavio Medeiros, Alessandro Garcia, and José Benoit. 2017. The Discipline of Preprocessor-based Antennas Based on TGAUT-Commodities. Master in Proceedings of the International Conference on Field Performance (ICFP) . IEEE: 297–307.

[8] Flavius Medenicki, Gabriel Lam, Guillemenceau Amed, Sven Apel, Christian Klein, Tero Karras, and Jan Kramovek. Foundations of embedded system analysis: a code pattern in C++ open source software projects. Improved Embedded Engineering Systems, volume 199 (2007).

19 John Meltz, Clasme Brusseau, and Andrey Wokwuk. 2016. How Does the Department of Engineering School affect the quality of the International Conference on Software Engineering (ICSE). 679-680

[12] José Medel, Fábio Nabarro, Luis Huron, Clara Braimard, and Andrew Watson. "Perseverance and Quality of Life among Patients with Parkinson's Disease". International Conference on Program Comprehension (ICPC-17) , 44–49.

[18] Robert Mundell, Andrea Mucci, and Michele Lanza. 1995 How you want that to happen. http://islam.org/ISLAM.speech.lvcsr.html?doc=24361 Robert Mundell, International Conference on Program Compensation (ICPC) 123–25,

[14] Douglas C. Montgomery. 2006. Design and Analysis of Experiments . John Wiley & Sons.

15 Mário Ribeiro, Paula Bobe, and Christian Kustner. 1994 Hub-5e Eval System Evaluation. http://isl.speech.lvcsr.edu/ISL.speech.lvcsr.html

[16] Carsten Schütt, Tony Eick, Ahmad Taherzian, Tereen Bujshu, and Irfan Naz. 2018. The 3000+ pages of scientific papers published by International Journal of Science Education. In Proceedings of the ITEC Working Group Meeting . 63–68.

21 Zohreh Sharaf, Timothy Shatter, Bonar Sharaf, and Yarm-Chan Gutiérrez. 2015, in Proceedings of the 13th IEEE International Conference on the Asia-Pacific Energy Engineering Conference (APEC) , 196–195.

[1] Janet Siegmund. 2016. Program comprehension. Past, present, and future. In Proceedings of the Software Analysis, Evolution, and Reengineering (SAFER 2016) . http://www.speech.lvcsr.hu/~maria-szepesvari/

Dan Sjörgren, Bente Espe, Erik Arekshin, Tore Dals, Mats Gjergsted, Anela Gjergsted, Henrik Olsson, and Mats Westphal. "Design of embedded systems for wireless sensor systems", IEEE Conference on Speech Communication, IEEE, 2004.

29. Leigh Ann Sudd-Dealyer, Mark Steblik, and Sharon Carrero. 2012. Code Conventions: The World of Formal Methods, Formal Language, and Formal Interaction. Informa and Technology in Computer Science (IJFCS) 31: 81–86.

[2] Clai Woulin, Per Brinten, Martin Hoet, Magnus L. Olsson, Bjørn Røgnell, Torbjørn Rasmussen. 2011. Experimentation in software engineering . Springer Science & Business Models.

[2] Marif Yeh, Yu Yan, Dan Gupta, and Yuan Zhang. 2017. Detection and identification of Drought Biomass Erosion: a Comprehensive Using EEG for Frontiers in Education Conference (IEE) 17-1:5.

