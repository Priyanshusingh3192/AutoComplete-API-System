# AutoComplete-API-System
Autocomplete API Scraper - Detailed Documentation


**1. Systematic Approach to Discovering API Behavior**
To understand how the API functions, I used a systematic and exploratory approach:

**Step 1: Initial API Testing**
I started by querying the API with an empty prefix ("") to see how it responds and after that i queried diff prefixes like - "a", "aa", "aab", "abc" etc.

I Observed that the API returns a maximum of 10 results per query.

I Noted that if fewer than 10 names are returned, no further names exist with that prefix.

**Step 2: Incremental Prefix Expansion**
Since the API supports prefix-based search, I designed a **recursive function** that extends prefixes only when necessary.

If an API query returns exactly 10 results, it suggests that there may be more names under that prefix, so further exploration is required and for further I used Recursive Approach.

Step 3: Understanding API Constraints
The API enforces rate limiting (429 Too Many Requests).

Some names returned do not strictly match the requested prefix, requiring additional filtering.

API responses need proper error handling to avoid crashes due to JSON parsing issues.

**2. Handling Various Constraints and Limitations**
Rate Limiting and Exponential Backoff
If the API returns a 429 error, I implemented an exponential backoff strategy:

First retry: Wait base delay (0.5s) before retrying.

Subsequent retries: Wait double the previous delay (e.g., 1s → 2s → 4s) to reduce request frequency.

This helps avoid API blocking while maximizing efficiency.

Error Handling for Robust Execution
JSON Parsing Errors:

If the response is not properly formatted, an exception is caught, and the script logs the error instead of crashing.

Unexpected HTTP Errors:

If the API returns any status code other than 200 or 429, an error message is displayed, and the prefix is skipped.

Limiting Recursion Depth
To prevent excessive API calls, I set a max recursion depth of 20.

This ensures the script terminates in a reasonable time while still discovering a significant number of names.

Efficient Storage and Duplicate Handling
Used a set (found_names) to store unique names, ensuring duplicates are ignored.

This prevents unnecessary processing and saves memory.

**3. Code Quality and Efficiency**
Optimized Recursive Search
The recursive function only expands a prefix when necessary, minimizing API calls.

The depth-first approach ensures that deeper prefixes are only explored if required.

Avoiding Redundant Queries
If an API request for a prefix returns less than 10 names, that branch of the search tree is pruned to prevent further exploration.

This significantly reduces unnecessary API calls.

Readable and Modular Code
Functions are well-structured (query_api() for API handling, search() for recursion).

Clear logging of discovered names and request counts for tracking progress.

Proper use of global variables (total_requests, found_names) to maintain efficiency.

**4. Problem-Solving Process**

**Step 1:** Identifying the Core Problem
The challenge was to retrieve all unique names from the API while handling rate limits and unknown constraints.

**Step 2:** Designing a Recursive Solution
Instead of brute-force querying, I designed a recursive prefix-based approach to efficiently explore possible name variations.

The trie-like traversal structure ensures optimal coverage without redundant queries.

**Step 3:** Implementing and Testing
Initially implemented a simple API query and analyzed response behavior.

Added recursion for prefix expansion, ensuring efficient discovery.

Implemented rate limit handling to avoid excessive failures.

Tested with different prefix lengths to fine-tune the depth limit.

**Step 4:** Refinements and Optimizations
Added **exponential backoff** to improve stability.

Pruned unnecessary searches when fewer than 10 results were returned.
