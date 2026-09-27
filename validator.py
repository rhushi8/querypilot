import re

# Word boundaries, so updated_at and deleted_flag pass.
FORBIDDEN_KEYWORDS = [
    "drop", "delete", "update", "insert", "alter",
    "truncate", "replace", "create", "attach", "detach",
    "pragma", "grant", "revoke", "vacuum", "reindex",
]

_FORBIDDEN_RE = re.compile(
    r"\b(" + "|".join(FORBIDDEN_KEYWORDS) + r")\b", re.IGNORECASE
)


def validate_sql(sql_query):
    cleaned_query = sql_query.strip().rstrip(";").strip()
    lowered = cleaned_query.lower()

    if not (lowered.startswith("select") or lowered.startswith("with")):
        return False, "Only SELECT queries are allowed."

    # No stacked statements (SELECT 1; DROP TABLE x).
    if ";" in cleaned_query:
        return False, "Multiple SQL statements are not allowed."

    match = _FORBIDDEN_RE.search(cleaned_query)
    if match:
        return False, f"Query contains forbidden keyword: {match.group(1).upper()}"

    return True, None
