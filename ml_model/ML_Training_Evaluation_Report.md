\# Machine Learning Training and Evaluation Report

\## AI-Powered Customer Service Chatbot



\### 1. Introduction



The objective of this work is to develop and evaluate machine learning models for customer-service intent classification. The chatbot aims to identify customer queries, such as order tracking, refund status, payment issues, complaints, and requests to speak to a human agent.



Two separate experiments were conducted:

1\. A custom dataset experiment for the project's 17 customer-service intents.

2\. A CLINC150 benchmark experiment for classifying 150 known intents and investigating out-of-scope (OOS) message detection.



These experiments use different datasets and label sets. Their results are reported separately.



\### 2. Main Chatbot Model



\#### 2.1 Dataset



The custom dataset contains 212 deduplicated examples across 17 customer-service intents. It combines the project's original and additional training examples.



The intents include greeting, order tracking, order status, order cancellation, delivery delay, return request, refund status, payment failure, payment issues, product information, account login, password reset, damaged product, complaint, human agent, goodbye, and unknown.



\#### 2.2 Preprocessing and Feature Extraction



Text was converted into numerical features using TF-IDF (Term Frequency–Inverse Document Frequency). The vectorizer uses word unigrams and bigrams, allowing the model to consider individual words and two-word phrases. Sublinear term frequency scaling was enabled.



\#### 2.3 Training Method



The dataset was divided using a stratified 75/25 train-test split with random state 42.



\- Training examples: 159

\- Test examples: 53

\- Models compared: Logistic Regression and Linear Support Vector Machine (Linear SVM)

\- Model-selection metric: Macro F1 score



Stratification helps preserve the distribution of intent labels between the training and test subsets.



\#### 2.4 Results



| Metric | Logistic Regression | Linear SVM |

|---|---:|---:|

| Accuracy | 73.58% | 75.47% |

| Macro precision | 0.7485 | 0.7680 |

| Macro recall | 0.7222 | 0.7288 |

| Macro F1 score | 0.7124 | 0.7237 |



The Linear SVM achieved the higher accuracy and macro F1 score, so it was selected as the preferred model.



After model selection, the selected model was refitted on all 212 custom training examples for use by the project.



\#### 2.5 Additional Project Test Cases



The main chatbot model was also evaluated on a separate set of 32 project test cases. The observed raw classification accuracy was 87.5%.



This result is based on a small, separate test set and should not be directly compared with the 75/25 split results as if both measurements came from the same test data.



\### 3. CLINC150 Benchmark Experiment



\#### 3.1 Dataset



A separate experiment used CLINC150, a benchmark dataset containing 150 known intent categories and out-of-scope examples.



The known-intent data used in the experiment consisted of:

\- Training set: 15,000 examples

\- Validation set: 3,000 examples

\- Held-out known-intent test set: 4,500 examples



The OOS data included 100 validation examples and 1,000 held-out test examples.



This benchmark experiment was kept separate from the custom 17-intent chatbot because its intent categories and dataset differ.



\#### 3.2 Model Training and Selection



TF-IDF word features using unigrams and bigrams were used. Sublinear term frequency scaling and Unicode accent stripping were enabled.



Logistic Regression and Linear SVM were compared using class-balanced training configurations. Macro F1 was used for model selection.



\#### 3.3 Validation Results



| Metric | Logistic Regression | Linear SVM |

|---|---:|---:|

| Validation accuracy | 88.33% | 90.83% |

| Validation macro F1 | 0.8826 | 0.9077 |



The Linear SVM achieved the better validation results and was selected for the CLINC150 experiment.



\#### 3.4 Held-Out Known-Intent Test Results



| Metric | Linear SVM |

|---|---:|

| Test examples | 4,500 |

| Accuracy | 91.13% |

| Macro F1 score | 0.9102 |



These results measure classification performance on known CLINC150 intents. They do not measure OOS detection performance.



\### 4. Out-of-Scope Detection Experiment



\#### 4.1 Objective



A separate threshold experiment investigated whether the CLINC150 Linear SVM could identify messages that do not belong to its known intent categories.



The model's maximum decision score across its intent classes was used as the detection score. If the maximum score fell below a chosen threshold, the message was flagged as OOS.



These decision scores are raw SVM scores, not calibrated probabilities. A negative score does not, by itself, mean the model is incorrect.



\#### 4.2 Validation Score Analysis



The validation score inspection used 3,000 known-intent examples and 100 OOS examples.



| Score statistic | Known intents | OOS examples |

|---|---:|---:|

| Minimum | -0.932 | -0.932 |

| Median | 0.643 | -0.531 |

| Maximum | 2.874 | 1.527 |

| 10th percentile | -0.190 | -0.777 |

| 25th percentile | 0.200 | -0.664 |

| 75th percentile | 0.994 | -0.242 |

| 90th percentile | 1.281 | 0.181 |



The OOS scores were generally lower than the known-intent scores, but the distributions overlapped. Therefore, a single threshold cannot perfectly separate all known and OOS messages.



\#### 4.3 Threshold Selection



Several thresholds were compared on the validation data. The threshold near -0.4899 was selected using the validation-based OOS F1 procedure.



At a rounded threshold of -0.49, the validation results were:



\- OOS precision: 36.1%

\- OOS recall: 56.0%

\- OOS F1 score: 0.439



The threshold near -0.55 also produced a rounded F1 score of 0.439. The selected threshold was retained according to the existing threshold-selection procedure.



\#### 4.4 Held-Out OOS Test Results



The selected threshold was evaluated on a separate test set containing 4,500 known-intent examples and 1,000 OOS examples.



| Metric | Result |

|---|---:|

| Overall known-vs-OOS accuracy | 89.04% |

| OOS precision | 80.03% |

| OOS recall | 52.90% |

| OOS F1 score | 0.637 |



The detector identified approximately 529 of the 1,000 OOS test examples and missed approximately 471. Its OOS precision of about 80% indicates that most messages flagged as OOS were genuinely OOS in this test.



The accuracy reported here measures the binary distinction between known and OOS messages. It is not the same as known-intent classification accuracy.



\### 5. Discussion



The custom chatbot experiment showed that Linear SVM performed better than Logistic Regression on the 17-intent dataset. However, the dataset is relatively small, so additional examples and broader testing would help establish how well the model generalizes to real customer messages.



The CLINC150 experiment achieved approximately 91% accuracy on held-out known-intent examples. This demonstrates strong performance on that benchmark's known-intent classification task.



The OOS experiment showed that threshold-based detection can identify many unfamiliar messages, but it does not detect all of them. The overlap between known and OOS decision scores creates a trade-off between catching more OOS messages and incorrectly flagging known-intent messages.



The two experiments should not be treated as one model evaluation. The CLINC150 benchmark uses a different set of intent labels, and the CLINC150 OOS threshold has not been integrated into the main 17-intent chatbot.



\### 6. Limitations



1\. The custom dataset contains only 212 examples, limiting the variety of customer language represented.

2\. The separate 32-case project test set is small and may not represent real-world traffic.

3\. CLINC150 benchmark results may not transfer directly to the project's customer-service domain.

4\. The OOS validation set contains only 100 examples, so its threshold estimates may be sensitive to the examples included.

5\. The SVM decision scores are not calibrated probabilities.

6\. The selected OOS threshold still misses a substantial proportion of OOS messages.

7\. Further testing is required before claiming reliable performance in a production customer-service environment.



\### 7. Future Improvements



\- Collect more realistic and diverse customer-service queries for all 17 project intents.

\- Evaluate the custom model on a larger, independent test set.

\- Inspect per-intent precision, recall, F1 scores, and confusion matrices to identify commonly confused categories.

\- Improve OOS detection using more representative out-of-scope examples and additional validation data.

\- Evaluate the effect of different thresholds according to the cost of false OOS flags versus missed OOS messages.

\- Test the complete chatbot pipeline, including clarification responses and escalation to a human agent.

\- Keep the custom chatbot and CLINC150 benchmark results separate unless a deliberate integration and evaluation plan is implemented.



\### 8. Conclusion



The project compared Logistic Regression and Linear SVM for customer-service intent classification. Linear SVM was selected for the custom 17-intent chatbot, achieving 75.47% accuracy and a macro F1 score of 0.7237 on the stratified test split. The separate project test set recorded 87.5% accuracy across 32 cases.



In a separate CLINC150 experiment, Linear SVM achieved 91.13% accuracy and a macro F1 score of 0.9102 on held-out known-intent examples. A threshold-based OOS detection experiment achieved an OOS F1 score of 0.637 on the held-out test set, with 80.03% precision and 52.90% recall.



Overall, the experiments demonstrate the usefulness of TF-IDF features and linear classifiers for intent recognition, while highlighting the need for more representative data, careful threshold evaluation, and further testing before deployment.



\### 9. Reproducibility and Project Files



The project includes scripts for training and evaluating the custom chatbot model and for conducting the separate CLINC150 experiments. Evaluation results are saved as JSON files under the `ml\_model/models` directory.



The CLINC150 dataset and model are separate experimental resources. Their presence in the local project directory does not imply that the dataset or model binary has been committed to the Git repository.



