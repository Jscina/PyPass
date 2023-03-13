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

