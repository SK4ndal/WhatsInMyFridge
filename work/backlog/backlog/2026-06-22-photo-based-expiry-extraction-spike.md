# Photo-Based Expiry Extraction Spike

## Type

spike

## Context

The brainstorm identifies an optional feature to extract dates from photos. This could reduce manual entry friction, but feasibility, accuracy, UX, and privacy implications are not yet clear.

## Functional Requirements

- Investigate whether expiry dates can be extracted from user-provided photos.
- Identify expected user flow for capturing or uploading a photo.
- Identify how users would confirm or correct extracted dates.
- Identify limitations for date formats, packaging variation, lighting, and language.
- Identify whether this should be part of MVP or deferred.

## Technical Requirements

- Decision: Treat photo extraction as a spike, not a committed feature, because the brainstorm labels it optional and the feasibility is unknown.
- Decision: Require user confirmation before any extracted expiry date is saved.
- Rejected alternative: Automatically trust photo-extracted dates; rejected because extraction may be inaccurate and expiry is already an estimate.
- Constraint: Privacy and local-versus-remote processing implications must be understood before implementation.

## Acceptance Criteria

- The spike documents feasible approaches for extracting dates from photos.
- The spike documents major risks and limitations.
- The spike recommends whether to build, defer, or reject the feature.
- The spike defines a confirmation flow if the feature is recommended.
