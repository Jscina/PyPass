let tbody = document.querySelector("tbody");
let table = document.querySelector("table");

// Populate the memory database and display the user accounts automatically
window.addEventListener('load', (event) => {
    let data=window.performance.getEntriesByType("navigation")[0].type;
    if(data !== "reload" && data !== "navigate")
    {
        eel.populate_memory_db();
    }
    event.preventDefault();
    displayTable(event);
});

//Add an event to the table
table.addEventListener("click", onDeleteRow);

//Display the accounts in the table
function displayTable() {
    eel.get_account_table()(buildTable);
}


// Build the user account table
function buildTable(table) {
    // If the user has no more accounts, fill the table with a generic None
    if (table.length < 1) {
        tbody.innerHTML += `
            <tr>
            <td>1</td>
            <td>None</td>
            <td>None</td>
            <td>None</td>
            <td>None</td>
            <td></td>
            </tr>`;
    }
    else {
        //Clear table before displaying
        tbody.innerHTML = '';
        for (let row = 0; row < table.length; row++) {
            tbody.innerHTML += `
            <tr>
            <td>${row + 1}</td>
            <td>${table[row][0]}</td>
            <td>${table[row][1]}</td>
            <td>${table[row][2]}</td>
            <td>${table[row][3]}</td>
            <td>
            <a class="btn btn-danger deleteBtn" href="#">Delete</a>
            </td>
    
            </tr>`;
        }
    }
}

function onDeleteRow(event) {
    if (!event.target.classList.contains("deleteBtn")) {
        return;
    }
    if (confirm("Are you sure you want to delete this entry?")) {
        const row = event.target;
        let index = row.closest("tr").cells[0].innerHTML;
        index = parseInt(index) - 1;
        deleteAccount(index);
    }
    else {
        return;
    }

}

// Delete an account from a specific index
function deleteAccount(deleteRow) {
    // Delete the account from both the permanent and transient database
    eel.delete_account(deleteRow);
    displayTable();
}