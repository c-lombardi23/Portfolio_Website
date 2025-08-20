document.querySelectorAll(".track-link").forEach(link => {
        link.addEventListener("click", function(event){
            event.preventDefault();
            const url = this.href;

            fetch("/track/external_click", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ url })
            }).finally(()=> {
                window.location.href = url;
            });
        });
    });