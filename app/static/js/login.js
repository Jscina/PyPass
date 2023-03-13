function checkStatus(data) {
	switch (data.status) {
		case "success":
			login();
			break;
		default:
			let error = document.getElementById("error_msg");
			error.innerText = data.message;
			break;
	}
}

function check_if_redirect(response) {
	// If the response is a redirect, switch the window to the new location
	if (response.redirected) {
		window.location.href = response.url;
		return;
	}
	// Return the response text if the response is not a redirect
	return response.text();
}

function login() {
	fetch('/home', {
		method: 'GET',
	})
		.then(response => {
			return check_if_redirect(response);
		})
		.then(data => {
			document.documentElement.innerHTML = data;
		})
		.catch(error => {
			console.error('Error fetching data:', error);
		});
}

function addLoginEventListener() {
	const login_form = document.getElementById("login");

	if (login_form === null)
		return;

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
				checkStatus(data);
			})
			.catch(error => {
				console.log(error);
			});
	});
}

window.addEventListener("load", addLoginEventListener);