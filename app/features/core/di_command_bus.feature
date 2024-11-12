Feature: DI Command Bus
  As a developer
  I want to use a DI Command Bus
  So that I can decouple my application logic

  Scenario: Register a handler
    Given a DI Command Bus
    When I register a handler for a command
    Then the query handler is registered in the bus

  Scenario: Register a handler that is already registered
    Given a DI Command Bus
    And a handler is already registered for a command
    When I try to register another handler for the same command
    Then a CommandAlreadyRegistered error is raised

  Scenario: Execute a command
    Given a DI Command Bus
    And a handler is registered for a command
    When I execute the command
    Then the query handler is called

  Scenario: Execute a command with no handler
    Given a DI Command Bus
    And no handler is registered for a command
    When I execute the command
    Then a HandlerNotFound error is raised from command bus