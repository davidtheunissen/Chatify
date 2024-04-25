document.addEventListener('DOMContentLoaded', function() {
    // Scroll to bottom function
    function scrollToBottom() {
        const container = document.getElementById('chat-box');
        container.scrollTop = container.scrollHeight;
    };
    scrollToBottom();


    // WEB SOCKETS

    // Update online count function
    function updateOnlineCount(data) {
        let count = data['online_count'];
        let onlineCount = document.getElementById('online-count');
        onlineCount.innerHTML = `${count} online`
    };


    function messageHandler(data) {
        const chatMessages = document.getElementById('chat-messages');
        let messageHTML = '';
        
        // Message placement logic and HTML code generation
        if (data.author === currentUser) {
            messageHTML = `
            <div class="d-flex justify-content-end my-2">
                <div class="bg-primary text-white pt-3 px-2 fade-in" style="border-radius: 15px; max-width: fit-content;">
                    <p>${data.message}</p>
                </div>
            </div>`;
        } else {
            if (isGroup === 'True') {
                messageHTML = `
                <div class="d-flex justify-content-start my-2">
                    <div class="bg-light text-dark pt-3 px-2 fade-in-up" style="border-radius: 15px; max-width: fit-content;">
                        <h5>${data.author}</h5>
                        <p>${data.message}</p>
                    </div>
                </div>`;
            } else {
                messageHTML = `
                <div class="d-flex justify-content-start my-2">
                    <div class="bg-light text-dark pt-3 px-2 fade-in-up" style="border-radius: 15px; max-width: fit-content;">
                        <p>${data.message}</p>
                    </div>
                </div>`;
            };
        };
        chatMessages.innerHTML += messageHTML;
        scrollToBottom();
    };


    // Get hidden inputs for context
    const roomName = document.getElementById('roomNameInput').value;
    const currentUser = document.getElementById('currentUser').value;
    const isGroup = document.getElementById('isGroup').value;
    socket = new WebSocket("ws://" + window.location.host + "/ws/room/" + roomName + "/");
    
    // Open WebSocket handler
    socket.onopen = function(event) {
        console.log('WebSocket connection established.');
    };

    // Message send handler
    const form = document.getElementById('message-box-input');
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const input = document.getElementById('chat-message-input');
        const message = input.value;

        socket.send(JSON.stringify({
            'body': message
        }));

        input.value = '';
        scrollToBottom();
    });
    
    // Message receive handler
    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        // Log received message data
        console.log('Received message:', data);

        if (data.hasOwnProperty('online_count')) {
            updateOnlineCount(data);
        } else {
            messageHandler(data);
        }


    // Close WebSocket handler
    socket.onclose = function(event) {
        console.log('WebSocket connection closed:', event);
    };

}});