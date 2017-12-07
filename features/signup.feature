Feature: Sign Up Feature

In order to able to login and use site feature that required it
user needs to sign up

    Scenario: A user sign up with duplicate username
        Given I am new user with the following data
            | username | email            | password   |
            | john     | john@example.com | studiocode |
        But Another user has already signup with the same username
            | username | email               | password   |
            | john     | johndoe@example.com | studiocode |
        When I go to home page and click sign on up link
        And I submit my invalid data on sign up form
        Then I should be notified about duplicate username

    Scenario: A user sign up with duplicate email
        Given I am new user with the following data
            | username | email            | password   |
            | john     | john@example.com | studiocode |
        But Another user has already signup with the same email
            | username | email               | password   |
            | johndoe     | john@example.com | studiocode |
        When I go to home page and click sign on up link
        And I submit my invalid data on sign up form
        Then I should be notified about duplicate email

    Scenario: A user sign up with unmatch password
        Given I am new user with the following data
            | username | email            | password   |
            | john     | john@example.com | studiocode |
        When I go to home page and click sign on up link
        But I submit unmatch password on sign up form
        Then I should be notified about unmatch password

    Scenario: A user confirm email after sign up and login
        Given I am new user with the following data
            | username | email            | password   |
            | john     | john@example.com | studiocode |
        When I go to home page and click sign on up link
        And I submit my data on sign up form
        Then I will receive a verification email
        When I confirm my email
        And I go to login page and login with my username
        Then I should be redirected to home page

    Scenario: A user hasn't confirm email after sign up and login
        Given I am new user with the following data
            | username | email            | password   |
            | john     | john@example.com | studiocode |
        When I go to home page and click sign on up link
        And I submit my data on sign up form
        Then I will receive a verification email
        But I didn't confirm my email
        And I go to login page and login with my username
        Then I should be asked to confirm my email