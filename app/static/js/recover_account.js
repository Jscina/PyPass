const recover_account_form = document.getElementById("recover_account");

recover_account_form.addEventListener("submit", (event) => {
	event.preventDefault();

	const email = document.querySelector('input[name="email"]').value;
	const password = document.querySelector('input[name="password"]').value;
    const confirm_password = document.querySelector("input[name='confirm_password']").value;
	
	fetch("/recover", {
		method: "POST",
		headers: {
			"Content-Type": "application/x-www-form-urlencoded"
		},
		body: `email=${email}&password=${password}&confirm_password=${confirm_password}`
	})
		.then(response => response.json())
		.then(data => {
			switch (data.status) {
				case "success":
					login();
					break;
				default:
					let error = document.getElementById("error_msg");
					error.innerText = data.message;
					break;
			}
		})
		.catch(error => {
			console.log(error);
		});
});