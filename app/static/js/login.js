/* 
* Check the status of the response
* If the status is ok trigger the login function
* Otherwise show an error message
*/
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

// Login even listener
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
			checkStatus(data)
		})
		.catch(error => {
			console.log(error);
		});
});