# The generation archive

One file per CAD generation, to the same structure. Until 2026-08-16 this record was uneven:
Gen1, Gen3 existed only as sections inside `cad/CHANGELOG_CAD.md`, Gen4 had a status document of its
own, and Gen5 and Gen6, the frozen baseline and the current design target, had no
per-generation record at all, only the ADRs that adopted them.

Each file answers the same seven questions, so two generations can be read against each other:

1. What it is, and what it was for
2. Dates and status
3. What is committed to this repository, file by file
4. Where the source document lives, and whether it is here
5. The operating point it was built at
6. Known defects
7. Why it was superseded

## The six

| | | Committed | Source |
|---|---|---|---|
| [Gen1](GEN1.md) | the geometric ancestor | 11 STEP | Fusion, not in this repository |
| [Gen2](GEN2.md) | first structured revision | 9 STEP | Fusion, not in this repository |
| [Gen3](GEN3.md) | parameter-reconciled; the masses come from here | 10 STEP, 2 STL | Fusion, not in this repository |
| [Gen4](GEN4.md) | last drawn by hand | none, P43 | Fusion, not in this repository |
| [Gen5](GEN5.md) | the frozen baseline | 8 STEP, 8 STL | `cad/build_gen5.py`, in this repository |
| [Gen6](GEN6.md) | the current design target | 6 STEP, 6 STL | `cad/build_gen6.py`, in this repository |

## The gap this table makes visible

No Fusion document is committed anywhere in this repository. Not one `.f3d`, for any of the
four generations built in Fusion. What exists for Gen1, Gen3 is STEP, which is a *result* of the
Fusion model and not the model; what exists for Gen4 is nothing at all.

That is a single point of failure outside version control. `cad/parameters.json` already warns
that Fusion user parameters are document-scoped and drift silently across documents, the
documents themselves are not in the repository to check that against. If the Fusion hub is lost,
Gen1 through Gen4 are lost with it, and only their exports survive.

Gen5 and Gen6 do not have this problem, and that is the whole argument of
[ADR-026](../adr/026-cad-built-from-parameters.md): their source is a script in this repository,
and the geometry is a function of a parameter file that is also here.

Recorded as [P74](../../OPEN_PROBLEMS.md). Closing it means exporting each Fusion document as
`.f3d` and committing it. That is a manual export nobody has done, and it cannot be done from
inside this repository.
