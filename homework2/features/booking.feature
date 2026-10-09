Feature: Reserving movie seats
  As a moviegoer
  I want to browse movies and reserve an available seat
  So that I can plan a visit to the theater

  Scenario: A visitor can browse the current movie catalogue
    Given a movie named "Feature Film" with an available seat "A1"
    When I visit the movie catalogue
    Then the response status is 200
    And I see "Feature Film"

  Scenario: A visitor creates an account before booking
    When I create an account named "grader"
    Then the response redirects to the movie catalogue
    And the account "grader" exists

  Scenario: A signed-in user reserves an available seat
    Given a registered moviegoer named "jordan"
    And a movie named "Feature Film" with an available seat "A1"
    When the moviegoer signs in
    And the moviegoer reserves seat "A1"
    Then the reservation is recorded for "jordan"
    And seat "A1" is marked as booked
