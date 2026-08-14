---
name: reusable-components
description: Identification, extraction, and design of shared utilities, domain services, UI components, adapters, and custom hooks without premature abstraction.
---

# Reusable Components Skill

## 1. When Should I Use This?

Use this skill when:
* Identifying repeated logic or copy-pasted blocks across multiple endpoints, models, views, or scripts.
* Deciding where a shared piece of functionality belongs (utility function, domain service, custom hook, base class, or adapter).
* Refactoring duplicate code to improve maintainability and consistency.
* Extracting UI component primitives in React/TypeScript.

Do NOT use this skill to create speculative, single-caller abstractions that add unnecessary indirection without clear value.

---

## 2. What Should I Inspect First?

1. **Occurrences & Variations**: How many call sites exist? Is the logic identical or are there slight domain-specific differences?
2. **Current Abstraction Locations**:
   * Python: Check `utils/`, `core/`, `services/base.py`, `common/`.
   * Frontend: Check `src/components/ui/`, `src/hooks/`, `src/lib/`.
3. **Coupling Risks**: Will extracting this component introduce tight coupling between otherwise independent feature domains?

---

## 3. What Workflow Should I Follow?

```text
Detect Repeated Behavior (Rule of Three)
                 ↓
Classify Component Role:
 ├── Pure Math / String / Formatting → Shared Utility (utils/)
 ├── Cross-cutting DB / Auth / Cache → Core Adapter (core/ / lib/)
 ├── Repeated Business Rules         → Domain Service (services/)
 └── Repeated Visual Element         → UI Component (components/ui/)
                 ↓
Design a Composable, Minimal Interface
                 ↓
Refactor Call Sites Sequentially
                 ↓
Verify All Callers via Unit Tests
```

### Component Classification Matrix

```text
┌────────────────────┬──────────────────────────────────────┬──────────────────────────────────┐
│ Component Type     │ Purpose                              │ Placement Location               │
├────────────────────┼──────────────────────────────────────┼──────────────────────────────────┤
│ Pure Utility       │ Deterministic transforms, formatting │ backend/app/utils/, frontend/lib │
│ Custom Hook        │ State + effect encapsulation         │ frontend/src/hooks/              │
│ UI Primitive       │ Visual presentation (Button, Modal)  │ frontend/src/components/ui/      │
│ Feature Component  │ Composed domain UI with context      │ frontend/src/features/<feat>/    │
│ Domain Service     │ Business entity orchestration        │ backend/app/services/            │
│ Adapter / Client   │ External SDK / Database wrapper      │ backend/app/core/ or adapters/   │
└────────────────────┴──────────────────────────────────────┴──────────────────────────────────┘
```

### Concrete Example: React UI Component Reusability Pattern

```typescript
// frontend/src/components/ui/status-badge.tsx
import React from 'react';
import { clsx } from 'clsx';

export type StatusType = 'success' | 'warning' | 'error' | 'info' | 'pending';

interface StatusBadgeProps {
  status: StatusType;
  label?: string;
  className?: string;
}

const statusStyles: Record<StatusType, string> = {
  success: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/20',
  warning: 'bg-amber-500/15 text-amber-400 border-amber-500/20',
  error:   'bg-rose-500/15 text-rose-400 border-rose-500/20',
  info:    'bg-sky-500/15 text-sky-400 border-sky-500/20',
  pending: 'bg-slate-500/15 text-slate-400 border-slate-500/20',
};

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, label, className }) => {
  return (
    <span
      className={clsx(
        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border',
        statusStyles[status],
        className
      )}
    >
      <span className="w-1.5 h-1.5 mr-1.5 rounded-full bg-current" />
      {label || status.toUpperCase()}
    </span>
  );
};
```

---

## 4. What Decisions Should I Make?

| Metric / Heuristic | Action |
| :--- | :--- |
| **Rule of Three** | If a block of code appears in 1 or 2 places, inline or keep local. When it appears in 3+ places with identical semantics, extract into a shared component. |
| **Parameter Bloat** | If a reusable component requires > 5 boolean flag props (`isUser`, `hasCustomHeader`, `skipValidation`), split it into distinct specialized components rather than creating a convoluted mega-component. |
| **Stateful vs Stateless** | Keep UI primitives stateless (`props` in, `JSX` out). Lift state management to container hooks or feature modules. |

---

## 5. What Should I Avoid?

* **NEVER create single-caller abstractions**: Do not invent base classes or helper functions that are used in only one file and obscure readability.
* **NEVER hardcode feature logic in generic UI primitives**: `Button` or `Modal` must never import authentication state or domain models.
* **NEVER copy-paste utility functions across files**: Consolidate `formatBytes`, `formatCurrency`, `dateUtils` into dedicated utility modules.

---

## 6. How Should I Verify Success?

```bash
# 1. Verify component isolation via unit tests
pytest tests/unit/test_utils.py
# Or frontend component testing
npm test src/components/ui/StatusBadge.test.tsx

# 2. Check that refactored callers build without type errors
npm run type-check # or mypy app/

# 3. Ensure no dead or unreferenced helper functions remain
ruff check --select F401 app/
```
