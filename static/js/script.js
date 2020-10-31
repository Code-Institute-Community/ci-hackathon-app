function toastMessage(tag, message) {
    // Sets the toast HTML.
    $(".toast-wrapper").html(
        `<div class="toast" data-delay="5000">
            <div class="toast-header bg-p-blue">
                <strong class="mr-auto text-white">${tag}</strong>
                <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="toast-body">${message}</div>
        </div>`
    );
    if ($("#enroll-judge").text() === "Withdraw as Judge") {
        $("#enroll-judge").text("Enroll as Judge")
    } else if ($("#enroll-judge").text() === "Enroll as Judge") {
        $("#enroll-judge").text("Withdraw as Judge")
    } else if ($("#enroll-part").text() === "Enroll as Participant") {
        $("#enroll-part").text("Withdraw from the Hackaton")
    } else {
        $("#enroll-part").text("Enroll as Participant")
    }

    // Fires the toast.
    $(".toast").toast("show");
}
        
// Sends the enrollment form with fetch.
function enroll(formData, formUrl) {
    // Sends form to Django view
    fetch(formUrl, {
        method: "POST",
        body: formData,
        credentials: "same-origin",
    })
    .then((response) => {
        if (response.ok) {
            return response.json();
        } else {
            console.log(response)
            throw Error(response.statusText);
        }
    })
    // Fires off a toast notification
    .then(data => toastMessage(data.tag, data.message))
    // Catches any errors and displays their text message
    .catch(error => toastMessage("Error", error))
}
            

// Watches the form for submission, then fires the Fetch function
$("#enroll-form").on("submit", function (ev) {
    // stops form from sending
    ev.preventDefault();
    
    // The data sent in the form POST request.
    const formData = new FormData(this);

    // The URL for the form
    const formUrl = this.action;

    // Fires the main fetch function
    enroll(formData, formUrl);
});

$(document).ready(function(){
    $( "#accordion" ).accordion();
});
