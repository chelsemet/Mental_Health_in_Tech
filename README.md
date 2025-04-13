# Mental_Health_in_Tech_DE_project
    
## Problem Description
The tech industry's unique workplace dynamics, including high pressure environments, long hours, and remote work, create distinct mental health challenges. Tech companies need more data-driven insights about how workplace factors, company policies, and demographics influence mental health outcomes and treatment-seeking behaviors among employees. 

This project aims to identify key factors correlated with treatment-seeking behavior.

## Project Architecture
Dataset: Kaggle<br>
Infrastructure: Terraform<br>
Cloud: Google Cloud<br>
Workflow Orchestration: Apache Airflow<br>
Data Warehouse: Google BigQuery<br>
Transformation: Spark<br>
Visualisation: Looker Studio<br>


## Dataset
https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey

## Usage
- Set up a GCP project<br>
  ![image](https://github.com/user-attachments/assets/16ae08fe-ec2b-46b7-a6ff-34abf498e682)

- Create a virtual machine instance (VM)<br>
  ![image](https://github.com/user-attachments/assets/42d270e7-0caf-48af-a906-ec653e70d77e)

- Create SSH Keys and Access VM Remotely

- Create your dataset in BigQuery<br>
  ![image](https://github.com/user-attachments/assets/debf9503-a818-44d6-bdd8-bc74fa58dc1b)

- Get docker installed on your VM instance
  Tutorial: https://docs.docker.com/compose/install/

- Clone this repository on your VM instance
  ```bash
  cd Mental_Health_in_Tech
  ```
- Setup your kaggle API
  Follow the instruction provided by kaggle: https://www.kaggle.com/docs/api#authentication
  Place your token in your VM instance at
  ```bash
  ~/.kaggle/kaggle.json
  ```
- Run kaggle_api.py to download the data
```bash
  python3 data_ingestion/kaggle_api.py
```
- Download your google credentials and save it to
```bash
    .credentials/google_credentials.json
```  
- Build the docker image
```bash
  docker-compose up --build
```
- Access the Airflow webserver by visiting http://localhost:8080 in your web browser.<br>
  default username: admin<br>
  default password: admin<br>

## DAG pipeline
You can now check the status of the pipeline:<br>
![image](https://github.com/user-attachments/assets/2ccdee5a-d9ee-4097-a29b-85df9aa9165a)

This is the DAG workflow graph
![image](https://github.com/user-attachments/assets/065feb83-98ff-4d0f-96cf-ece6fa1727fa)

## Visualization
https://lookerstudio.google.com/reporting/1deb713d-5309-427a-89af-d493c36d304c
<br> 
![image](https://github.com/user-attachments/assets/8237f3ad-2d57-4abd-9a5f-7be35ed6aadf)
<br> 
![image](https://github.com/user-attachments/assets/a80b8b59-5e46-474c-8705-aa10cb19439e)

##Conclusion
- The key factors include:
  1. family_history: Do you have a family history of mental illness?
  2. care_options: Do you know the options for mental health care your employer provides?
  3. benefits: Does your employer provide mental health benefits?
  4. obs_consequence: Have you heard of or observed negative consequences for coworkers with mental health conditions in your workplace?
  5. anonymity: Is your anonymity protected if you choose to take advantage of mental health or substance abuse treatment resources?
  ...
  
- There appears to be some separation between the "Yes" and "No" treatment groups, though there's significant overlap. The "Yes" group tends to cluster more toward the upper left side of the plot, while the "No" group tends toward the lower right.
-The overlap between the two groups indicates that the features you've captured don't perfectly predict treatment status. This suggests that seeking mental health treatment in tech environments is influenced by factors beyond what's represented in the principal components.
- National differences seem less influential than individual factors or perhaps industry-specific factors that transcend national boundaries.
The partial separation indicates that PCA has captured some meaningful signal, but additional features or analysis approaches might be needed to better understand the factors influencing mental health treatment decisions in tech environments.
