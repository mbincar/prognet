Feature: Reset Password

    User should be able to reset their own Password
    when they forgot it, provied that they give a valid
    email address

    Scenario: A user forgot password and reset it
        Given I already sign up with the following data
            | username | email            | password   |
            | john     | john@example.com | studiocode |
        But I forgot my password when trying to login
        When I click on reset password link
        And I will be redirected to reset password page
        When I submit my email on reset password form
        Then I will receive an email with reset password link
        When I open my reset password link and submit new password
            | new_password      |
            | studiocodeinsider |
        Then I will be able to login with my new password

    Scenario: A user forgot username but submit wrong email on reset password
        Given I already sign up with the following data
            | username | email            | password   |
            | john     | john@example.com | studiocode |
        But I forgot my password when trying to login
        When I click on reset password link
        And I will be redirected to reset password page
        But I submit wrong email address
        Then I should be notified about it

    Scenario: A user forgot username but submit unmatch password on reset password
        Given I already sign up with the following data
            | username | email            | password   |
            | john     | john@example.com | studiocode |
        But I forgot my password when trying to login
        When I click on reset password link
        And I will be redirected to reset password page
        When I submit my email on reset password form
        Then I will receive an email with reset password link
        But I submit unmatch new password
            | new_password      | new_password2     |
            | studiocodeinsider | studiocodeinsious |
        Then I should be notified about unmatch password for reset password

    Scenario: A user forgot username and try to use already used reset password link
        Given I already sign up with the following data
            | username | email            | password   |
            | john     | john@example.com | studiocode |
        But I forgot my password when trying to login
        When I click on reset password link
        And I will be redirected to reset password page
        When I submit my email on reset password form
        Then I will receive an email with reset password link
        When I open my reset password link and submit new password
            | new_password      |
            | studiocodeinsider |
        When I try to request reset password using the same url
        Then I will be notified about invalid reset password link
