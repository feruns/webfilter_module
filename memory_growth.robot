*** Settings ***
Library    Process
Library    memory_monitor    memory_monitor.py

*** Variables ***
${PROCESS_NAMES}    my_process_name_1    my_process_name_2

*** Test Cases ***
Memory Usage Test
    Given I start monitoring memory for processes ${PROCESS_NAMES}
    When I run processes
        # Example to start processes
        Start Process    ${CURDIR}/my_program_1.exe
        Start Process    ${CURDIR}/my_program_2.exe

    Then I stop memory monitoring and check for memory growth

*** Keywords ***
I start monitoring memory for processes ${process_names}
    Start Memory Monitoring    ${process_names}    10

I stop memory monitoring and check for memory growth
    [Documentation]    This will stop memory monitoring and check for any significant memory growth
    ${growth_detected}    ${message}=    Stop Memory Monitoring And Check Growth
    Should Be False    ${growth_detected}    ${message}

I run processes
    [Documentation]    This keyword runs all the required processes
    # You can list specific commands here or reuse a "Run Processes" keyword.
