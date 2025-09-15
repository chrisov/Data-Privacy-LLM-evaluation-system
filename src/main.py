import utils
import LLM_loader as llm
import gliner_model as ner
import baseline as gtruth

def main():
    config = utils.load_config()
    prompts = utils.load_json(config['prompts_filepath'], 'query')
    print("\n------------------------------------\n")
    for prompt in prompts:
        ground_truth = gtruth.create_dict(config['prompts_filepath'], prompt)
        respond = llm.loader(config['model_name'], prompt)
        data = ner.loader(prompt, respond, config['NER_model_name'], )

        print(f"Question: {prompt}\n")
        print(f"Answer: {respond}\n")
        print("Sensitive data: ")
        for key, value in data.items():
            print(f"{key}: {value}")
        print("\nGround truth: ")
        if (ground_truth):
            for key, value in ground_truth.items():
                print(f"{key}: {value}")
        else:
            print("No ground truth!")

    # Compare the NER model's output with the ground truth's output

if __name__ == "__main__":
    main()
