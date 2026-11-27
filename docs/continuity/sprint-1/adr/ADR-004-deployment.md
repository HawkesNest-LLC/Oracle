# ADR-004: Deployment

## Status

Accepted for Sprint 1. This decision governs the whole quarter. It can be revised only by a later ADR plus Creator approval.

## Context

The 90-day plan ends with a test on the Creator's iPhone. The application must open in a mobile browser, run, and preserve state. That test needs a way to reach the application from the phone.

Three options exist: serve it locally, serve it from a hosted development environment, or deploy it publicly. Only one of them fits the constraints.

The constraints are firm. No paid cloud spend in this quarter. No public deployment in this quarter. No private family history or unpublished manuscripts in the public repo, fixtures, or logs. The Star Trek elements are fan-world research use in a private prototype. Any public or commercial use needs a rights review first.

The governing rules apply here. Rule 1: no overwriting. Rule 2: generated is not established. Rule 3: authority outranks coherence. The supreme rule: the simulator never becomes the source of truth. Rule 4: AI-assisted writing is still the Creator's writing.

## Decision

No public deployment and no paid cloud spend in this quarter.

Sprint 1 and Sprint 2 serve locally and for development only. The core service and the database run on a local machine. Nothing is reachable from the public internet.

The day-90 iPhone acceptance test runs against a locally or development-served application, not a public host. In practice that means the application is served from a machine on the same local network as the phone, or from a development tunnel that is open only for the test and closed after it. The phone reaches the application through the mobile browser. No app store install is needed. No public URL is published.

No deployment step in this quarter publishes anything. No domain is registered. No hosting account is opened. No paid service is started.

## Consequences

Good consequences:

- Zero cost. The quarter spends nothing on hosting.
- Zero public exposure. No rights review is needed for a private prototype, because nothing is public.
- Zero public attack surface. The application is reachable only on the local network or through a temporary test tunnel.
- The team can change the schema, the API, and the client freely, because no public user depends on any of them.

Costs and risks:

- The iPhone test needs a local network and a working development server at test time. If the network or the server fails, the test cannot run. The test plan must include a check that the server is up before the test starts.
- A development tunnel is a temporary public address, even if it is short lived. It must be closed after the test. It must not be shared beyond the testers. It must not be left running.
- Local-only serving hides deployment problems. If a public deployment is ever wanted later, that work is unstarted. That is accepted. The quarter proves the substrate, not the deployment.
- The Creator cannot open the application from anywhere. He can open it only where the development server is reachable. That is a real limit on the day-90 test, and the test plan must say where the server runs and how the phone reaches it.

## Alternatives considered

Hosted development environment. A free tier host or a development platform that serves the application from a private link. Rejected for this quarter because it adds an account, a dependency, and a link that can leak, for a benefit the local network already provides. A free tier is also a future bill: free tiers change, and a build that depends on one can break without warning.

Public staging deployment. A staging URL that is public but unadvertised. Rejected because public is public. A staging URL needs a rights review for the franchise elements, a privacy review for the data, and a hosting decision. None of those is in scope this quarter.

Public production deployment. Rejected for the same reasons as staging, plus cost. No paid cloud spend is authorized.

App store distribution. Rejected because the plan requires a mobile browser application, not a store app. A store app adds review, signing, and delay that the quarter does not need.

## Criteria for a future deployment decision

A deployment decision needs all of the following. If any one is missing, there is no deployment.

1. The day-90 acceptance test has passed on the locally served application, and the result is recorded.
2. A named deployment target exists: a host, a cost, and an owner.
3. The cost is stated in writing and approved. No paid spend happens without that approval.
4. A rights review has been completed for the franchise elements in the deployed content. If the review requires changes, the changes are made first.
5. A privacy review has been completed. It confirms that no private family history and no unpublished manuscripts are in the deployed application, its fixtures, or its logs.
6. The Creator has approved the deployment in his own words. No other approval counts.

A deployment decision is recorded in a new ADR. It does not edit this one. This ADR stays as the record that the quarter was local-only.

## Migration path

- Sprint 1 to Sprint 2: local only. The service and the database run on a development machine.
- Sprint 6 to Sprint 7: the client is served from the same development machine, reachable on the local network. The phone opens it in the mobile browser.
- Day 90: the acceptance test runs against that locally served application. If a temporary development tunnel is used, it is opened for the test and closed after it. The tunnel address is not published and not kept.
- After day 90: if a deployment is wanted, the criteria above must be met first. The migration to a host is a new piece of work, not a step in this quarter.

## Open questions

- Which machine runs the development server for the day-90 test, and how does the phone reach it? The test plan must name both before Sprint 7.
- Is a temporary development tunnel acceptable to the Creator, or must the test run on the local network only? The answer decides whether a tunnel is even an option.
- Who closes the tunnel after the test, and how is that verified? A tunnel left open is a deployment by accident.
- What happens if the local network is unavailable on test day? The test plan needs a fallback, or the test date moves. The fallback must not be a quiet public deployment.
