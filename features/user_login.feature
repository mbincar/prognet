Feature: User Login

    User needs to login to buy and make and payment

    Scenario: A user login with invalid username
        Given I already sign up with the following data
            | username | email            | password   |
            | john     | john@example.com | studiocode |
        When I go to login page and misspelled username on sumbit data
        Then I should be notified about invalid username/password

    Scenario: A user login with invalid email
        Given I already sign up with the following data
            | username | email            | password   |
            | john     | john@example.com | studiocode |
        When I go to login page and misspelled email on sumbit data
        Then I should be notified about invalid email/password

    Scenario: A user login with valid username but invalid password
        Given I already sign up with the following data
            | username | email            | password   |
            | john     | john@example.com | studiocode |
        When I go to login page and misspelled password on login
        Then I should be notified about invalid username/password

    Scenario: A user login with valid email and password
        Given I already sign up with the following data
            | username | email            | password   |
            | john     | john@example.com | studiocode |
        When I go to login page and login with my email
        Then I should be redirected to home page

    Scenario: A user login with valid username and password
        Given I already sign up with the following data
            | username | email            | password   |
            | john     | john@example.com | studiocode |
        When I go to login page and login with my username
        Then I should be redirected to home page