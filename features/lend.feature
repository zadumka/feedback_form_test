@lend
Feature: test lend

@browser.headless @lend1
  Scenario Outline: User check lend form

    When user goes to lend page with "<host>"
    When user fills in correct data to the feedback form
    Then expected validation errors are under the form fields submit button is enabled
    When user fills correct data and sends feedback form
    Then intercept form submission and check data on "<host>"
    When user sees modall whith telegram button
    Then user sees the transition page to Telegram
    Examples:
      | host  |
      | host1 |
      | host2 |
#      | host3 |
#      | host4 |
#      | host5 |
#      | host6 |
#      | host7 |
#      | host8 |




  @browser.headless @lend2
  Scenario Outline: User check request form

    When user goes to request page with "<host>"
    When user fills correct data and sends request form
    Then intercept request form submission and check data on "<host>"
    When user sees thanks modal
    Examples:
      | host  |
      | host1 |
      | host2 |
      | host3 |
      | host4 |
      | host5 |
      | host6 |





#  @browser.headed @lend3
#  Scenario: User check alt
#    When user goes to lend page with "host9"
#    Then check all images have non-empty alt attributes
##    Then check all images alt text matches page language