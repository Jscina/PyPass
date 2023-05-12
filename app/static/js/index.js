"use strict";
class UserAccount {
    service;
    username;
    password;
    constructor(service, username, password) {
        this.service = service;
        this.username = username;
        this.password = password;
    }
}
function setSidebarVisibility(isVisible) {
    const sidebar = document.getElementById("sidebar");
    const headerTitle = document.getElementById("header-title");
    const mainContent = document.getElementById("content");
    const navmenu = document.getElementById("navmenu");
    sidebar.style.width = isVisible ? "250px" : "0";
    headerTitle.classList[isVisible ? 'add' : 'remove']("shifted");
    mainContent.classList[isVisible ? 'add' : 'remove']("shifted");
    navmenu.style.display = isVisible ? "hidden" : "block";
}
function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    setSidebarVisibility(sidebar.style.width !== "250px");
}
function createAccountRow(account, table) {
    const row = table.insertRow(table.rows.length - 1);
    const service = row.insertCell(0);
    const username = row.insertCell(1);
    const password = row.insertCell(2);
    const action = row.insertCell(3);
    service.textContent = account.service;
    username.textContent = account.username;
    // Store the actual password in a data attribute and display *** by default
    password.textContent = "******";
    password.setAttribute("data-password", account.password);
    // Create delete button and attach click event
    const deleteButton = document.createElement("a");
    deleteButton.href = "javascript:void(0)";
    deleteButton.classList.add("link", "delete");
    deleteButton.innerText = "Delete";
    deleteButton.addEventListener("click", handleDeleteClick);
    action.appendChild(deleteButton);
}
function buildAccountTable(accounts) {
    const table = document.getElementById("dashboard_passwords");
    if (table === null)
        return;
    while (table.rows.length > 1)
        table.deleteRow(0);
    accounts.forEach((account) => {
        createAccountRow(account, table);
    });
}
function processAccountData(data) {
    const accounts = [];
    data.forEach((account) => {
        accounts.push(new UserAccount(account.service, account.username, account.password));
    });
    return accounts;
}
function fetchUserAccounts() {
    return fetch("/fetch_accounts", { method: "POST" })
        .then((response) => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
        .then((data) => processAccountData(data))
        .catch((error) => {
        console.log(error);
        return [];
    });
}
function showDialog(message) {
    const dialog = document.querySelector("dialog");
    const errorMsg = document.querySelector("#error-msg");
    const closeDialog = document.querySelector("#cancel");
    errorMsg.innerText = message;
    dialog.show();
    closeDialog.addEventListener("click", () => {
        dialog.close();
    });
}
function handleDeleteRequest(serverRowIndex) {
    fetch("/delete_account", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            order: serverRowIndex,
        }),
    })
        .then((response) => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
        .then((data) => {
        if (data.status !== "success") {
            showDialog("Failed to delete password");
        }
    })
        .catch((error) => {
        console.log(error);
        showDialog("Failed to delete password");
    });
}
function handleAddAccountRequest(service, username, password) {
    fetch("/add_account", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            service: service.value,
            username: username.value,
            password: password.value,
        }),
    })
        .then((response) => {
        console.log(response);
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
        .then((data) => {
        if (data.status === "success") {
            fetchUserAccounts().then((accounts) => {
                buildAccountTable(accounts);
            });
        }
        else
            showDialog("Failed to add password");
    })
        .catch((error) => {
        console.log(error);
        showDialog("Failed to add password");
    });
}
function handleDeleteClick(event) {
    // Check if the clicked element is a delete button
    const target = event.target;
    const table = document.getElementById("dashboard_passwords");
    // Get the row containing the delete button
    const row = target.closest("tr");
    if (row) {
        const rowID = row.rowIndex - 1;
        const serverRowIndex = row.rowIndex;
        // If this row is the last row (the add password row), then just return
        if (rowID === table.rows.length)
            return;
        // Else proceed to delete the row from the table
        table.deleteRow(rowID);
        // Make a request to your server to delete the account data
        handleDeleteRequest(serverRowIndex);
    }
}
function addNewAccount() {
    // Get the input values
    const service = document.getElementById("service");
    const username = document.getElementById("username");
    const password = document.getElementById("password");
    // Validate and process the input values
    if (!(service.value && username.value && password.value)) {
        showDialog("Please enter a value for all fields");
        return;
    }
    handleAddAccountRequest(service, username, password);
    // Clear the input fields
    service.value = "";
    username.value = "";
    password.value = "";
}
function addPasswordListener() {
    const table = document.getElementById("dashboard_passwords");
    if (table === null)
        return;
    // Loop through all rows in the table
    for (let i = 0; i < table.rows.length - 1; i++) {
        const row = table.rows[i];
        const passwordCell = row.cells[2];
        // If the password is currently hidden, show it; otherwise, hide it
        if (passwordCell.textContent === "******") {
            passwordCell.textContent = passwordCell.getAttribute("data-password");
        }
        else {
            passwordCell.textContent = "******";
        }
    }
}
document.addEventListener("DOMContentLoaded", () => {
    const menu = document.querySelector("#navmenu");
    const closeMenu = document.querySelector("#closebtn");
    const addNewPassword = document.querySelector(".add-password .link");
    const viewPasswords = document.querySelector("#view-passwords");
    addNewPassword.addEventListener("click", addNewAccount);
    menu.addEventListener("click", toggleSidebar);
    closeMenu.addEventListener("click", toggleSidebar);
    for (let i = 0; i < 2; i++)
        toggleSidebar();
    viewPasswords.addEventListener("click", addPasswordListener);
    fetchUserAccounts().then((accounts) => {
        buildAccountTable(accounts);
    });
});
//# sourceMappingURL=index.js.map