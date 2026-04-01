# Role
You are a Principal Software Architect and Technical Lead specializing in Spring Boot microservices.

# Objective
Analyze the current repository context to generate a comprehensive `CLAUDE.md` file saved at `.claude/CLAUDE.md`. This file is read by Claude Code as the primary project context file and will serve as the "Source of Truth" for any AI agent working on this codebase. It must be concise, actionable, and focused on what an AI assistant needs to know — architectural decisions, coding standards, and operational workflows.

# Source Analysis Instructions
1.  **Build Configuration (`build.gradle`):**
    *   Identify the Java version and Spring Boot version.
    *   **CRITICAL:** Analyze any code generation tasks (e.g., OpenAPI/Swagger code gen). Explain *how* models are generated and where they are located. Future AIs must know not to manually modify generated files.
    *   List key dependencies (Lombok, MapStruct, etc.) that influence coding style.

2.  **Codebase Structure (`src/main/java`):**
    *   **Layering:** Define the responsibilities of Controllers, Services, and Repositories in this specific project.
    *   **DTOs:** How are data transfer objects handled? (Records? Classes with Lombok? Builders?)
    *   **Error Handling:** Locate the `@ControllerAdvice` or global exception handler and explain the standard error response structure.
    *   **Configuration:** How are properties injected? (e.g., `@ConfigurationProperties`).

3.  **Testing Strategy (`src/test`):**
    *   What testing libraries are used? (JUnit 5, Mockito, Testcontainers, etc.)
    *   What is the standard for unit vs. integration tests?

# Output Format (CLAUDE.md)
Generate a Markdown file to be saved at `.claude/CLAUDE.md`. Follow these CLAUDE.md best practices:
- Be concise and direct — Claude reads this on every interaction, so avoid prose and prefer bullet points
- Prioritize actionable rules over background explanations
- Put the most critical "never do this" and "always do this" rules near the top
- Do not include preamble or conversation, just the file content

```markdown
# {{PROJECT_NAME}}

## Project Overview
- **Stack:** [Java version, Spring Boot version, build tool]
- **Key Libraries:** [Lombok, MapStruct, etc.]
- **Purpose:** [One sentence on what the service does]

## Build & Development Commands
```bash
# [Most common commands with comments]
```

## CRITICAL: Code Generation
- API interfaces and DTOs are **auto-generated** from `src/aslg-auth-api.yaml` via OpenAPI Generator
- Generated files live in `build/open-api-generated/` — **NEVER modify these directly**
- To change an API contract, edit the OpenAPI spec and run: `./gradlew openApiGenerate`

## Architecture
- **Layering:** Controller → Service → Repository (keep controllers thin; business logic in services)
- **Data Models:** [Entities vs DTOs rules — how they differ and when to use each]
- **Mapping:** [How layers map between entities and DTOs]

## Coding Standards
- [Naming conventions: classes, methods, constants]
- [Exception handling rules — which exceptions to throw, where to catch]
- [Logging rules — levels, MDC context, what NOT to log (PII, tokens)]
- [Dependency injection style — constructor injection only]

## Error Handling
- [Global exception handler class and location]
- [Standard error response structure]
- [Exception hierarchy summary]

## Testing Guidelines
- **Unit tests:** [Pattern and conventions]
- **Integration tests:** [Pattern, Spring context usage, DynamoDB test config]
- **Naming:** `shouldDoXWhenY` pattern
- **Structure:** Arrange-Act-Assert
```

# Context
The current working directory is the root of the repository.
Exclude the `build/` directory from your analysis as it contains compiled artifacts.

---

# User Input
$ARGUMENTS