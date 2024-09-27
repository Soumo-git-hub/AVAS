$(document).ready(function () {

    // SiriWave Initialization
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 900,
        height: 250,
        style: "ios",
        amplitude: 1,
        speed: 0.08,
        autostart: true
    });

    // Wave text animation using Textillate.js
    $('.wave-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeIn",
            sync: true
        },
        out: {
            effect: "fadeOut",
            sync: true
        }
    });

    // Mic button click to toggle between "Oval" and "Wave" sections
    $("#MicBtn").click(function () {
        eel.playassistantsound(); // Call eel function with a semicolon
        $("#Oval").attr("hidden", true);  // Hide the "Oval" section
        $("#Wave").attr("hidden", false); // Show the "Wave" section

        // Execute the eel function for voice recognition
        eel.TaskExecution();
    });

    function doc_keyUp(e) {
        // Test for the 'A' key and the Meta key (Command key on Mac or Windows key)
        if (e.key === 'A' && e.metaKey) {
            eel.playassistantsound();
            $("#Oval").attr("hidden", true);
            $("#Wave").attr("hidden", false);
            eel.TaskExecution();
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    // Play the assistant message
    function PlayAssistant(message) {
        if (message !== "") {
            $("#Oval").attr("hidden", true);
            $("#Wave").attr("hidden", false);
            eel.TaskExecution(message); // Pass the message to the eel function
            $("#chatbox").val("");
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
    }

    // Toggle function to hide and display mic and send buttons
    function ShowHideButton(message) {
        if (message.length === 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        } else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    // Key up event handler on the text box
    $("#chatbox").keyup(function () {
        let message = $("#chatbox").val();
        ShowHideButton(message);
    });

    // Send button event handler
    $("#SendBtn").click(function () {
        let message = $("#chatbox").val();
        PlayAssistant(message);
    });


        // enter press event handler on chat box
        $("#chatbox").keypress(function (e) {
            key = e.which;
            if (key == 13) {
                let message = $("#chatbox").val()
                PlayAssistant(message)
            }
        });

});
