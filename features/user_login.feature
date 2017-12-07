Feature: User Login

    User needs to login to buy and make and payment

    Scenario: A user that already sign up and confirm email login
        Given I already sign up with the following data
            | username | email            | password   |
            | john     | john@example.com | studiocode |
        When I go to login page and submit my login data
        Then I should be redirected to the home page