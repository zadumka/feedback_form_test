@lend
Feature: test lend

@browser.headed @lend1
  Scenario: User check lend form

    When user goes to lend page with "host1"
    When user fills in correct data to the feedback form
    Then expected validation errors are under the form fields
    When user fills correct data and sends feedback form
    Then intercept form submission and check data on "host1"
    When user sees modall whith telegram button
    Then user sees the transition page to Telegram


  @browser.headed @lend2
  Scenario: User check lend form

    When user goes to lend page with "host3"
    When user fills in correct data to the feedback form
    Then expected validation errors are under the form fields
    When user fills correct data and sends feedback form
    Then intercept form submission and check data on "host3"
    When user sees thanks modall


  @browser.headed @lend3
  Scenario: User check alt
    When user goes to lend page with "host3"
    Then check all images have non-empty alt attributes
#    Then check all images alt text matches page language