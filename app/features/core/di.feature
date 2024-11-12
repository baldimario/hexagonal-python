Feature: Container works correctly

  Scenario: Check that all dependencies are installed
    Given I have a container "container"
    When the container "container" is set up
    When the container "container" has the "foo" service registered as "Foo"
    Then the container "container" should have the "foo" service registered
    And the container "container" should not have the "bar" service registered

  Scenario: Check that container works the same if imported again as well as the first time
    Given I have a container "containerOne"
    And I have a container "containerTwo"
    When the container "containerTwo" has the "foo" service registered as "Foo"
    Then the container "containerTwo" should have the "foo" service registered
    And the container "containerTwo" should not have the "bar" service registered

  Scenario: Check that container injection occurs correctly
    Given I have a container "myContainer"
    When the container "myContainer" has the "parameter" service registered as "FOO"
    And an Example class with parameter is injected with "myContainer" container
    Then the container "myContainer" should have the "example" service registered
    And the "myContainer" container service example class get_parameter is "FOO"
