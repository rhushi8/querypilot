# SQL Analytics Assistant

Ask a database a question in plain English. Get back the SQL it wrote, a chart,
an explanation of what the query does, and a one-line business takeaway.

## Why

Most people who need answers from a database can't write SQL, so they wait on
someone who can. Handing the job to an LLM on its own is worse, because left
unconstrained it invents table names, invents column names, and will cheerfully
write a DELETE. The aim here is to keep the question in English while
guaranteeing that whatever actually runs is valid, read-only and safe.

## What it does

Generation is schema-aware. The real table and column names go into the prompt
as context, so the model isn't guessing at them.

If a query fails, the SQLite error goes back to the model for one corrective
retry before giving up. A hallucinated column name usually survives that round
trip.

Recent question and SQL turns are kept as context, so a follow-up like "now
break that down by month" resolves against what you just asked.

Validation happens before execution, not after. SELECT and CTEs only.
Destructive keywords are matched on word boundaries, so a column called
`updated_at` is fine while a `DROP` is not, and stacked statements are rejected
outright.

Charts are chosen by the shape of the result: one numeric column gives a
histogram, a category plus a metric gives a bar chart, two categories plus a
metric gives a grouped bar.

The plain-English explanation and the business insight both degrade gracefully
if the LLM is unavailable.

## How it works

```
question → schema-aware SQL generation → validation (SELECT-only) → run on SQLite
         → on error, one repair attempt → chart + explanation + insight
```

Generation, validation and repair all live in `sql_engine.py`, away from the
UI, so they can be unit-tested without Streamlit or a running LLM.

## Stack

Python, Streamlit, SQLite, pandas, Plotly, sqlparse, and Ollama running
CodeLlama locally.

## Quickstart

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python database_setup.py            # builds the sample SQLite database
streamlit run app.py
```

SQL generation needs a local Ollama model running, CodeLlama for example.

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

The tests cover the validator guardrails and the generate/validate/repair engine
using a stub LLM and an in-memory SQLite database, so Ollama isn't needed to run
them.

## Layout

```
app.py               streamlit interface
sql_engine.py        generation, validation, one-shot repair (UI-free, tested)
llm.py               local Ollama client with error handling
validator.py         SQL safety checks
db.py                database access
database_setup.py    builds the sample data
database.db          sample database, so the repo runs as cloned
```

## Example

Ask "for each region, show total revenue for January" and it writes the JOIN and
GROUP BY, runs it, draws a bar chart, explains the SQL in English, and
summarises what the numbers say.
