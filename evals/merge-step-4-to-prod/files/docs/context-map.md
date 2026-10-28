# Context map

- **assets** (master data): two farms, capacity, bidding zone, vendor aliases (C1).
- **market_prices**: keyed by bidding zone, not by farm (C2).
- **metering**, **forecast**: keyed by asset.
- **revenue_report** (downstream) reads the upstream services (C3).
- Shared kernel: DeliveryDay, units, AssetId, BiddingZone only (C4).

| Date | ID | Decision |
|---|---|---|
| 2026-09-04 | C1 | assets is a context, config file as storage |
| 2026-09-04 | C2 | prices keyed by bidding zone |
| 2026-09-04 | C3 | report reads services, not tables |
| 2026-09-04 | C4 | kernel holds value types only |
