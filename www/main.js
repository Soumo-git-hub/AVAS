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
            sync: true,
        },
        out: {
            effect: "fadeOut",
            sync: true,
        },
    });

    // Mic button click to toggle between "Oval" and "Wave" sections
    $("#MicBtn").click(function () {
        eel.playassistantsound() // Ensure you call eel function with a semicolon
        $("#Oval").attr("hidden", true);  // Hide the "Oval" section
        $("#Wave").attr("hidden", false); // Show the "Wave" section

        // Execute the eel function for voice recognition
        eel.TaskExecution()(); 
    });

    function doc_keyUp(e) {
        // this would test for whichever key is 40 (down arrow) and the ctrl key at the same time

        if (e.key === 'A' && e.metaKey) {
            eel.playassistantsound()
            $("#Oval").attr("hidden", true);
            $("#Wave").attr("hidden", false);
            eel.TaskExecution()()
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

});
