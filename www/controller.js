$(document).ready(function () {

    // Display Speak Message
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {
        $(".wave-message li:first").text(message);
        $('.wave-message').textillate('start');
    }

    // Show hood (GUI)
    eel.expose(ShowHood);
    function ShowHood() {
        $("#Oval").attr("hidden", false);
    }

    // Hide hood (GUI)
    eel.expose(HideHood);
    function HideHood() {
        $("#Oval").attr("hidden", true);  // Hide the hood, can be adjusted to suit your design
        $(".wave-message").text("");      // Clear any messages
    }

    // Set the assistant state
    eel.expose(SetAssistantState);
    function SetAssistantState(state) {
        localStorage.setItem('assistant_state', state);
    }

    // Get the assistant state
    eel.expose(GetAssistantState);
    function GetAssistantState() {
        return localStorage.getItem('assistant_state') || 'active';
    }

    // Handle user commands based on assistant state
    function handleCommand(command) {
        if (GetAssistantState() === 'sleep') {
            if (command.toLowerCase() === 'wake up') {
                SetAssistantState('active');
                eel.DisplayMessage("Assistant is awake and ready to assist.");
            } else {
                eel.DisplayMessage("Assistant is in sleep mode. Say 'wake up' to reactivate.");
            }
        } else {
            // Process commands normally
            eel.TaskExecution(command);
        }
    }

});
