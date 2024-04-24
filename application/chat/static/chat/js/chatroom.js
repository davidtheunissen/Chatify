document.addEventListener('DOMContentLoaded', function() {
    function scrollToBottom() {
        const container = document.getElementById('chat-box');
        container.scrollTop = container.scrollHeight;
    };
    scrollToBottom();
});