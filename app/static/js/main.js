/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./node_modules/js-cookie/dist/js.cookie.js":
/*!**************************************************!*\
  !*** ./node_modules/js-cookie/dist/js.cookie.js ***!
  \**************************************************/
/***/ (function(module) {

eval("/*! js-cookie v3.0.5 | MIT */\n;\n(function (global, factory) {\n   true ? module.exports = factory() :\n  0;\n})(this, (function () { 'use strict';\n\n  /* eslint-disable no-var */\n  function assign (target) {\n    for (var i = 1; i < arguments.length; i++) {\n      var source = arguments[i];\n      for (var key in source) {\n        target[key] = source[key];\n      }\n    }\n    return target\n  }\n  /* eslint-enable no-var */\n\n  /* eslint-disable no-var */\n  var defaultConverter = {\n    read: function (value) {\n      if (value[0] === '\"') {\n        value = value.slice(1, -1);\n      }\n      return value.replace(/(%[\\dA-F]{2})+/gi, decodeURIComponent)\n    },\n    write: function (value) {\n      return encodeURIComponent(value).replace(\n        /%(2[346BF]|3[AC-F]|40|5[BDE]|60|7[BCD])/g,\n        decodeURIComponent\n      )\n    }\n  };\n  /* eslint-enable no-var */\n\n  /* eslint-disable no-var */\n\n  function init (converter, defaultAttributes) {\n    function set (name, value, attributes) {\n      if (typeof document === 'undefined') {\n        return\n      }\n\n      attributes = assign({}, defaultAttributes, attributes);\n\n      if (typeof attributes.expires === 'number') {\n        attributes.expires = new Date(Date.now() + attributes.expires * 864e5);\n      }\n      if (attributes.expires) {\n        attributes.expires = attributes.expires.toUTCString();\n      }\n\n      name = encodeURIComponent(name)\n        .replace(/%(2[346B]|5E|60|7C)/g, decodeURIComponent)\n        .replace(/[()]/g, escape);\n\n      var stringifiedAttributes = '';\n      for (var attributeName in attributes) {\n        if (!attributes[attributeName]) {\n          continue\n        }\n\n        stringifiedAttributes += '; ' + attributeName;\n\n        if (attributes[attributeName] === true) {\n          continue\n        }\n\n        // Considers RFC 6265 section 5.2:\n        // ...\n        // 3.  If the remaining unparsed-attributes contains a %x3B (\";\")\n        //     character:\n        // Consume the characters of the unparsed-attributes up to,\n        // not including, the first %x3B (\";\") character.\n        // ...\n        stringifiedAttributes += '=' + attributes[attributeName].split(';')[0];\n      }\n\n      return (document.cookie =\n        name + '=' + converter.write(value, name) + stringifiedAttributes)\n    }\n\n    function get (name) {\n      if (typeof document === 'undefined' || (arguments.length && !name)) {\n        return\n      }\n\n      // To prevent the for loop in the first place assign an empty array\n      // in case there are no cookies at all.\n      var cookies = document.cookie ? document.cookie.split('; ') : [];\n      var jar = {};\n      for (var i = 0; i < cookies.length; i++) {\n        var parts = cookies[i].split('=');\n        var value = parts.slice(1).join('=');\n\n        try {\n          var found = decodeURIComponent(parts[0]);\n          jar[found] = converter.read(value, found);\n\n          if (name === found) {\n            break\n          }\n        } catch (e) {}\n      }\n\n      return name ? jar[name] : jar\n    }\n\n    return Object.create(\n      {\n        set,\n        get,\n        remove: function (name, attributes) {\n          set(\n            name,\n            '',\n            assign({}, attributes, {\n              expires: -1\n            })\n          );\n        },\n        withAttributes: function (attributes) {\n          return init(this.converter, assign({}, this.attributes, attributes))\n        },\n        withConverter: function (converter) {\n          return init(assign({}, this.converter, converter), this.attributes)\n        }\n      },\n      {\n        attributes: { value: Object.freeze(defaultAttributes) },\n        converter: { value: Object.freeze(converter) }\n      }\n    )\n  }\n\n  var api = init(defaultConverter, { path: '/' });\n  /* eslint-enable no-var */\n\n  return api;\n\n}));\n\n\n//# sourceURL=webpack://pypass/./node_modules/js-cookie/dist/js.cookie.js?");

/***/ }),

/***/ "./src/index.ts":
/*!**********************!*\
  !*** ./src/index.ts ***!
  \**********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";
eval("\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\nexports.addPassword = exports.fetchUserAccounts = exports.buildAccountTable = exports.toggleSidebar = void 0;\nconst js_cookie_1 = __webpack_require__(/*! js-cookie */ \"./node_modules/js-cookie/dist/js.cookie.js\");\nclass User_Accounts {\n    website;\n    account_name;\n    account_username;\n    account_password;\n    constructor(website, account_name, account_username, account_password) {\n        this.website = website;\n        this.account_name = account_name;\n        this.account_username = account_username;\n        this.account_password = account_password;\n    }\n}\nfunction toggleSidebar() {\n    const sidebar = document.getElementById(\"sidebar\");\n    const headerTitle = document.getElementById(\"header-title\");\n    const mainContent = document.getElementById(\"content\");\n    const navmenu = document.getElementById(\"navmenu\");\n    if (sidebar.style.width === \"250px\") {\n        sidebar.style.width = \"0\";\n        headerTitle.classList.remove(\"shifted\");\n        mainContent.classList.remove(\"shifted\");\n        navmenu.style.display = \"block\";\n    }\n    else {\n        sidebar.style.width = \"250px\";\n        headerTitle.classList.add(\"shifted\");\n        mainContent.classList.add(\"shifted\");\n        navmenu.style.display = \"hidden\";\n    }\n}\nexports.toggleSidebar = toggleSidebar;\nfunction createAccountRow(account, index, table) {\n    const row = table.insertRow(index + 1);\n    const website = row.insertCell(0);\n    const account_name = row.insertCell(1);\n    const account_username = row.insertCell(2);\n    const account_password = row.insertCell(3);\n    website.innerHTML = account.website;\n    account_name.innerHTML = account.account_name;\n    account_username.innerHTML = account.account_username;\n    account_password.innerHTML = account.account_password;\n}\nfunction buildAccountTable(accounts) {\n    const table = document.getElementById(\"password_table\");\n    if (table === null)\n        return;\n    accounts.forEach((account, index) => {\n        createAccountRow(account, index, table);\n    });\n}\nexports.buildAccountTable = buildAccountTable;\nfunction processAccountData(data) {\n    console.log(data);\n    const accounts = [];\n    data.accounts.forEach((account) => {\n        accounts.push(new User_Accounts(account.website, account.account_name, account.account_username, account.account_password));\n    });\n    return accounts;\n}\nfunction fetchUserAccounts() {\n    const user_id = (0, js_cookie_1.get)(\"user_id\");\n    const logged_in = (0, js_cookie_1.get)(\"logged_in\");\n    return fetch(\"/fetch_accounts\", {\n        method: \"POST\",\n        headers: {\n            \"Content-Type\": \"application/json\",\n        },\n        body: JSON.stringify({\n            user_id: user_id,\n            logged_in: logged_in,\n        }),\n    })\n        .then((response) => {\n        console.log(response);\n        if (!response.ok) {\n            throw new Error(\"Network response was not ok\");\n        }\n        return response.json();\n    })\n        .then(processAccountData)\n        .catch((error) => {\n        console.log(error);\n        return [];\n    });\n}\nexports.fetchUserAccounts = fetchUserAccounts;\nfunction showDialog(message) {\n    const dialog = document.querySelector(\"dialog\");\n    const closeDialog = document.querySelector(\"#close\");\n    dialog.show();\n    closeDialog.addEventListener(\"click\", () => {\n        dialog.close();\n    });\n}\nfunction addPassword() {\n    // Get the input values\n    const website = document.getElementById(\"website\");\n    const username = document.getElementById(\"username\");\n    const password = document.getElementById(\"password\");\n    // Validate and process the input values\n    if (website.value && username.value && password.value) {\n        const user_id = (0, js_cookie_1.get)(\"user_id\");\n        console.log(user_id);\n        fetch(\"/add_password\", {\n            method: \"POST\",\n            headers: {\n                \"Content-Type\": \"application/json\",\n            },\n            body: JSON.stringify({\n                user_id: user_id,\n                website: website.value,\n                username: username.value,\n                password: password.value,\n            }),\n        })\n            .then((response) => {\n            console.log(response);\n            if (!response.ok) {\n                throw new Error(\"Network response was not ok\");\n            }\n            return response.json();\n        })\n            .then((data) => {\n            console.log(data);\n            if (data.status === \"success\") {\n                showDialog(\"Password added successfully\");\n            }\n            else {\n                showDialog(\"Failed to add password\");\n            }\n        })\n            .catch((error) => {\n            console.log(error);\n            showDialog(\"Failed to add password\");\n        });\n        // Clear the input fields\n        website.value = \"\";\n        username.value = \"\";\n        password.value = \"\";\n    }\n    else {\n        showDialog(\"Please enter all the values\");\n    }\n}\nexports.addPassword = addPassword;\n\n\n//# sourceURL=webpack://pypass/./src/index.ts?");

/***/ }),

/***/ "./src/main.js":
/*!*********************!*\
  !*** ./src/main.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _index__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./index */ \"./src/index.ts\");\n\n  \n  document.addEventListener(\"DOMContentLoaded\", () => {\n    document.querySelector(\"#navmenu\").addEventListener(\"click\", _index__WEBPACK_IMPORTED_MODULE_0__.toggleSidebar);\n    document.querySelector(\"#closebtn\").addEventListener(\"click\", _index__WEBPACK_IMPORTED_MODULE_0__.toggleSidebar);\n    document.querySelector(\".add-password .link\").addEventListener(\"click\", _index__WEBPACK_IMPORTED_MODULE_0__.addPassword);\n  \n    for (let i = 0; i < 2; i++) (0,_index__WEBPACK_IMPORTED_MODULE_0__.toggleSidebar)();\n  \n    (0,_index__WEBPACK_IMPORTED_MODULE_0__.fetchUserAccounts)().then((accounts) => {\n      (0,_index__WEBPACK_IMPORTED_MODULE_0__.buildAccountTable)(accounts);\n    });\n  });\n  \n\n//# sourceURL=webpack://pypass/./src/main.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./src/main.js");
/******/ 	
/******/ })()
;