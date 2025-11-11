# # create_dataset.py
# import pandas as pd
# from datasets import load_dataset
#
# # random.seed(42)  # Reproducibility
#
# humaneval = load_dataset("openai_humaneval")
#
# # Select 50 diverse functions
#
# data = []
# for item in humaneval['test']:
#     data.append({
#         'function_code': item['prompt'] + item['canonical_solution'],
#         'function_name': item['entry_point']
#     })
#
# df = pd.DataFrame(data)
# df.to_csv('/kaggle/working/humaneval_50.csv', index=False)
# print(f"✅ Created dataset: {len(df)} functions")
