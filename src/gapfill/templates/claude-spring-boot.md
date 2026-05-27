# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Tech Stack

- Java 17+, Spring Boot 3.x
- Build tool: Maven (pom.xml) or Gradle (build.gradle)
- Database: PostgreSQL/MySQL + Spring Data JPA + Hibernate 6
- API design: REST, OpenAPI 3.0 (springdoc-openapi)
- Testing: JUnit 5 + Mockito + Testcontainers

## Code Conventions

- All Service classes use `@Service`, transactions managed via `@Transactional`
- Controller layer only handles request parsing and response formatting; business logic goes in Service layer
- Entity classes go in `entity/` package, DTOs in `dto/` package; never expose Entity in API responses
- Use constructor injection (`@RequiredArgsConstructor` + `private final` fields); never use `@Autowired` field injection
- Unified exception handling via `@RestControllerAdvice` with custom exception classes
- Keep tests co-located with source classes
- Follow RESTful API design principles

## Build Commands

Run each command separately. Do not chain.

- Build: `mvn clean package -DskipTests`
- Run tests: `mvn test`
- Run single test: `mvn test -Dtest=ClassName#methodName`
- Integration tests (requires Docker): `mvn verify`
- Run app: `mvn spring-boot:run`

## Security Rules

- Do not hardcode credentials or API keys; use environment variables or Spring Cloud Config
- Do not expose sensitive endpoints (actuator, health, metrics) to the public
- Use parameterized queries; never concatenate SQL strings

## Anti-Patterns

- Do NOT write business logic in Controllers
- Do NOT use `@Data` on Entity classes (causes equals/hashCode issues); use `@Getter` + `@Setter` instead
- Do NOT use `Optional` as a field type; only as method return type
- Do NOT write complex queries in Repository layer; use Specification or Querydsl
- Do NOT use `@Transactional` on read-only operations without `readOnly = true`
