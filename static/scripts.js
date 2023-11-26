function addCompany() {
    // Get the table body
    var table = document.querySelector("table");

    // Create a new row
    var row = table.insertRow(-1);

    // Create cells for company, net income, and total asset
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);

    // Add a company select input with a unique name
    cell1.innerHTML = '<select name="symbol" onchange="updateName(this)"><option selected>select</option><option value="nifra">nifra</option><option value="nabil">NABIL</option><option value="pli">PLI</option><option value="nica">NICA</option></select>';

    // Add a net income input with a unique name
    cell2.innerHTML = '<input name="" type="text">';

    // Add a total asset input with a unique name
    cell3.innerHTML = '<input name="" type="text">';
}

function updateName(select) {
    // Get the selected company
    var selectedCompany = select.value;

    select.name = selectedCompany + "_symbol";

    // Get the corresponding input fields
    var netIncomeInput = select.parentElement.nextElementSibling.querySelector('input');
    var totalAssetInput = select.parentElement.nextElementSibling.nextElementSibling.querySelector('input');

    // Update the name attribute of the input fields
    netIncomeInput.name = selectedCompany + "_netincome";
    totalAssetInput.name = selectedCompany + "_totalasset";
}