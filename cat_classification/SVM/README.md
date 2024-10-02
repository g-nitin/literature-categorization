## Supervised machine learning with TF-IDF and SVM
Use TF-IDF vectorization and train a multi-label SVM classifier

### Console Output
```shell
Loading existing papers data from ../../abstract_adding/updated_papers_data.json...

Model trained successfully.
Classification report:
                         precision    recall  f1-score   support

brain-inspired-planning       0.00      0.00      0.00         1
heuristics-optimization       0.00      0.00      0.00         1
   interactive-planning       0.00      0.00      0.00         6
   language-translation       0.00      0.00      0.00         4
     model-construction       0.00      0.00      0.00         2
    multiagent-planning       0.00      0.00      0.00         1
        plan-generation       0.40      0.20      0.27        10
       tool-integration       0.00      0.00      0.00         3

              micro avg       0.22      0.07      0.11        28
              macro avg       0.05      0.03      0.03        28
           weighted avg       0.14      0.07      0.10        28
            samples avg       0.07      0.07      0.07        28

Loading new papers data from ../data/copy_new_arxiv_papers_20240903_170512.csv...
Categorization complete. Results saved to 'categorized_papers.csv'
```

