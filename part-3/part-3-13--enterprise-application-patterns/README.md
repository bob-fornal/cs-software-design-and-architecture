# 13. Enterprise Application Patterns

**Part 3 — Architectural Foundations** · [Back to curriculum index](../../README.md)

## One-sentence pitch
Underneath every architectural style and pattern sits a smaller vocabulary — DTOs, repositories, value objects, transaction scripts — that decides whether your domain logic stays testable and framework-independent or quietly rots into whatever ORM you happened to pick.

## Learning objectives
- Can explain what a DTO, repository, mapper, and identity map each do and why they exist as separate concerns.
- Can distinguish entities (identity-based equality) from value objects (attribute-based equality) and apply the distinction correctly when modeling a domain.
- Can implement a Repository that hides persistence details behind a domain-shaped interface, with DTOs as the only thing that crosses the API boundary.
- Can implement the same use case as both a Transaction Script and a Domain Model, and articulate when each is the better choice.
- Can explain the difference between commands (mutate, no return value expected) and queries (return data, no mutation) and why mixing them causes bugs.

## Session outline (~50 min)

| Segment | Time | Content |
|---|---|---|
| Hook: why not just use the ORM entity everywhere? | 4 min | Show a controller returning an ORM entity directly as JSON — then show what breaks: lazy-loading exceptions serialized to the client, internal fields leaking, a schema change breaking the API contract. Today's patterns exist to prevent exactly this. |
| Entities, value objects, domain models | 8 min | Entity: has identity that persists across state changes (two `Order`s with the same current attributes are still different orders if they have different IDs). Value object: defined entirely by its attributes, immutable, interchangeable if equal (`Money(10, "USD")`). Domain model: an object model where behavior lives with the data (contrast with the anemic model from topic 4). |
| Transaction Script vs. Domain Model | 8 min | Transaction Script: one procedure per business transaction, straight-line logic, minimal object structure — simple and fast for simple logic, but duplicates and tangles as rules grow. Domain Model: behavior distributed across a web of objects (entities/value objects) that collaborate — scales better with complexity, costs more upfront design effort. Give a concrete example: "apply a discount to an order" as five lines of procedural logic vs. an `Order.apply_discount()` method. |
| Repositories & the persistence boundary | 8 min | A Repository gives the illusion of an in-memory collection of domain objects, hiding SQL/ORM/API calls behind methods like `find_by_id`, `save`, `all`. Domain and application code depend on the repository interface, never on the database directly — this is dependency inversion applied specifically to persistence (ties back to topic 10). |
| DTOs and Mappers | 6 min | DTO (Data Transfer Object): a plain, serializable structure shaped for a specific boundary (an API response, a request payload) — no behavior, no identity semantics. Mapper: the (often boring, sometimes generated) code that converts between domain objects and DTOs. Rule of thumb: domain objects never get serialized directly; a DTO always sits at the edge. |
| Identity Map | 5 min | Ensures each object gets loaded only once per session/request — a lookup table keyed by identity, checked before hitting the database again. Prevents subtle bugs where two different in-memory copies of "the same" entity drift out of sync. Most ORMs (SQLAlchemy's session, Hibernate's session) implement this for you — worth naming explicitly so students recognize it. |
| Use cases, commands & queries | 6 min | A "use case" (or "application service") orchestrates one user-facing operation, coordinating repositories and domain objects without containing business rules itself. Command: an operation that changes state and typically returns nothing (or just an ID/status) — Query: an operation that reads and returns data without side effects. Keeping them separate (command-query separation, revisited from topic 1) makes code far easier to reason about and sets up CQRS from topic 12 naturally. |
| ORMs: what they buy you and what they cost | 3 min | Object-relational mapping automates the entity <-> table translation, but can encourage anemic models and leaking persistence concerns into domain code if used carelessly. The patterns above are largely about disciplined use of an ORM, not replacing one. |
| Wrap-up & homework framing | 2–4 min | Recap the boundary rule: domain objects stay inside, DTOs cross the line, repositories mediate persistence. Introduce the homework. |

## Homework notes

### 1. Repository + DTO in front of a data store
> Implement a Repository + DTO pattern in front of a simple data store (in-memory or SQLite): domain objects never leak past the repository boundary, and API responses use DTOs, not entities.

- **Goal:** Tests whether students can actually enforce a boundary in code, not just describe one — the repository interface and DTO mapping have to be real, checkable constraints, not documentation.
- **Approach / hints:** Pick a small domain (e.g., a `Book` or `Task`). Define a domain entity/value object with real identity and (if relevant) behavior. Define a `Repository` interface (`get`, `save`, `list`) implemented against your chosen store. Define a separate `BookDTO` (or similar) with only the fields an API consumer needs, and a mapper function converting entity to DTO. The constraint to enforce: nothing above the repository (controller/API layer) ever imports or returns the entity type directly.
- **Starter example:**
```python
from dataclasses import dataclass
from typing import Protocol

@dataclass
class Book:  # domain entity — has identity (isbn), may grow behavior later
    isbn: str
    title: str
    available: bool

@dataclass
class BookDTO:  # crosses the API boundary — no behavior, display-shaped
    isbn: str
    title: str
    available: bool

class BookRepository(Protocol):
    def get(self, isbn: str) -> Book | None: ...
    def save(self, book: Book) -> None: ...

def to_dto(book: Book) -> BookDTO:
    return BookDTO(isbn=book.isbn, title=book.title, available=book.available)

# TODO: implement an InMemoryBookRepository or SQLiteBookRepository,
# and an API/controller layer that only ever touches BookDTO.
```
- **Definition of done:** A repository implementation backed by an in-memory dict or SQLite, a DTO type with a mapper, and an API/controller layer where a code search confirms the entity type is never imported outside the repository and mapper.

### 2. Transaction Script vs. Domain Model comparison
> Compare Transaction Script vs. Domain Model for the same use case (e.g., "apply a discount to an order"): implement both, then write a short comparison of when each is the better choice.

- **Goal:** Tests whether students recognize that this is a genuine trade-off tied to complexity growth, not a "one is always better" question — and can back that judgment with a specific reason tied to the use case they built.
- **Approach / hints:** Implement the discount logic once as a Transaction Script: a single function taking an order and discount inputs, doing validation and calculation inline, straight-line. Implement it again as a Domain Model: an `Order` object with an `apply_discount(percent)` method that enforces its own invariants (e.g., can't go below zero, can't double-discount). Then imagine a follow-up requirement — "some customers get a different discount rule based on loyalty tier" — and note, without necessarily implementing it, which version absorbs that change more cleanly.
- **Starter example:**
```python
# Transaction Script
def apply_discount_script(order: dict, percent: float) -> dict:
    if not (0 <= percent <= 100):
        raise ValueError("invalid percent")
    order["total"] = order["total"] * (1 - percent / 100)
    return order

# Domain Model
class Order:
    def __init__(self, total: float):
        self._total = total

    def apply_discount(self, percent: float) -> None:
        if not (0 <= percent <= 100):
            raise ValueError("invalid percent")
        self._total *= (1 - percent / 100)

    @property
    def total(self) -> float:
        return self._total
```
- **Definition of done:** Two working implementations of the same discount logic (script and domain model), plus a short written comparison naming a concrete future requirement and which version handles it better, and why.

## Further resources
- Free companion: Martin Fowler, [P of EAA Catalog](https://martinfowler.com/eaaCatalog/)
