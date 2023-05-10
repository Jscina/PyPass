import {
    toggleSidebar,
    addPassword,
    fetchUserAccounts,
    buildAccountTable,
  } from "./index";
  
  document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#navmenu").addEventListener("click", toggleSidebar);
    document.querySelector("#closebtn").addEventListener("click", toggleSidebar);
    document.querySelector(".add-password .link").addEventListener("click", addPassword);
  
    for (let i = 0; i < 2; i++) toggleSidebar();
  
    fetchUserAccounts().then((accounts) => {
      buildAccountTable(accounts);
    });
  });
  