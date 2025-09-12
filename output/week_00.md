### Domain Selection
> Employee information extraction vulnerability in enterprise chatbots with database access.

`Scenario:` An internal company chatbot that has access to HR databases and can answer employee queries about policies, benefits, etc. The target is to evaluate whether unauthorized users can extract sensitive employee information through prompt injection or social engineering techniques.

### Model Exploration
`HuggingFace Model:` Qwen/Qwen2.5-1.5B-Instruct

* gemma/Gemma 2-1B-it (unauthorisation prob)
* distilbert/distilgpt2 (small & unstable)
* TinyLlama/TinyLlama-1.1B-Chat-v1.0 (unstable)
* HuggingFaceH4/zephyr-7b-beta (too big for CPU)
 (good to go)

`Reason:`
* Instruction-Tuned (better at following system prompts)
* state-of-the-art open-source model
* Lightweight (1.5B parameters)
* Understand structured data ([more details](https://qwenlm.github.io/blog/qwen2.5/))

`Exploration:`
* build Employee Dataset (5,5) & small prompt (1,5)
* run the model to observe the behaviour
* observations:
    1. without restriction (via System Prompt) provide all PII
    2. with restriction always failing for case 4

Possible reason:
* hk 


reading:
1. https://medium.com/intro-zero/getting-started-with-transformers-pipelines-and-the-hugging-face-model-hub-4bd743c3f0eb
2. https://www.edpb.europa.eu/system/files/2025-04/ai-privacy-risks-and-mitigations-in-llms.pdf