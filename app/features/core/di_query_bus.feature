Feature: DI Query Bus
  As a developer
  I want to use a DI Query Bus
  So that I can decouple my application logic

  Scenario: Register a handler
    Given a DI Query Bus
    When I register a handler for a query
    Then the command handler is registered in the bus

  Scenario: Register a handler that is already registered
    Given a DI Query Bus
    And a handler is already registered for a query
    When I try to register another handler for the same query
    Then a QueryAlreadyRegistered error is raised

  Scenario: Execute a query
    Given a DI Query Bus
    And a handler is registered for a query
    When I execute the query
    Then the command handler is called

  Scenario: Execute a query with no handler
    Given a DI Query Bus
    And no handler is registered for a query
    When I execute the query
    Then a HandlerNotFound error is raised from query bus