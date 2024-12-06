document.addEventListener('DOMContentLoaded', function() {
    const eventSource = new EventSource("/events");
    const eventsContainer = document.getElementById("events");
    const maxMessages = 20;

    eventSource.onmessage = function(event) {
        const newElement = document.createElement("div");
        newElement.innerText = event.data;
        eventsContainer.appendChild(newElement);

        while (eventsContainer.childElementCount > maxMessages) {
            eventsContainer.removeChild(eventsContainer.firstChild);
        }
    };
});
