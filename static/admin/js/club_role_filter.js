document.addEventListener("DOMContentLoaded", function () {
    const clubField = document.getElementById("id_club");
    const roleField = document.getElementById("id_role");

    if (!clubField || !roleField) return;

    // Keep a copy of all original roles
    const allRoles = Array.from(roleField.options).map(option => [option.value, option.text]);

    const harmonixRoles = allRoles.filter(([value, text]) => value !== "Dancer");
    const dancerOnly = allRoles.filter(([value, text]) => value === "Dancer");

    function updateRoles() {
        const selectedClub = clubField.value;
        const currentRoleValue = roleField.value;
        roleField.innerHTML = "";

        let choices;
        if (selectedClub === "Harmonix") {
            choices = harmonixRoles;
        } else if (selectedClub === "Groovex") {
            choices = dancerOnly;
        } else {
            // Default case if needed, maybe show all roles
            choices = allRoles;
        }

        choices.forEach(([value, label]) => {
            const option = new Option(label, value);
            roleField.add(option);
        });

        // Try to preserve the selected role if it's still valid
        if (choices.some(([value, text]) => value === currentRoleValue)) {
            roleField.value = currentRoleValue;
        }
    }

    clubField.addEventListener("change", updateRoles);
    updateRoles(); // set on load
});