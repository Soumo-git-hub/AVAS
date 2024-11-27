$(document).ready(function () {

    // Function to display a speak message
    eel.expose(DisplayMessage);
    function DisplayMessage(message) {
        $(".wave-message li:first").text(message);
        $('.wave-message').textillate('start');
    }

    // Show the GUI hood
    eel.expose(ShowHood);
    function ShowHood() {
        $("#Oval").removeAttr("hidden");
    }

    // Hide the GUI hood
    eel.expose(HideHood);
    function HideHood() {
        $("#Oval").attr("hidden", true);  // Hide the hood
        $(".wave-message").empty();       // Clear the wave message
    }

    // Set the assistant's state (active or sleep)
    eel.expose(SetAssistantState);
    function SetAssistantState(state) {
        localStorage.setItem('assistant_state', state);
    }

    // Get the current state of the assistant
    eel.expose(GetAssistantState);
    function GetAssistantState() {
        return localStorage.getItem('assistant_state') || 'active';
    }

    // Handle user commands based on the assistant's state
    eel.expose(HandleCommand);
    function HandleCommand(command) {
        const assistantState = GetAssistantState();

        if (assistantState === 'sleep') {
            if (command.toLowerCase() === 'wake up') {
                SetAssistantState('active');
                DisplayMessage("Assistant is awake and ready to assist.");
                ShowHood();
            } else {
                DisplayMessage("Assistant is in sleep mode. Say 'wake up' to reactivate.");
            }
        } else {
            // Call TaskExecution from Python side via eel
            eel.TaskExecution(command);
        }
    }

    eel.expose(senderText)
    function senderText(message) {
    var chatBox = document.getElementById("chat-canvas-body");
    if (message.trim() !== "") {
        chatBox.innerHTML += `<div class="row justify-content-end mb-4">
        <div class = "width-size">
        <div class="sender_message">${message}</div>
    </div>`; 

        // Scroll to the bottom of the chat box
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

eel.expose(receiverText)
function receiverText(message) {

    var chatBox = document.getElementById("chat-canvas-body");
    if (message.trim() !== "") {
        chatBox.innerHTML += `<div class="row justify-content-start mb-4">
        <div class = "width-size">
        <div class="receiver_message">${message}</div>
        </div>
    </div>`; 

        // Scroll to the bottom of the chat box
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    
}
});


