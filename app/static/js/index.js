"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const js_cookie_1 = require("js-cookie");
class User_Accounts {
    constructor(website, account_name, account_username, account_password) {
        this.website = website;
        this.account_name = account_name;
        this.account_username = account_username;
        this.account_password = account_password;
    }
}
function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const headerTitle = document.getElementById("header-title");
    const mainContent = document.getElementById("content");
    const navmenu = document.getElementById("navmenu");
    if (sidebar.style.width === "250px") {
        sidebar.style.width = "0";
        headerTitle.classList.remove("shifted");
        mainContent.classList.remove("shifted");
        navmenu.style.display = "block";
    }
    else {
        sidebar.style.width = "250px";
        headerTitle.classList.add("shifted");
        mainContent.classList.add("shifted");
        navmenu.style.display = "hidden";
    }
}
function createAccountRow(account, index, table) {
    const row = table.insertRow(index + 1);
    const website = row.insertCell(0);
    const account_name = row.insertCell(1);
    const account_username = row.insertCell(2);
    const account_password = row.insertCell(3);
    website.innerHTML = account.website;
    account_name.innerHTML = account.account_name;
    account_username.innerHTML = account.account_username;
    account_password.innerHTML = account.account_password;
}
function buildAccountTable(accounts) {
    const table = document.getElementById("password_table");
    if (table === null)
        return;
    accounts.forEach((account, index) => {
        createAccountRow(account, index, table);
    });
}
function processAccountData(data) {
    console.log(data);
    const accounts = [];
    data.accounts.forEach((account) => {
        accounts.push(new User_Accounts(account.website, account.account_name, account.account_username, account.account_password));
    });
    return accounts;
}
function fetchUserAccounts() {
    const user_id = js_cookie_1.Cookie.get("user_id");
    const logged_in = js_cookie_1.Cookie.get("logged_in");
    return fetch("/fetch_accounts", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            user_id: user_id,
            logged_in: logged_in,
        }),
    })
        .then((response) => {
        console.log(response);
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
        .then(processAccountData)
        .catch((error) => {
        console.log(error);
        return [];
    });
}
window.addEventListener("load", () => {
    for (let i = 0; i < 2; i++)
        toggleSidebar();
    fetchUserAccounts().then((accounts) => {
        buildAccountTable(accounts);
    });
});
//# sourceMappingURL=index.js.map