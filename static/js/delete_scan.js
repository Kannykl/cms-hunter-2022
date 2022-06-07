deleteButtons = document.getElementsByClassName("scan_delete");

for (button of deleteButtons){
    id=button.getAttribute("id")
    console.log(id)
    button.addEventListener("click", function () {
        result = window.confirm("Are u sure want to delete this scan?");
        if (result){
            sendDeleteRequest(id);
        }
    })
}

function sendDeleteRequest(id) {
   $.ajax({
            type: 'POST',
            url: `/scan/${id}`,
            data: {
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function () {
                console.log('done');
                alert('DONE');
            }
        });
}
