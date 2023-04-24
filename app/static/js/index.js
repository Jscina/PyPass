class User_Accounts {
    constructor(website, account_name, account_username, account_password) {
        this.website = website;
        this.account_name = account_name;
        this.account_username = account_username;
        this.account_password = account_password;
    }
}
function toggle_sidebar() {
    const sidebar = document.getElementById("sidebar");
    const content = document.getElementById("content");
    const navmenu = document.getElementById("navmenu");
    if (sidebar.style.width === "250px") {
        sidebar.style.width = "0";
        content.classList.remove("shifted");
        navmenu.style.display = "block";
    }
    else {
        sidebar.style.width = "250px";
        content.classList.add("shifted");
        navmenu.style.display = "none";
    }
}
function buildAccountTable() {
    const table = document.getElementById("password_table");
    if (table === null)
        return;
}
function fetchUserAccounts() {
    const accounts = [];
    fetch("/fetch_accounts", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => {
        // Check if the response is successful (status code 200-299)
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        console.log(response.json());
        return response.json();
    })
        .then((data) => {
        data.accounts.forEach((account) => {
            accounts.push(new User_Accounts(account.website, account.account_name, account.account_username, account.account_password));
        });
    })
        .catch((error) => {
        console.log(error);
        return;
    });
    return accounts;
}
window.onload = () => {
    const accounts = fetchUserAccounts();
    console.log(accounts);
};
//# sourceMappingURL=index.js.map