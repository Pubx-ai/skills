# Examples

## A complete requirements document

This is the level of specificity to aim for — every field is concrete enough that an
implementer wouldn't have to guess.

```text
DESCRIPTION:
Persistent shopping cart for add/remove/manage products before checkout. Persists across
sessions and syncs across devices for authenticated users.

USER STORY:
As a shopper, I want to add products to a cart so I can review before purchasing.
As a returning customer, I want cart persistence so I don't lose selections.
As a multi-device user, I want cart sync so I can start on mobile and finish on desktop.

ACCEPTANCE CRITERIA:
- Add products with quantity (1-99)
- Display: name, image, price, quantity, subtotal
- Update quantities or remove items
- Show total count in header
- Persist in localStorage (guests)
- Sync to database (authenticated)
- Auto-sync on login (merge carts)
- Empty state with CTA
- Optimistic UI updates
- Stock availability warnings

KEY DECISIONS:
- Guest carts: localStorage only, or DB-backed anonymous carts? → localStorage only (user-confirmed)
- On login with items in both carts: merge or replace? → merge, summing quantities up to stock (user-confirmed)
- Cart state: extend existing Zustand store or new store? → new `src/stores/cart.ts` following `userPreferences.ts` pattern (user-confirmed)

TECHNICAL CONTEXT:
- Tech Stack: Next.js 14.2, React 18.2, TypeScript 5.4
- Existing Systems: Product API `/api/products`, NextAuth.js 4.24, Checkout `/checkout`
- Database: PostgreSQL 15, Prisma 5.8
- Authentication: NextAuth.js, JWT sessions
- Styling: Tailwind CSS 3.4, shadcn/ui
- State Management: Zustand 4.5

CONSTRAINTS:
- Performance: Cart ops < 100ms, icon update < 50ms
- Security: Server-side validation, prevent price/quantity manipulation
- Accessibility: WCAG 2.1 AA, keyboard nav, screen reader
- Browser Support: Chrome 90+, Safari 14+, Firefox 88+, mobile responsive
- SEO: Cart page noindex

TESTING REQUIREMENTS:
- Test Coverage: 80% minimum for cart logic
- Testing Tools: Jest, React Testing Library, Playwright
- Critical Scenarios: Add/remove/update, persistence, sync on auth, stock validation, concurrent updates
- Testing Patterns: Follow `__tests__/components/`, `e2e/flows/`

SCOPE:
- MVP: Add to cart, view cart, update quantities, remove items, persistence (localStorage + DB), auth sync, stock validation
- Future: Save for later, cart sharing, recently removed, recommendations, bulk actions
- Out of Scope: Wishlist, price calculations (checkout), discounts (checkout)

INTEGRATION POINTS:
- Components: `src/components/ui/Button.tsx`, `Badge.tsx`, `ProductCard.tsx`, `layouts/Header.tsx`
- APIs: GET `/api/products/:id`, GET/POST `/api/cart`, PATCH/DELETE `/api/cart/items/:id`, POST `/api/cart/sync`
- Models: Extend `prisma/schema.prisma`, use `src/types/product.ts`, create `src/types/cart.ts`
- Utilities: `src/lib/api-client.ts`, `src/lib/storage.ts`, `src/hooks/useAuth.ts`

ASSUMPTIONS & OPEN QUESTIONS:
- Assumptions: Guest carts live only in localStorage until login; max 50 line items.
- Open Questions: Should an out-of-stock item block checkout or just warn?

ADDITIONAL CONTEXT:
- Design: https://figma.com/file/abc123
- Docs: `/docs/api-patterns.md`, `/docs/state-management.md`
- References: `src/stores/userPreferences.ts`, `src/hooks/useWishlist.ts`
```

## An under-specified request (what to avoid handing off)

```text
Add a shopping cart to the site. Users should be able to add products and checkout.
Make it fast and secure.
```

Why it isn't ready: no user stories or acceptance criteria, no technical stack, vague
constraints ("fast and secure" aren't measurable), no integration details, no testing
requirements, no scope boundaries, and no business context. A request like this is the
*input* to this skill — the job is to close those gaps and turn it into the document above.
