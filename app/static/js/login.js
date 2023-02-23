const login_form = document.getElementById("login");

login_form.addEventListener("submit", (event) => {
	event.preventDefault();

	const username = document.querySelector('input[name="username"]').value;
	const password = document.querySelector('input[name="password"]').value;
	
	fetch("/login", {
		method: "POST",
		headers: {
			"Content-Type": "application/x-www-form-urlencoded"
		},
		body: `username=${username}&password=${password}`
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