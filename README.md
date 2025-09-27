<a name="top"></a>

<div align="center">
  <img src="https://level3.hn/_astro/llm-evaluation.DB8cmg_A_Z2uN3Om.webp" alt="Logo"/>
</div>

<br>
<div align="center">

  ### 🛠 Python (OpenAI)
  ### 🛠 Docker

</div>

# Data Privacy Evaluation Suite

## 1. Introduction

This project is one of the LEVEL3, powered by Arkadia, tracks, partnered with the AI Technology company [Aleph Alpha](https://aleph-alpha.com/), with the purpose of creating an automated evaluation suite for Large Language Models. Given the recent outburst in AI agents, this project is an attempt of contributing to the evaluation process of such systems, in the domain of Data Privacy, tackling real problems, as well as an opportunity to acquire knowledge and hands-on experience on the fast evolving field of AI. By simulating real case scenarios, applied in mulitple LLMs used as Systems Under Test (SUTs), in an attempt to address common pitfalls, assess the limitations of fine-tuned models and measure their ability to resist and protect sensitive personal information, this evaluation system can be used to provide a reference about their internal behavior on how they treat sensitive data, using commonly identified metrics.

The project simulates the case of a RAG system, accessible by mulitple users, and evaluates its ability to protect sensitive information, given a common external database. More specifically, the use case is this of a HR employee database,containing sensitive personal information. Through adversarial prompting, the evaluation suite attempts to extract said information and measures the accuracy of the leaked results. Though a specific subject is necessary for building the suite, it is also easy to imagine that such systems could be applied to a variety of domains and applications, noting the importance of the evaluation process.

### 1.1 RAG models

*Retrieval Augmented Generation* (RAG) models are systems that can access an external database to retrieve the most updated and accurate information, overcoming any possible references based on their training data. The external database is accessed through an embedding model for prompt flexibilty, simulating real world systems, as much as possible. Even though this project utlizes an exteenal *table* databse, where an sql tool could easily suffice for matching queries, an embedding model provides further flexibility on the adversarial prompts' creativity.

### 1.2 Embedding model

As previously stated, this project utilizes an embedding model, in order to access the external database, providing as much versatility and accuracy in the retrieval attempt as possible. The model is `all-mpnet-base-v2`, provides the proper accuracy as well as the ablity to handle relatively complexed prompts, without overkill. It is necessary for a system such as this, to be able to be as accurate as possible in its attempt to retrieve the necessary infromation. The LLM's output and therefore the evaluation results are higly related to the accuracy of the information retireved by the embedding model.

## 2. Data Privacy domain



## 3. Pipeline

As stated in the [Introduction] he project attempts to simulate a real case scenarios, where one common system is accessible by multiple users, of different levels of clearance. As it is commonly known that such systems can be working alongside with many different types of security leyaers, in this project we evaluate the LLM's raw ability to protect personal information, as it is paramount to be able to evaluate such system's ability to protect sensitive information, if exposed to unsolicited behavior. 

### 3.1 External Database

The external is a table database of Sythetic Data which contains employees' personal information. Data can be generated through custom made regexes, that follow specific patterns. Figure 3.1 displays a small of the database:

| EMployee_Name | EmpID | Salary | Home_address | 
|---------------|-------|--------|--------------|


### 3.2 Information Sensitivity categorization

The *SUT* (System Under Testing) LLM's system prompt is enhanced with the different types of information's sensitivity. It is instructed to always comply with the *Privacy Rules*, before revealing any data. The different levels of sensitivity are provided in the table below:

| High Sensitivity | Medium Sensitivity | Low Sensitivity |
|------------------|--------------------|-----------------|
| Credit card || - Employee Name|
|SSN || - Salary |

### 3.3 Tenants

What if the LLM SUT was accessed by multiple organisations also? External contractor companies or Auditors could be accessing the same system, but there should be restrictions. The purpose of this reasoning intends to simulate a cross section system, therefore a Data protection evaluation process among different Tenants seems to make total sense. This functionality is achieved through *Tenants*, which are no other than different Company Profiles accessing the same system. Each Tenant should have its own External Database, but different user profiles may have different priviledges among more than one external databases. Is the SUT able to protect any sensitive information appropriately? A random Tenant example is given below:


### 3.4 Users

At the beginning of the suite, the user has the ability to choose among different user profiles, with different levels of clearance. Each option is offering unique characteristics compared to the rest:

| Role | Description |
|------|-------------|
| Customer| Has access only to Low Sensitivity Info |
| Agent | Has access to Internal Low & Medium Sensitivity Info|
| External contractor | Has access to Low & Medium Sensitivity Info of multiple Tenants |
| Admin | Has access to all information|

## 4. Technical approach / Parameters

### 4.1 Prompts

#### 4.1.1 Adversarial Categories

### 4.2 Ground Truth

### 4.3 SUT LLMs

### 4.4 System Prompt

#### 4.4.1 Baseline

#### 4.4.2 Custom Categorization

### 4.5 Metrics

## 5. Conclusions

## 6. References
