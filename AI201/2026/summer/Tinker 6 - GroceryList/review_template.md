# Code Review Notes

Fill this in as you work through the milestones. Each section mirrors the structure of a real GitHub pull request review.

---

## PR #1 — Bulk Purchase (`pr1_bulk_purchase.py`)

### Summary
*What does this PR do? (1–2 sentences in your own words)*

> This PR adds a bulk purchase endpoint (`POST /lists/<list_id>/purchase-all`) that allows a user to mark all items on a specific grocery list as purchased in a single operation. 

### Issues

For each issue you find, note: where it is (file + function), what's wrong, and why it matters in production.

**Issue 1**
- Location: `prs/pr1_bulk_purchase.py` — `purchase_all_items()`
- What's wrong: The function iterates over all items in the list and marks them as purchased, overwriting the `purchased_by` and `purchased_at` values even if the item was already purchased by someone else prior to this call.
- Why it matters: In a production app with shared lists, this will corrupt historical shopping data. If User A purchased Milk yesterday, and User B runs a bulk purchase on the remaining items today, User A's contribution gets overwritten as if User B bought it today.
- Suggested fix: Check if `item.is_purchased` is already true, and only update items that haven't been purchased yet:
  ```python
  for item in items:
      if not item.is_purchased:
          item.is_purchased = True
          item.purchased_by = user_id
          item.purchased_at = datetime.now(timezone.utc)
  ```

**Issue 2**
- Location: `prs/pr1_bulk_purchase.py` — `purchase_all()` (route function)
- What's wrong: The route retrieves `user_id` from the request JSON but does not check if it is missing or empty. If a client sends an empty JSON payload `{}` or omits `user_id`, the function accepts it and calls `purchase_all_items` with `user_id = None`.
- Why it matters: This puts the database into an invalid state where items are marked as `is_purchased = True` but their `purchased_by` is set to `null` (since the database column is nullable).
- Suggested fix: Add a validation check in the route handler to verify that `user_id` is provided in the request body, returning a 400 Bad Request if it's missing:
  ```python
  if not user_id:
      return jsonify({"error": "Missing required field: user_id"}), 400
  ```

**Issue 3**
- Location: `prs/pr1_bulk_purchase.py` — `purchase_all()` and `purchase_all_items()`
- What's wrong: The code does not check if the `list_id` actually exists in the database. If a nonexistent `list_id` is requested, it silently returns `{"purchased": 0}` with a `200 OK` status, rather than returning a `404 Not Found` error.
- Why it matters: This can cause clients to believe a bulk purchase succeeded on a list that does not exist, leading to confusing behavior and hiding potential routing or client-side bugs.
- Suggested fix: Query for the list first and raise a `ValueError` or return a `404` error if it doesn't exist, matching the behavior of the other routes:
  ```python
  list_exists = GroceryList.query.get(list_id)
  if not list_exists:
      return jsonify({"error": f"List '{list_id}' not found"}), 404
  ```

### Questions for the Author
*Things you're uncertain about — design choices that could be intentional or bugs depending on intent.*

> 1. Was it intentional to allow already-purchased items to have their purchaser history overwritten during a bulk purchase? 
> 2. Should we validate that the `user_id` corresponds to a real user in the database before updating the records?

### Verdict
- [ ] Approve — ship it
- [x] Request Changes — needs fixes before merging
- [ ] Comment — needs discussion before a verdict

**Rationale** *(1–2 sentences)*:
> The PR currently corrupts historical data by overwriting already-purchased items' buyer info, and it lacks request validation, which allows items to be marked as purchased with a `null` purchaser ID. These issues must be fixed before merging to production.

---

## PR #2 — List Stats (`pr2_list_stats.py`)

### Summary
*What does this PR do? (1–2 sentences in your own words)*

> This PR adds a list statistics endpoint (`GET /lists/<list_id>/stats`) to summarize the total, purchased, and remaining items on a grocery list, along with a category-wise item count breakdown for active shopping.

### Issues

**Issue 1**
- Location: `prs/pr2_list_stats.py` — `get_list_stats()`
- What's wrong: The function queries the database for items belonging to `list_id` without verifying if the list itself actually exists in the `GroceryList` table.
- Why it matters: If a client calls this endpoint with a nonexistent list ID, the server returns a `200 OK` with all counts set to 0. This is inconsistent with other routes in the app (like `GET /lists/<list_id>/items`), which correctly return a `404 Not Found` for invalid lists.
- Suggested fix: Verify the list's existence by fetching it first, raising a `ValueError` if it's missing (which the route handler will convert to a `404`):
  ```python
  grocery_list = db.session.get(GroceryList, list_id)
  if not grocery_list:
      raise ValueError(f"List {list_id!r} not found")
  ```

**Issue 2**
- Location: `prs/pr2_list_stats.py` — `get_list_stats()`
- What's wrong: The `by_category` dictionary counts all items in the list, including those that have already been purchased. This contradicts the frontend request, which asked for a breakdown of "what's left" (remaining items) by category.
- Why it matters: In production, the active shopping view will show categories and counts for items that are already purchased and marked done, confusing the shopper and cluttering the navigation view.
- Suggested fix: Only increment the category count if the item is not yet purchased:
  ```python
  by_category = {}
  for item in items:
      if not item.is_purchased:
          cat = item.category or "uncategorized"
          by_category[cat] = by_category.get(cat, 0) + 1
  ```

### Questions for the Author
*A good code review often surfaces design questions, not just bugs. What would you want to clarify before approving?*

> 1. Did the frontend team specify if they wanted the category breakdown to include all items on the list, or only the remaining (unpurchased) ones? (The request says "what's left by category").
> 2. Should we align this endpoint's error response with the standard `GET /lists/<list_id>/items` behavior by raising a `404 Not Found` when the list ID doesn't exist?

### Verdict
- [ ] Approve — ship it
- [x] Request Changes — needs fixes before merging
- [ ] Comment — needs discussion before a verdict

**Rationale** *(1–2 sentences)*:
> The PR fails to return a 404 error for invalid lists, and the category breakdown incorrectly includes already purchased items, which does not match the frontend's functional request.

---

## Reflection

*Answer after completing both reviews.*

**1.** Which issue was hardest to spot, and why?

>

**2.** Which issues do you think an LLM reviewer (like Claude reviewing its own code) would most likely miss? Why?

>

**3.** One thing you'd add to a code review checklist for AI-generated backend code:

>
