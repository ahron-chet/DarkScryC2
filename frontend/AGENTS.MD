Based on our full conversation and the system you've been building, here's a full and professional `AGENTS.md` spec file for **frontend AI agents** contributing to your project:

---

# 📁 AGENTS.md

> **Frontend Agent Instruction Manual**
> *Last updated: 2025-07-09*

---

## 🎯 Purpose

This repository powers a cyber intelligence and offensive operations panel. Frontend agents are responsible for creating modular, responsive, and cyber-themed UI components for security operators. The design aesthetic must evoke a **high-tech, stealthy, futuristic** dashboard while remaining intuitive and Bootstrap-compliant.

---

## 🧠 Core Technologies

| Area          | Stack                                        |
| ------------- | -------------------------------------------- |
| Framework     | **Next.js 14** with `use client`             |
| Styling       | **Bootstrap 5** with custom dark theme       |
| Font Stack    | `Orbitron` (heading), `Rajdhani` (body)      |
| Icons         | **Bootstrap Icons** (`bi bi-xxx`)            |
| Auth          | `next-auth` for token & session              |
| API Requests  | Custom hook `useAxiosAuth()` for auth calls  |
| Task Results  | `useTaskRunner()` to fetch long-running jobs |
| Design System | Highly modular, **card-based panels**        |

---

## 📐 Layout & Design Principles

### 🌒 Dark Cyber Theme

* Global `body` background: `#10131a`

* Primary accent: `#497ea5`

* Font:

  ```css
  --font-heading: "Orbitron", sans-serif;
  --font-body: "Rajdhani", sans-serif;
  ```

* All cards and modules:

  ```css
  background-color: #1c1f24;
  border-radius: 16px;
  ```

### 🧱 Component Architecture

* Each module **must** be a standalone component:

  * File name: `ModuleNamePanel.tsx`
  * Props: at minimum, accept `agent: Agent`
* Reusable logic (e.g., upload, modal, fetch wrappers) should be abstracted.
* Responsive behavior is **required** for all views.
* Always use `bootstrap grid` (`row`/`col` or `row-cols-auto`) for layouts.

---

## ✅ UI Component Checklist

| Element          | Rule                                                                 |
| ---------------- | -------------------------------------------------------------------- |
| Cards            | `card bg-dark text-white` with rounded corners and consistent shadow |
| Headers          | `<h5>` with `Orbitron` font and `text-info` or white                 |
| Buttons          | Use Bootstrap buttons (`btn-primary`, `btn-secondary`)               |
| Tables           | Must use `.table-dark`, `.table-sm`, `.table-hover`, `table-fixed`   |
| Scrollable Areas | Use `max-height` and `overflow-y: auto` with `.table-responsive`     |
| Icons            | Prefer `bi bi-xxx` Bootstrap icons; inline with buttons where needed |
| Loaders          | Use `Loading.tsx` component (spinner + text)                         |

---

## 🧩 Modules Structure Examples

### 🔍 File Explorer

* Fetches via:
  `POST /agents/:agent_id/modules/collection/files/stream_files_explorer`
* Displays directories + files in a `grid`, styled with `.file-explorer-item`.
* Uses:

  * Upload (base64)
  * Go to path (`input-group-sm`)
  * Path parsing (via `pathToSegments`, `segmentsToPath`)
  * Modal: shows file metadata + download

### 🔐 Wi-Fi Password Table

* Displayed as credential-style table:

  * Table class: `.credential-table`
  * Passwords styled:

    ```css
    .cred-password-col { color: #66d9ef; font-family: monospace; }
    .unsafe-credential { color: #ff5555; }
    .unsafe-protocol { color: #f39c12; }
    ```

### 🌐 Web Credentials

* Tabular structure with:

  * Dropdown for browser selector
  * Dropdown for profile selector
  * Responsive table with password coloring (same rules as Wi-Fi)
* Selector style:

  * Use `form-select-sm bg-secondary text-white border-0`
  * Label styling: `form-label mb-1` with `fontSize: 0.9rem`

---

## 🧬 Special Components

### 🧠 Process Injection Panel

* Displays process enumeration as table
* Button: `Inject` opens modal
* Modal:

  * Describes technique (left for author)
  * Accepts `.bin` shellcode via file input
  * Hints that PE should be converted to shellcode via pre-module

### 🔍 Search Inputs

Match this style for search bars:

```tsx
<div className="d-flex align-items-center" style={{
  backgroundColor: "#242830",
  borderRadius: "16px",
  padding: "0.4rem 1rem"
}}>
  <i className="bi bi-search me-2" style={{ color: "#bbb" }} />
  <input type="text" placeholder="Search..." className="form-control bg-transparent border-0 text-white" />
</div>
```

---

## 📏 Code Styling Rules

| Category          | Style                                                       |
| ----------------- | ----------------------------------------------------------- |
| Naming            | Use camelCase variables, PascalCase components              |
| File Names        | Match module e.g. `WifiPasswordsPanel.tsx`                  |
| CSS               | All styles in `clients.css` with scoped classes             |
| No Inline Styles  | Avoid inline styles except for dynamic sizes/colors         |
| Responsive Layout | Use `.row-cols-auto`, `.d-flex`, `.gap-2`, `.overflow-auto` |
| Typography        | Use `.text-muted`, `.text-info`, `.text-warning` as needed  |

---

## 🧪 Best Practices

* ✅ Always use `table-responsive` and `overflow-auto` together.
* ✅ Each table column should be `max-width` constrained and `text-truncate`.
* ✅ Passwords and unsafe values must be visually styled.
* ✅ Dropdown menus use **Bootstrap multi-level**, fixed via `initAgentViewDropdowns()`.
* ✅ Never leak internal logic (e.g., shellcode) into UI unless inside modal explanation.
* ✅ Always show feedback: loading spinners, empty states, or error alerts.

---

## 📎 Reference Snippets

```tsx
// Orbitron Section Header
<h5 className="mb-0" style={{ fontFamily: "Orbitron, sans-serif" }}>
  Wi-Fi Passwords
</h5>

// Cyber Password Coloring
<td className={`cred-password-col ${isUnsafe ? "unsafe-credential" : ""}`}>{pwd}</td>

// Table Scroll
<div className="card-body p-0 flex-grow-1 overflow-auto" style={{ maxHeight: "70vh" }}>
  <div className="table-responsive">
    <table className="table table-dark table-sm credential-table">...</table>
  </div>
</div>
```

---

## 🚫 Anti-Patterns

* ❌ No Tailwind, AntD, MUI or 3rd-party styles
* ❌ Avoid global CSS (except shared cyber classes)
* ❌ Don’t use `<div className="row"><div className="col-12">...` unless needed
* ❌ Don’t use `style={{ fontWeight: 900 }}` — use Bootstrap classes
* ❌ Don’t write modal logic inline in the render tree — extract when reusable

---
🧪 QA Checklist
Before merging or registering your panel:

 Looks good in desktop and mobile

 Table has horizontal scroll when needed

 All user actions (upload, select, download) show feedback

 No hardcoded error strings

 Icons use Bootstrap or SVG

 Cyber style is respected in layout & colors
---
## 🧭 Future Modules Planned

* [ ] Credential Harvesting (Windows Vault)
* [ ] Token Extraction (Azure, Chrome Local)
* [ ] Anti-EDR Mapping Panel

---

**Pre-commit Checklist:**

Before committing your code, always run:

```bash
npx tsc --noEmit
npm run lint
```

Do **not** ignore any errors—especially TypeScript errors. If an error genuinely cannot be resolved, clearly document the reason in your Pull Request.

