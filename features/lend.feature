@lend
Feature: test lend

@browser.headed @lend1
  Scenario: User check lend form

    When user goes to lend page with "host2"
    Then user fills and sends feedback form
    Then intercept form submission and check data on "host2"
    When user sees modall whith telegram button
    Then user sees the transition page to Telegram


  @browser.headed @lend2
  Scenario: User check lend form

    When user goes to lend page with "host3"
    Then user fills and sends feedback form
    Then intercept form submission and check data on "host3"
    When user sees thanks modall