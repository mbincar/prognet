Feature: Change Password

    User change password after login

    Scenario: A login user change password
        Given I already sign up with the following data
            | username | email            | password   |
            | john     | john@example.com | studiocode |
        When I go to login page and login with my username
        Then I should be redirected to home page
        When I go to change password link and submit new password
            | new_password      |
            | studiocodeinsider |
        And I logout
        Then I will be able to login with my new password