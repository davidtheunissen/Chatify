document.addEventListener('DOMContentLoaded', function() {
    // Scroll to bottom function
    function scrollToBottom() {
        const container = document.getElementById('chat-box');
        container.scrollTop = container.scrollHeight;
    };

    // Call scrollToBottom() function after chat messages are loaded
    document.getElementById('chat_messages').addEventListener('DOMNodeInserted', function() {
        scrollToBottom();
    });

    // Call scrollToBottom() function when page initially loads
    scrollToBottom();
});