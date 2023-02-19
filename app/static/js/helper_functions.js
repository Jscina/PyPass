// Switches the window to the index.html as long as login was successful
function login() {
	fetch('/home', {
		method: 'GET',
	})
		.then(response => {
			if (response.redirected) {
				window.location.href = response.url;
			} else {
				return response.text();
			}
		})
		.then(data => {
			document.documentElement.innerHTML = data;
		})
		.catch(error => {
			console.error('Error fetching data:', error);
		});
}

// Opens/Closes the sidebar
function toggle_sidebar() {
	const sidebar = document.getElementById("sidebar");
	const content = document.getElementById("content");
	const navmenu = document.getElementById("navmenu");

	if (sidebar.style.width === "250px") {
		sidebar.style.width = "0";
		content.classList.remove("shifted");
		navmenu.style.display = "block";
	} else {
		sidebar.style.width = "250px";
		content.classList.add("shifted");
		navmenu.style.display = "none";
	}
}
