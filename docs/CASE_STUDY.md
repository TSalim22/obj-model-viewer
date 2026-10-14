# 3D OBJ Model Viewer: project notes

## Goal

Understand 3D file parsing and projection.

## Main challenge

Handle malformed geometry safely.

## Implementation choice

Validated indices, normalisation and rotation before projection. The repository is intentionally small, with its main application code and tests kept close together.

## Outcome and validation

The local workflow is implemented, with automated checks covering its core behaviour. See the README for limits and any service-dependent features. External API tests use simulated clients rather than paid or private live data. This is an implementation case study, not a claim of commercial use or earlier completion.

## Next improvements

Improve the interface based on real usage and extend tests when adding new behaviour. Keep changes incremental so the project remains easy to explain.
