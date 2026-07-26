# Example: a fully specified task file

This is one file from a plan directory — `docs/plans/shopping-cart/tasks/02-cart-store.md`
— at the level of specificity to aim for. Note what makes it executable by an
agent that has read only `plan.md` and this file: exact paths, an Interfaces
block that spells out neighbouring tasks' contracts, TDD steps with exact
commands and expected output, boundary values spelled out, and acceptance
criteria that map one-to-one onto unit tests.

~~~text
# Task 2: Implement Cart Zustand Store

**Objective:** Create Zustand store for global cart state with add/remove/update
operations and localStorage persistence for guests.

**Files to Create/Modify:**
- `src/types/cart.ts` - Cart types
- `src/stores/cartStore.ts` - Store with actions/state
- `src/stores/cartStore.test.ts` - Unit tests

**Dependencies:**
- Prerequisites: Task 1 (product types)
- Libraries: `zustand@4.5.0`, `immer@10.0.3`

**Interfaces:**
- Consumes: `Product` from `src/types/product.ts` (created in Task 1):
  `{ id: string; name: string; price: number; imageUrl: string }`
- Produces (Tasks 3–5 import these names verbatim):
  - `CartItem`, `CartState` from `src/types/cart.ts`
  - `useCartStore` hook from `src/stores/cartStore.ts` exposing state
    `{ items: CartItem[]; totalItems: number; totalPrice: number }` and actions
    `addItem(item: CartItem): void`, `removeItem(productId: string): void`,
    `updateQuantity(productId: string, quantity: number): void`,
    `clearCart(): void`

**Implementation Steps:**

- [ ] *Step 1: Define types*

```typescript
// src/types/cart.ts
export interface CartItem {
  productId: string;
  quantity: number;
  price: number;
  name: string;
  imageUrl: string;
}

export interface CartState {
  items: CartItem[];
  totalItems: number;
  totalPrice: number;
}
```

- [ ] *Step 2: Write the failing tests*

`src/stores/cartStore.test.ts`, mocking localStorage. Scenarios:
- `addItem` with a new product appends; with an existing productId increments
  its quantity
- `removeItem` removes exactly the matching productId
- `updateQuantity` accepts 1–99, removes the item at 0, rejects -1 and 100
- `totalItems` / `totalPrice` recomputed after every mutation
- 51st distinct item is rejected (max 50)
- state persists under localStorage key `shopping-cart`

- [ ] *Step 3: Run the tests, verify they fail*

Run: `npx vitest run src/stores/cartStore.test.ts`
Expected: FAIL — "useCartStore is not defined" (or module not found)

- [ ] *Step 4: Implement the store*

- Use `create` with the `persist` middleware, localStorage key `shopping-cart`
- Actions: `addItem`, `removeItem`, `updateQuantity`, `clearCart`
- `addItem`: check existence by productId, increment or append; max 50 items
- `updateQuantity`: validate 1–99, remove item at 0
- Compute `totalItems`, `totalPrice` on every change
- Use Immer for immutable updates
- Handle localStorage quota-exceeded with try-catch and in-memory fallback
- Follow the store pattern in `src/stores/userPreferences.ts` (lines 1–45)

- [ ] *Step 5: Run the tests, verify they pass*

Run: `npx vitest run src/stores/cartStore.test.ts`
Expected: PASS, all scenarios green

- [ ] *Step 6: Commit*

```bash
git add src/types/cart.ts src/stores/cartStore.ts src/stores/cartStore.test.ts
git commit -m "feat(cart): add cart store with localStorage persistence"
```

**Acceptance Criteria:**
- [ ] `useCartStore` exports with the types listed under Produces
- [ ] `addItem()` adds new items and increments existing ones
- [ ] `removeItem()` removes by productId
- [ ] `updateQuantity()` validates 1-99, removes at 0
- [ ] `totalItems`/`totalPrice` calculated correctly
- [ ] Persists under key `shopping-cart`
- [ ] Max 50 items enforced
- [ ] Immutable updates maintained

**Code References:**
- Store pattern: `src/stores/userPreferences.ts` (lines 1-45)
- Immer usage: `src/stores/wishlistStore.ts`
- localStorage helpers: `src/lib/storage.ts`

**Potential Issues:**
- localStorage quota exceeded → try-catch, notify user, in-memory fallback
- Race conditions between tabs → storage event listener (handled in Task 6)
- Price changes after add → store price at add time, mark stale (Task 8)
- Boundary validation (0, 1, 99, 100) → explicit checks + explicit tests
~~~

## What to avoid

A task like this forces the executing agent to guess everything that matters:

~~~text
# Task 2: Add cart state management

Set up state management for the cart. Make sure items can be added and removed
and the state persists. Write tests and handle errors appropriately.
~~~

No file paths, no named actions, no validation rules, no pattern to follow, no
boundary values, and "appropriately" is not a specification.

Placeholder-style steps are just as bad, even inside an otherwise detailed task:

~~~text
- [ ] *Step 3: Implement the store* — similar to the wishlist store in Task 4;
  add validation and error handling as appropriate. TODO: decide max items.
~~~

"Similar to Task 4" breaks self-containment (the executor never opens Task 4 —
repeat the content), "as appropriate" is not a specification, and a "TODO" means
the planning decision was pushed onto the executor.
