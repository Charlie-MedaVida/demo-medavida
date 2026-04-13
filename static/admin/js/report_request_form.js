'use strict';

(function () {
    function updateIdFields() {
        const idType = document.getElementById('id_id_type');
        const ssnRow = document.getElementById('id_ssn');
        const einRow = document.getElementById('id_ein');

        if (!idType || !ssnRow || !einRow) return;

        const value = idType.value;

        ssnRow.disabled = value === 'EIN';
        einRow.disabled = value === 'SSN';

        if (value === 'EIN') ssnRow.value = '';
        if (value === 'SSN') einRow.value = '';
    }

    document.addEventListener('DOMContentLoaded', function () {
        const idType = document.getElementById('id_id_type');
        if (!idType) return;

        idType.addEventListener('change', updateIdFields);
        updateIdFields();
    });
})();