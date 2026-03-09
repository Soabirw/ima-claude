---
name: "py-fp"
description: "Python FP principles with anti-over-engineering focus - Simple > Complex | Evidence > Assumptions"
---

# Python Functional Programming

Core functional programming principles for Python with anti-over-engineering enforcement. Python is a multi-paradigm language with solid FP support — but it's not Haskell. This skill teaches you to be functional in spirit, Pythonic in expression.

## When to Use This Skill

- Implementing pure, testable Python functions
- Data transformation pipelines (pandas, polars, ML preprocessing)
- Need FP architectural guidance for Python
- Preventing over-engineering and custom FP utility creation
- Comprehensive testing strategies with pytest
- Evidence-based performance optimization

## CRITICAL: Anti-Over-Engineering (PRIMARY FOCUS)

**Core Principle**: "Simple > Complex | Evidence > Assumptions"

> **Clarification**: This skill prevents CREATING custom FP utility functions (pipe, compose, curry, monads) to make Python "feel" like Haskell. Using established libraries (toolz, pandas, itertools, etc.) is perfectly fine. FP is a mindset — pure functions, immutability, composition — not a rigid API signature.

### Don't Create Custom FP Utilities

```python
# DON'T CREATE: pipe() utility
def pipe(value, *functions):
    for fn in functions:
        value = fn(value)
    return value

# INSTEAD: Native function calls with early returns
def validate_user(user_data: dict) -> dict:
    required_check = validate_required(["email", "name"], user_data)
    if not required_check["valid"]:
        return required_check

    email_check = validate_email(user_data)
    if not email_check["valid"]:
        return email_check

    return validate_name_length(user_data)

# DON'T CREATE: compose() utility
def compose(*fns):
    def composed(x):
        for fn in reversed(fns):
            x = fn(x)
        return x
    return composed

# INSTEAD: Direct function calls
def process_data(raw: dict) -> dict:
    normalized = normalize(raw)
    validated = validate(normalized)
    return transform(validated)

# DON'T CREATE: curry() utility
# INSTEAD: functools.partial or closures
from functools import partial

validate_min_length = partial(validate_length, min_len=3)

# Or closures for more complex cases
def create_validator(rules: list) -> callable:
    def validate(value):
        errors = [r["message"] for r in rules if not r["check"](value)]
        return {"valid": True} if not errors else {"valid": False, "errors": errors}
    return validate

# DON'T CREATE: Custom monads (Maybe, Either, IO)
# INSTEAD: Native error handling with result dicts
def get_user(user_id: int, db) -> dict:
    try:
        user = db.find(user_id)
        return {"success": True, "data": user}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### Context-Appropriate Complexity

```python
# CLI Script: Simple and direct
def process_file(file_path: str) -> list[str]:
    with open(file_path) as f:
        return [line.upper() for line in f if line.strip()]

# Production Service: Appropriate error handling
def process_file(file_path: str, logger) -> dict:
    try:
        with open(file_path) as f:
            lines = [line.strip() for line in f if line.strip()]
        logger.info("File processed", extra={"path": file_path, "lines": len(lines)})
        return {"success": True, "data": [line.upper() for line in lines]}
    except OSError as e:
        logger.error("File processing failed", extra={"path": file_path, "error": str(e)})
        return {"success": False, "error": str(e)}

# Data Pipeline: Composable transformations
def create_file_processor(transforms: list[callable]):
    compiled = [compile_transform(t) for t in transforms]

    def process(file_path: str, logger) -> dict:
        with open(file_path) as f:
            data = f.read()
        for transform in compiled:
            data = transform(data)
        return {"success": True, "data": data}

    return process
```

## Core FP Patterns (Error-Preventing Essentials)

### 1. Purity and Side Effect Isolation

**Rule**: Separate business logic from side effects.

```python
# IMPURE - side effects mixed with logic
def calculate_total(items: list[dict]) -> float:
    print("Processing items")  # Side effect
    global running_total
    running_total += sum(i["price"] for i in items)  # Mutation
    return running_total

# PURE: business logic
def calculate_total(items: list[dict]) -> float:
    return sum(item["price"] for item in items)

# ISOLATED: side effects separate
def log_and_calculate(items: list[dict], logger) -> float:
    total = calculate_total(items)  # Pure calculation
    logger.info(f"Total: {total}")  # Side effect isolated
    return total
```

**Benefits**:
- 100% testable with all edge cases
- Predictable behavior and debugging
- Safe for `multiprocessing` (pure functions serialize trivially)
- Enables memoization via `@lru_cache`

### 2. Composition Over Inheritance

**Rule**: Build complex behavior from simple functions.

```python
# Class hierarchy approach (avoid)
class BaseValidator:
    def validate(self, value): raise NotImplementedError

class EmailValidator(BaseValidator):
    def validate(self, value): ...

# Function composition (no utilities needed)
def validate_required(value) -> bool:
    return value is not None and value != ""

def validate_email(value: str) -> bool:
    return "@" in value and "." in value.split("@")[-1]

def validate_length(min_len: int, max_len: int):
    return lambda value: min_len <= len(value) <= max_len

# Simple composition without pipe() utility
def validate_user_email(email: str) -> dict:
    if not validate_required(email):
        return {"valid": False, "error": "Required"}
    if not validate_email(email):
        return {"valid": False, "error": "Invalid email"}
    if not validate_length(5, 100)(email):
        return {"valid": False, "error": "Length"}
    return {"valid": True}
```

### 3. Dependency Injection Through Parameters

**Rule**: Pass dependencies explicitly, avoid global state.

```python
# Hidden dependencies, hard to test
def save_user(user_data: dict) -> dict:
    hashed = bcrypt.hash(user_data["password"])  # Hidden
    return database.save({**user_data, "password": hashed})  # Hidden

# Explicit dependencies, fully testable
def save_user(user_data: dict, hasher, database) -> dict:
    hashed = hasher.hash(user_data["password"])
    return database.save({**user_data, "password": hashed})

# Factory for repeated use (closure-based DI)
def create_user_service(hasher, database):
    def save(user_data: dict) -> dict:
        return save_user(user_data, hasher, database)

    def find(user_id: int) -> dict:
        return database.find_by_id(user_id)

    return {"save": save, "find": find}
```

### 4. Immutability Patterns

**Rule**: Don't mutate input data. Create new structures.

```python
from dataclasses import dataclass, replace, field
from typing import NamedTuple

# Frozen dataclasses — the primary immutable record
@dataclass(frozen=True)
class User:
    name: str
    email: str
    settings: dict = field(default_factory=dict)

# "Update" via replace() — returns new instance
def update_email(user: User, new_email: str) -> User:
    return replace(user, email=new_email)

# NamedTuple — lighter weight alternative
class Point(NamedTuple):
    x: float
    y: float

def translate(point: Point, dx: float, dy: float) -> Point:
    return Point(point.x + dx, point.y + dy)

# Dict immutability — spread with {**d}
def update_settings(user: dict, settings: dict) -> dict:
    return {**user, "settings": {**user.get("settings", {}), **settings}}

# List operations without mutation
def add_item(items: list, new_item) -> list:
    return [*items, new_item]

def remove_item(items: list[dict], item_id: int) -> list[dict]:
    return [i for i in items if i["id"] != item_id]

def update_item(items: list[dict], item_id: int, updates: dict) -> list[dict]:
    return [{**i, **updates} if i["id"] == item_id else i for i in items]
```

> **Important**: `frozen=True` is shallow — it prevents attribute reassignment but doesn't freeze mutable attribute values (like dicts or lists inside). For deep immutability, use `pyrsistent` or keep nested values as tuples/frozensets.

## Python-Specific Patterns

### Comprehensions Over map/filter (Pythonic FP)

```python
# map/filter style (less Pythonic)
active_names = list(map(
    lambda u: u["name"],
    filter(lambda u: u["active"], users)
))

# Comprehension style (Pythonic FP)
active_names = [u["name"] for u in users if u["active"]]

# Dict comprehension for transformations
name_by_id = {u["id"]: u["name"] for u in users}

# Generator expression for lazy evaluation (large data)
totals = sum(item["price"] for item in items if item["taxable"])
```

### Generators for Lazy Pipelines

```python
# Generators are Python's answer to lazy evaluation
def read_records(path: str):
    with open(path) as f:
        for line in f:
            yield parse_record(line)

def filter_valid(records):
    for record in records:
        if record["status"] == "active":
            yield record

def transform(records):
    for record in records:
        yield {**record, "name": record["name"].upper()}

# Compose lazily — no intermediate lists
pipeline = transform(filter_valid(read_records("data.csv")))
results = list(pipeline)  # Materializes only when needed
```

### itertools and functools (The FP Standard Library)

```python
from functools import partial, lru_cache, reduce
from itertools import chain, groupby, islice, takewhile
from operator import itemgetter

# partial — the Pythonic way to "curry"
multiply_by_tax = partial(lambda rate, price: price * (1 + rate), 0.08)

# lru_cache — memoize pure functions (MUST be pure!)
@lru_cache(maxsize=256)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# operator module — eliminate trivial lambdas
from operator import itemgetter, attrgetter

sorted_by_name = sorted(users, key=itemgetter("name"))
# vs: sorted(users, key=lambda u: u["name"])

# itertools for complex transformations
from itertools import groupby

def group_by_category(items: list[dict]) -> dict:
    sorted_items = sorted(items, key=itemgetter("category"))
    return {
        k: list(v)
        for k, v in groupby(sorted_items, key=itemgetter("category"))
    }
```

### Pattern Matching (Python 3.10+)

```python
# Structural pattern matching for clean dispatch
def process_event(event: dict) -> dict:
    match event:
        case {"type": "click", "target": target}:
            return handle_click(target)
        case {"type": "submit", "data": data}:
            return handle_submit(data)
        case {"type": "error", "code": code, "message": msg}:
            return handle_error(code, msg)
        case _:
            return {"error": f"Unknown event type: {event.get('type')}"}

# Pattern matching with guards
def categorize_score(score: int) -> str:
    match score:
        case n if n >= 90: return "A"
        case n if n >= 80: return "B"
        case n if n >= 70: return "C"
        case _: return "F"
```

### Type Hints for FP Clarity

```python
from typing import TypeVar, Callable, Optional
from collections.abc import Iterable, Iterator

T = TypeVar("T")
U = TypeVar("U")

# Type hints make pure function contracts explicit
def transform_all(items: Iterable[T], fn: Callable[[T], U]) -> list[U]:
    return [fn(item) for item in items]

# Union types (3.10+) for result patterns
def divide(a: float, b: float) -> dict:
    if b == 0:
        return {"success": False, "error": "Division by zero"}
    return {"success": True, "data": a / b}

# Optional signals nullable return
def find_user(users: list[dict], user_id: int) -> Optional[dict]:
    return next((u for u in users if u["id"] == user_id), None)
```

## Data Science / ML Patterns

### pandas pipe() for Transformation Chains

```python
import pandas as pd

# Each function: DataFrame in, DataFrame out (pure transforms)
def clean_nulls(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(subset=["email", "name"])

def normalize_names(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(name=df["name"].str.strip().str.title())

def add_age_group(df: pd.DataFrame) -> pd.DataFrame:
    bins = [0, 18, 35, 55, 120]
    labels = ["youth", "young_adult", "adult", "senior"]
    return df.assign(age_group=pd.cut(df["age"], bins=bins, labels=labels))

# Compose via pipe() — FP pipeline, Pythonic syntax
result = (
    raw_df
    .pipe(clean_nulls)
    .pipe(normalize_names)
    .pipe(add_age_group)
)
```

### Pure Feature Engineering

```python
# Pure transformation functions for ML pipelines
def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(
        word_count=df["text"].str.split().str.len(),
        has_url=df["text"].str.contains(r"https?://", regex=True),
        text_length=df["text"].str.len(),
    )

# scikit-learn FunctionTransformer for pipeline integration
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline

feature_extractor = FunctionTransformer(extract_features)

pipeline = Pipeline([
    ("features", feature_extractor),
    ("scaler", StandardScaler()),
    ("model", LogisticRegression()),
])
```

### Polars (FP-Friendly Alternative to pandas)

```python
import polars as pl

# Polars expressions are lazy and composable by design
result = (
    pl.scan_csv("data.csv")  # Lazy — nothing runs yet
    .filter(pl.col("status") == "active")
    .with_columns(
        full_name=pl.col("first_name") + " " + pl.col("last_name"),
        age_group=pl.when(pl.col("age") < 30).then(pl.lit("young"))
                    .otherwise(pl.lit("senior")),
    )
    .group_by("department")
    .agg(pl.col("salary").mean().alias("avg_salary"))
    .collect()  # Execute the entire plan at once
)
```

## Result Type Pattern

```python
# Standard result shape — consistent across the codebase
def success(data=None) -> dict:
    return {"success": True, "data": data}

def failure(error: str) -> dict:
    return {"success": False, "error": error}

# Chain results with early return
def process_order(order: dict) -> dict:
    validated = validate_order(order)
    if not validated["success"]:
        return validated

    priced = calculate_pricing(validated["data"])
    if not priced["success"]:
        return priced

    return submit_order(priced["data"])
```

## Testing Essentials (Enabled by Purity)

**Philosophy**: Pure functions enable testing all edge cases systematically.

```python
import pytest

# Parametrized testing — the FP way
@pytest.mark.parametrize("price,rate,expected", [
    (100.0, 0.1, 10.0),
    (50.0, 0.2, 10.0),
    (0.0, 0.1, 0.0),
    (100.0, 0.0, 0.0),
])
def test_calculate_discount(price, rate, expected):
    assert calculate_discount(price, rate) == expected

# Edge case testing — pure functions handle all inputs
@pytest.mark.parametrize("invalid_input", [None, "", [], {}, 0])
def test_validate_required_rejects_invalid(invalid_input):
    assert not validate_required(invalid_input)

# Testing result chains
def test_process_order_validation_failure():
    result = process_order({"items": []})
    assert not result["success"]
    assert "empty" in result["error"].lower()

# Frozen dataclass testability
def test_update_email_returns_new_instance():
    user = User(name="Alice", email="old@test.com")
    updated = update_email(user, "new@test.com")
    assert updated.email == "new@test.com"
    assert user.email == "old@test.com"  # Original unchanged
```

## Performance Patterns (Evidence-Based)

**IMPORTANT**: Optimize only when needed with evidence.

### Memoization for Expensive Pure Functions

```python
from functools import lru_cache

# ONLY memoize pure functions with hashable arguments
@lru_cache(maxsize=128)
def parse_template(template: str) -> dict:
    # Expensive parsing — cached after first call
    return heavy_parse(template)

# For unhashable args, manually cache
_cache = {}
def get_config(key: str) -> dict:
    if key not in _cache:
        _cache[key] = load_config(key)
    return _cache[key]
```

### Generator Pipelines for Large Data

```python
# Memory-efficient: processes one record at a time
def process_large_file(path: str):
    records = read_records(path)       # Generator
    valid = filter_valid(records)       # Generator
    transformed = transform(valid)      # Generator

    # Only materializes in batches
    batch = []
    for record in transformed:
        batch.append(record)
        if len(batch) >= 1000:
            yield batch
            batch = []
    if batch:
        yield batch
```

### multiprocessing with Pure Functions

```python
from multiprocessing import Pool

# Pure functions parallelize trivially
def process_item(item: dict) -> dict:
    return {**item, "score": compute_score(item)}

# No shared state, no locks, no bugs
with Pool(4) as pool:
    results = pool.map(process_item, items)
```

## Python-Specific Gotchas

### Recursion Limit

```python
# Python has a 1000-call recursion limit. No tail call optimization.
# DON'T: recursive algorithms for large inputs
def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)  # Blows up at n > 1000

# DO: iterative or reduce
from functools import reduce
from operator import mul

def factorial(n: int) -> int:
    return reduce(mul, range(1, n + 1), 1)
```

### Mutable Default Arguments

```python
# NEVER use mutable defaults
def add_item(item, items=[]):  # BUG: shared mutable default
    items.append(item)
    return items

# INSTEAD: None sentinel
def add_item(item, items=None):
    items = items if items is not None else []
    return [*items, item]  # Return new list, don't mutate
```

### Shallow vs Deep Copy

```python
# frozen=True is SHALLOW
@dataclass(frozen=True)
class Config:
    settings: dict  # This dict is still mutable!

config = Config(settings={"debug": True})
# config.settings = {}  # FrozenInstanceError
config.settings["debug"] = False  # This WORKS — shallow freeze

# For deep immutability: use tuples, frozensets, or pyrsistent
from types import MappingProxyType

def freeze_dict(d: dict):
    return MappingProxyType(d)  # Read-only view
```

## Quality Gates (Pre-Implementation Checklist)

1. **"Can this be pure?"** - Separate business logic from side effects
2. **"Can this use native patterns?"** - Comprehensions, generators, functools, itertools
3. **"Can this be simplified?"** - Choose simple solution over complex abstraction
4. **"Is this complexity justified?"** - Evidence-based complexity decisions
5. **"Is this testable?"** - Pure functions enable comprehensive testing
6. **"Are type hints used?"** - Type hints on all public function signatures

## When to Load Reference Files

### Deep Principles and Explanations
**File**: `references/core-principles.md`
**Load when**:
- Learning mode or explaining WHY behind patterns
- Making architectural decisions
- Need complete Result Type patterns
- Anti-pattern recognition details
- Python-specific FP philosophy deep-dive

### Testing Methodology
**File**: `references/testing-patterns.md`
**Load when**:
- Building comprehensive test suites with pytest
- Improving test coverage
- Edge case analysis and boundary testing
- Testing data pipelines and ML code
- Property-based testing with Hypothesis

### Working Examples
**Directory**: `examples/`
**Load when**:
- Need complete working code
- Integration examples
- Learning implementation patterns

## Integration with Domain Skills

This core skill provides the foundation for:

- **py-fp-django**: Django patterns with FP principles (future)
- **py-fp-fastapi**: FastAPI patterns with FP principles (future)
- **py-fp-ml**: ML/data science patterns with FP principles (future)

Each domain skill references this core and adds domain-specific patterns.

## Philosophy

*"Pure functions, Pythonic patterns, type hints, appropriate complexity, and comprehensive testing for maintainable, predictable code. Be functional in spirit, Pythonic in expression — don't fight the language, work with it."*
