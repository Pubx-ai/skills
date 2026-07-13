# AdCP rules — media buy & campaign semantics

Apply these when the diff maps internal campaign/inventory concepts onto AdCP tasks or
reports delivery data.

> Curated AdCP 3.x snapshot (last curated: 2026-07-12) — when you have web access, fetch the live sources and let
> them win on any conflict:
> https://docs.adcontextprotocol.org/docs/media-buy/task-reference/index.md

## Field semantics

- Mapping internal campaign or inventory concepts onto AdCP tasks must preserve the
  protocol's field semantics (budgets, dates, targeting, delivery status) — do not
  overload a protocol field with an internal meaning that differs from its spec
  definition.
- `budget` is a plain number in the currency implied by the selected
  `pricing_option_id`; do not attach ad-hoc currency fields.
- Flight dates are half-open `[start_time, end_time)` ISO 8601 with timezone. A buy
  ending "2026-05-01T00:00:00Z" does not serve on May 1.
- `update_media_buy` uses PATCH semantics — omitted fields are unchanged. Code that
  re-sends the full object and expects unset fields to clear values is wrong.

## Discovery → buy flow

- Product IDs are only guaranteed valid for the `get_products` response that returned
  them; sellers may rotate them per call. Buy flows should discover, then buy against
  fresh IDs — caching product IDs across sessions and buying against stale IDs yields
  `PRODUCT_NOT_FOUND`.

## Delivery reporting

- Metrics reported through AdCP (`get_media_buy_delivery`, `report_usage`) must be in
  the units and granularity the protocol defines, not internal conventions.
- Delivery/status data must come from the protocol surface, not inferred client-side
  from elapsed time or internal state.
