@lend
Feature: test lend

@browser.headed @lend1
  Scenario: User check lend form

    When user goes to lend page with "host1"
    Then user fills and sends feedback form
    Then intercept form submission and check data on "host1"
    When user sees modall whith telegram button
    Then user sees the transition page to Telegram