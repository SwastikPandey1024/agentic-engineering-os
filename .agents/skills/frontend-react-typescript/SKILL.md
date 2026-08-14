---
name: frontend-react-typescript
description: React 19, TypeScript, Vite, Tailwind CSS, TanStack Query, Radix UI, Zod validation, and container/presentational component architecture.
---

# Frontend (React + TypeScript) Skill

## 1. When Should I Use This?

Use this skill when:
* Building or refactoring frontend user interfaces using **React 19**, **TypeScript**, and **Vite**.
* Styling with **Tailwind CSS**, Lucide React icons, and Radix UI primitives.
* Managing server state and caching with **TanStack Query** (`@tanstack/react-query`).
* Handling form validation with **React Hook Form** + **Zod**.
* Designing responsive, resilient, accessible component hierarchies.

---

## 2. What Should I Inspect First?

1. **Package Manifest**: Check `frontend/package.json` for React version (React 18 vs 19), Tailwind CSS version, routing (`react-router-dom`), and query client dependencies.
2. **Component Directory Structure**: Inspect `src/components/ui/`, `src/features/`, `src/hooks/`, `src/lib/`.
3. **API Client & Base URL**: Inspect `src/lib/api-client.ts` or `src/lib/axios.ts` to see how backend authentication headers and base URLs are configured.

---

## 3. What Workflow Should I Follow?

```text
Define TypeScript Interfaces & API Response Types
                     ↓
Create API Fetcher Functions (Axios / Fetch)
                     ↓
Wrap in TanStack Query Custom Hooks (useQuery / useMutation)
                     ↓
Build Modular Presentational Components (props in, JSX out)
                     ↓
Handle Loading, Error, Empty, and Success States Explicitly
                     ↓
Validate User Inputs with React Hook Form + Zod
                     ↓
Run Type-Check (tsc -b) and Lint (eslint)
```

### Server State Management with TanStack Query

```typescript
// frontend/src/features/documents/hooks/use-documents.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';

export interface DocumentItem {
  id: string;
  title: string;
  user_id: string;
  created_at: string;
}

export const useDocuments = () => {
  return useQuery<DocumentItem[], Error>({
    queryKey: ['documents'],
    queryFn: async () => {
      const response = await apiClient.get('/api/v1/documents');
      return response.data;
    },
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
};

export const useUploadDocument = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (formData: FormData) => {
      const response = await apiClient.post('/api/v1/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
    },
  });
};
```

### Resilient Component Pattern (Loading, Error, Empty States)

```tsx
// frontend/src/features/documents/components/document-list.tsx
import React from 'react';
import { useDocuments } from '../hooks/use-documents';
import { FileText, AlertCircle, Loader2 } from 'lucide-react';

export const DocumentList: React.FC = () => {
  const { data: documents, isLoading, isError, error } = useDocuments();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-12 text-slate-400">
        <Loader2 className="w-6 h-6 animate-spin mr-2" />
        <span>Loading documents...</span>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="p-4 bg-rose-500/10 border border-rose-500/20 rounded-lg text-rose-400 flex items-center">
        <AlertCircle className="w-5 h-5 mr-2 shrink-0" />
        <span>Error loading documents: {error.message}</span>
      </div>
    );
  }

  if (!documents || documents.length === 0) {
    return (
      <div className="text-center p-12 border-2 border-dashed border-slate-700 rounded-xl">
        <FileText className="w-12 h-12 text-slate-500 mx-auto mb-3" />
        <h3 className="text-lg font-medium text-slate-300">No documents found</h3>
        <p className="text-sm text-slate-500 mt-1">Upload a document to begin OCR processing.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {documents.map((doc) => (
        <div key={doc.id} className="p-4 bg-slate-900 border border-slate-800 rounded-xl hover:border-slate-700 transition">
          <h4 className="font-medium text-white">{doc.title}</h4>
          <span className="text-xs text-slate-500">{new Date(doc.created_at).toLocaleDateString()}</span>
        </div>
      ))}
    </div>
  );
};
```

---

## 4. What Decisions Should I Make?

| Area | Best Practice Decision |
| :--- | :--- |
| **State Management** | Use local `useState` for UI toggles; use `TanStack Query` for server state/cache; use React `Context` or `Zustand` only for global client state (e.g. auth user, theme). |
| **Form Handling** | Always use `react-hook-form` + `@hookform/resolvers/zod` for forms with more than 2 fields. |
| **Utility Classes** | Use `tailwind-merge` + `clsx` (`cn()` helper) for merging conflicting dynamic Tailwind class names. |

---

## 5. What Should I Avoid?

* **NEVER store server response data in manual `useEffect` + `useState` chains**: TanStack Query handles caching, deduplication, retry, and refetching automatically.
* **NEVER use `any` type in TypeScript**: Create strict interface contracts for all API requests and props.
* **NEVER hardcode API base URLs**: Always reference `import.meta.env.VITE_API_BASE_URL`.
* **NEVER ignore the Empty state**: Every list view must gracefully handle zero items without rendering a broken blank box.

---

## 6. How Should I Verify Success?

```bash
# 1. Run TypeScript type check
npm run type-check

# 2. Run ESLint check
npm run lint

# 3. Test production build bundle
npm run build
```
