function toggle_sidebar() {
  const sidebar = document.getElementById("sidebar") as HTMLElement;
  const content = document.getElementById("content") as HTMLElement;
  const navmenu = document.getElementById("navmenu") as HTMLElement;

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
