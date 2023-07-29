# Chain-of-Thought LLM-Agent
Chain of Thoughts is a MRKL system - a modular, neuro-symbolic architecture that combines large language models, external knowledge sources and discrete reasoning built on top of LLMs.

**knowledge-tools**
- google search for finding most recent information
- calculate for solving math problem
- chinook for custom database as alternative to Northwind
- wikipedia for common knownledge
- terminal shell
---
```
# setting up chinook database
download: https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql
sqlite3 Chinook.db
.read Chinook_Sqlite.sql

# install libs
bash install_libs.sh

```
## Run it locally
```
bash run.sh
```
![screenshot](./assets/cot_screenshot.png?raw=true "screenshot")

## Benefits
MRKL systems enjoy important benefits when compared to fine-tuned multi-task models:

1. Safe fallback: In case the input doesn’t match any existing expert module, the router sends the input directly to the general-purpose huge LM.
2. Robust extensibility: Since each expert is trained independently we are able to cheaply add new capabilities while guaranteeing that they do not compromise the performance of existing ones. The only component that requires retraining is the router which is a relatively lightweight task.
3. Interpretability: When the router invokes a specific module, that often has the side benefit of providing a rationale for the MRKL system’s output (“1 + 1 = 2 because the calculator said so”); such explanations are crucially lacking in existing language models.
4. Up-to-date information: The integration of external APIs allows the MRKL system to hook into dynamic knowledge bases, and correctly answer inputs that static models cannot.
5. Proprietary knowledge: Access to proprietary databases and other information sources.
6. Compositionality: By routing compounded multi-hop inputs to different experts we are able to naturally integrate their responses and correctly address complex inputs [20].

Useful Links 🔗
(research paper: MRKL SystemsDocumentation https://arxiv.org/pdf/2205.00445.pdf)

## Examples 
```
How many people live in canada as of 2023?
```
```
99 bottles of beers on the wall. One of them fell. How many are left?
```
```
Who is justin trudeau's girlfriend? What is her current age raised to the 0.5 power?
```
```
What is the full name of the artist who recently released an album called 'The Storm Before the Calm' and are they in the FooBar database? If so, what albums of theirs are in the FooBar database?
```

