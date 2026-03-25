# PyODPS Reference for SQL Export Agent

## Scope

Use this reference when the task depends on the `odps` / `pyodps` Python package that powers MaxCompute (ODPS) access in [`run_sql_export.py`](C:/Users/haotian.liu/Documents/GitHub/xyf-competition-mvp/.agents/skills/dataworks/scripts/run_sql_export.py).

This file focuses on the subset of PyODPS that matters for this skill:

- package installation
- `ODPS(...)` client construction
- SQL execution with `run_sql`
- waiting for completion
- fetching result sets with `open_reader`
- converting results to pandas
- DataWorks-specific Tunnel behavior and common pitfalls

## Primary sources

- Official docs: <https://pyodps.readthedocs.io/en/stable/>
- Chinese docs: <https://pyodps.readthedocs.io/zh_CN/latest/>
- PyPI package: <https://pypi.org/project/pyodps/>
- Official GitHub repo: <https://github.com/aliyun/aliyun-odps-python-sdk>

## What PyODPS is

PyODPS is Alibaba Cloud MaxCompute's Python SDK and data analysis framework. In this skill, it is used as the execution client for ODPS SQL plus result retrieval into pandas.

The current script imports:

```python
from odps import ODPS
```

That import comes from the `pyodps` package published on PyPI, while the runtime module name remains `odps`.

## Install and import

For this skill, the practical install commands are:

```bash
pip install pyodps
```

If a fuller environment is needed, the GitHub README also documents:

```bash
pip install pyodps[full]
```

Decision rule:

- prefer `pip install pyodps` for the SQL export script unless there is a confirmed dependency on notebook / extended features
- treat `ImportError: No module named odps` as a package-install problem, not a credential problem

## Authentication and client construction

The core constructor pattern documented by PyODPS is:

```python
from odps import ODPS

o = ODPS(access_id, access_key, project="your-project", endpoint="your-endpoint")
```

For this skill, the constructor arguments map directly to:

- `access_id`
- `secret_access_key`
- `project`
- `endpoint`

The current script uses named arguments:

```python
odps = ODPS(
    access_id=access_id,
    secret_access_key=access_key,
    project=project,
    endpoint=endpoint,
)
```

Operational guidance:

- keep credentials outside source files whenever possible
- prefer env vars or caller-supplied CLI args
- treat `project` and `endpoint` as first-class configuration, because many connection failures are actually endpoint mismatches

## Recommended env var mapping for this skill

This skill currently resolves credentials from custom env vars:

- `ALIBABA_CLOUD_ACCESS_KEY_ID`
- `ALIBABA_CLOUD_ACCESS_KEY_SECRET`
- `ALIBABA_CLOUD_PROJECT_JINGYING`
- `ALIBABA_CLOUD_REGION_ENDPOINT`

These names are skill-local conventions, not canonical PyODPS requirements. When updating the script later, keep this distinction clear:

- PyODPS requires values
- the skill chooses how those values are sourced

## SQL execution model

The PyODPS pattern used by this skill is:

```python
instance = odps.run_sql(sql_text)
instance.wait_for_success()
```

Meaning:

- `run_sql(...)` submits SQL and returns an Instance handle
- execution is asynchronous at submit time
- `wait_for_success()` turns the workflow into a blocking wait before result retrieval

This is the right model for this skill because the export workflow should not proceed until the SQL instance has finished successfully.

## Logview handling

PyODPS instances can expose a Logview URL via:

```python
instance.get_logview_address()
```

Use Logview when:

- SQL execution fails and you need engine-side diagnostics
- the query is slow and you need progress visibility
- you need to share execution details with another operator

This is why the script prints the Logview address immediately after submission.

## Result retrieval

The skill currently uses:

```python
with instance.open_reader(tunnel=True, limit=False) as reader:
    df = reader.to_pandas(n_process=multiprocessing.cpu_count())
```

Interpretation:

- `open_reader(...)` opens the instance result reader
- `tunnel=True` requests Tunnel-based retrieval
- `limit=False` avoids the default row cap behavior that can appear in non-Tunnel result paths
- `to_pandas(...)` materializes the result as a pandas DataFrame

Why this matters:

- this skill is designed for export, so silent truncation is worse than a loud failure
- Tunnel mode is the safer default when the result may exceed the regular instance result limit

## DataWorks-specific note: Instance Tunnel

The official Chinese PyODPS docs for DataWorks note that in some DataWorks environments, Instance Tunnel is not enabled by default. In that case, `instance.open_reader` may fall back to the normal result interface, which only returns up to 10,000 rows.

Practical implication for this skill:

- if the caller expects large exports, keep `tunnel=True`
- if the environment blocks Instance Tunnel, expect result-fetch failures or row-count surprises
- when row counts look suspiciously capped near 10,000, check whether Tunnel is actually available in that environment

## Pandas conversion

PyODPS supports converting readers to pandas directly. The script uses:

```python
reader.to_pandas(n_process=multiprocessing.cpu_count())
```

Guidance:

- this is convenient for Excel export and DuckDB write-back
- multiprocessing can improve conversion speed on larger result sets
- memory pressure still happens in the local Python process, so very large result sets can fail even if the SQL succeeds

Agent rule:

- distinguish "SQL ran successfully" from "local result materialization failed"
- report fetch / reader failures separately from ODPS execution failures

## Common failure patterns

### Import failure

Symptom:

- `failed to import odps package`

Likely cause:

- `pyodps` not installed in the active Python environment

### Authentication or endpoint failure

Symptoms:

- access denied
- signature errors
- endpoint-related errors

Likely causes:

- wrong AccessKey pair
- wrong project
- wrong endpoint for the target MaxCompute region

### SQL instance failure

Symptoms:

- `wait_for_success()` raises
- Logview shows parser, permission, resource, or partition errors

Likely cause:

- the SQL itself failed in MaxCompute, even though client creation succeeded

### Result fetch failure

Symptoms:

- `open_reader(...)` or `to_pandas(...)` raises

Likely causes:

- Tunnel not available
- result too large for local memory
- network instability during download

## Safe usage guidance for this skill

- submit exactly the SQL text read from disk; do not silently rewrite it
- print or surface Logview early whenever possible
- wait for success before opening a reader
- prefer Tunnel reads for export-oriented workflows
- treat empty results as a valid business outcome, not necessarily an error
- keep ODPS-stage errors separate from local pandas / Excel / DuckDB-stage errors

## Useful alternatives and extensions

PyODPS also exposes a DBAPI-compatible interface documented in the official docs. That can be useful for tools expecting a DBAPI connection, but this skill should keep `ODPS.run_sql(...)` as the canonical path unless there is a specific need to switch abstraction layers.

If the skill later needs:

- MCQA / SQA execution
- quota configuration
- advanced options such as `odps.options`

add those as separate references instead of bloating this file.

## Source links

- PyODPS docs home: <https://pyodps.readthedocs.io/en/stable/>
- DataWorks usage note on Instance Tunnel: <https://pyodps.readthedocs.io/zh_CN/latest/platform-d2.html>
- Options reference including `tunnel.use_instance_tunnel`: <https://pyodps.readthedocs.io/zh-cn/latest/options.html>
- DBAPI docs: <https://pyodps.readthedocs.io/en/stable/db-dbapi.html>
- PyPI package page: <https://pypi.org/project/pyodps/>
- Official GitHub repository: <https://github.com/aliyun/aliyun-odps-python-sdk>
