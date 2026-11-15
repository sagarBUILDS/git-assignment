# Login System Test Cases

| Test Case ID | Test Scenario | Input Data | Expected Output |
|---|---|---|---|
| TC-001 | Valid login | Username: `student01`; Password: `Pass1234` | Login succeeds and the user is redirected to the dashboard. |
| TC-002 | Invalid username | Username: `unknown01`; Password: `Pass1234` | Display: `Invalid username or password.` No session is created. |
| TC-003 | Invalid password | Username: `student01`; Password: `Wrong123` | Display: `Invalid username or password.` No session is created. |
| TC-004 | Both credentials incorrect | Username: `unknown01`; Password: `Wrong123` | Display: `Invalid username or password.` No session is created. |
| TC-005 | Empty username | Username: empty; Password: `Pass1234` | Display: `Username cannot be empty.` Login is not attempted. |
| TC-006 | Empty password | Username: `student01`; Password: empty | Display: `Password cannot be empty.` Login is not attempted. |
| TC-007 | Both fields empty | Username: empty; Password: empty | Display: `Username cannot be empty.` and `Password cannot be empty.` Login is not attempted. |
| TC-008 | Password less than 6 characters | Username: `student01`; Password: `Ab123` (5 characters) | Display: `Password must be at least 6 characters.` Login is not attempted. |
| TC-009 | Password exactly 6 characters | Username: `student01`; Password: `Ab1234` (6 characters) | Password length validation passes; with valid credentials, login succeeds and the user is redirected to the dashboard. |
| TC-010 | Three consecutive failed attempts | Username: `student01`; Passwords: `Wrong01`, `Wrong02`, `Wrong03` | After the third consecutive failure, display: `Account locked after 3 failed login attempts. Contact support.` Further login attempts are blocked. |
