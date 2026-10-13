# Architecture
One Spring Boot 4.1 service, Java 21, Maven. Layers: `api` (one REST controller and one response record), `store` (RequestStore,
reads the nightly export from the classpath; the production store is out of this cut), `model` (PriorAuthRequest record).
No database, no messaging, no security filter in this cut. JSON via Jackson 3 (Spring Boot's default); dates as ISO strings.
