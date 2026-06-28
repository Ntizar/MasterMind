# Adela_api — Referencia completa

Módulo creado el 2026-06-15. Category: `api-layer`. Zero deps. 53 tests.

## Estructura de archivos

```
src/
├── index.ts        # Barrel export: createApiHelpers, paginate, filter, sort + 11 tipos
├── api.ts          # createApiHelpers() factory — orquesta todo
├── pagination.ts   # paginate() — offset/limit y cursor-based
├── filter.ts       # filter() — 9 operadores, AND entre condiciones
├── sort.ts         # sort() — multi-campo con dirección por campo
└── types.ts        # 11 interfaces: PaginationOptions, PaginatedResult, FilterCondition,
                    # SortOption, ApiResponse, ApiError, ApiHelpers, ApiHelpersOptions...
```

## Funciones exportadas

| Función | Firma | Descripción |
|---------|-------|-------------|
| `createApiHelpers` | `(opciones?: ApiHelpersOptions) => ApiHelpers` | Factory principal |
| `paginate` | `<T>(items: T[], options: PaginationOptions) => PaginatedResult<T>` | Paginación |
| `filter` | `<T extends Record<string, unknown>>(items: T[], options: FilterOptions) => T[]` | Filtrado |
| `sort` | `<T extends Record<string, unknown>>(items: T[], options: SortOptions) => T[]` | Ordenación |

## Operadores de filter

`eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `like` (case-insensitive), `in`, `nin`

## Pitfalls documentados en adela-new-module

- **Sort numeric vs date:** numeric comparison MUST come before date parsing
- **Cursor pagination:** hash-based cursors are non-invertible; use `c_<offset>` or HMAC
- **TypeScript generics:** `filter`/`sort` need `T extends Record<string, unknown>` constraint
