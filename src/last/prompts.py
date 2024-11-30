PROMPTS = [
    "Analyze this Python project for potential violations of the Hexagonal Architecture principles. Specifically, check if the domain layer contains infrastructure-related code, such as direct database queries, HTTP requests, or other external system calls. Highlight any instances and suggest how to refactor them to ensure proper separation of concerns.",
    "Review the ports and adapters in this Python project. Are they designed with appropriate granularity? Look for ports that are either too broad (e.g., handling unrelated operations in a single interface) or too fine-grained (e.g., splitting highly related operations into separate interfaces). Provide recommendations to balance granularity in alignment with business context.",
    "Assess the testing strategy in this Python project. Are there sufficient unit tests for the domain logic, and are they isolated from external dependencies? Check if ports are tested using mock objects or fakes, and whether adapters are validated with integration tests. Identify gaps in test coverage and suggest improvements to align with Hexagonal Architecture principles.",
]